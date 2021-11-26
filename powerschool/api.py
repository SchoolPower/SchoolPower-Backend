import asyncio
from typing import Any

import httpx
from zeep import AsyncClient, Settings
from zeep.cache import SqliteCache
from zeep.proxy import AsyncServiceProxy
from zeep.transports import AsyncTransport

from config.config import PS_API


class AuthException(Exception):
    pass


class PowerSchoolApi:
    service: AsyncServiceProxy
    _client: AsyncClient

    def __init__(self, url: str, cache_location=None, auth_user: str = 'pearson', auth_password: str = 'm0bApP5'):
        settings = Settings()
        settings.force_https = False  # we are not using those http endpoints anyways
        auth = httpx.DigestAuth(auth_user, auth_password)
        self._transport = AsyncTransport(
            client=httpx.AsyncClient(auth=auth),
            wsdl_client=httpx.Client(auth=auth),
            cache=SqliteCache(path=cache_location),
        )
        self._client = AsyncClient(
            f'{url}/pearson-rest/services/PublicPortalServiceJSON?wsdl',
            transport=self._transport,
            settings=settings,
        )

        # a workaround due to async client not supporting create_service
        self.service = AsyncServiceProxy(
            self._client,
            self._client.wsdl.bindings[
                '{http://publicportal.rest.powerschool.pearson.com}PublicPortalServiceJSONSoap11Binding'],
            address=f'{url}/pearson-rest/services/PublicPortalServiceJSON')

    async def login(self, username: str, password: str):
        result = await self.service.loginToPublicPortal(username=username, password=password)
        if len(result.messageVOs) != 0:
            error_message = result.messageVOs[0]
            raise AuthException({
                "title": error_message.title,
                "description": error_message.description,
                "code": error_message.msgCode
            })
        return result.userSessionVO

    async def get_student_data(self, user_session: Any):
        return await self.service.getStudentData(
            userSessionVO={
                'userId': user_session.userId,
                'serviceTicket': user_session.serviceTicket,
                'serverInfo': {'apiVersion': user_session.serverInfo.apiVersion},
                'serverCurrentTime': user_session.serverCurrentTime,
                'userType': user_session.userType
            },
            studentIDs=user_session.studentIDs,
            qil={'includes': '1'}
        )

    async def close(self):
        await self._transport.aclose()


if __name__ == '__main__':
    api = PowerSchoolApi(PS_API)


    async def get_student_data(username: str, password: str):
        session = await api.login(username, password)
        import pickle
        pickle.dump(await api.get_student_data(session), open('../student_data', 'wb'))
        await api.close()


    import sys

    asyncio.run(get_student_data(sys.argv[1], sys.argv[2]))
