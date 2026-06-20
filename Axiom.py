from pyromod import Client
from pyrogram import __version__
from pyrogram.raw.all import layer
from info import Config
import logging
import logging.config
from aiohttp import web

logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(
        [
            web.get(
                "/",
                lambda r: web.Response(
                    text="𝐀‌xɪσϻ 𝐌‌ᴧss 𝐑‌єᴘσꝛᴛєꝛ 𝐁‌σᴛ ✅"
                ),
            )
        ]
    )
    return web_app


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="AxiomMRT",
            in_memory=True,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={"root": "plugins"},
        )

    async def start(self, *args, **kwargs):
        await super().start()

        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        app = web.AppRunner(await web_server())
        await app.setup()

        await web.TCPSite(
            app,
            "0.0.0.0",
            Config.PORT
        ).start()

        logging.info(
            f"✅ {me.first_name} with Pyrogram v{__version__} "
            f"(Layer {layer}) started on {me.username}. ✅"
        )

        try:
            await self.send_message(
                Config.OWNER,
                f"**{me.first_name}  ɪs 𝐒‌ᴛᴧꝛᴛєᴅ 𝐒‌υᴄᴄєssғυʟʟʏ ✨️**"
            )
        except Exception as e:
            logging.error(f"Owner message error: {e}")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped ⛔")


bot = Bot()
bot.run()
