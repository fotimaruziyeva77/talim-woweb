from loader import bot, db, dp, ADMINS, CHANNELS
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command, CommandStart
from filters.admin import IsBotAdminFilter
from states.reklama import Adverts
from aiogram.fsm.context import FSMContext
from keyboard_buttons.default import admin_keyboard
from filters.check_sub_channel import IsCheckSubChannels
import time
from aiogram import F

@dp.message(Command("admin"), IsBotAdminFilter(ADMINS))
async def is_admin(message: Message):
    await message.answer(text="Admin menu", reply_markup=admin_keyboard.admin_button)


@dp.message(F.text == "Foydalanuvchilar soni", IsBotAdminFilter(ADMINS))
async def users_count(message: Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)


@dp.message(F.text == "Reklama yuborish", IsBotAdminFilter(ADMINS))
async def advert_dp(message: Message, state: FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")


@dp.message(Adverts.adverts)
async def send_advert(message: Message, state: FSMContext):
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0], from_chat_id=from_chat_id, message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.01)

    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


# ================== OBUNA TEKSHIRISH =====================
async def is_user_subscribed(channel, user_id):
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Xatolik: {e}")
        return False


async def send_subscription_prompt(message: Message):
    text = "Iltimos, quyidagi kanallarga obuna bo'ling:"
    inline_channel = InlineKeyboardBuilder()
    remaining_channels = []

    for index, channel in enumerate(CHANNELS):
        if not await is_user_subscribed(channel, message.from_user.id):
            ChatInviteLink = await bot.create_chat_invite_link(channel)
            inline_channel.add(InlineKeyboardButton(text=f"{index + 1}-kanal", url=ChatInviteLink.invite_link))
            remaining_channels.append(channel)

    if remaining_channels:
        inline_channel.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subscription"))
        inline_channel.adjust(1, repeat=True)
        await message.answer(
            f"{text}\nSizda obuna bo'lish uchun {len(remaining_channels)} kanal qoldi. 'Obunani tekshirish' tugmasini bosing.",
            reply_markup=inline_channel.as_markup()
        )
    else:
        await message.answer("Rahmat! Siz barcha kanallarga obuna bo'lgansiz ✅")
        

@dp.callback_query(F.data == "check_subscription")
async def check_subscription(call: CallbackQuery):
    user_id = call.from_user.id
    remaining_channels = []

    for channel in CHANNELS:
        if not await is_user_subscribed(channel, user_id):
            remaining_channels.append(channel)

    if remaining_channels:
        text = f"Siz hali {len(remaining_channels)} ta kanalga obuna bo‘lmadingiz."
        inline_channel = InlineKeyboardBuilder()

        for index, channel in enumerate(remaining_channels):
            ChatInviteLink = await bot.create_chat_invite_link(channel)
            inline_channel.add(InlineKeyboardButton(text=f"{index + 1}-kanal", url=ChatInviteLink.invite_link))

        inline_channel.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subscription"))
        inline_channel.adjust(1, repeat=True)

        await call.message.edit_text(
            text=text,
            reply_markup=inline_channel.as_markup()
        )
    else:
        await call.message.edit_text("Rahmat! Siz barcha kanallarga obuna bo‘lgansiz ✅")


