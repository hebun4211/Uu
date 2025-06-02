import asyncio
import random
import shutil
import os
from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityMentionName, ChannelParticipantsAdmins, User
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, UserNotMutualContactError, UserAlreadyParticipantError, ChatAdminRequiredError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.errors.rpcerrorlist import RPCError
from datetime import datetime, timezone
import psutil

api_id = APİ İD
api_hash = "APİ HASH "
session_name = "SESSİON NAME"

admin_id = HESAP İD 

client = TelegramClient(session_name, api_id, api_hash)

# Geçici veri alanları
pending_uyecik_requests = {}
add_process_running = {}

# Yetki kontrol fonksiyonu
def is_authorized(user_id):
    return user_id == admin_id

@client.on(events.NewMessage(pattern=r'^\.üyeçek (.+)'))
async def start_uyecik(event):
    if not is_authorized(event.sender_id):
        return await event.reply("🚫 Bu komutu kullanmaya yetkin yok.")
    chat_id = event.chat_id
    source_link = event.pattern_match.group(1).strip()
    pending_uyecik_requests[chat_id] = {"step": 2, "source_link": source_link}
    await event.reply("🔢 Kaç mesaj taransın? (sayı gir, örn: 50000)")

@client.on(events.NewMessage)
async def handle_uyecik_steps(event):
    chat_id = event.chat_id
    sender_id = event.sender_id
    if chat_id not in pending_uyecik_requests or not is_authorized(sender_id):
        return
    step_data = pending_uyecik_requests[chat_id]
    user_input = event.raw_text.strip()
    if step_data["step"] == 2:
        if not user_input.isdigit():
            return await event.reply("❌ Geçerli bir sayı gir.")
        step_data["limit"] = int(user_input)
        step_data["step"] = 3
        return await event.reply("📤 Üyelerin ekleneceği hedef grubun linkini gönder.")
    if step_data["step"] == 3:
        step_data["target_link"] = user_input
        step_data["step"] = 4
        await event.reply("🔍 Üyeler taranıyor, lütfen bekle...")
        try:
            source = await client.get_entity(step_data["source_link"])
            admins = set()
            async for admin in client.iter_participants(source, filter=ChannelParticipantsAdmins):
                admins.add(admin.id)
            usernames = set()
            count = 0
            async for msg in client.iter_messages(source, limit=step_data["limit"]):
                sender = msg.sender
                if not sender or not isinstance(sender, User):
                    continue
                if sender.bot or sender.id in admins or not sender.username:
                    continue
                usernames.add(sender.username.lower())
                count += 1
                if count % 10000 == 0:
                    await event.reply(f"🔄 {count} mesaj tarandı...")
            if not usernames:
                await event.reply("⚠️ Kullanıcı adı olan uygun kimse bulunamadı.")
                return pending_uyecik_requests.pop(chat_id, None)
            await event.reply(f"✅ {len(usernames)} kullanıcı bulundu. Hedef gruba ekleniyor...")
            target = await client.get_entity(step_data["target_link"])
            add_process_running[chat_id] = True
            added = 0
            failed = 0
            for username in usernames:
                if not add_process_running.get(chat_id, True):
                    break
                try:
                    await client(InviteToChannelRequest(target, [username]))
                    added += 1
                    await asyncio.sleep(3)
                except (UserPrivacyRestrictedError, UserAlreadyParticipantError, ChatAdminRequiredError):
                    failed += 1
                    continue
                except Exception:
                    failed += 1
                    continue
            await event.reply(f"✅ Ekleme tamamlandı:\n🟢 Başarılı: {added}\n🔴 Başarısız: {failed}")
        except Exception as e:


            await event.reply(f"❌ Hata oluştu: {e}")
        finally:
            pending_uyecik_requests.pop(chat_id, None)
            add_process_running.pop(chat_id, None)

@client.on(events.NewMessage(pattern=r'^\.üyedurdur$'))
async def stop_uyecik(event):
    if not is_authorized(event.sender_id):
        return await event.reply("🚫 Bu komutu kullanmaya yetkin yok.")
    chat_id = event.chat_id
    add_process_running[chat_id] = False
    await event.reply("⛔️ Üye ekleme işlemi durduruldu.")

client.start()
client.run_until_disconnected()
