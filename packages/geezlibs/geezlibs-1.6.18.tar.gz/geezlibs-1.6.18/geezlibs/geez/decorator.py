import logging
from datetime import datetime
from traceback import format_exc
import pytz
from geezlibs import ContinuePropagation, StopPropagation, filters
from geezlibs.enums import ChatMemberStatus, ChatType
from geezlibs.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    MessageEmpty,
    UserNotParticipant
)
from geezlibs.handlers import MessageHandler

from geezlibs.geez._wrappers import eor

from geezlibs import DEVS
from Geez import BOTLOG_CHATID, app, cmds, bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9, bot10

async def is_admin_or_owner(message, user_id) -> bool:
    """Check If A User Is Creator Or Admin Of The Current Group"""
    if message.chat.type in [ChatType.PRIVATE, ChatType.BOT]:
        # You Are Boss Of Pvt Chats.
        return True
    user_s = await message.chat.get_member(int(user_id))
    if user_s.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR):
        return True
    return False


def geez(
    cmd: list,
    group: int = 0,
    devs: bool = False,
    pm_only: bool = False,
    group_only: bool = False,
    channel_only: bool = False,
    admin_only: bool = False,
    pass_error: bool = False,
    propagate_to_next_handler: bool = True,
):
    """- Main Decorator To Register Commands. -"""
    if not devs:
        filterm = (
            filters.me
            & filters.command(cmd, cmds)
            & ~filters.via_bot
            & ~filters.forwarded
        )
    else:
        filterm = (
            filters.user(DEVS)
            & filters.command(cmd, "*")
        )

    def decorator(func):
        async def wrapper(client, message):
            message.client = client
            chat_type = message.chat.type
            if admin_only and not await is_admin_or_owner(
                message, (client.me).id
            ):
                await eor(
                    message, "<code>This Command Only Works, If You Are Admin Of The Chat!</code>"
                )
                return
            if group_only and chat_type != (
                    ChatType.GROUP or ChatType.SUPERGROUP):
                await eor(message, "<code>Are you sure this is a group?</code>")
                return
            if channel_only and chat_type != ChatType.CHANNEL:
                await eor(message, "This Command Only Works In Channel!")
                return
            if pm_only and chat_type != ChatType.PRIVATE:
                await eor(message, "<code>This Cmd Only Works On PM!</code>")
                return
            if pass_error:
                await func(client, message)
            else:
                try:
                    await func(client, message)
                except StopPropagation:
                    raise StopPropagation
                except KeyboardInterrupt:
                    pass
                except MessageNotModified:
                    pass
                except MessageIdInvalid:
                    logging.warning(
                        "Please Don't Delete Commands While it's Processing..."
                    )
                except UserNotParticipant:
                    pass
                except ContinuePropagation:
                    raise ContinuePropagation
                except BaseException:
                    logging.error(
                        f"Exception - {func.__module__} - {func.__name__}"
                    )
                    TZZ = pytz.timezone("Asia/Jakarta")
                    datetime_tz = datetime.now(TZZ)
                    text = "<b>!ERROR - REPORT!</b>\n\n"
                    text += f"\n<b>Dari:</b> <code>{client.me.first_name}</code>"
                    text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                    text += f"\n<b>Plugin-Name :</b> <code>{func.__module__}</code>"
                    text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                    text += datetime_tz.strftime(
                        "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                    )
                    try:
                        xx = await app.send_message(BOTLOG_CHATID, text)
                        await xx.pin(disable_notification=False)
                    except BaseException:
                        logging.error(text)
        add_handler(filterm, wrapper, cmd)
        return wrapper

    return decorator


def listen(filter_s):
    """Simple Decorator To Handel Custom Filters"""
    def decorator(func):
        async def wrapper(client, message):
            try:
                await func(client, message)
            except StopPropagation:
                raise StopPropagation
            except ContinuePropagation:
                raise ContinuePropagation
            except UserNotParticipant:
                pass
            except MessageEmpty:
                pass
            except BaseException:
                logging.error(
                    f"Exception - {func.__module__} - {func.__name__}")
                TZZ = pytz.timezone("Asia/Jakarta")
                datetime_tz = datetime.now(TZZ)
                text = "<b>!ERROR WHILE HANDLING UPDATES!</b>\n\n"
                text += f"\n<b>Dari:</b> <code>{client.me.first_name}</code>"
                text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                text += f"\n<b>Plugin Name :</b> <code>{func.__module__}</code>"
                text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                text += datetime_tz.strftime(
                    "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                )
                try:
                    xx = await app.send_message(BOTLOG_CHATID, text)
                    await xx.pin(disable_notification=False)
                except BaseException:
                    logging.error(text)
            message.continue_propagation()
        if bot1:
            bot1.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot2:
            bot2.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot3:
            bot3.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot4:
            bot4.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot5:
            bot5.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot6:
            bot6.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot7:
            bot7.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot8:
            bot8.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot9:
            bot9.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if bot10:
            bot10.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)

        return wrapper

    return decorator


def add_handler(filter_s, func_, cmd):
    if bot1:
        bot1.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot2:
        bot2.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot3:
        bot3.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot4:
        bot4.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot5:
        bot5.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot6:
        bot6.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot7:
        bot7.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot8:
        bot8.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot9:
        bot9.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if bot10:
        bot10.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    
