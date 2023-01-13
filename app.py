from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from states import *
from aiogram.dispatcher import FSMContext
from buttons import *
from loader import dp
from config import *


@dp.message_handler(CommandStart())
async def cmd_start(m: types.Message):
    if m.from_user.id == ADMIN_ID:
        await m.answer("Welcome to the bot!\nSelect the desired menu:", reply_markup=keyboard_admin_main_menu())
        await state_Admin.main_menu.set()
    else:
        await m.answer('Assalomu aleykum ' + str(
            m.from_user.full_name) + "bu bot yordamida siz ingliz tilini o'rganishni osonlashtirishingiz "
                                     "mumkin.\nIltimos kerakli menyuni tanlang:", )


# Information
@dp.message_handler(content_types=types.ContentType.TEXT, state=state_Admin.main_menu)
async def cmd_admin_main(m: types.Message) -> None:
    if m.text == "Information":
        await m.answer("You have selected the information menu. Select the desired menu:",
                       reply_markup=keyboard_admin_menu_information())
        await state_Admin.about_menu.set()
    elif m.text == "Books":
        await m.answer("You have selected the books menu. Select the desired menu:", reply_markup=keyboard_books())
        await state_Admin.book.set()
    else:
        await m.answer("Bunday menyu mavjud emas!")


# information
@dp.message_handler(content_types=types.ContentType.TEXT, state=state_Admin.about_menu)
async def cmd_admin_about_menu(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_admin_main_menu())
        await state_Admin.main_menu.set()
    elif m.text == "Developer":
        await state.update_data(about_menu="developer")
        await m.answer(text=str(database_get_information_developer()[-1]), reply_markup=keyboard_get_update())
        await state_Admin.about.set()
    elif m.text == "Admin":
        await state.update_data(about_menu="admin")
        await m.answer(text=str(database_get_information_admin()[-1]), reply_markup=keyboard_get_update())
        await state_Admin.about.set()
    elif m.text == "Bot":
        await state.update_data(about_menu="bot")
        await m.answer(text=str(database_get_information_bot()[-1]), reply_markup=keyboard_get_update())
        await state_Admin.about.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=state_Admin.about)
async def cmd_admin_about(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_admin_menu_information())
        await state_Admin.about_menu.set()
    elif m.text == "Update":
        data = await state.get_data()
        menu = data.get("about_menu")
        await m.answer(f"Enter the new {menu} information:", reply_markup=keyboard_close())
        await state_Admin.about_update.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=state_Admin.about_update)
async def cmd_admin_about_update(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_get_update())
        await state_Admin.about.set()
    else:
        data = await state.get_data()
        menu = data.get("about_menu")
        if menu == "developer":
            database_update_information(developer=m.text)
        elif menu == "bot":
            database_update_information(bot=m.text)
        elif menu == "admin":
            database_update_information(admin=m.text)
        await m.answer("Updated data", reply_markup=keyboard_get_update())
        await state_Admin.about.set()


@dp.message_handler(state=state_Admin.book.set(), content_types=types.ContentType.TEXT)
async def cmd_admin_books_menu(m: types.Message, state: FSMContext):
    if m.text in database_get_books():
        await m.answer(f"You have selected the book {m.text}. Please select the desired menu:",
                       reply_markup=keyboard_books_create_menu())
        await state.update_data(book=m.text)
        await state_Admin.book_menu.set()
    elif m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_admin_main_menu())
        await state_Admin.main_menu.set()
    else:
        await m.answer("The information entered is incorrect")


@dp.message_handler(state=state_Admin.book_menu, content_types=types.ContentType.TEXT)
async def cmd_admin_books_menu_selected(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Information the book":
        await m.answer(f"{database_get_books_about_by_book_name(book_name)}", reply_markup=keyboard_get_update())
        await state_Admin.book_malumoti.set()
    elif m.text == 'About the teacher':
        await m.answer(f"{database_get_books_teacher_by_book_name(book_name)}", reply_markup=keyboard_get_update())
        await state_Admin.teacher_malumoti.set()
    elif m.text == 'Lessons':
        await m.answer(f"Please selected a desired menu:", reply_markup=keyboard_get_lessons_menu(book_name))
        await state_Admin.lesson_number.set()
    elif m.text == "Training":
        pass
    elif m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_books())
        await state_Admin.book.set()


@dp.message_handler(state=state_Admin.lesson_number, content_types=types.ContentType.TEXT)
async def cmd_admin_books_lessons_menu_selected(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text in database_get_topics(book_name):
        await state.update_data(lesson_number=m.text)
        await m.answer(f"You selected {m.text}.Please selected a desired menu:", reply_markup=keyboard_get_lesson_menu()
                       )
        await state_Admin.lessons_main.set()
    elif m.text == "Close":
        await m.answer("Closed.",
                       reply_markup=keyboard_books_create_menu())
        await state.update_data(book=m.text)
        await state_Admin.book_menu.set()


@dp.message_handler(state=state_Admin.lessons_main, content_types=types.ContentType.TEXT)
async def cmd_admin_books_lessons_main_menu_selected(m: types.Message, state: FSMContext):
    pass


async def cmd_admin_books_lesson_menu_selected(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed. Please select the desired menu:",
                       reply_markup=keyboard_books_create_menu())
        await state.update_data(book=m.text)
        await state_Admin.book_menu.set()
    elif m.text == "Vocabulary":
        pass
    elif m.text == "Exercise":
        pass
    elif m.text == "Rules":
        pass


@dp.message_handler(state=state_Admin.book_malumoti.set(), content_types=types.ContentType.TEXT)
async def cmd_admin_books_about(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_books_create_menu())
        await state_Admin.book_menu.set()
    elif m.text == "Update":
        data = await state.get_data()
        book_name = data.get("book")
        await m.answer(f"You want to update the information of the book {book_name}. Please enter the new information:")
        await state_Admin.book_malumoti_ozgartirish.set()


@dp.message_handler(state=state_Admin.book_malumoti_ozgartirish, content_types=types.ContentType.TEXT)
async def cmd_admin_books_about_update(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Close":
        await m.answer(f"Closed.\n{database_get_books_about_by_book_name(book_name)}",
                       reply_markup=keyboard_get_update())
        await state_Admin.book_malumoti.set()
    else:
        database_update_book_by_name(book_name, about=m.text)
        await m.answer(f"Information has been updated:\n" + database_get_books_about_by_book_name(book_name),
                       reply_markup=keyboard_get_update())
        await state_Admin.book_malumoti.set()


@dp.message_handler(state=state_Admin.teacher_malumoti.set(), content_types=types.ContentType.TEXT)
async def cmd_admin_books_about(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_books_create_menu())
        await state_Admin.book_menu.set()
    elif m.text == "Update":
        data = await state.get_data()
        book_name = data.get("book")
        await m.answer(
            f"You want to update the teacher information of the book {book_name}. Please enter the new information:")
        await state_Admin.teacher_malumoti_ozgartirish.set()


@dp.message_handler(state=state_Admin.teacher_malumoti_ozgartirish, content_types=types.ContentType.TEXT)
async def cmd_admin_books_about_update(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Close":
        await m.answer(f"Closed.\n{database_get_books_teacher_by_book_name(book_name)}",
                       reply_markup=keyboard_get_update())
        await state_Admin.teacher_malumoti.set()
    else:
        database_update_book_by_name(book_name, teacher=m.text)
        await m.answer(f"Information has been updated:\n" + database_get_books_teacher_by_book_name(book_name),
                       reply_markup=keyboard_get_update())
        await state_Admin.teacher_malumoti.set()
