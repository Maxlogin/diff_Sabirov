import telebot
import sqlite3
import csv
API_KEY = '6758181956:AAGpdPEiF9Ae-FNNg95X3bZ0OYUmhEGQvvU'

bot = telebot.TeleBot(API_KEY)

def connect_to_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    return conn, cursor

@bot.message_handler(commands=['start'])
def start(message):
    conn, cursor = connect_to_db()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                           id_book INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           id_author INTEGER,
                           publication_year INTEGER,
                           isbn TEXT,
                           genre TEXT,
                           available BOOLEAN DEFAULT 1,
                           FOREIGN KEY (id_author) REFERENCES Authors(id_author)
                           )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Authors (
                           id_author INTEGER PRIMARY KEY AUTOINCREMENT,
                           first_name TEXT NOT NULL,
                           last_name TEXT NOT NULL,
                           date_of_birth TEXT
                           )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Readers (
                           id_reader INTEGER PRIMARY KEY AUTOINCREMENT,
                           first_name TEXT NOT NULL,
                           last_name TEXT NOT NULL,
                           email TEXT,
                           phone TEXT
                           )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Issues (
                           id_issue INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_book INTEGER,
                           id_reader INTEGER,
                           issue_date TEXT NOT NULL,
                           return_date TEXT,
                           is_returned BOOLEAN DEFAULT 0,
                           FOREIGN KEY (id_book) REFERENCES Books(id_book),
                           FOREIGN KEY (id_reader) REFERENCES Readers(id_reader)
                           )''')

    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Таблицы в базе данных успешно созданы!")
#Книга
@bot.message_handler(commands=['add_book'])
def add_book(message):
    conn, cursor = connect_to_db()

    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, get_book_title)

def get_book_title(message):
    title = message.text
    bot.send_message(message.chat.id, "Введите ID автора:")
    bot.register_next_step_handler(message, get_author_id, title)

def get_author_id(message, title):
    id_author = int(message.text)
    bot.send_message(message.chat.id, "Введите год публикации:")
    bot.register_next_step_handler(message, get_publication_year, title, id_author)

def get_publication_year(message, title, id_author):
    publication_year = int(message.text)
    bot.send_message(message.chat.id, "Введите ISBN:")
    bot.register_next_step_handler(message, get_isbn, title, id_author, publication_year)

def get_isbn(message, title, id_author, publication_year):
    isbn = message.text
    bot.send_message(message.chat.id, "Введите жанр:")
    bot.register_next_step_handler(message, save_book, title, id_author, publication_year, isbn)

def save_book(message, title, id_author, publication_year, isbn):
    genre = message.text
    conn, cursor = connect_to_db()

    cursor.execute("INSERT INTO Books (title, id_author, publication_year, isbn, genre) VALUES (?, ?, ?, ?, ?)",
                   (title, id_author, publication_year, isbn, genre))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Книга успешно добавлена!")


#Для авторов
@bot.message_handler(commands=['add_authors'])
def add_authors(message):
    conn, cursor = connect_to_db()
    bot.send_message(message.chat.id, "Введите first_name:")
    bot.register_next_step_handler(message, get_author_first_name)

def get_author_first_name(message):
    first_name = message.text
    bot.send_message(message.chat.id, "Введите last_name:")
    bot.register_next_step_handler(message, get_author_last_name, first_name)

def get_author_last_name(message, first_name):
    last_name = message.text
    bot.send_message(message.chat.id, "Введите date_of_birth:")
    bot.register_next_step_handler(message, save_author, first_name, last_name)

def save_author(message, first_name, last_name):
    date_of_birth = message.text
    conn, cursor = connect_to_db()

    cursor.execute("INSERT INTO Authors (first_name, last_name, date_of_birth) VALUES (?, ?, ?)",
                   (first_name, last_name, date_of_birth))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Автор успешно добавлен!")

#Для читателей
@bot.message_handler(commands=['add_readers'])
def add_readers(message):
    conn, cursor = connect_to_db()
    bot.send_message(message.chat.id, "Введите first_name:")
    bot.register_next_step_handler(message, get_reader_first_name)

def get_reader_first_name(message):
    first_name = message.text
    bot.send_message(message.chat.id, "Введите last_name:")
    bot.register_next_step_handler(message, get_reader_last_name, first_name)

def get_reader_last_name(message, first_name):
    last_name = message.text
    bot.send_message(message.chat.id, "Введите email:")
    bot.register_next_step_handler(message, get_reader_email, first_name, last_name)

def get_reader_email(message, first_name, last_name):
    email = message.text
    bot.send_message(message.chat.id, "Введите номер телефона:")
    bot.register_next_step_handler(message, save_reader, first_name, last_name, email)

def save_reader(message, first_name, last_name, email):
    phone = message.text
    conn, cursor = connect_to_db()

    cursor.execute("INSERT INTO Readers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
                   (first_name, last_name, email, phone))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Читатель успешно добавлен!")

#Последний
@bot.message_handler(commands=['add_vidacha'])
def add_vidacha(message):
    conn, cursor = connect_to_db()
    bot.send_message(message.chat.id, "Введите id книги:")
    bot.register_next_step_handler(message, get_book_faf)

def get_book_faf(message):
    titlev = message.text
    bot.send_message(message.chat.id, "Введите ID Читателя:")
    bot.register_next_step_handler(message, get_fee, titlev)

def get_fee(message, titlev):
    id_author = message.text
    bot.send_message(message.chat.id, "Введите issue_date:")
    bot.register_next_step_handler(message, get_raaaf, titlev, id_author)

def get_raaaf(message, titlev, id_author):
    publication_year = (message.text)
    bot.send_message(message.chat.id, "Введите return_date:")
    bot.register_next_step_handler(message, get_babay, titlev, id_author, publication_year)

def get_babay(message, titlev, id_author, publication_year):
    isbn = message.text
    bot.send_message(message.chat.id, "Введите вернута ли:")
    bot.register_next_step_handler(message, save_book4, titlev, id_author, publication_year, isbn)

def save_book4(message, titlev, id_author, publication_year, isbn):
    genre = int(message.text)
    conn, cursor = connect_to_db()

    cursor.execute("INSERT INTO Issues (id_book, id_reader, issue_date, return_date, is_returned) VALUES (?, ?, ?, ?, ?)",
                   (titlev, id_author, publication_year, isbn, genre))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Книга успешно выдана!")

@bot.message_handler(commands=['export'])
def export_command(message):
    export_to_csv()
    bot.send_message(message.chat.id, "Экспорт в CSV файлы выполнен успешно.")

def export_to_csv():
    conn, cursor = connect_to_db()

    cursor.execute("SELECT * FROM Books")
    with open('Books.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['id_book', 'title', 'id_author', 'publication_year', 'isbn', 'genre', 'available'])
        csv_writer.writerows(cursor.fetchall())

    cursor.execute("SELECT * FROM Authors")
    with open('Authors.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['id_author', 'first_name', 'last_name', 'date_of_birth'])
        csv_writer.writerows(cursor.fetchall())

    cursor.execute("SELECT * FROM Readers")
    with open('Readers.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['id_reader', 'first_name', 'last_name', 'email', 'phone'])
        csv_writer.writerows(cursor.fetchall())

    cursor.execute("SELECT * FROM Issues")
    with open('Issues.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['id_issue', 'id_book', 'id_reader', 'issue_date', 'return_date', 'is_returned'])
        csv_writer.writerows(cursor.fetchall())

    conn.close()
    print("Экспорт в CSV файлы завершен.")

bot.polling()
