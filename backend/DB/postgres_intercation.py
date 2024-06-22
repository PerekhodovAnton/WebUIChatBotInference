class DBinsert:
    def __init__(self, pool):
        self.pool = pool

    async def user(self, name, user_type):
        existing_user = await self.pool.fetchrow(
            'SELECT userid FROM users WHERE name = $1;',
            name
        )
        if existing_user:
            print(f"User with name '{name}' already exists!")
            return existing_user['userid']  # возвращаем существующий userid
        else:
            result = await self.pool.fetchrow(
                'INSERT INTO users (name, type) VALUES ($1, $2) RETURNING userid;',
                name, user_type
            )
            print("User inserted successfully!")
            return result['userid']

    async def query(self, user_id, message):
        result = await self.pool.fetchrow(
            "INSERT INTO queries (message, validity, date_time, userid) VALUES ($1, 'valid', NOW(), $2) RETURNING queryid, userid;",
            message, user_id
        )
        print("Query inserted successfully!")
        return result['userid'], result['queryid'] 

    async def response(self, text, query_id):
        await self.pool.execute(
            "INSERT INTO responses (text, date_time, queryid) VALUES ($1, NOW(), $2);",
            text, query_id
        )
        print("Response inserted successfully!")

