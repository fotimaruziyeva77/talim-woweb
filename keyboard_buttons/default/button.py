from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Do'stlarni taklif qilish ")],
        [KeyboardButton(text="Test ishlash")],
        [KeyboardButton(text="Natijalar")],
        [KeyboardButton(text="Viktorina shartlari")],
        [KeyboardButton(text="Savollarga javob")]
    ],
    resize_keyboard=True
)
