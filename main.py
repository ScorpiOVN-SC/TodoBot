from handlers import bot
from database import init_db
from config import TOKEN

if __name__ == "__main__":
    init_db()
    
    bot.infinity_polling()