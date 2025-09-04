from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo
user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔹 Do‘stlarni taklif qilish ")],  
        [
            KeyboardButton(text="✅ Testlarni ishlash",web_app=WebAppInfo(url='https://tanlovhtml.netlify.app/test.html')),
            KeyboardButton(text="📊 Natijalar",web_app=WebAppInfo(url='https://tanlovhtml.netlify.app/result.html'))
        ],  
        [
            KeyboardButton(text="📝 Viktorina shartlari"),
            KeyboardButton(text="❓ Savollarga javoblar",web_app=WebAppInfo(url='https://tanlovhtml.netlify.app/faqs.html'))
        ]  
    ],
    resize_keyboard=True
)
