from aiogram import executor
from loader import bot
from config import ADMIN_ID
from datetime import datetime
from database import view_employees_state, delete_employee_state
from buttons import button_users_main_menu


async def on_shutdown(dp):
    text = f"""
            Salom admin.
bot ishdan toxtadi!
server vaqti: {datetime.now()}
        """
    await bot.send_message(ADMIN_ID, text)
    await bot.close()


async def on_startup(dp):
    for id in view_employees_state():
        id = id[0]
        await bot.send_message(chat_id=id,text="Bot update",reply_markup=button_users_main_menu())
        delete_employee_state(id)
    text = f"""
            Salom admin.
bot ishga tushdi!
server vaqti: {datetime.now()}
        """
    await bot.send_message(ADMIN_ID, text)


if __name__ == '__main__':
    from app import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
