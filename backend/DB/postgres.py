class DBInteractions:
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