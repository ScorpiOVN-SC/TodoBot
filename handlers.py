import telebot
from telebot.types import Message, CallbackQuery
from database import add_user, add_task, get_active_tasks, mark_task_done, get_stats
from keyboards import get_main_keyboard, get_task_actions_keyboard
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    add_user(user_id, username)
    
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}!\n\n"
        "/add ... - добавить задачу\n"
        "/list - активные задачи\n"
        "/stats - статистика выполнения\n"
        "/help - помощь",
        reply_markup=get_main_keyboard()
    )

@bot.message_handler(commands=['help'])
def cmd_help(message: Message):
    bot.send_message(
        message.chat.id,
        "Помощь по командам:\n\n"
        "/add ... - добавить задачу\n"
        "/list - список дел\n"
        "/stats - статистика выполнения\n\n"
    )

@bot.message_handler(commands=['add'])
def cmd_add(message: Message):
    user_id = message.from_user.id
    
    task_text = message.text.replace('/add', '').strip()
    
    if not task_text:
        bot.reply_to(message, "Напишите текст задачи после /add ...", parse_mode='Markdown')
        return
    
    if len(task_text) > 200:
        bot.reply_to(message, "Задача слишком длинная (максимум 200 символов)")
        return
    
    add_task(user_id, task_text)
    bot.reply_to(message, f"Задача добавлена:\n«{task_text}»")

@bot.message_handler(commands=['list'])
def cmd_list(message: Message):
    user_id = message.from_user.id
    tasks = get_active_tasks(user_id)
    
    if not tasks:
        bot.send_message(message.chat.id, "У вас нет активных задач")
        return
    
    for task_id, task_text, created_at in tasks:
        date_short = created_at[:10]
        text = f"*Задача #{task_id}*\n`{task_text}`\nДобавлено: {date_short}"
        
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_task_actions_keyboard(task_id)
        )

@bot.message_handler(commands=['stats'])
def cmd_stats(message: Message):
    user_id = message.from_user.id
    total, active, done = get_stats(user_id)
    
    if total == 0:
        bot.send_message(message.chat.id, "Пока нет ни одной задачи...")
        return
    
    progress = int((done / total) * 100) if total > 0 else 0
    
    stats_text = (
        f"*Ваша статистика*\n\n"
        f"Всего задач: {total}\n"
        f"Активных: {active}\n"
        f"Выполнено: {done}\n"
        f"Прогресс: {progress}%"
    )
    
    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('done_'))
def handle_done_task(call: CallbackQuery):
    user_id = call.from_user.id
    task_id = int(call.data.split('_')[1])
    
    success = mark_task_done(task_id, user_id)
    
    if success:
        bot.answer_callback_query(call.id, "Задача выполнена")
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None  # убираем кнопку
        )
        bot.edit_message_text(
            call.message.text + "\n\n*Выполнено*",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
    else:
        bot.answer_callback_query(call.id, "Задача уже выполнена или не найдена")

@bot.message_handler(func=lambda message: True)
def handle_text(message: Message):
    bot.reply_to(
        message,
        "Используйте команды:\n/add, /list, /stats, /help"
    )