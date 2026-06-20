import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import psutil
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from info import Config, Txt

config_path = Path("config.json")


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


@Client.on_callback_query()
async def handle_Query(bot: Client, query: CallbackQuery):

    data = query.data

    if data == "help":

        HelpBtn = [
            [InlineKeyboardButton(text='𝐓‌ᴧꝛɢєᴛ 🎯', callback_data='targetchnl'),
            InlineKeyboardButton(text='𝐃‌єʟєᴛє 𝐂‌σηғɪɢ ❌', callback_data='delete_conf')],
            [InlineKeyboardButton(text='𝐓‌ɢ 𝐀‌ᴄᴄσυηᴛs 👥', callback_data='account_config'),
            InlineKeyboardButton(text='⟸ 𝐁‌ᴧᴄᴋ', callback_data='home')]
        ]

        await query.message.edit(text=Txt.HELP_MSG, reply_markup=InlineKeyboardMarkup(HelpBtn))

    elif data == "server":
        try:
            msg = await query.message.edit(text="__Processing...__")
            currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(
                time.time() - Config.BOT_START_TIME))
            total, used, free = shutil.disk_usage(".")
            total = humanbytes(total)
            used = humanbytes(used)
            free = humanbytes(free)
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            ms_g = f"""<b><u>𝐁‌σᴛ 𝐒‌ᴛᴧᴛυs</b></u>

✦ 𝐔‌ᴘᴛɪϻє : <code>{currentTime}</code>
✦ 𝐂‌𝐏‌𝐔‌ 𝐔‌sᴧɢє : <code>{cpu_usage}%</code>
✦ 𝐑‌𝐀‌𝐌‌ 𝐔‌sᴧɢє : <code>{ram_usage}%</code>
✦ 𝐓‌σᴛᴧʟ 𝐃‌ɪsᴋ 𝐒‌ᴘᴧᴄє : <code>{total}</code>
✦ 𝐔‌sєᴅ 𝐒‌ᴘᴧᴄє : <code>{used} ({disk_usage}%)</code>
✦ 𝐅‌ꝛєє 𝐒‌ᴘᴧᴄє : <code>{free}</code>"""

            await msg.edit_text(text=ms_g, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='⟲ 𝐁‌ᴧᴄᴋ', callback_data='home')]]))
        except Exception as e:
            print('Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    elif data == "about":
        botuser = await bot.get_me()
        await query.message.edit(text=Txt.ABOUT_MSG.format(botuser.username, botuser.username), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='⟲ 𝐁‌ᴧᴄᴋ', callback_data='home')]]))

    elif data == "home":
        Btn = [
            [InlineKeyboardButton(text='❗𝐇‌єʟᴘ', callback_data='help'),
            InlineKeyboardButton(text='🌀𝐒‌єꝛᴠєꝛ 𝐒‌ᴛᴧᴛs', callback_data='server')],
            [InlineKeyboardButton(text='🌻𝐔‌ᴘᴅᴧᴛєs', url='https://t.me/urstarkz'),
            InlineKeyboardButton(text='🌨️𝐀‌ʙσυᴛ', callback_data='about')],
            [InlineKeyboardButton(text='❄️𝐃‌єᴠєʟσᴘєꝛ',
                                url='https://t.me/urstarkz')]
        ]

        await query.message.edit(text=Txt.START_MSG.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(Btn))

    elif data == "delete_conf":

        if query.from_user.id != Config.OWNER:
            return await query.message.edit("**𝐘‌συ'ꝛє 𝐍‌σᴛ 𝐀‌ᴅϻɪη 𝐓‌σ 𝐏‌єꝛғσꝛϻ ᴛʜɪs ᴛᴧsᴋ ❌**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='⟲ 𝐁‌ᴧᴄᴋ', callback_data='help')]]))
            
        btn = [
            [InlineKeyboardButton(text='𝐘‌єs', callback_data='delconfig-yes')],
            [InlineKeyboardButton(text='𝐍‌σ', callback_data='delconfig-no')]
        ]

        await query.message.edit(text="**⚠️ 𝐀‌ꝛє ʏσυ 𝐒‌υꝛє ?**\n\n➜ 𝐘‌συ ᴡᴧηᴛ ᴛσ ᴅєʟєᴛє ᴛʜє 𝐂‌σηғɪɢ.", reply_markup=InlineKeyboardMarkup(btn))

    elif data == "targetchnl":

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

        else:
            return await query.message.edit(text="𝐘‌συ ᴅɪᴅη'ᴛ ϻᴧᴋє ᴧ ᴄσηғɪɢ ʏєᴛ !\n\n➜ 𝐅‌ɪꝛsᴛʟʏ ϻᴧᴋє ᴄσηғɪɢ ʙʏ υsɪηɢ /make_config", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='⟲ 𝐁‌ᴧᴄᴋ', callback_data='help')]]))

        Info = await bot.get_chat(config['Target'])

        btn = [
            [InlineKeyboardButton(text='𝐂‌ʜᴧηɢє 𝐓‌ᴧꝛɢєᴛ',
                                  callback_data='chgtarget')],
            [InlineKeyboardButton(text='⟲ 𝐁‌ᴧᴄᴋ', callback_data='help')]
        ]

        text = (
            f"𝐂‌ʜᴧηηєʟ 𝐍‌ᴧϻє :- <code> {Info.title} </code>\n"
            f"𝐂‌ʜᴧηηєʟ 𝐔‌sєꝛηᴧϻє :- <code> @{Info.username} </code>\n"
            f"𝐂‌ʜᴧηηєʟ 𝐂‌ʜᴧᴛ 𝐈‌ᴅ :- <code> {Info.id} </code>"
        )

        await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "chgtarget":

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

            try:
                target = await bot.ask(text=Txt.SEND_TARGET_CHANNEL, chat_id=query.message.chat.id, filters=filters.text, timeout=60)
            except:

                await bot.send_message(query.from_user.id, "𝐄‌ꝛꝛσꝛ!!\n\n𝐑‌єǫυєsᴛ ᴛɪϻєᴅ συᴛ.\n𝐑‌єsᴛᴧꝛᴛ ʙʏ υsɪηɢ /target", reply_to_message_id=target.id)
                return

            ms = await query.message.reply_text("**𝐏‌ʟєᴧsє 𝐖‌ᴧɪᴛ...**", reply_to_message_id=query.message.id)

            group_target_id = target.text
            gi = re.sub("(@)|(https://)|(http://)|(t.me/)",
                        "", group_target_id)

            for account in config['accounts']:
                # Run a shell command and capture its output
                try:

                    process = subprocess.Popen(
                        ["python", f"login.py", f"{gi}",
                            f"{account['Session_String']}"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                except Exception as err:
                    await bot.send_message(msg.chat.id, text=f"<b>𝐄‌𝐑‌𝐑‌𝐎‌𝐑‌ :</b>\n<pre>{err}</pre>")

                # Use communicate() to interact with the process
                stdout, stderr = process.communicate()

                # Get the return code
                return_code = process.wait()

                # Check the return code to see if the command was successful
                if return_code == 0:
                    # Print the output of the command
                    print("𝐂‌σϻϻᴧηᴅ συᴛᴘυᴛ:")
                    # Assuming output is a bytes object
                    output_bytes = stdout
                    # Decode bytes to string and replace "\r\n" with newlines
                    output_string = output_bytes.decode(
                        'utf-8').replace('\r\n', '\n')
                    print(output_string)

                else:
                    # Print the error message if the command failed
                    print("𝐂‌σϻϻᴧηᴅ ғᴧɪʟєᴅ ᴡɪᴛʜ єꝛꝛσꝛ:")
                    print(stderr)
                    return await query.message.edit('**𝐒‌σϻєᴛʜɪηɢ 𝐖‌єηᴛ 𝐖‌ꝛσηɢ 𝐊‌ɪηᴅʟʏ 𝐂‌ʜєᴄᴋ ʏσυꝛ 𝐈‌ηᴘυᴛs 𝐖‌ʜєᴛʜєꝛ 𝐘‌συ 𝐇‌ᴧᴠє 𝐅‌ɪʟʟєᴅ 𝐂‌σꝛꝛєᴄᴛʟʏ σꝛ 𝐍‌σᴛ !**')

            newConfig = {
                "Target": gi,
                "accounts": config['accounts']
            }

            with open(config_path, 'w', encoding='utf-8') as file:
                json.dump(newConfig, file, indent=4)

            await ms.edit("**𝐓‌ᴧꝛɢєᴛ 𝐔‌ᴘᴅᴧᴛєᴅ ✅**\n\n➜ 𝐔‌sє /target ᴛσ ᴄʜєᴄᴋ ʏσυꝛ ᴛᴧꝛɢєᴛ")
        except Exception as e:
            print('Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    elif data.startswith('delconfig'):
        condition = data.split('-')[1]
        try:
            if condition == 'yes':
                os.remove('config.json')
                await query.message.edit("**𝐒‌υᴄᴄєssғυʟʟʏ 𝐃‌єʟєᴛєᴅ ✅**")
            else:
                await query.message.edit("**𝐘‌συ 𝐂‌ᴧηᴄєʟєᴅ 𝐓‌ʜє 𝐏‌ꝛσᴄєss ❌**")
        except Exception as e:
            await query.message.edit(f"{e}\n\n n𝐄‌ꝛꝛσꝛ 😵")

    elif data == "account_config":

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

        else:
            return await query.message.edit(text="𝐘‌συ ᴅɪᴅη'ᴛ ϻᴧᴋє ᴧ ᴄσηғɪɢ ʏєᴛ !\n\n➜ 𝐅‌ɪꝛsᴛʟʏ ϻᴧᴋє ᴄσηғɪɢ ʙʏ υsɪηɢ /make_config", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='⟲ 𝐁‌ᴧᴄᴋ', callback_data='help')]]))

        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

        UserInfo = []
        for account in config["accounts"]:
            OwnerUid = account["OwnerUid"]
            OwnerName = account['OwnerName']
            UserInfo.append([InlineKeyboardButton(
                text=f"{OwnerName}", callback_data=f"{OwnerUid}")])

        UserInfo.append([InlineKeyboardButton(
            text='⟲ 𝐁‌ᴧᴄᴋ', callback_data='help')])

        await query.message.edit(text="**𝐓‌ʜє 𝐓‌єʟєɢꝛᴧϻ 𝐀‌ᴄᴄσυηᴛs 𝐘‌συ 𝐇‌ᴧᴠє 𝐀‌ᴅᴅєᴅ 👇**", reply_markup=InlineKeyboardMarkup(UserInfo))

    elif int(data) in [userId['OwnerUid'] for userId in (json.load(open("config.json")))['accounts']]:
        accountData = {}
        for account in (json.load(open("config.json")))['accounts']:
            if int(data) == account["OwnerUid"]:
                accountData.update({'Name': account['OwnerName']})
                accountData.update({'UserId': account['OwnerUid']})

        await query.message.edit(text=Txt.ACCOUNT_INFO.format(accountData.get('Name'), accountData.get('UserId')), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='⟲ 𝐁‌ᴧᴄᴋ', callback_data='help')]]))
        accountData = {}
