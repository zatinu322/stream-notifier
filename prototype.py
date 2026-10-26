# noqa

import asyncio
import json
from io import BytesIO

import httpx
from environs import Env

env = Env()
env.read_env()

with open("nlo.png", "rb") as f:
    # можно кидать и напрямую BufferedReader, но для универсальности лучше оборачивать
    IMAGE = BytesIO(f.read())

DS_PAYLOAD_ATTACHMENT = {
    "content": "<@&1270388891739750584> <@273944928604913664> Test",  # упоминание роли и пользователя
    "embeds": [{
        "title": "Title",
        "description": "Description",
        "image": {"url": "attachment://image.png"},
    }],
}

DS_PAYLOAD_URL = {
    "content": "Test",
    "embeds": [{
        "title": "Title",
        "description": "Description",
        "type": "image",
        "image": {
            "url": "https://t3.ftcdn.net/jpg/02/22/96/00/360_F_222960005_bVo8WMI5rRTYi4wABTszEnM5YXcAzHZQ.jpg",
            "width": None,
            "height": None,
            "description": "image",
        },
    }],
}


async def send_discord_attachment() -> None:
    files_multiple = {
        "files[0]": ("image.png", IMAGE.getvalue(), "image/png"),
        "files[1]": ("image2.png", IMAGE.getvalue(), "image/png"),
    }

    file_single = {
        "file": ("image.png", IMAGE.getvalue(), "image/png"),
    }

    r = httpx.post(
        "https://discord.com/api/v10/channels/1276511059678728226/messages",
        headers={
            "Authorization": f"Bot {env.str("DISCORD_BOT_TOKEN")}",
        },
        data={"payload_json": json.dumps(DS_PAYLOAD_ATTACHMENT)},
        files=files_multiple,
        timeout=300,
    )
    print(r.text)
    r.raise_for_status()


async def send_discord_url() -> None:
    r = httpx.post(
        "https://discord.com/api/v10/channels/1276511059678728226/messages",
        headers={
            "Authorization": f"Bot {env.str("DISCORD_BOT_TOKEN")}",
        },
        data={"payload_json": json.dumps(DS_PAYLOAD_URL)},
    )
    print(r.text)
    r.raise_for_status()


async def send_tg_photo_bytes() -> None:
    photo = {
        "photo": ("image.png", IMAGE.getvalue(), "image/png"),
    }
    r = httpx.post(
        f"https://api.telegram.org/bot{env.str("TG_BOT_TOKEN")}/sendPhoto",
        data={
            "chat_id": env.str("TG_ID"),
            "caption": "test",
        },
        files=photo,
    )
    # print(r.text)
    r.raise_for_status()


async def send_tg_photo_id() -> None:
    r = httpx.post(
        f"https://api.telegram.org/bot{env.str("TG_BOT_TOKEN")}/sendPhoto",
        data={
            "chat_id": env.str("TG_ID"),
            "caption": "test",
            # "photo": "AgACAgIAAxkDAAIITGq-ThUC5lilcIhAuKDWNO_3zic_AALQIGsba4H4SZnbXL_GeNg1AQADAgADcwADPQQ",
            "photo": "https://t3.ftcdn.net/jpg/02/22/96/00/360_F_222960005_bVo8WMI5rRTYi4wABTszEnM5YXcAzHZQ.jpg",
        },
    )
    # print(r.text)
    r.raise_for_status()


async def send_vk_text() -> None:
    headers = {
        "Authorization": f"Bearer {env.str("VK_TOKEN")}",
    }
    r = httpx.post(
        "https://api.vk.com/method/wall.post",
        data={
            "message": "test",
            "from_group": 1,
            "owner_id": env.str("VK_GROUP_ID"),
            "v": "5.199",
        },
        headers=headers,
    )
    print(r.text)
    r.raise_for_status()


async def main() -> None:
    await send_discord_attachment()
    # await send_discord_url()
    # await send_tg_photo_id()
    # await send_vk_text()
    ...


if __name__ == "__main__":
    asyncio.run(main())
