 # Powered by @Darkranger00 | TELE:- @aadillllll
# Dear Pero ppls Plish Don't remove this line from here🌚
# created by Aadil Shiekh
import logging
import re
import os
import sys, platform
# import functie as S
from asyncio import sleep
from os import getenv
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
import telethon.utils
from telethon.tl import functions
from telethon.tl.functions.channels import LeaveChannelRequest
from asyncio import sleep
from telethon import __version__ as tel
from str import dad as gg, dady as g, startxt2, startxt, hlptxt
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChatAdminRights
from telethon.tl.functions.channels import EditBannedRequest
from datetime import datetime

#Logging...
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
API_ID = "10738943"
API_HASH = "da61e3a08b5ac78ce28b4a4cd854aeec"
BOT_TOKEN = "7269425990:AAElkYfpjGBp0rI2sLtRb83lKLIK7IMhrYk"
OWNER_ID = "8016828914"
SUDO_ID = "8016828914"
LUCIFER = "8016828914"
COWNER_ID = "8016828914"
OP  = [ int(OWNER_ID), int(SUDO_ID), int(COWNER_ID), int(LUCIFER)]
#TelegramClient..
sree = TelegramClient(
    "BanAll",
    api_id=API_ID,
    api_hash=API_HASH
).start(bot_token=BOT_TOKEN)

Owner = "@Arayanlarbulamadi"
repo = "https://github.com/Darkanger00/Banall"


      

@app.on_message(
    filters.command("b") 
    & filters.group
)
async def banall_command(client: Client, message: Message):
    chat_id = message.chat.id
    bot = await client.get_me()  # Bot ka ID aur admin status check karne ke liye
    bot_id = bot.id

    print(f"Checking bot permissions in {chat_id}...")

    # Pehle check karo ki bot admin hai ya nahi
    chat_member = await client.get_chat_member(chat_id, bot_id)
    if chat_member.status not in ["administrator", "creator"]:
        print("Bot is not an admin! Make the bot an admin with 'Ban Members' permission.")
        await message.reply_text("❌ Bot is not an admin! Please give me 'Ban Members' permission.")
        return

    print(f"Bot is admin in {chat_id}. Starting ban process...")

    async for member in client.get_chat_members(chat_id):
        user_id = member.user.id

        # Self-ban prevent
        if user_id == bot_id:
            print("Skipping self-ban attempt.")
            continue

        # Admins ko skip karo
        if member.status in ["administrator", "creator"]:
            print(f"Skipping admin {user_id}")
            continue

        try:
            await client.ban_chat_member(chat_id=chat_id, user_id=user_id)
            print(f"Banned {user_id} from {chat_id}")
        except Exception as e:
            print(f"Failed to ban {user_id}: {e}")
            await message.reply_text(f"❌ Failed to ban {user_id}: {e}")

    print("Ban process completed.")
    await message.reply_text("✅ All non-admin members have been banned!")







print("Your Bot  Deployed Successfully ✅")
print("Join @crushbot_support if you facing any kind of issue!!")



sree.run_until_disconnected()
