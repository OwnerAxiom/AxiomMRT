import os
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
# from pyrogram.enums import ButtonStyle

from info import Config, Txt

# def axiombtn():
#     return random.choice([
#         ButtonStyle.SUCCESS,
#         ButtonStyle.DANGER,
#         ButtonStyle.PRIMARY
#     ])

@Client.on_message(filters.private & filters.command('start'))
async def handle_start(bot:Client, message:Message):

    Btn = [
        [
            InlineKeyboardButton(text='𝐇єʟᴘ 𝐀ηᴅ 𝐂σϻϻᴧηᴅ', callback_data='help')
        ],
        [
            InlineKeyboardButton(text='⌯ 𝐀xɪσϻ ⌯', url='https://t.me/CreativeAxiom'),
            InlineKeyboardButton(text='𝐒‌єꝛᴠєꝛ 𝐒‌ᴛᴧᴛs', callback_data='server')
        ],
        [
            InlineKeyboardButton(text='𝐀xɪσϻ 𝐔ᴘᴅᴧᴛєs ⎘', url='https://t.me/AxiomBots'),
            InlineKeyboardButton(text='𝐀‌ʙσυᴛ', callback_data='about')
        ]
    ]

    await message.reply_text(text=Txt.START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(Btn))


#Restart to cancell all process 
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.OWNER))
async def restart_bot(b, m):
    await m.reply_text("🔄__Rᴇꜱᴛᴀʀᴛɪɴɢ.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)
