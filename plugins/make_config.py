import json
import os
from pathlib import Path
import re
import subprocess
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from info import Config, Txt


config_path = Path("config.json")


@Client.on_message(filters.private & filters.chat(Config.OWNER) & filters.command('make_config'))
async def make_config(bot: Client, msg: Message):
    try:
        if config_path.exists():
            return await msg.reply_text(text="**𝐘‌συ ʜᴧᴠє ᴧʟꝛєᴧᴅʏ ϻᴧᴅє ᴧ ᴄσηғɪɢ ғɪꝛsᴛ ᴅєʟєᴛє ɪᴛ ᴛʜєη ʏσυ'ʟʟ ᴧʙʟє ᴛσ ϻᴧᴋє ɪᴛ ᴄσηғɪɢ**\n\n➜ 𝐔‌sє /del_config", reply_to_message_id=msg.id)
        else:

            while True:

                try:
                    n = await bot.ask(text=Txt.SEND_NUMBERS_MSG, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:
                    await bot.send_message(msg.from_user.id, "𝐄‌ꝛꝛσꝛ!!\n\n𝐑‌єǫυєsᴛ ᴛɪϻєᴅ συᴛ.\n𝐑‌єsᴛᴧꝛᴛ ʙʏ υsɪηɢ /make_config", reply_to_message_id=n.id)
                    return

                try:
                    target = await bot.ask(text=Txt.SEND_TARGET_CHANNEL, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:

                    await bot.send_message(msg.from_user.id, "𝐄‌ꝛꝛσꝛ!!\n\n𝐑‌єǫυєsᴛ ᴛɪϻєᴅ συᴛ.\n𝐑‌єsᴛᴧꝛᴛ ʙʏ υsɪηɢ /make_config", reply_to_message_id=msg.id)
                    return

                if str(n.text).isnumeric():

                    if not str(target.text).isnumeric():
                        break
                    else:
                        await msg.reply_text(text="⚠️ **𝐏‌ʟєᴧsє 𝐒‌єηᴅ 𝐕‌ᴧʟɪᴅ 𝐓‌ᴧꝛɢєᴛ 𝐂‌ʜᴧηηєʟ 𝐋‌ɪηᴋ σꝛ 𝐔‌sєꝛηᴧϻє !**", reply_to_message_id=target.id)
                        continue

                else:
                    await msg.reply_text(text="⚠️ **𝐏‌ʟєᴧsє 𝐒‌єηᴅ 𝐈‌ηᴛєɢєꝛ 𝐍‌υϻʙєꝛ ησᴛ 𝐒‌ᴛꝛɪηɢ !**", reply_to_message_id=n.id)
                    continue

            group_target_id = target.text
            gi = re.sub("(@)|(https://)|(http://)|(t.me/)",
                        "", group_target_id)

            try:
                await bot.get_chat(gi)
            except Exception as e:
                return await msg.reply_text(text=f"{e} \n\n𝐄‌ꝛꝛσꝛ !", reply_to_message_id=target.id)

            config = {
                "Target": gi,
                "accounts": []
            }

            for _ in range(int(n.text)):
                try:
                    session = await bot.ask(text=Txt.SEND_SESSION_MSG, chat_id=msg.chat.id, filters=filters.text, timeout=60)
                except:
                    await bot.send_message(msg.from_user.id, "𝐄‌ꝛꝛσꝛ!!\n\n𝐑‌єǫυєsᴛ ᴛɪϻєᴅ συᴛ.\n𝐑‌єsᴛᴧꝛᴛ ʙʏ υsɪηɢ /make_config", reply_to_message_id=msg.id)
                    return

                for acocunt in config['accounts']:
                    if acocunt['Session_String'] == session.text:
                        return await msg.reply_text(text=f"**{acocunt['OwnerName']} ᴧᴄᴄσυηᴛ ᴧʟꝛєᴧᴅʏ єxɪsᴛ ɪη ᴄσηғɪɢ ʏσυ ᴄᴧη'ᴛ ᴧᴅᴅ sᴧϻє ᴧᴄᴄσυηᴛ ϻυʟᴛɪᴘʟє ᴛɪϻєs 🤡**\n\n𝐄‌ꝛꝛσꝛ !")

                # Run a shell command and capture its output
                try:

                    process = subprocess.Popen(
                        ["python", f"login.py",
                            f"{config['Target']}", f"{session.text}"],
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
                    AccountHolder = json.loads(output_string)

                else:
                    # Print the error message if the command failed
                    print("𝐂‌σϻϻᴧηᴅ ғᴧɪʟєᴅ ᴡɪᴛʜ єꝛꝛσꝛ:")
                    print(stderr)
                    return await msg.reply_text('**𝐒‌σϻєᴛʜɪηɢ 𝐖‌єηᴛ 𝐖‌ꝛσηɢ 𝐊‌ɪηᴅʟʏ 𝐂‌ʜєᴄᴋ ʏσυꝛ 𝐈‌ηᴘυᴛs 𝐖‌ʜєᴛʜєꝛ 𝐘‌συ 𝐇‌ᴧᴠє 𝐅‌ɪʟʟєᴅ 𝐂‌σꝛꝛєᴄᴛʟʏ σꝛ 𝐍‌σᴛ !**')

                try:

                    new_account = {
                        "Session_String": session.text,
                        "OwnerUid": AccountHolder['id'],
                        "OwnerName": AccountHolder['first_name']
                    }
                    config["accounts"].append(new_account)

                    with open(config_path, 'w', encoding='utf-8') as file:
                        json.dump(config, file, indent=4)
                except Exception as e:
                    print(e)

            acocunt_btn = [
                [InlineKeyboardButton(
                    text='𝐀‌ᴄᴄσυηᴛs 𝐘‌συ 𝐀‌ᴅᴅєᴅ', callback_data='account_config')]
            ]
            await msg.reply_text(text=Txt.MAKE_CONFIG_DONE_MSG.format(n.text), reply_to_message_id=n.id, reply_markup=InlineKeyboardMarkup(acocunt_btn))

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_message(filters.private & filters.chat(Config.OWNER) & filters.command('see_accounts'))
async def see_account(bot: Client, msg: Message):

    try:

        config = (json.load(open("config.json")))['accounts']
        acocunt_btn = [
            [InlineKeyboardButton(text='𝐀‌ᴄᴄσυηᴛs 𝐘‌συ 𝐀‌ᴅᴅєᴅ',
                                  callback_data='account_config')]
        ]
        await msg.reply_text(text=Txt.ADDED_ACCOUNT.format(len(config)), reply_to_message_id=msg.id, reply_markup=InlineKeyboardMarkup(acocunt_btn))

    except:
        return await msg.reply_text(text="**𝐘‌συ 𝐃‌ση'ᴛ 𝐇‌ᴧᴠє 𝐀‌ᴅᴅєᴅ 𝐀‌ηʏ 𝐀‌ᴄᴄσυηᴛs 𝟶️⃣**\n\n➜ 𝐔‌sє /make_config ᴛσ ᴧᴅᴅ ᴧᴄᴄσυηᴛs 👥", reply_to_message_id=msg.id)
