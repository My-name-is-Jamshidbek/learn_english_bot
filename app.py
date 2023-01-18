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
        await m.answer("You have selected the books menu. Select the desired menu:",
                       reply_markup=keyboard_books())
        await state_Admin.book.set()
    else:
        await m.answer("Bunday menyu mavjud emas!")


# books
@dp.message_handler(state=state_Admin.book, content_types=types.ContentType.TEXT)
async def cmd_admin_books_menu(m: types.Message, state: FSMContext):
    if m.text in [name[1] for name in database_get_books()]:
        await m.answer(f"You have selected the book {m.text}. Please select the desired menu:",
                       reply_markup=keyboard_books_create_menu())
        await state.update_data(book=m.text)
        await state_Admin.book_menu.set()
    elif m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_admin_main_menu())
        await state_Admin.main_menu.set()
    elif m.text == "Add a book":
        await m.answer("Enter the title of the book:", reply_markup=keyboard_close())
        await state_Admin.add_book.set()
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
    elif m.text == "Delete this book":
        await m.answer("Are you sure you want to delete this book?\n"
                       "If you confirm, all information about the book will be deleted!",
                       reply_markup=keyboard_confirmation())
        await state_Admin.delete_book.set()
    elif m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_books())
        await state_Admin.book.set()



@dp.message_handler(state=state_Admin.lesson_number, content_types=types.ContentType.TEXT)
async def cmd_admin_books_lessons_menu_selected(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Add a lesson":
        await m.answer("Enter a new lesson name:", reply_markup=keyboard_close())
        await state_Admin.add_lesson.set()
    elif m.text == "Close":
        await m.answer("Closed.",
                       reply_markup=keyboard_books_create_menu())
        await state_Admin.book_menu.set()
    elif m.text in database_get_topics(book_name)[0]:
        await state.update_data(lesson_number=m.text)
        await m.answer(f"You selected {m.text}.Please selected a desired menu:", reply_markup=keyboard_get_lesson_menu()
                       )
        await state_Admin.lessons_main.set()



@dp.message_handler(state=state_Admin.lessons_main, content_types=types.ContentType.TEXT)
async def cmd_admin_main_lesson(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    topic = data.get("lesson_number")
    if m.text == "Close":
        await m.answer("Closed", reply_markup=keyboard_get_lessons_menu(book_name))
        await state_Admin.lesson_number.set()
    elif m.text == "Vocabulary":
        await m.answer(text = str(database_get_words_by_topic(book_name, topic)[0][0]))
    elif m.text == "Exercise":
        await m.answer(text = str(database_get_exercise_by_topic(book_name, topic)[0][0]))
    elif m.text == "Rules":
        await m.answer(text = str(database_get_rule_by_topic(book_name, topic)[0][0]))
    elif m.text == "Delete this lesson":
        database_delete_by_topic_and_book(book=book_name, topic=topic)
        await m.answer("Deleted this lesson", reply_markup=keyboard_get_lessons_menu(book_name))
        await state_Admin.lesson_number.set()






















# add a lesson
@dp.message_handler(state=state_Admin.add_lesson,content_types=types.ContentType.TEXT)
async def cmd_admin_add_lesson(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Close":
        await m.answer(f"Closed:", reply_markup=keyboard_get_lessons_menu(book_name))
        await state_Admin.lesson_number.set()
    else:
        await state.update_data(add_lesson = m.text)
        await m.answer("Please enter new lesson words separated by commas!")
        await state_Admin.add_lesson_vocabulary.set()


@dp.message_handler(state=state_Admin.add_lesson_vocabulary,content_types=types.ContentType.TEXT)
async def cmd_admin_add_lesson(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Close":
        await m.answer(f"Closed:", reply_markup=keyboard_get_lessons_menu(book_name))
        await state_Admin.lesson_number.set()
    else:
        await state.update_data(add_lesson_vocabulary = m.text)
        await m.answer("Please enter new lesson exercise!")
        await state_Admin.add_lesson_exercise.set()


@dp.message_handler(state=state_Admin.add_lesson_exercise,content_types=types.ContentType.TEXT)
async def cmd_admin_add_lesson(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Close":
        await m.answer(f"Closed:", reply_markup=keyboard_get_lessons_menu(book_name))
        await state_Admin.lesson_number.set()
    else:
        await state.update_data(add_lesson_exercise=m.text)
        await m.answer("Please enter new lesson rules!")
        await state_Admin.add_lesson_rules.set()


@dp.message_handler(state=state_Admin.add_lesson_rules,content_types=types.ContentType.TEXT)
async def cmd_admin_add_lesson(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Close":
        await m.answer(f"Closed:", reply_markup=keyboard_get_lessons_menu(book_name))
        await state_Admin.lesson_number.set()
    else:
        database_add_rule(book=book_name,topic=data.get("add_lesson"),rule=m.text)
        database_add_exercise(book=book_name,topic=data.get("add_lesson"),exercise=data.get("add_lesson_exercise"))
        database_add_words(book=book_name,topic=data.get("add_lesson"),word=data.get("add_lesson_vocabulary"))
        await m.answer("New lesson added!", reply_markup=keyboard_get_lessons_menu(book_name))
        await state_Admin.lesson_number.set()


# delete a book
@dp.message_handler(state=state_Admin.delete_book, content_types=types.ContentType.TEXT)
async def cmd_admin_book_delete(m: types.Message, state: FSMContext):
    if m.text == "No":
        await m.answer("Closed.",
                       reply_markup=keyboard_books_create_menu())
        await state_Admin.book_menu.set()
    elif m.text == "Yes":
        data = await state.get_data()
        book_name = data.get("book")
        database_delete_book_data(book_name)
        await m.answer("This book has been deleted.", reply_markup=keyboard_books())
        await state_Admin.book.set()


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


# book malumoti tugatilgan
@dp.message_handler(state=state_Admin.book_malumoti, content_types=types.ContentType.TEXT)
async def cmd_admin_books_about(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_books_create_menu())
        await state_Admin.book_menu.set()
    elif m.text == "Update":
        data = await state.get_data()
        book_name = data.get("book")
        await m.answer(f"You want to update the information of the book {book_name}. Please enter the new information:",
                       reply_markup=keyboard_close())
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


# teacher ma'lumoti
@dp.message_handler(state=state_Admin.teacher_malumoti, content_types=types.ContentType.TEXT)
async def cmd_admin_books_about(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_books_create_menu())
        await state_Admin.book_menu.set()
    elif m.text == "Update":
        data = await state.get_data()
        book_name = data.get("book")
        await m.answer(
            f"You want to update the teacher information of the book {book_name}. Please enter the new information:",
            reply_markup=keyboard_close())
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


# add book tugatilan
@dp.message_handler(state=state_Admin.add_book, content_types=types.ContentType.TEXT)
async def cmd_admin_add_book(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed. Select the desired menu:",
                       reply_markup=keyboard_books())
        await state_Admin.book.set()
    else:
        await state.update_data(add_book_name=m.text)
        await m.answer("Enter the about of the book:", reply_markup=keyboard_close())
        await state_Admin.add_book_about.set()


@dp.message_handler(state=state_Admin.add_book_about, content_types=types.ContentType.TEXT)
async def cmd_admin_add_book_about(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed. Select the desired menu:",
                       reply_markup=keyboard_books())
        await state_Admin.book.set()
    else:
        await state.update_data(add_book_about=m.text)
        await m.answer("Enter the teacher about of the book:", reply_markup=keyboard_close())
        await state_Admin.add_book_teacher.set()


@dp.message_handler(state=state_Admin.add_book_teacher, content_types=types.ContentType.TEXT)
async def cmd_admin_add_book_about(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer("Closed. Select the desired menu:",
                       reply_markup=keyboard_books())
        await state_Admin.book.set()
    else:
        data = await state.get_data()
        book_name = data.get("add_book_name")
        book_about = data.get("add_book_about")
        database_add_book(name=book_name, about=book_about, teacher=m.text)
        await m.answer("Book added.", reply_markup=keyboard_books())
        await state_Admin.book.set()