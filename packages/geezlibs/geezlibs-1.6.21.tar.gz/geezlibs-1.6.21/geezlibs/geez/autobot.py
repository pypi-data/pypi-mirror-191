import asyncio
import sys
import socket
import dotenv
from random import randint
from pyrogram import Client
import heroku3

from config import (
    API_ID,
    API_HASH,
    STRING_SESSION1,
    BOT_TOKEN,
    BOTLOG_CHATID,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
)
HAPP = None

bot1 = (
    Client(
        name="bot1",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION1,))

def is_heroku():
    return "heroku" in socket.getfqdn()

def heroku():
    global HAPP
    if is_heroku:
        if HEROKU_API_KEY and HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(HEROKU_API_KEY)
                HAPP = Heroku.app(HEROKU_APP_NAME)
                print("Geez").info(f"Heroku App Configured")
            except BaseException as e:
                print("Heroku").error(e)
                print("Heroku").info(
                    f"Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku."
                )

async def in_heroku():
    return "heroku" in socket.getfqdn()

heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


async def sayur_asem():
    await bot1.start()
    if HAPP is None:
        return
    print("Membuat Group log")
    desc = "Group Log untuk RamPyro-Bot.\n\nHARAP JANGAN KELUAR DARI GROUP INI.\n\n⭐ Powered By ~ @userbotch ⭐"
    try:
        gruplog = await bot1.create_supergroup("Logs RamPyro-Bot", desc)
        if await in_heroku():
            heroku_var = HAPP.config()
            heroku_var["BOTLOG_CHATID"] = gruplog.id
        else:
            path = dotenv.find_dotenv("config.env")
            dotenv.set_key(path, "BOTLOG_CHATID", gruplog.id)
    except Exception:
        print("var BOTLOG_CHATID kamu belum di isi. Buatlah grup telegram dan masukan bot @MissRose_bot lalu ketik /id Masukan id grup nya di var BOTLOG_CHATID"
        )
        
        
async def jengkol_balado():
    if BOT_TOKEN:
        return
    await bot1.start()
    await bot1.send_message(
        BOTLOG_CHATID, "**GUA LAGI BIKIN BOT ASISSTANT DI @BOTFATHER YA NGENTOD, SABAR DULU LU, KALO GA SABAR MATI AJA NYUSUL BAPAK LO**"
    )
    who = await bot1.get_me()
    name = who.first_name + " Assistant"
    if who.username:
        username = who.username + "_ubot"
    else:
        username = "geez" + (str(who.id))[5:] + "ubot"
    bf = "BotFather"
    await bot1.unblock_user(bf)
    await bot1.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await bot1.send_message(bf, "/start")
    await asyncio.sleep(1)
    await bot1.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await bot1.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        print(
            "Silakan buat Bot dari @BotFather dan tambahkan tokennya di var BOT_TOKEN"
        )
        sys.exit(1)
    await bot1.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await bot1.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot1.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await bot1.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            print(
                "Silakan buat Bot dari @BotFather dan tambahkan tokennya di var BOT_TOKEN"
            )
            sys.exit(1)
    await bot1.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await bot1.get_messages(bf, limit=1))[0].text
    await bot1.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "Asisstant" + (str(who.id))[6:] + str(ran) + "Bot"
        await bot1.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await bot1.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            await bot1.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await bot1.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot1.send_message(bf, "Search")
            await asyncio.sleep(3)
            await bot1.send_message(bf, "/setuserpic")
            await asyncio.sleep(1)
            await bot1.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot1.send_file(bf, "geezlibs/raw/geez.png")
            await asyncio.sleep(3)
            await bot1.send_message(bf, "/setabouttext")
            await asyncio.sleep(1)
            await bot1.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot1.send_message(bf, f"Asisstan punya si kontol {who.first_name}")
            await asyncio.sleep(3)
            await bot1.send_message(bf, "/setdescription")
            await asyncio.sleep(1)
            await bot1.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot1.send_message(
                bf, f"Owner ~ {who.first_name}\n\n Powered By Geez|Ram"
            )
            await bot1.send_message(
                BOTLOG_CHATID,
                f"**BERHASIL MEMBUAT BOT TELEGRAM DENGAN USERNAME @{username}**",
            )
            await bot1.send_message(
                BOTLOG_CHATID,
                "**Tunggu Sebentar, Sedang MeRestart Heroku untuk Menerapkan Perubahan.**",
            )
            heroku_var["BOT_TOKEN"] = token
            heroku_var["BOT_USERNAME"] = f"@{username}"
        else:
            print(
                "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
            )
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        await bot1.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await bot1.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot1.send_message(bf, "Search")
        await asyncio.sleep(3)
        await bot1.send_message(bf, "/setuserpic")
        await asyncio.sleep(1)
        await bot1.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot1.send_file(bf, "userbot/utils/styles/asisstant.jpg")
        await asyncio.sleep(3)
        await bot1.send_message(bf, "/setabouttext")
        await asyncio.sleep(1)
        await bot1.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot1.send_message(bf, f"Buatan anak kontol {who.first_name}")
        await asyncio.sleep(3)
        await bot1.send_message(bf, "/setdescription")
        await asyncio.sleep(1)
        await bot1.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot1.send_message(
            bf, f"{who.first_name} \n\n Powered By ~ Geez|Ram "
        )
        await bot1.send_message(
            BOTLOG_CHATID,
            f"**BERHASIL MEMBUAT BOT TELEGRAM DENGAN USERNAME @{username}**",
        )
        await bot1.send_message(BOTLOG_CHATID, f"/invite {username}")
        await bot1.send_message(
            BOTLOG_CHATID,
            "**Tunggu Sebentar, Sedang MeRestart Heroku untuk Menerapkan Perubahan.**",
        )
        heroku_var["BOT_TOKEN"] = token
        heroku_var["BOT_USERNAME"] = f"@{username}"
    else:
        print(
            "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
        )