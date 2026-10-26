# TODO: Delete this file

import asyncio
from pathlib import Path

from environs import Env

from notifier import DiscordConfig, NotifierClient, TelegramConfig

TEST_MARKDOWN = """**жирный** и __подчёркнутый__

__*underline italics*__

__**underline bold**__

***bold italics***

__***underline bold italics***__

*курсив* и _тоже курсив_

~~зачёркнутый~~ и ||спойлер||

`инлайн-код` и обычный текст

[ссылка на пример](https://example.com)

> цитата **первая**
> цитата вторая

```python
def hello():~
    print("world")
```
"""


async def main() -> None:
    env = Env()
    env.read_env()

    image = Path("nlo.png").read_bytes()
    tg_config = TelegramConfig(
        api_token=env.str("TG_BOT_TOKEN"),
        chat_id=env.str("TG_ID"),
        message_text=TEST_MARKDOWN,
        image=image,
        has_spoiler=True,
    )
    discord_config = DiscordConfig(
        api_token=env.str("DISCORD_BOT_TOKEN"),
        channel_id="1276511059678728226",
        message_text="Test",
    )
    async with NotifierClient(
        telegram_config=tg_config,
        discord_config=discord_config,
    ) as client:
        # await client.send_telegram()
        # print(response)  # has id and nickname in response
        await client.send_discord()


if __name__ == "__main__":
    asyncio.run(main())
