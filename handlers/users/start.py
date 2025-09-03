from loader import dp,db
from aiogram.types import Message
from aiogram.filters import CommandStart
from states.register import Registration
from aiogram.fsm.context import FSMContext

@dp.message(CommandStart())
async def start_command(message:Message, state: FSMContext):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name, telegram_id=telegram_id, phone=None) 
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz")
        await message.answer(text="Ro'yxatdan o'tish uchun ismingiz va familiyangizni kiriting:")
        await state.set_state(Registration.full_name)
    except:
        await message.answer(text="Assalomu alaykum")
        await message.answer(text="Avval ro'yxatdan o'ting ismingiz va familiyangizni kiriting:")
        await state.set_state(Registration.full_name)