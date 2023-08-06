from os import remove
from os import environ
from pyrogram.types import Chat
from re import search as resr
from .misc import MARKDOWN_FIX_CHAR
from Geez import app


_LOG_ID = environ.get('BOTLOG_CHATID', None)
LOG_ID = int(_LOG_ID) if _LOG_ID and resr(r'^-?\d+$', _LOG_ID) else None
del _LOG_ID

def send(client, chat, text, fix_markdown=False, reply_id=None):
    if fix_markdown:
        text += MARKDOWN_FIX_CHAR

    if len(text) < 4096:
        if not reply_id:
            client.send_message(chat.id if isinstance(chat, Chat) else chat, text)
        else:
            client.send_message(
                chat.id if isinstance(chat, Chat) else chat,
                text,
                reply_to_message_id=reply_id,
            )
        return

    file = open('temp.txt', 'w+')
    file.write(text)
    file.close()
    send_doc(client, chat, 'temp.txt')


def send_sticker(client, chat, sticker):
    try:
        client.send_sticker(chat.id if isinstance(chat, Chat) else chat, sticker)
    except BaseException:
        pass


def send_doc(client, chat, doc, caption='', fix_markdown=False):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        client.send_document(
            chat.id if isinstance(chat, Chat) else chat, doc, caption=caption
        )
    except BaseException:
        pass

def send_log(text, fix_markdown=False):
    send(app, LOG_ID or 'me', text, fix_markdown=fix_markdown)


def send_log_doc(doc, caption='', fix_markdown=False, remove_file=False):
    send_doc(app, LOG_ID or 'me', doc, caption=caption, fix_markdown=fix_markdown)
    if remove_file:
        remove(doc)