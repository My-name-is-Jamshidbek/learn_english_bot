import time

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from states import *
from aiogram.dispatcher import FSMContext
from buttons import *
from loader import dp, bot
from config import *
from aiogram.types import InputFile, Message



@dp.message_handler(CommandStart())
async def cmd_start(m: types.Message):
    if m.from_user.id == ADMIN_ID:
        await m.answer("Welcome to the bot!\nSelect the desired menu:", reply_markup=keyboard_admin_main_menu())
        await state_Admin.main_menu.set()
    else:
        add_employee(id=m.from_user.id,name=m.from_user.full_name)
        await m.answer('Welcome to the bot ' + str(
            m.from_user.full_name) + " with this bot you can make learning English easier. \nPlease select the desired "
                                     "menu:", reply_markup=button_users_main_menu())
        await state_user.main_menu.set()


@dp.message_handler()
async def user_main_menu(m:types.Message, state:FSMContext):
    add_employee_state(m.from_user.id)
    if m.text == "Information":
        await m.answer("You have selected the information menu. Select the desired menu:",
                       reply_markup=button_users_menu_information())
        await state_user.about_menu.set()
    elif m.text == "Books":
        await m.answer("You have selected the books menu. Select the desired menu:",
                       reply_markup=button_users_books_menu())
        await state_user.books_menu.set()
    else:
        await m.answer("No such menu exists!")


@dp.message_handler(state=state_user.main_menu, content_types=types.ContentType.TEXT)
async def user_main_menu(m:types.Message, state:FSMContext):
    add_employee_state(m.from_user.id)
    if m.text == "Information":
        await m.answer("You have selected the information menu. Select the desired menu:",
                       reply_markup=button_users_menu_information())
        await state_user.about_menu.set()
    elif m.text == "Books":
        await m.answer("You have selected the books menu. Select the desired menu:",
                       reply_markup=button_users_books_menu())
        await state_user.books_menu.set()
    else:
        await m.answer("No such menu exists!")


@dp.message_handler(state=state_user.about_menu, content_types=types.ContentType.TEXT)
async def user_information(m:types.Message, state:FSMContext):
    if m.text == "Close":
        await m.answer("Closed.", reply_markup=button_users_main_menu())
        await state_user.main_menu.set()
    elif m.text == "Developer":
        await m.answer(text=str(database_get_information_developer()[-1]))
    elif m.text == "Admin":
        await m.answer(text=str(database_get_information_admin()[-1]))
    elif m.text == "Bot":
        await m.answer(text=str(database_get_information_bot()[-1]))
    else:
        await m.answer("No such menu exists!")


@dp.message_handler(state=state_user.books_menu, content_types=types.ContentType.TEXT)
async def user_books_menu(m:types.Message, state:FSMContext):
    if m.text in [name[1] for name in database_get_books()]:
        await m.answer(f"You have selected the book {m.text}. Please select the desired menu:",
                       reply_markup=button_users_book_menu())
        await state.update_data(book=m.text)
        await state_user.book_menu.set()
    elif m.text == "Close":
        await m.answer("Closed.", reply_markup=button_users_main_menu())
        await state_user.main_menu.set()
    else:
        await m.answer("No such menu exists!")

