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
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired

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
    return

@Client.on_message(filters.forwarded & filters.private)
async def forwardedHandler(bot:Update, msg:Message):
    if msg.id == Config.OWNER_ID:
        forwardInfo = msg.forward_from_chat
        if forwardInfo.type == "channel":
            try:
                environ["CHANNELID"]
            except KeyError:
                channelID = forwardInfo.id
                try:
                    botStatus = await bot.get_chat_member(channelID, 'me')
                except ChatAdminRequired:
                    await msg.reply_text(
                    "Make me admin in your Channel, and forward message from channel again",
                    parse_mode = "html"
                    )
                else:
                    adminRights = [botStatus.can_post_messages, botStatus.can_edit_messages, botStatus.can_delete_messages]
                    for right in adminRights:
                        if not right:
                            await msg.reply_text(
                                "Make sure to give permission to Post, Edit & Delete Message",
                                parse_mode = "html"
                            )
                            break
                    else:
                        environ["CHANNELID"] = str(channelID)
                        await msg.reply_text(
                            "Channel Connected Successfully.",
                            parse_mode = "html"
                        )
            else:
                await msg.reply_text(
                    "Channel is already connected.",
                    parse_mode = "html"
                )
    return

@app.on_message(filters.group & filters.regex("^#request (.*)"))
async def requestHandler(bot:Update, msg:Message):
    # try:
    #     environ["CHANNELID"]
    #     environ["GROUPID"]
    # except KeyError:
    #     return
    # else:
    #     print(msg)
    # if msg.chat.id == int(environ["GROUPID"]):
    if msg.chat.id == -1001664940650:
        fromUser = msg.from_user
        requestText = f"<b>Request by <a href='tg://user?id={fromUser.id}'>{fromUser.first_name}</a>\n\n{msg.text}</b>"
        # await bot.send_message(int(environ["CHANNELID"]))
        await bot.send_message(-1001664615028, requestText, reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Requested Message", url = f"https://t.me/c/1664940650/{msg.message_id}")],
            [InlineKeyboardButton("🚫Reject", "reject"),
            InlineKeyboardButton("Done✅", "done")],
            [InlineKeyboardButton("⚠️Unavailable⚠️", "unavailable")]
        ]))
        replyText = ""
        await msg.reply_text()
    # print(msg)




app.run()