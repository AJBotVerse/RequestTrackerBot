#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from os import environ
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Update,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

# Importing Credentials & Required Data
try:
    from testexp.config import Config
except ModuleNotFoundError:
    from config import Config


app = Client(
    session_name = "RequestBot",
    api_id = Config.API_ID,
    api_hash = Config.API_HASH,
    bot_token = Config.BOT_TOKEN
)


@app.on_message(filters.private & filters.command("start"))
async def startHandler(bot:Update, msg:Message):
    botInfo = await bot.get_me()
    await msg.reply_text(
        "Add me to your Group & Channel",
        parse_mode = "html",
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Add me to your Channel.",
                        url = f"https://telegram.me/{botInfo.username}?startgroup=true"
                    )
                ]
            ]
        )
    )

@app.on_message(filters.new_chat_members)
async def chatHandler(bot:Update, msg:Message):
    if msg.from_user == Config.OWNER_ID:
        if msg.new_chat_members[0].is_self:
            try:
                environ["GROUPID"]
            except KeyError:
                environ["GROUPID"] == str(msg.chat.id)
                await msg.reply_text(
                    "Group Added Successfully.",
                    parse_mode = "html"
                )
            else:
                await msg.reply_text(
                    "Group is already added.",
                    parse_mode = "html"
                )
    else:
        await msg.reply_text(
            "Deploy your Own Bot.",
            parse_mode = "html",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Click Here To Deploy",
                            url = "https://heroku.com/deploy?template=https://github.com/AJTimePyro/AJPyroManager"
                        )
                    ]
                ]
            )
        )



app.run()