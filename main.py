import sqlite3
import sys
from libdb import DB
from getpass import getpass
import re


HELP_STRING = """Ключи программы:\n\t-r Регистрация нового пользователя\n\t-a Аутентификация\n\t-c Изменение пароля\n\t-h Вывод вспомогательной строки\n"""
PASSWORD_SECURITY = """Требования к паролю:\n\t1. Минимум 7 символов\n\t2. Состоит только из малых кириллических букв\n"""


def main():
    if len(sys.argv) < 2:
        print(HELP_STRING)
        return

    if sys.argv[1] == '-r':
        print(PASSWORD_SECURITY)
        username, password = input('Введите имя пользователя: '), getpass(prompt='Введите пароль: ')
        surname, name, patronymic = input('Введите вашу фамилию: '), input('Введите ваше имя: '), input('Введите ваше отчество: ')
        birthday, birth_place, phone_number = input('Введите вашу дату рождения (формат дд-мм-гггг): '), input('Введите ваше место рождения: '), input('Введите ваш номер телефона (формат +7 xxx xxx xx xx): ')

        db = DB('database')
        try:
            db.cur.execute('select * from users;')
        except sqlite3.OperationalError:
            db.cur.execute('create table users (id integer primary key autoincrement, username varchar(50), password varchar(50), surname varchar(100), name varchar(100), patronymic varchar(100), birthday datetime, birth_place text, phone_number varchar(30));')

        db.cur.execute(f"""select 1 from users where username = '{username}' or phone_number = '{phone_number}'""")
        if db.cur.fetchone():
            print('\nПользователь с таким именем пользователя или телефоном уже существует, повторите попытку!')
            return
        if len(password) < 7:
            print('\nСлишком короткий пароль, должно быть минимум 7 малых кириллических символов, повторите попытку!')
            return
        if not re.fullmatch(pattern=r'[а-я]{7,}', string=password):
            print('\nПароль должен состоять из кириллицы нижнего регистра, повторите попытку!')
            return
        if not re.fullmatch(pattern=r'[0-3]\d-[0-1]\d-\d{4}', string=birthday):
            print('\nНеверный формат даты рождения или ее значение, повторите попытку!')
            return
        if not re.fullmatch(pattern=r'\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}', string=phone_number):
            print('\nНеверный формат номера телефона, повторите попытку!')
            return

        answer = input('Сохранить? Д/н: ')
        if answer.lower().strip() == 'д':
            db.cur.execute(f"""insert into users (username, password, surname, name, patronymic, birthday, birth_place, phone_number) values ('{username}', '{password}', '{surname}', '{name}', '{patronymic}', '{birthday}', '{birth_place}', '{phone_number}');""")
            db.db.commit()
            print('\nПользователь успешно зарегистрирован!')
        else:
            print('\nДействие успешно отменено!')

    elif sys.argv[1] == '-a':
        username, password = input('Введите имя пользователя: '), getpass(prompt='Введите пароль: ')
        db = DB('database')
        try:
            db.cur.execute(f"""select 1 from users where username = '{username}' and password = '{password}';""")
            if db.cur.fetchone():
                print('\nАвторизация успешно пройдена!')
            else:
                print('\nНеверные имя пользователя или пароль, повторите попытку!')
        except sqlite3.OperationalError:
            print('\nНеверные имя пользователя или пароль, повторите попытку!')

    elif sys.argv[1] == '-c':
        print(PASSWORD_SECURITY)
        username, old_password, new_password = input('Введите имя пользователя: '), getpass(prompt='Введите старый пароль: '), getpass(prompt='Введите новый пароль: ')
        try:
            db = DB('database')
            db.cur.execute(f"""select 1 from users where username = '{username}' and password = '{old_password}';""")
            if db.cur.fetchone():
                if len(new_password) < 7:
                    print('\nСлишком короткий пароль, должно быть минимум 7 малых кириллических символов, повторите попытку!')
                    return
                if not re.fullmatch(pattern=r'[а-я]{7,}', string=new_password):
                    print('\nПароль должен состоять из кириллицы нижнего регистра, повторите попытку!')
                    return
                answer = input('Сохранить? Д/н: ')
                if answer.lower().strip() == 'д':
                    db.cur.execute(f"""update users set password = '{new_password}' where username = '{username}';""")
                    db.db.commit()
                    print('\nПароль успешно изменен!')
                else:
                    print('\nДействие успешно отменено!')
            else:
                print('\nНеверные имя пользователя или старый пароль, повторите попытку!')
        except sqlite3.OperationalError:
            print('\nНеверные имя пользователя или старый пароль, повторите попытку!')

    elif sys.argv[1] == '-h':
        print(HELP_STRING)

    else:
        print(HELP_STRING)


if __name__ == '__main__':
    main()
