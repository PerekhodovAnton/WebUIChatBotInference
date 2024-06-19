import asyncio
import asyncpg
from fastapi import FastAPI


app = FastAPI()

# подключаемся к БД
async def connect_to_database(user, password, database, host):
    try:
        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=database,
            host=host
        )
        print("Connected to the database successfully!")
        return conn
    except asyncpg.PostgresError as e:
        print(f"Error connecting to the database: {e}")

import asyncpg

# реализован класс для вставки данных в БД
class DBinsert:
    @staticmethod
    async def user(conn, name, user_type):
        existing_user = await conn.fetchrow(
            'SELECT userid FROM users WHERE name = $1;',
            name
        )
        if existing_user:
            print(f"User with name '{name}' already exists!")
            return existing_user['userid']  # возвращаем существующий userid
        else:
            result = await conn.fetchrow(
                'INSERT INTO users (name, type) VALUES ($1, $2) RETURNING userid;',
                name, user_type
            )
            print("User inserted successfully!")
            return result['userid']

    @staticmethod
    async def query(conn, user_id, message):
        result = await conn.fetchrow(
            "INSERT INTO queries (message, validity, date_time, userid) VALUES ($1, 'valid', NOW(), $2) RETURNING queryid, userid;",
            message, user_id
        )
        print("Query inserted successfully!")
        return result['userid'], result['queryid'] 

    @staticmethod
    async def response(conn, text, query_id):
        await conn.execute(
            "INSERT INTO responses (text, date_time, queryid) VALUES ($1, NOW(), $2);",
            text, query_id
        )
        print("Response inserted successfully!")

