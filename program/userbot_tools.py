import asyncio
from driver.veez import user
from pyrogram.types import Message
from pyrogram import Client, filters
from config import BOT_USERNAME, SUDO_USERS
from driver.filters import command, other_filters
from driver.filters import command2, other_filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from driver.decorators import authorized_users_only, sudo_users_only
from config import SUDO_USERS, ASSISTANT_NAME
from driver.decorators import authorized_users_only, sudo_users_only, errors


@Client.on_message(
    command(["userbotjoin"]) & other_filters
)
@authorized_users_only
async def join_chat(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    try:
        invitelink = await c.export_chat_invite_link(chat_id)
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
            await user.join_chat(invitelink)
            return await user.send_message(chat_id, "انا جيت اهو يارب مكونش اتٲخرت")
    except UserAlreadyParticipant:
        return await user.send_message(chat_id, "انا موجود هنا😐")

@Client.on_message(
    command2(["انضم"]) & other_filters
)
@authorized_users_only
async def join_chat(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    try:
        invitelink = await c.export_chat_invite_link(chat_id)
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
            await user.join_chat(invitelink)
            return await user.send_message(chat_id, "انا جيت اهو يارب مكونش اتٲخرت")
    except UserAlreadyParticipant:
        return await user.send_message(chat_id, "انا موجود هنا😐")

@Client.on_message(
    command(["userbotleave"]) & other_filters
)
@authorized_users_only
async def leave_chat(_, m: Message):
    await m.delete()
    chat_id = m.chat.id
    try:
        await user.leave_chat(chat_id)
        return await _.send_message(
            chat_id,
            "✅ غادر الحساب المساعد المجموعه بنجاح",
        )
    except UserNotParticipant:
        return await _.send_message(
            chat_id,
            "❌ غادر الحساب المساعد المجموعه بالفعل",
        )
        
@Client.on_message(
    command2(["غادر","خروج المساعد"]) & other_filters
)
@authorized_users_only
async def leave_chat(_, m: Message):
    await m.delete()
    chat_id = m.chat.id
    try:
        await user.leave_chat(chat_id)
        return await _.send_message(
            chat_id,
            "✅ غادر الحساب المساعد المجموعه بنجاح",
        )
    except UserNotParticipant:
        return await _.send_message(
            chat_id,
            "❌ غادر الحساب المساعد المجموعه بالفعل",
        )


@Client.on_message(command(["leaveall"]))
@sudo_users_only
async def leave_all(client, message):
    await message.delete()
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    
    msg = await message.reply("🔄 Userbot leaving all Group !")
    async for dialog in user.iter_dialogs():
        try:
            await user.leave_chat(dialog.chat.id)
            left += 1
            await msg.edit(
                f"Userbot leaving all Group...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        except BaseException:
            failed += 1
            await msg.edit(
                f"Userbot leaving...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await msg.delete()
    await client.send_message(
        message.chat.id, f"✅ Left from: {left} chats.\n❌ Failed in: {failed} chats."
    )
    
@Client.on_message(command2(["مغادره"]))
@sudo_users_only
async def leave_all(client, message):
    await message.delete()
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    
    msg = await message.reply("🔄 Userbot leaving all Group !")
    async for dialog in user.iter_dialogs():
        try:
            await user.leave_chat(dialog.chat.id)
            left += 1
            await msg.edit(
                f"Userbot leaving all Group...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        except BaseException:
            failed += 1
            await msg.edit(
                f"Userbot leaving...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await msg.delete()
    await client.send_message(
        message.chat.id, f"✅ Left from: {left} chats.\n❌ Failed in: {failed} chats."
    )

@Client.on_message(filters.left_chat_member)
async def ubot_leave(c: Client, m: Message):
#    ass_id = (await user.get_me()).id
    bot_id = (await c.get_me()).id
    chat_id = m.chat.id
    left_member = m.left_chat_member
    if left_member.id == bot_id:
        await user.leave_chat(chat_id)
#    elif left_member.id == ass_id:
#        await c.leave_chat(chat_id)
