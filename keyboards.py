from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/add"))
    keyboard.add(KeyboardButton("/list"), KeyboardButton("/stats"))
    keyboard.add(KeyboardButton("/help"))
    return keyboard

def get_task_actions_keyboard(task_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Отметить выполненной", callback_data=f"done_{task_id}"))
    return keyboard