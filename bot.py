#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Update,
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired

# Importing Credentials & Required Data
try:
    from testexp.config import *
except ModuleNotFoundError:
    from config import *


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

@app.on_message(filters.forwarded & filters.private)
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
    try:
        environ["CHANNELID"]
        environ["GROUPID"]
    except KeyError:
        return
    else:
        chatInfo = msg.chat
        
        groupID = environ["GROUPID"]
        channelID = environ["CHANNELID"]

        if chatInfo.id == int(groupID):
            fromUser = msg.from_user
            mentionUser = f"<a href='tg://user?id={fromUser.id}'>{fromUser.first_name}</a>"
            requestText = f"<b>Request by {mentionUser}\n\n{msg.text}</b>"
            
            groupIDPro = groupID.removeprefix(str(-100))

            channelIDPro = channelID.removeprefix(str(-100))

            requestMSG = await bot.send_message(
                int(channelID),
                requestText,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Requested Message",
                                url = f"https://t.me/c/{groupIDPro}/{msg.message_id}"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "🚫Reject",
                                "reject"
                            ),
                            InlineKeyboardButton(
                                "Done✅",
                                "done"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "⚠️Unavailable⚠️",
                                "unavailable"
                            )
                        ]
                    ]
                )
            )

            replyText = f"<b>👋 Hello {mentionUser} !!\n\n📍 Your Request for {chatInfo.title} has been submitted to the admins.\n\n🚀 Your Request Will Be Uploaded In 48hours or less.\n📌 Please Note that Admins might be busy. So, this may take more time.\n\n👇 See Your Request Status Here 👇</b>"

            await msg.reply_text(
                replyText,
                parse_mode = "html",
                reply_to_message_id = msg.message_id,
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "⏳Request Status⏳",
                                url = f"https://t.me/c/{channelIDPro}/{requestMSG.message_id}"
                            )
                        ]
                    ]
                )
            )

@app.on_callback_query()
async def callBackButton(bot:Update, callback_query:CallbackQuery):
    if callback_query.from_user.id == Config.OWNER_ID:
        data = callback_query.data

        if data == "reject":
            result = "REJECTED"
            groupResult = "has been Rejected."
            button = InlineKeyboardButton("Request Rejected🚫", "rejected")
        elif data == "done":
            result = "COMPLETED"
            groupResult = "is Completed."
            button = InlineKeyboardButton("Request Completed✅", "completed")
        elif data == "unavailable":
            result = "UNAVAILABLE"
            groupResult = "has been rejected due to Unavailablity."
            button = InlineKeyboardButton("Request Rejected🚫", "rejected")

        elif data == "rejected":
            return await callback_query.answer(
                "This request Is Completed...\nCheckout in Channel",
                show_alert = True
            )
        elif data == "completed":
            return await callback_query.answer(
                "This request is rejected...\nAsk admins in group for more info",
                show_alert = True
            )

        msg = callback_query.message
        originalMsg = msg.text
        animeRequested = originalMsg.split('#request ')[1]
        requestedBy = originalMsg.removeprefix("Request by ").split('\n\n')[0]
        userid = msg.entities[1].user.id
        mentionUser = f"<a href='tg://user?id={userid}'>{requestedBy}</a>"
        originalMsgMod = originalMsg.replace(requestedBy, mentionUser)
        originalMsgMod = f"<s>{originalMsgMod}</s>"

        newMsg = f"<b>{result}</b>\n\n{originalMsgMod}"

        await callback_query.edit_message_text(
            newMsg,
            parse_mode = "html",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        button
                    ]
                ]
            )
        )

        replyText = f"Dear {mentionUser}\nYour request for {animeRequested} {groupResult}\nThanks for requesting!"
        groupID = environ["GROUPID"]
        await bot.send_message(
            groupID,
            replyText,
            parse_mode = "html"
        )
    else:
        await callback_query.answer(
            "Your are not Owner.",
            show_alert = True
        )
    return


app.run()

