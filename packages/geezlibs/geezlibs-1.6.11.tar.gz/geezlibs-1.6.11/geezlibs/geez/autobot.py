import asyncio
import sys
from random import randint

import heroku3

from Geez import (
    LOGGER,
    BOT_TOKEN,
    BOTLOG_CHATID,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    LOGS,
    bot1,
)

heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


async def sayur_asem():
    LOGGER.info("Membuat Group Log")
    group_name = "Gezz Pyro Log Chat"
    desc = "Gezz Pyro Log Chat, Jangan delete atau keluar dari group"
    try:
        _id = await bot1.create_supergroup(group_name, desc)
        link = await bot1.get_chat(_id["id"])
    except Exception as e:
        LOGS.error(str(e))
        LOGS.warning(
            "var BOTLOG_CHATID kamu belum di isi. Buatlah grup telegram dan masukan bot @geezramrobot lalu ketik /id Masukan id grup nya di var BOTLOG_CHATID"
        )
    if not str(grup_id).startswith("-100"):
        grup_id = int(f"-100{str(grup_id)}")
    heroku_var["BOTLOG_CHATID"] = grup_id
        
        
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
        LOGS.info(
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
            LOGS.info(
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
            LOGS.info(
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
        LOGS.info(
            "Silakan Hapus Beberapa Bot Telegram Anda di @Botfather atau Set Var BOT_TOKEN dengan token bot"
        )