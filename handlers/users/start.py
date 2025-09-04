from loader import dp, db
from aiogram.types import Message
from aiogram.filters import CommandStart
from states.register import Registration
from aiogram.fsm.context import FSMContext
from keyboard_buttons.default.button import user_menu
from aiogram import F
from loader import bot 
from aiogram import types


@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id


    user = db.get_user(telegram_id) 
    if user:
        await message.answer(f"Assalomu alaykum, {user[0]}! 👋\n Quyidagi menyudan kerakli bo'limni  tanlang",reply_markup=user_menu)
    else:
        await message.answer("Assalomu alaykum, botimizga hush kelibsiz! 🤗")
        await message.answer("Ro'yxatdan o'tish uchun ismingiz va familiyangizni kiriting:")
        await state.set_state(Registration.full_name)

@dp.message(F.text == "📝 Viktorina shartlari")
async def viktorina_shartlari(message: Message):
    text = (
        "❗️<b>Viktorina shartlari:</b>\n\n"
        "🔹1) “Mustaqillik” onlayn viktorinasida hamma O‘zbekiston fuqarolari ishtirok etishi mumkin (umuman cheklov yo‘q);\n"
        "🔹2) Viktorina testlari 4-5-sentyabr kunlari bot orqali bo‘lib o‘tadi. Testni ishlash uchun kamida +5 referal ball bo‘lishi shart;\n"
        "🔹3) Har bir test uchun 1 ball va 30 soniya vaqt beriladi. Testlar kuniga 50 tadan (jami 100 ta), har xil mavzuda aralash tushadi.\n"
        "🔹4) Viktorina testlari maktab darsliklari asosida mustaqillik va O‘zbekistonning yutuqlari mavzularida bo‘ladi.\n"
        "🔹5) Testlarni 4-5-sentyabr kunlari soat 09:00 dan 22:00 ga qadar istalgan vaqtda ishlash mumkin bo‘ladi.\n"
        "🔹6) Yakunda referal ball bo‘yicha alohida, test bali bo‘yicha alohida 12 tadan (jami 24 nafar) g‘oliblar aniqlanadi va quyidagicha taqdirlanadi:\n\n"
        "🏆 <b>GranPri (3 nafar)</b> – Smartwatch + Quloqchin;\n"
        "🥇 <b>1-o‘rin (3 nafar)</b> – Smart RGB, LED kalonka;\n"
        "🥈 <b>2-o‘rin (3 nafar)</b> – SmartWatch 10;\n"
        "🥉 <b>3-o‘rin (3 nafar)</b> – Quloqchin Pro Max.\n\n"
        "🔸Yakunda referal bo‘yicha o‘rin olganlarni ballari teng bo‘lib qolsa test baliga qaraladi;\n"
        "🔸Test bo‘yicha ballar teng bo‘lib qolsa, testni ishlash uchun sarflangan vaqtga qaraladi (bot har bir ishtirokchini test vaqtini avtomatik hisoblab boradi).\n"
        "🔸Test ishlashda qatnashgan barcha ishtirokchilarga QR kodli elektron sertifikat beriladi."
    )
    await message.answer(text, parse_mode="HTML")
@dp.message(F.text == "🔹 Do‘stlarni taklif qilish ")
async def dostlarni_taklif_qilish(message: types.Message):
    user_id = message.from_user.id
    bot_username = (await bot.get_me()).username   
    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    text = (
        "📢 <b>Do‘stlaringizni taklif qiling!</b>\n\n"
        "Quyidagi havolani ulashing 👇\n"
        f"{referral_link}\n\n"
        "✅ Har bir do‘stingiz ro‘yxatdan o‘tsa sizga 1 referal ball qo‘shiladi."
    )
    await message.answer(text, parse_mode="HTML")