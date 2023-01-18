from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import *


def keyboard_admin_main_menu():
    # Tugmalar matni
    books_button = KeyboardButton('Books')
    information_button = KeyboardButton('Information')

    # Tugmalar matnini ReplyKeyboardMarkup obyektiga qo'shish
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(books_button)
    markup.add(information_button)
    return markup


def keyboard_admin_menu_information():
    # Tugmalar matni
    developer_button = KeyboardButton('Developer')
    bot_button = KeyboardButton('Bot')
    admin_button = KeyboardButton('Admin')
    close = KeyboardButton("Close")
    # Tugmalar matnini ReplyKeyboardMarkup obyektiga qo'shish
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(developer_button)
    markup.add(bot_button)
    markup.add(admin_button)
    markup.add(close)
    return markup


def keyboard_books():
    book_names = database_get_books_name()
    book_buttons = [KeyboardButton(name[0]) for name in book_names]

    # Add the "Close" button
    book_buttons.append(KeyboardButton("Close"))
    book_buttons.append(KeyboardButton("Add a book"))
    # Create a ReplyKeyboardMarkup object
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*book_buttons)

    return keyboard


def keyboard_books_create_menu():
    # Tugmalar matni
    information_button = KeyboardButton('Information the book')
    teacher_button = KeyboardButton('About the teacher')
    lesson_button = KeyboardButton('Lessons')
    activity_button = KeyboardButton('Training')
    cancel_button = KeyboardButton('Close')
    delete_book = KeyboardButton("Delete this book")
    # Tugmalar matnini ReplyKeyboardMarkup obyektiga qo'shish
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(information_button)
    markup.add(teacher_button)
    markup.add(lesson_button)
    markup.add(activity_button)
    markup.add(delete_book)
    markup.add(cancel_button)
    return markup


def keyboard_get_update():
    # Create the "Update" button
    update_button = KeyboardButton("Update")
    close = KeyboardButton("Close")
    # Create a ReplyKeyboardMarkup object
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(update_button)
    keyboard.add(close)
    return keyboard


def keyboard_get_lessons_menu(book):
    data = database_get_topics(book)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    try:
        for i in data[0]:
            markup.add(KeyboardButton(i))
    except:pass
    markup.add("Add a lesson")
    markup.add("Close")
    return markup
def keyboard_get_lesson_menu():
    data = ["Vocabulary", "Exercise", "Rules", "Close", "Delete this lesson"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in data:
        markup.add(KeyboardButton(i))
    return markup


def keyboard_close():
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Close"))
    return markup


def keyboard_confirmation():
    data = ["No", "Yes",]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in data:
        markup.add(KeyboardButton(i))
    return markup
