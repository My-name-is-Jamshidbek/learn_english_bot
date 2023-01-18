from aiogram.dispatcher.filters.state import State, StatesGroup


class state_Admin(StatesGroup):
    main_menu = State()

    book = State()

    book_menu = State()

    add_book = State()
    add_book_name = State()
    add_book_about = State()
    add_book_teacher = State()

    add_lesson = State()
    add_lesson_vocabulary = State()
    add_lesson_exercise = State()
    add_lesson_rules = State()

    delete_book = State()

    book_malumoti = State()
    book_malumoti_ozgartirish = State()

    teacher_malumoti = State()
    teacher_malumoti_ozgartirish = State()

    lessons = State()
    lesson_number = State()
    lessons_main = State()

    lesson_vocabulary = State()
    lesson_vocabulary_ozgartirish = State()

    lesson_exercise = State()
    lesson_exercise_ozgartirish = State()

    lesson_tests = State()
    lesson_tests_ozgartirish = State()
    lesson_tests_ozgartirish_test_number = State()
    lesson_tests_ozgartirish_test_savol = State()
    lesson_tests_ozgartirish_test_javoblar = State()
    lesson_tests_ozgartirish_test_javoblar_togrisi = State()

    lesson_writing = State()
    lesson_writing_ozgartirish = State()
    lesson_writing_ozgartirish_writing_number = State()
    lesson_writing_ozgartirish_writing_savol = State()
    lesson_writing_ozgartirish_writing_javob_togrisi = State()

    lesson_speaking = State()
    lesson_speaking_ozgartirish = State()
    lesson_speaking_ozgartirish_speaking_number = State()
    lesson_speaking_ozgartirish_speaking_savol = State()
    lesson_speaking_ozgartirish_speaking_javob_togrisi = State()

    lesson_spelling_a = State()
    lesson_spelling_a_ozgartirish = State()
    lesson_spelling_a_ozgartirish_spelling_a_number = State()
    lesson_spelling_a_ozgartirish_spelling_a_savol = State()
    lesson_spelling_a_ozgartirish_spelling_a_javob_togrisi = State()

    lesson_spelling_b = State()
    lesson_spelling_b_ozgartirish = State()
    lesson_spelling_b_ozgartirish_spelling_b_number = State()
    lesson_spelling_b_ozgartirish_spelling_b_savol = State()
    lesson_spelling_b_ozgartirish_spelling_b_javob_togrisi = State()

    about = State()
    about_menu = State()
    about_update = State()
