import random
from loader import dp, db
from states.register import Registration
from aiogram.fsm.context import FSMContext
from keyboard_buttons.default.button import user_menu
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


@dp.message(Registration.full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(Registration.phone)

    phone_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )

    await message.answer("Telefon raqamingizni yuboring:", reply_markup=phone_button)


# 2. Telefon
@dp.message(Registration.phone)
async def get_phone(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    await state.update_data(phone=phone)

    # captcha uchun random kod
    code = random.randint(1000, 9999)
    await state.update_data(captcha_code=code)

    await state.set_state(Registration.captcha)
    await message.answer(f"Tasdiqlash uchun quyidagi kodni kiriting: {code}", reply_markup=None)


# 3. Captcha
@dp.message(Registration.captcha)
async def check_captcha(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == str(data["captcha_code"]):
        # DB ga yozamiz
        full_name = data["full_name"]
        phone = data["phone"]
        telegram_id = message.from_user.id

        db.add_user(full_name=full_name, telegram_id=telegram_id, phone=phone)

        await message.answer("Ro‘yxatdan o‘tish muvaffaqiyatli ✅", reply_markup=user_menu)
        await state.clear()
    else:
        await message.answer("❌ Kod noto‘g‘ri. Qayta urinib ko‘ring.")
