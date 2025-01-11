# Library API

***

- [Установка и запуск](#установка-и-запуск)
- [Выдача админки (Docker)](#выдача-админки-docker)
- [Эндпоинты](#эндпоинты)

***

## Установка и запуск
1. Скопируйте себе репозиторий `git clone`
2. Создайте виртуальное окружение `python3 -m venv venv`
3. Активируйте его `source venv/bin/activate`
4. Создайте два файла в корне проекта: `.env` и `.end.db`, заполните следующим образом
и вставьте свои значения:

    ### .env
    ```
    DB_HOST=
    DB_PORT=
    DB_USER=
    DB_PASSWORD=
    DB_NAME=
    ```
   
    ### .env.db
    ```
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=
    ```

5. Вы можете либо запустить проект с помощью команды из консоли:
`uvicorn main:app --reload`, либо с помощью Docker: `docker-compose build` и `docker-compose up`.

## Выдача админки (Docker)
У модели пользователя есть флаг `is_admin`, который позволяет делать ему все основные
запросы на создание, обновление и удаление объектов. Если вы не используете докер, то можете поменять
этот флаг у пользователя с помощью утилиты `pgAdmin 4`. Но чтобы сделать это во время
запущенного докер контейнера необходимо выполнить следующие команды:
1. Зарегистрировать пользователя по эндпоинту `/users/register`
2. Войти в контейнер и в бд `docker exec -it postgres_db psql -U <db_username> -d <db_name>`
3. Выполнить команду `UPDATE public.user SET is_admin = TRUE WHERE id = <user_id>;`

После этого у вас будет возможность выполнять все основные crud операции.

## Эндпоинты

Хоть каждый из них и передает суть своим названием, я коротко опишу их здесь:

### /users

- `/register`: регистрация пользователя
- `/token`: получение jwt токена
- `/me`: информация о текущем пользователе (необходимо передавать токен с заголовком `Authorization: Bearer ...`)
- `/readers`: список читателей (т.к. модель у всех пользователей одна, то по сути читателем
является любой пользователь, у которого флаг `is_admin=False`)

### /authors

- ``