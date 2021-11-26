from typing import Optional

from tortoise import fields, Tortoise, run_async
from tortoise.models import Model

from config.config import DB_LOCATION


class UserAvatar(Model):
    username = fields.CharField(pk=True, max_length=16)
    avatar = fields.TextField()
    remove_code = fields.TextField()


class APN(Model):
    token = fields.CharField(pk=True, max_length=64)


async def update_avatar(username: str, avatar: str, remove_code: str):
    existing = await UserAvatar.filter(username=username).first()
    if existing:
        existing.avatar = avatar
        existing.remove_code += ";" + remove_code
        await existing.save()
    else:
        await UserAvatar.create(username=username, avatar=avatar, remove_code=remove_code)


async def get_user_avatar(username: str) -> Optional[str]:
    user = await UserAvatar.filter(username=username).first()
    return user.avatar if user else None


async def add_token(token: str):
    if (await APN.get_or_none(token=token)) is not None:
        return
    await APN.create(token=token)


async def remove_token(token: str):
    await APN.filter(token=token).delete()


def get_all_tokens():
    return APN.all()


async def init():
    await Tortoise.init(
        db_url=f'sqlite://{DB_LOCATION}',
        modules={'models': ['db.db']}
    )
    await Tortoise.generate_schemas()


async def close():
    await Tortoise.close_connections()


async def main():
    await init()

    await add_token('token1')
    await add_token('token1')
    await add_token('token2')

    async for apn in get_all_tokens():
        print(apn.token)

    await remove_token('token1')
    print()
    async for apn in get_all_tokens():
        print(apn.token)

    print("avatars")
    await update_avatar(username='test', avatar='ava', remove_code='rem')
    print(await get_user_avatar('test'))
    await update_avatar(username='test', avatar='ava new', remove_code='sec')
    print(await get_user_avatar('test'))


if __name__ == '__main__':
    run_async(main())
