from pyrogram.types import InlineKeyboardButton, WebAppInfo
from Geez import CMD_HNDLR as cmds
class Data:

    text_help_menu = (
        f"**Command List & Help**\n**— Prefixes:**{cmds}"
    )
    reopen = [[InlineKeyboardButton("Re-Open", callback_data="reopen")]]