@dp.message_handler(state=state_user.book_menu, content_types=types.ContentType.TEXT)
async def user_book_menu(m:types.Message, state:FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Close":
        await m.answer("Closed.",
                       reply_markup=button_users_books_menu())
        await state_user.books_menu.set()
    elif m.text == "Information the book":
        await m.answer(f"{database_get_books_about_by_book_name(book_name)}")
    elif m.text == 'About the teacher':
        await m.answer(f"{database_get_books_teacher_by_book_name(book_name)}")
    elif m.text == 'Lessons':
        await m.answer(f"Please selected a desired menu:", reply_markup=button_get_lessons_menu(book_name))
        await state.update_data(lt=m.text)
        await state_user.lessons_menu.set()
    elif m.text == "Training":
        await state.update_data(lt=m.text)
        await m.answer("Please selected a desired menu:", reply_markup=button_get_lessons_menu(book_name))
        await state_user.lessons_menu.set()
    else:
        await m.answer("No such menu exists!")

@dp.message_handler(state=state_user.lessons_menu, content_types=types.ContentType.TEXT)
async def user_lessons_menu(m:types.Message, state:FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    lt = data.get("lt")
    if m.text == "Close":
        await m.answer("Closed.",
                       reply_markup=button_users_books_menu())
        await state_user.books_menu.set()
    elif m.text in database_get_topics(book_name)[0]:
        await state.update_data(lesson=m.text)
        if lt == "Training":
            await m.answer(f"You selected {m.text}.Please selected a desired menu:", reply_markup=button_get_training_menu()
                           )
            await state_user.training_menu.set()
        elif lt == "Lessons":
            await m.answer(f"You selected {m.text}.Please selected a desired menu:",
                           reply_markup=button_get_lesson_menu()
                           )
            await state_user.lesson_menu.set()
    else:
        await m.answer("No such menu exists!")


@dp.message_handler(state=state_user.lesson_menu, content_types=types.ContentType.TEXT)
async def user_lesson_menu(m:types.Message, state:FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    topic = data.get("lesson")
    if m.text == "Close":
        await m.answer("Closed", reply_markup=button_get_lessons_menu(book_name))
        await state_user.lessons_menu.set()
    elif m.text == "Vocabulary":
        await m.answer(text = str(database_get_words_by_topic(book_name, topic)[0][0]))
    elif m.text == "Exercise":
        await m.answer(text = str(database_get_exercise_by_topic(book_name, topic)[0][0]))
    elif m.text == "Rules":
        await m.answer(text = str(database_get_rule_by_topic(book_name, topic)[0][0]))
    else:
        await m.answer("No such menu exists!")


@dp.message_handler(state=state_user.training_menu, content_types=types.ContentType.TEXT)
async def user_training_menu(m:types.Message, state:FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    topic = data.get("lesson")
    if m.text == "Close":
        await m.answer("Closed", reply_markup=button_get_lessons_menu(book_name))
        await state_user.lessons_menu.set()
    elif m.text == "Tests":
        await m.answer(f"You selected {m.text}.Please selected a desired menu", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await state_user.lesson_tests.set()
    elif m.text == "Writing":
        await state.update_data(training_type = m.text)
        await m.answer(f"You selected {m.text}.Please selected a desired menu", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await state_user.lesson_words.set()
    elif m.text == "Speaking":
        await state.update_data(training_type = m.text)
        await m.answer(f"You selected {m.text}.Please selected a desired menu", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await state_user.lesson_words.set()
    elif m.text == "Spelling A":
        await state.update_data(training_type = m.text)
        await m.answer(f"You selected {m.text}.Please selected a desired menu", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await state_user.lesson_words.set()
    elif m.text == "Spelling B":
        await state.update_data(training_type = m.text)
        await m.answer(f"You selected {m.text}.Please selected a desired menu", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await state_user.lesson_words.set()
    else:
        await m.answer("No such menu exists!")


# writing
@dp.message_handler(state=state_user.lesson_words)
async def cmd_user_tests_main_menu(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer(f"Closed.", reply_markup=button_get_training_menu()
                           )
        await state_user.training_menu.set()
    elif m.text.lower() == "start".lower():
        data = await state.get_data()
        words = database_get_words_by_topic(data.get("book"),data.get("lesson"))
        word = ""
        if "," in words:
            for i in range(len(words)):
                if words[i] == ",":
                    words = words[i + 1:]
                    break
                else:
                    word += words[i]
        else:
            word = words
            words = "0"
        training_type = data.get("training_type")
        await state.update_data(answers='')
        await state.update_data(training_words=words)
        await state.update_data(current_word=word)
        await state.update_data(word_number=1)
        if training_type == "Writing":
            audio = InputFile("data/audio/writing/"+word+".mp3")
            await m.answer_voice(voice=audio,caption="Write me your answer:",
                           reply_markup=keyboard_get_button(["Close"]))
        elif training_type == "Spelling A":
            audio = InputFile("data/audio/spelling/"+word+".mp3")
            await m.answer_voice(voice=audio,caption="Write me your answer:", reply_markup=keyboard_get_button([
                "Close"]))
        elif training_type == "Spelling B" or training_type == "Speaking":
            await m.answer(word,reply_markup=keyboard_get_button(["Close"]))


        if words == "0":
            await state_user.training_word_close.set()
        else:
            await state_user.training_word.set()
    else:
        await m.answer("No such menu exists!")

@dp.message_handler(state=state_user.training_word, content_types=[types.ContentType.VOICE, types.ContentType.TEXT])
async def cmd_user_tests_menu(m: types.Message, state: FSMContext):
    if m.text == "Close":
        data = await state.get_data()
        answers = data.get("answers")
        await m.answer(f"Writing is over.", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await m.answer('Results:\n'+answers)
        await state_user.lesson_words.set()
    else:
        data = await state.get_data()
        words = data.get("training_words")
        word = ""
        if "," in words:
            for i in range(len(words)):
                if words[i] == ",":
                    words = words[i + 1:]
                    break
                else:
                    word += words[i]
        else:
            word = words
            words = "0"
        training_type = data.get("training_type")
        answers = data.get('answers')
        word_number = data.get('word_number')
        current_word = data.get("current_word")
        text = ''
        if training_type == "Writing" or training_type == "Spelling A":
            if m.text == current_word:
                text += "\nCorrect ✅\n"+current_word
            else:
                text += "\n"+m.text+" ❎\n" + current_word + "✅"
        elif training_type == "Spelling B" or training_type == "Speaking":
            file_id = m.voice.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, "data/voices/"+str(file_id)+".mp3")
            time.sleep(5)
            ans = database_chek_voice("data/voices/"+str(file_id)+".mp3",m.from_user.id)
            if ans == current_word:
                text += "\nCorrect ✅"
            else:
                text += "\n"+ans+"\nIncorrect ❎\n"

        if answers == None:answers=str(word_number)+") "+text+'\n'
        else:answers+=str(word_number)+") "+text+'\n'
        await state.update_data(answers=answers)
        await state.update_data(training_words=words)
        await state.update_data(current_word=word)
        await state.update_data(word_number=word_number+1)
        if training_type == "Writing":
            audio = InputFile("data/audio/writing/"+word+".mp3")
            await m.answer_voice(voice=audio,caption="Write me your answer:",
                           reply_markup=keyboard_get_button(["Close"]))
        elif training_type == "Spelling A":
            audio = InputFile("data/audio/spelling/"+word+".mp3")
            await m.answer_voice(voice=audio,caption="Write me your answer:", reply_markup=keyboard_get_button([
                "Close"]))
        elif training_type == "Spelling B" or training_type == "Speaking":
            await m.answer(word,reply_markup=keyboard_get_button(["Close"]))


        if words == "0":
            await state_user.training_word_close.set()
        else:
            await state_user.training_word.set()



@dp.message_handler(state=state_user.training_word_close, content_types=[types.ContentType.TEXT,
                                                                         types.ContentType.VOICE])
async def user_tests_close(m:types.Message, state:FSMContext):
    if m.text == "Close":
        data = await state.get_data()
        answers = data.get("answers")
        await m.answer(f"Writings is over.", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await m.answer('Results:\n'+answers)
        await state_user.lesson_words.set()

    else:
        data = await state.get_data()
        training_type = data.get("training_type")
        answers = data.get('answers')
        word_number = data.get('word_number')
        current_word = data.get("current_word")
        text = ''
        if training_type == "Writing" or training_type == "Spelling B":
            if m.text == current_word:
                text += "\nCorrect ✅\n" + current_word
            else:
                text += "\n" + m.text + " ❎\n" + current_word + "✅"
        elif training_type == "Spelling B" or training_type == "Speaking":
            file_id = m.voice.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, "data/voices/"+str(file_id)+".mp3")
            time.sleep(5)
            ans = database_chek_voice("data/voices/"+str(file_id)+".mp3",m.from_user.id)
            if ans == current_word:
                text += "\nCorrect ✅"
            else:
                text += "\n" + ans + "\nIncorrect ❎\n"

        if answers == None:
            answers = str(word_number) + ") " + text + '\n'
        else:
            answers += str(word_number) + ") " + text + '\n'
        await m.answer(f"{training_type} is over.", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await m.answer(answers)
        await state_user.lesson_words.set()

# tests
@dp.message_handler(state=state_user.lesson_tests, content_types=types.ContentType.TEXT)
async def cmd_user_tests_main_menu(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer(f"Closed.", reply_markup=button_get_training_menu()
                           )
        await state_user.training_menu.set()
    elif m.text.lower() == "start".lower():
        data = await state.get_data()
        tests_id = database_get_tests_id_by_topic(data.get("book"),data.get("lesson"))
        test_id = ""
        if "_" in tests_id:
            for i in range(len(tests_id)):
                if tests_id[i] == "_":
                    tests_id = tests_id[i + 1:]
                    break
                else:
                    test_id += tests_id[i]
        else:
            test_id = tests_id
            tests_id = "0"
        await state.update_data(answers='')
        await state.update_data(training_tests=tests_id)
        await state.update_data(current_test_id=test_id)
        answers = database_get_test_answers_by_id(test_id)
        await state.update_data(test_number=1)
        await state.update_data(current_test_question = answers["test_question"])
        await state.update_data(current_test_answer_text = answers["correct_answer_text"])
        await state.update_data(current_test_answer = answers["correct_answer"])
        await m.answer(text=str(1)+") "+answers["question_full_text"],
                       reply_markup=keyboard_get_button(["A","B","C","Close"]))
        if tests_id == "0":
            await state_user.training_test_close.set()
        else:
            await state_user.training_tests.set()
    else:
        await m.answer("No such menu exists!")

@dp.message_handler(state=state_user.training_tests, content_types=types.ContentType.TEXT)
async def cmd_user_tests_menu(m: types.Message, state: FSMContext):
    if m.text == "Close":
        data = await state.get_data()
        answers = data.get("answers")
        await m.answer(f"Tests is over.", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await m.answer('Results:\n'+answers)
        await state_user.lesson_tests.set()
    elif m.text in ["A", "B", "C"]:
        data = await state.get_data()
        tests_id = data.get("training_tests")
        test_id = ""
        if "_" in tests_id:
            for i in range(len(tests_id)):
                if tests_id[i] == "_":
                    tests_id = tests_id[i + 1:]
                    break
                else:
                    test_id += tests_id[i]
        else:
            test_id = tests_id
            tests_id = "0"
        answers = data.get('answers')
        old_test_id = data.get("current_test_id")
        correct_answer = data.get('current_test_answer')
        test_number = data.get('test_number')
        text = data.get("current_test_question")
        correct_answer_text = data.get("current_test_answer_text")
        if m.text == correct_answer:
            text += "\nCorrect ✅\n"+correct_answer_text
        else:
            text += "\nIncorrect ⚠\n"+correct_answer_text+"✅"
        if answers == None:answers=str(test_number)+") "+text+'\n'
        else:answers+=str(test_number)+") "+text+'\n'
        await state.update_data(answers=answers)
        await state.update_data(training_tests=tests_id)
        await state.update_data(current_test_id=test_id)
        answers = database_get_test_answers_by_id(test_id)
        await state.update_data(test_number=test_number+1)
        await state.update_data(current_test_question=answers["test_question"])
        await state.update_data(current_test_answer_text=answers["correct_answer_text"])
        await state.update_data(current_test_answer=answers["correct_answer"])
        await m.answer(text=str(test_number)+") "+answers["question_full_text"],
                       reply_markup=keyboard_get_button(["A", "B", "C", "Close"]))
        if tests_id == "0":
            await state_user.training_test_close.set()
        else:
            await state_user.training_tests.set()
    else:
        await m.answer("No such menu exists!")


@dp.message_handler(state=state_user.training_test_close, content_types=types.ContentType.TEXT)
async def user_tests_close(m:types.Message, state:FSMContext):
    if m.text == "Close":
        data = await state.get_data()
        answers = data.get("answers")
        await m.answer(f"Tests is over.", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await m.answer('Results:\n'+answers)
        await state_user.lesson_tests.set()

    elif m.text in ["A", "B", "C"]:
        data = await state.get_data()
        answers = data.get("answers")
        old_test_id = data.get("current_test_id")
        correct_answer = data.get('current_test_answer')
        test_number = data.get('test_number')
        text = data.get("current_test_question")
        correct_answer_text = data.get("current_test_answer_text")
        if m.text == correct_answer:
            text += "\nCorrect ✅\n" + correct_answer_text
        else:
            text += "\nIncorrect ⚠\n" + correct_answer_text + "✅"
        if answers == None:answers=str(test_number)+") "+text
        else:answers+=str(test_number)+") "+text

        await m.answer(f"Tests is over.", reply_markup=keyboard_get_test_menu(
            test_add_btn=False))
        await m.answer(answers)
        await state_user.lesson_tests.set()
    else:
        await m.answer("No such menu exists!")


"""
ADMIN
"""

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
        await m.answer("Please selected a desired menu:", reply_markup=keyboard_get_lessons_menu(book=book_name,
                                                                                               add_less_btn=False))
        await state_Admin.training_main_menu.set()
    elif m.text == "Delete this book":
        await m.answer("Are you sure you want to delete this book?\n"
                       "If you confirm, all information about the book will be deleted!",
                       reply_markup=keyboard_confirmation())
        await state_Admin.delete_book.set()
    elif m.text == "Close":
        await m.answer("Closed.", reply_markup=keyboard_books())
        await state_Admin.book.set()





@dp.message_handler(state=state_Admin.training_main_menu, content_types=types.ContentType.TEXT)
async def cmd_admin_books_training_menu_selected(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Close":
        await m.answer("Closed.",
                       reply_markup=keyboard_books_create_menu())
        await state_Admin.book_menu.set()
    elif m.text in database_get_topics(book_name)[0]:
        await state.update_data(lesson_number=m.text)
        await m.answer(f"You selected {m.text}.Please selected a desired menu:", reply_markup=keyboard_get_training_menu()
                       )
        await state_Admin.training_main_menu_select.set()


@dp.message_handler(state=state_Admin.training_main_menu_select, content_types=types.ContentType.TEXT)
async def cmd_admin_books_training_menu(m: types.Message, state: FSMContext):
    data = await state.get_data()
    book_name = data.get("book")
    if m.text == "Tests":
        await m.answer(f"You selected {m.text}.Please selected a desired menu",reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()
    elif m.text == "Writing":
        pass
    elif m.text == "Speaking":
        pass
    elif m.text == "Spealling A":
        pass
    elif m.text == "Spealling B":
        pass
    elif m.text == "Close":
        await m.answer("Closed:", reply_markup=keyboard_get_lessons_menu(book=book_name,
                                                                         add_less_btn=False))
        await state_Admin.training_main_menu.set()


# tests
@dp.message_handler(state=state_Admin.lesson_tests, content_types=types.ContentType.TEXT)
async def cmd_admin_tests_main_menu(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer(f"Closed.",
                       reply_markup=keyboard_get_training_menu()
                       )
        await state_Admin.training_main_menu_select.set()
    elif m.text.lower() == "start".lower():
        data = await state.get_data()
        tests_id = database_get_tests_id_by_topic(data.get("book"),data.get("lesson_number"))
        test_id = ""
        if "_" in tests_id:
            for i in range(len(tests_id)):
                if tests_id[i] == "_":
                    tests_id = tests_id[i + 1:]
                    break
                else:
                    test_id += tests_id[i]
        else:
            test_id = tests_id
            tests_id = "0"
        await state.update_data(training_tests=tests_id)
        await state.update_data(current_test_id=test_id)
        answers = database_get_test_answers_by_id(test_id)
        await m.answer(text=answers["question_full_text_admin"],
                       reply_markup=keyboard_get_button(["Delete", "Close", "Next"]))
        if tests_id == "0":
            await state_Admin.training_test_close.set()
        else:
            await state_Admin.training_tests.set()
    elif m.text == "add a test":
        await m.answer("Please enter this test question:", reply_markup=keyboard_close())
        await state_Admin.lesson_tests_ozgartirish_test_savol.set()


@dp.message_handler(state=state_Admin.training_tests, content_types=types.ContentType.TEXT)
async def cmd_Admin_tests_menu(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer(f"Closed", reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()
    elif m.text == "Delete":
        data = await state.get_data()
        database_delete_test(data.get("current_test_id"))
        await m.answer(f"Test has been deleted.", reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()
    elif m.text == "Next":
        data = await state.get_data()
        tests_id = data.get("training_tests")
        test_id = ""
        if "_" in tests_id:
            for i in range(len(tests_id)):
                if tests_id[i] == "_":
                    tests_id = tests_id[i + 1:]
                    break
                else:
                    test_id += tests_id[i]
        else:
            test_id = tests_id
            tests_id = "0"
        await state.update_data(training_tests=tests_id)
        await state.update_data(current_test_id=test_id)
        answers = database_get_test_answers_by_id(test_id)
        await m.answer(text=answers["question_full_text_admin"],
                       reply_markup=keyboard_get_button(["Delete", "Close", "Next"]))
        if tests_id == "0":
            await state_Admin.training_test_close.set()
        else:
            await state_Admin.training_tests.set()


@dp.message_handler(state=state_Admin.training_test_close, content_types=types.ContentType.TEXT)
async def admin_tests_close(m:types.Message, state:FSMContext):
    if m.text == "Close":
        await m.answer(f"Closed", reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()
    elif m.text == "Delete":
        data = await state.get_data()
        database_delete_test(data.get("current_test_id"))
        await m.answer(f"Test has been deleted.", reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()
    elif m.text == "Next":
        await m.answer(f"Tests are over.", reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()


@dp.message_handler(state=state_Admin.lesson_tests_ozgartirish_test_savol, content_types=types.ContentType.TEXT)
async def cmd_Admin_test_add_name(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer(f"Closed", reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()
    else:
        await state.update_data(lesson_tests_ozgartirish_test_savol=m.text)
        await m.answer("Please enter this test answers:\nA answer text .\nB answer text .\nC answer text .",
                       reply_markup=keyboard_close())
        await state_Admin.lesson_tests_ozgartirish_test_javoblar.set()


@dp.message_handler(state=state_Admin.lesson_tests_ozgartirish_test_javoblar, content_types=types.ContentType.TEXT)
async def cmd_Admin_test_add_answers(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer(f"Closed", reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()
    else:
        await state.update_data(lesson_tests_ozgartirish_test_javob=m.text)
        await m.answer("Please selected a True answer:",
                      reply_markup= keyboard_get_button(["A","B","C","Close"]))
        await state_Admin.lesson_tests_ozgartirish_test_javoblar_togrisi.set()


@dp.message_handler(state=state_Admin.lesson_tests_ozgartirish_test_javoblar_togrisi, content_types=types.ContentType.TEXT)
async def cmd_Admin_test_add_answers(m: types.Message, state: FSMContext):
    if m.text == "Close":
        await m.answer(f"Closed", reply_markup=keyboard_get_test_menu())
        await state_Admin.lesson_tests.set()
    else:
        await state.update_data(lesson_tests_ozgartirish_test_javob_togrisi=m.text)
        data = await state.get_data()
        c_a = False
        if m.text == "A":c_a = "answer1"
        elif m.text == "B":c_a = "answer2"
        elif m.text == "C":c_a = "answer3"
        if c_a:
            database_add_test(
                book=data.get("book"),
                topic=data.get("lesson_number"),
                test_question=data.get("lesson_tests_ozgartirish_test_savol"),
                answer1=data.get("lesson_tests_ozgartirish_test_javob").split(".")[0][2:],
                answer2=data.get("lesson_tests_ozgartirish_test_javob").split(".")[1][3:],
                answer3=data.get("lesson_tests_ozgartirish_test_javob").split(".")[2][3:],
                correct_answer=c_a
            )
            await m.answer(f"Test added.", reply_markup=keyboard_get_test_menu())
            await state_Admin.lesson_tests.set()


# lessons
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
        await m.answer(text = str(database_get_words_by_topic(book_name, topic)))
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
        words = word=data.get("add_lesson_vocabulary")
        database_add_words_audio(words)
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