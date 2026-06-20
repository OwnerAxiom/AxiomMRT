import json
from pathlib import Path
import subprocess
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from info import Config, Txt

config_path = Path("config.json")


@Client.on_message(filters.private & filters.user(Config.OWNER) & filters.command('add_account'))
async def add_account(bot: Client, cmd: Message):
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

        else:
            return await cmd.reply_text(text="𝐘‌συ ᴅɪᴅη'ᴛ ϻᴧᴋє ᴧ ᴄσηғɪɢ ʏєᴛ !\n\n➜ 𝐅‌ɪꝛsᴛʟʏ ϻᴧᴋє ᴄσηғɪɢ ʙʏ υsɪηɢ /make_config", reply_to_message_id=cmd.id)

        try:
            session = await bot.ask(text=Txt.SEND_SESSION_MSG, chat_id=cmd.chat.id, filters=filters.text, timeout=60)
        except:
            await bot.send_message(cmd.from_user.id, "𝐄‌ꝛꝛσꝛ!!\n\n𝐑‌єǫυєsᴛ ᴛɪϻєᴅ συᴛ.\n𝐑‌єsᴛᴧꝛᴛ ʙʏ υsɪηɢ /make_config", reply_to_message_id=session.id)
            return

        ms = await cmd.reply_text('**𝐏‌ʟєᴧsє 𝐖‌ᴧɪᴛ...**', reply_to_message_id=cmd.id)

        for acocunt in config['accounts']:
            if acocunt['Session_String'] == session.text:
                return await ms.edit(text=f"**{acocunt['OwnerName']} ᴧᴄᴄσυηᴛ ᴧʟꝛєᴧᴅʏ єxɪsᴛ ɪη ᴄσηғɪɢ ʏσυ ᴄᴧη'ᴛ ᴧᴅᴅ sᴧϻє ᴧᴄᴄσυηᴛ ϻυʟᴛɪᴘʟє ᴛɪϻєs 🤡**\n\n𝐄‌ꝛꝛσꝛ !")

        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

         # Run a shell command and capture its output
        try:

            process = subprocess.Popen(
                ["python", f"login.py",
                    f"{config['Target']}", f"{session.text}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            await bot.send_message(cmd.chat.id, text=f"<b>𝐄‌𝐑‌𝐑‌𝐎‌𝐑‌ :</b>\n<pre>{err}</pre>")

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
            output_string = output_bytes.decode('utf-8').replace('\r\n', '\n')
            print(output_string)
            AccountHolder = json.loads(output_string)

        else:
            # Print the error message if the command failed
            print("𝐂‌σϻϻᴧηᴅ ғᴧɪʟєᴅ ᴡɪᴛʜ єꝛꝛσꝛ:")
            print(stderr)
            return await ms.edit('**𝐒‌σϻєᴛʜɪηɢ 𝐖‌єηᴛ 𝐖‌ꝛσηɢ 𝐊‌ɪηᴅʟʏ 𝐂‌ʜєᴄᴋ ʏσυꝛ 𝐈‌ηᴘυᴛs 𝐖‌ʜєᴛʜєꝛ 𝐘‌συ 𝐇‌ᴧᴠє 𝐅‌ɪʟʟєᴅ 𝐂‌σꝛꝛєᴄᴛʟʏ σꝛ 𝐍‌σᴛ !**')

        try:
            NewConfig = {
                "Target": config['Target'],
                "accounts": list(config['accounts'])
            }

            new_account = {
                "Session_String": session.text,
                "OwnerUid": AccountHolder['id'],
                "OwnerName": AccountHolder['first_name']
            }
            NewConfig["accounts"].append(new_account)

            with open(config_path, 'w', encoding='utf-8') as file:
                json.dump(NewConfig, file, indent=4)

        except Exception as e:
            print(e)

        await ms.edit(text="**𝐀‌ᴄᴄσυηᴛ 𝐀‌ᴅᴅєᴅ 𝐒‌υᴄᴄєssғυʟʟʏ ✅**\n\n➜ 𝐂‌ʟɪᴄᴋ ᴛʜє ʙυᴛᴛση ʙєʟσᴡ ᴛσ ᴠɪєᴡ ᴧʟʟ ᴛʜє ᴧᴄᴄσυηᴛs ʏσυ ʜᴧᴠє ᴧᴅᴅєᴅ 👇.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='𝐀‌ᴄᴄσυηᴛs 𝐘‌συ 𝐀‌ᴅᴅєᴅ', callback_data='account_config')]]))

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_message(filters.private & filters.user(Config.OWNER) & filters.command('target'))
async def target(bot: Client, cmd: Message):

    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

        else:
            return await cmd.reply_text(text="𝐘‌συ ᴅɪᴅη'ᴛ ϻᴧᴋє ᴧ ᴄσηғɪɢ ʏєᴛ !\n\n➜ 𝐅‌ɪꝛsᴛʟʏ ϻᴧᴋє ᴄσηғɪɢ ʙʏ υsɪηɢ /make_config", reply_to_message_id=cmd.id)

        Info = await bot.get_chat(config['Target'])

        btn = [
            [InlineKeyboardButton(text='𝐂‌ʜᴧηɢє 𝐓‌ᴧꝛɢєᴛ',
                                  callback_data='chgtarget')]
        ]

        text = (
            f"𝐂‌ʜᴧηηєʟ 𝐍‌ᴧϻє :- <code> {Info.title} </code>\n"
            f"𝐂‌ʜᴧηηєʟ 𝐔‌sєꝛηᴧϻє :- <code> @{Info.username} </code>\n"
            f"𝐂‌ʜᴧηηєʟ 𝐂‌ʜᴧᴛ 𝐈‌ᴅ :- <code> {Info.id} </code>"
        )

        await cmd.reply_text(text=text, reply_to_message_id=cmd.id, reply_markup=InlineKeyboardMarkup(btn))
    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_message(filters.private & filters.user(Config.OWNER) & filters.command('del_config'))
async def delete_config(bot: Client, cmd: Message):

    btn = [
        [InlineKeyboardButton(text='𝐘‌єs', callback_data='delconfig-yes')],
        [InlineKeyboardButton(text='𝐍‌σ', callback_data='delconfig-no')]
    ]

    await cmd.reply_text(text="**⚠️ 𝐀‌ꝛє ʏσυ 𝐒‌υꝛє ?**\n\n➜ 𝐘‌συ ᴡᴧηᴛ ᴛσ ᴅєʟєᴛє ᴛʜє 𝐂‌σηғɪɢ.", reply_to_message_id=cmd.id, reply_markup=InlineKeyboardMarkup(btn))
