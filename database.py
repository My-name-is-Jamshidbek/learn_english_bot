from config import DATABASE_NAME
import sqlite3


def create_database():
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # create the "information" table
    cursor.execute('''
        CREATE TABLE information (
            id INTEGER PRIMARY KEY,
            developer TEXT,
            bot TEXT,
            admin TEXT
        )
    ''')

    # create the "books" table
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            name TEXT, 
            about TEXT, 
            teacher TEXT
        )
    ''')

    # Create the "tests" table
    cursor.execute('''
        CREATE TABLE tests (
            id INTEGER PRIMARY KEY,
            book TEXT,
            topic TEXT,
            test_question TEXT,
            answer1 TEXT,
            answer2 TEXT,
            answer3 TEXT,
            correct_answer TEXT
        )
    ''')

    # Create the "writing" table
    cursor.execute('''
        CREATE TABLE words (
            id INTEGER PRIMARY KEY,
            book TEXT,
            topic TEXT,
            word TEXT
        )
    ''')

    # Create the "speaking" table
    cursor.execute('''
        CREATE TABLE exercises (
            id INTEGER PRIMARY KEY,
            book TEXT,
            topic TEXT,
            exercise TEXT
        )
    ''')

    # create the "rules" table
    cursor.execute('''
            CREATE TABLE rules (
                id INTEGER PRIMARY KEY,
                book TEXT,
                topic TEXT,
                rule TEXT
            )
        ''')

    # create the "lessons" table
    cursor.execute('''
        CREATE TABLE lessons (
            id INTEGER PRIMARY KEY,
            book TEXT,
            topic TEXT,
            about TEXT
        )
    ''')

    # Insert data into the "information" table
    cursor.execute("INSERT INTO information (developer, bot, admin) VALUES ('developer name','about the bot',"
                   "'about the admin')")

    # Insert data into the "information" table
    cursor.execute("INSERT INTO books (name, about, teacher) VALUES ('book1','about1','about1')")
    cursor.execute("INSERT INTO books (name, about, teacher) VALUES ('book2','about2','about2')")

    conn.commit()
    conn.close()


def database_books_insert_data(name, about, teacher):
    """
    Function to insert data into the "books" table in the "books.db" database
    :param name: str : name of the book
    :param about: str : about the book
    :param teacher: str : about the teacher
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insert data into the "books" table
    cursor.execute("INSERT INTO books (name, about, teacher) VALUES (?,?,?)", (name, about, teacher))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def database_get_books():
    """
    Function to retrieve all data from the "books" table in the "books.db" database
    :return: list : list of tuples, each tuple representing a row of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select data from the "books" table
    cursor.execute("SELECT * FROM books")

    # Fetch all the data
    books = cursor.fetchall()

    # Close the connection
    conn.close()

    return books


def database_get_books_about_by_book_name(book_name):
    """
    Function to retrieve data from the "books" table in the "books.db" database where teacher=teacher
    :param book_name: str : book name
    :return: list : list of tuples, each tuple representing a row of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Select data from the "books" table where teacher=teacher
    cursor.execute("SELECT about FROM books WHERE name=?", (book_name, ))

    # Fetch all the data
    books = cursor.fetchall()

    # Close the connection
    conn.close()

    return books[0][0]


def database_get_books_teacher_by_book_name(book_name):
    """
    Function to retrieve data from the "books" table in the "books.db" database where teacher=teacher
    :param book_name: str : book name
    :return: list : list of tuples, each tuple representing a row of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select data from the "books" table where teacher=teacher
    cursor.execute("SELECT teacher FROM books WHERE name=?", (book_name, ))

    # Fetch all the data
    books = cursor.fetchall()

    # Close the connection
    conn.close()

    return books[0][0]


def database_get_books_name():
    """
    Function to retrieve data from the "books" table in the "books.db" database where teacher=teacher
    :return: list : list of tuples, each tuple representing a row of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select data from the "books" table where teacher=teacher
    cursor.execute("SELECT name FROM books")

    # Fetch all the data
    books = cursor.fetchall()

    # Close the connection
    conn.close()

    return books


def database_update_information(developer=None, bot=None, admin=None):
    """
    Function to update information in the "information" table in the "database.db" database
    :param developer: str : teacher information
    :param bot: str : bot information
    :param admin: str : admin information
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Update information in the "information" table
    if developer:
        cursor.execute("UPDATE information SET developer = ?", (bot,))
    if bot:
        cursor.execute("UPDATE information SET bot = ?", (bot,))
    if admin:
        cursor.execute("UPDATE information SET admin = ?", (admin,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def database_get_information_developer():
    """
    Function to retrieve all data from the "information" table in the "database.db" database
    :return: tuple : tuple representing a row of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select data from the "information" table
    cursor.execute("SELECT developer FROM information")

    # Fetch the data
    information = cursor.fetchone()

    # Close the connection
    conn.close()

    return information


def database_get_information_bot():
    """
    Function to retrieve all data from the "information" table in the "database.db" database
    :return: tuple : tuple representing a row of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select data from the "information" table
    cursor.execute("SELECT bot FROM information")

    # Fetch the data
    information = cursor.fetchone()

    # Close the connection
    conn.close()

    return information


def database_get_information_admin():
    """
    Function to retrieve all data from the "information" table in the "database.db" database
    :return: tuple : tuple representing a row of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select data from the "information" table
    cursor.execute("SELECT admin FROM information")

    # Fetch the data
    information = cursor.fetchone()

    # Close the connection
    conn.close()

    return information


def database_update_book_by_name(name, about=None, teacher=None):
    """
    Function to update a book in the "books" table in the "books.db" database by its name
    :param name: str : name of the book
    :param about: str : about the book
    :param teacher: str : about the teacher
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    updates = []
    if about:
        updates.append(f'about = "{about}"')
    if teacher:
        updates.append(f'teacher = "{teacher}"')
    updates_str = ','.join(updates)
    # Update the book in the "books" table by its name
    cursor.execute(f"UPDATE books SET {updates_str} WHERE name = '{name}'")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def database_add_test(book, topic, test_question, answer1, answer2, answer3, correct_answer):
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insert data into the "tests" table
    cursor.execute("INSERT INTO tests (book, topic, test_question, answer1, answer2, answer3, correct_answer) VALUES "
                   "(?, ?, ?, ?, ?, ?, ?)", (book, topic, test_question, answer1, answer2, answer3, correct_answer))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def database_add_words(book, topic, word):
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insert data into the "writing" table
    cursor.execute("INSERT INTO words (book, topic, word) VALUES (?, ?, ?)", (book, topic, word))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def database_add_exercise(book, topic, exercise):
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insert data into the "writing" table
    cursor.execute("INSERT INTO exercises (book, topic, exercise) VALUES (?, ?, ?)", (book, topic, exercise))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def database_add_rule(book, topic, rule):
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Insert data into the "writing" table
    cursor.execute("INSERT INTO rules (book, topic, rule) VALUES (?, ?, ?)", (book, topic, rule))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def database_get_tests_by_topic(book, topic):
    """
    Function to retrieve a test from the "tests" table in the "database.db" database by topic
    :param book: str : book name
    :param topic: str : topic of the test
    :return: tuple : tuple representing a row of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select data from the "tests" table by topic
    cursor.execute("SELECT * FROM tests WHERE (topic = ? and book = ?)", (topic, book))

    # Fetch the data
    test = cursor.fetchone()

    # Close the connection
    conn.close()

    return test


def database_get_words_by_topic(book, topic):
    """
    Function to retrieve words from the "words" table in the "database.db" database by topic
    :param book: str : book name
    :param topic: str : topic of the words
    :return: list : list of tuples representing rows of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Select data from the "words" table by topic
    cursor.execute("SELECT word FROM words WHERE (topic = ? and book = ?)", (topic, book))

    # Fetch the data
    words = cursor.fetchall()

    # Close the connection
    conn.close()

    return words


def database_get_exercise_by_topic(book, topic):
    """
    Function to retrieve exercises from the "exercises" table in the "database.db" database by topic
    :param book: str : book name
    :param topic: str : topic of the exercises
    :return: list : list of tuples representing rows of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Select data from the "exercises" table by topic
    cursor.execute("SELECT exercise FROM exercises WHERE (topic = ? and book = ?)", (topic, book))

    # Fetch the data
    exercises = cursor.fetchall()
    # Close the connection
    conn.close()

    return exercises


def database_get_rule_by_topic(book, topic):
    """
    Function to retrieve rules from the "rules" table in the "database.db" database by topic
    :param book: str : name book
    :param topic: str : topic of the rules
    :return: list : list of tuples representing rows of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Select data from the "rules" table by topic
    cursor.execute("SELECT rule FROM rules WHERE (topic = ? and book = ?)", (topic, book))

    # Fetch the data
    rules = cursor.fetchall()

    # Close the connection
    conn.close()

    return rules


def database_get_topics(book):
    """
    Function to retrieve rules from the "rules" table in the "database.db" database by topic
    :param book: str : book name
    :return: list : list of tuples representing rows of data
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Select data from the "rules" table by topic
    cursor.execute("SELECT topic FROM rules WHERE book = ?", book)

    # Fetch the data
    topics = cursor.fetchall()

    # Close the connection
    conn.close()

    return topics

# create_database()
# print(database_get_information_())
# print(database_get_books())
# print([name[1] for name in database_get_books()])