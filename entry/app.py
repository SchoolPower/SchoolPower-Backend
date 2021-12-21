import asyncio
import random
import time

import httpx
import jwt
from httpx import ConnectTimeout
from sanic import Sanic, response
from sanic.log import logger
from sanic.request import Request
from sanic.response import HTTPResponse, text, json
from sanic_gzip import Compress

from common.log import log
from config.config import CACHE_DB_LOCATION, PS_API, SECRET
from db import db
from powerschool import parser, parser_old
from powerschool.api import PowerSchoolApi, AuthException
from localization.localize import use_localize

app = Sanic("SchoolPower")

compress = Compress()
db_inited = False
powerschool_api = None


async def get_student_data(api: PowerSchoolApi, username: str, password: str, parse_func):
    session = await api.login(username, password)
    return parse_func((await api.get_student_data(session)).studentDataVOs[0])


def db_operation(func):
    async def wrapper(request: Request):
        global db_inited
        if not db_inited:
            await db.init()
            db_inited = True
        return await func(request)

    return wrapper


async def get_powerschool_api():
    global powerschool_api

    if powerschool_api is not None:
        return powerschool_api
    try:
        powerschool_api = await asyncio.get_event_loop().run_in_executor(
            None, PowerSchoolApi, PS_API, CACHE_DB_LOCATION
        )
        return powerschool_api
    except ConnectTimeout:
        print("Failed to establish connection to PowerSchool Api")
        raise


@app.get('/')
def home(request: Request) -> HTTPResponse:
    return text('SchoolPower backend is running here')


@app.post('/api/2.0/get_data.php')
@db_operation
@compress.compress()
async def old_api(request: Request) -> HTTPResponse:
    username = request.form['username'][0]
    password = request.form['password'][0]

    if username == 'test' or (username == '19050069' and password == '19050069'):
        return text(httpx.get('https://schoolpower.oss-cn-shanghai.aliyuncs.com/test/test.json').text,
                    content_type="application/json")

    start_time = time.time()
    try:
        api = await get_powerschool_api()
        parsed_data, avatar = await asyncio.gather(
            get_student_data(api, username, password, parser_old.parse_old_api),
            db.get_user_avatar(username)
        )
        parsed_data.additional.avatar = avatar or ''
    except asyncio.CancelledError:
        raise
    except ConnectTimeout:
        log({'error': "TIMED_OUT"})
        return json({
            "err": "200",
            "description": "Timed out when connecting to your school's PowerSchool server. Please retry later.",
            "alert": "Timed out when connecting to your school's PowerSchool server. Please retry later.",
        })
    except AuthException as e:
        description = e.args[0]['description']
        resp = {
            "err": "200",
            "description": description,
            "reserved": "Something went wrong! Invalid Username or password",
        }
        if 'ERROR_PASSWORD_ADMIN_RESET' in e.args[0]['description']:
            resp["alert"] = "Your password is reset by admin. Please contact your school."
        return json(resp)
    except Exception as e:
        logger.exception(e)
        log({
            'error': repr(e)
        })
        return json({
            "err": "200",
            "description": repr(e),
            "reserved": "",
        })
    finally:
        log({
            "username": username,
            "os": request.form.get("os"),
            "action": request.form.get("action"),
            "version": request.form.get("version"),
            "duration": time.time() - start_time,
            "api_version": 2,
        })

    return json(parsed_data.to_dict(include_default_values=True))


@app.post('/v3/get_data')
@db_operation
@compress.compress()
async def get_data(request: Request) -> HTTPResponse:
    username = request.json['username']
    password = request.json['password']

    localize = use_localize(request.headers.get("X-Locale"))

    if username == 'test':
        mock = httpx.get('https://schoolpower.oss-cn-shanghai.aliyuncs.com/test/mock_data.json').text
        return text(mock.replace('%random%', str(random.randint(0, 1))), content_type="application/json")

    if username == 'test2' or (username == '19050069' and password == '19050069'):
        mock = httpx.get('https://schoolpower.oss-cn-shanghai.aliyuncs.com/test/test_v2_full.json').text
        augmented = parser.augment_test_data_with_schedule(mock)
        return json(augmented.to_dict())

    start_time = time.time()
    try:
        api = await get_powerschool_api()
        parsed_data, avatar = await asyncio.gather(
            get_student_data(api, username, password, parser.parse),
            db.get_user_avatar(username)
        )
        parsed_data.extra_info.avatar_url = avatar
        parsed_data.extra_info.jwt = jwt.encode({"username": username}, SECRET, algorithm="HS256").decode()
    except asyncio.CancelledError:
        raise
    except ConnectTimeout:
        log({"error": "TIMED_OUT"})
        return json({
            "success": False,
            "title": localize("Error.ConnectionTimedOut.Title"),
            "description": localize("Error.ConnectionTimedOut.Message")
        })
    except AuthException as e:
        return json({"success": False, **e.args[0]})
    except Exception as e:
        logger.exception(e)
        log({'error': repr(e)})
        return json({"success": False, "title": localize("Error.Unexpected.Title"), "description": repr(e)})
    finally:
        log({
            "username": username,
            "os": request.headers.get("X-OS"),
            "action": request.headers.get("X-Action"),
            "version": request.headers.get("X-App-Version"),
            "locale": request.headers.get("X-Locale"),
            "os_version": request.headers.get("X-OS-Version"),
            "duration": time.time() - start_time,
            "api_version": 3,
        })

    return json(parsed_data.to_dict())


@app.post("/api/notifications/register.php")
@app.post("/v3/register_device")
@db_operation
async def register_device(request: Request) -> HTTPResponse:
    await db.add_token(request.json['token'])
    return json({"success": True})


@app.post("/api/2.0/set_avatar.php")
@app.post("/v3/set_avatar")
@db_operation
async def set_avatar(request: Request) -> HTTPResponse:
    username = request.json['username']
    password = request.json['password']
    new_avatar = request.json['new_avatar']
    remove_code = request.json['remove_code']

    api = PowerSchoolApi(PS_API)
    try:
        await api.login(username, password)
        await api.close()
    except asyncio.CancelledError:
        raise
    except AuthException as e:
        return json({"success": False, **e.args[0]})
    except Exception as e:
        logger.exception(e)
        return json({"success": False, "title": "Unexpected Internal Error", "description": str(e)})

    await db.update_avatar(username, new_avatar, remove_code)
    return json({"success": True})


@app.get("/api/2.0/update.json.php")
@app.get("/v3/android_version")
async def android_update_info(request: Request) -> HTTPResponse:
    return json(httpx.get('https://files.schoolpower.tech/update.json').json())


@app.get("/dist/latest.php")
@app.get("/v3/latest_download")
def latest_download(request: Request) -> HTTPResponse:
    return response.redirect('https://files.schoolpower.tech/dist/latest.apk')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, workers=3)
    asyncio.get_event_loop().close()
