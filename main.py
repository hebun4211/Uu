import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import User, ChannelParticipantsAdmins
from telethon.errors import UserPrivacyRestrictedError, UserAlreadyParticipantError, ChatAdminRequiredError
from telethon.tl.functions.channels import InviteToChannelRequest


api_id = 25504446
api_hash = "47db27cde56c3e4690e244e6de10f919"

string_session = "BQGFKr4AFDnE1I1Ej267c6hjHs0Q04sXTTfZOP1yWV8TeBKC8l7ZZ3dvVTSFTtBXDDe3rFZ3fP-V6BBy5YbkGUDZ22HG8cQIKMgbko9OWzSkvz-rVr_gceNJPKVk5F5sNjFwUluFI1I5nZqc1fY26gBWjz2MRvHHoIq-RWvRPp9JnEGhCTUe9aiz0f5Tt1AdAqeM-hKMFRUQdPfIOa2Ls94gFn8P99845xZHu8TwwVamCMld0wgQKWFwplFybnWwnnHhtD4JosAWY6TbH5kLQg48r2VOVuZ6xCZV5qUADTQkTisjgdZ1jrSQz8l5NKGNq6C09rXaSBIFk7omt74odqYze8dtgQAAAAGYRrxGAA"

admin_id = 6849739846


client = TelegramClient(StringSession(string_session), api_id, api_hash)

pending_uyecik_requests = {}
add_process_running = {}

def is_authorized(user_id):
    return user_id == admin_id

@client.on(events.NewMessage(pattern=r'^\.üyeçek (.+)'))
async def start_uyicik(event):
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
                pending_uyecik_requests.pop(chat_id, None)
                return

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
            

@client.on(events.NewMessage(pattern=r'^\.üyedurdur$'))
async def stop_uyecik(event):
    if not is_authorized(event.sender_id):
        return await event.reply("🚫 Bu komutu kullanmaya yetkin yok.")
    chat_id = event.chat_id
    add_process_running[chat_id] = False
    await event.reply("⛔️ Üye ekleme işlemi durduruldu.")

print("Userbot (Session String ile) başlatılıyor...")

with client:
    client.run_until_disconnected()
            add_process_running.pop(chat_id, None)
 app.start()
client.start()
client.run_until_disconnected()
