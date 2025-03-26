import aiosqlite

NAME_DB = 'bot_1.db'

async def create_tables():
    """создаем таблицу в базе данных"""
    async with aiosqlite.connect(NAME_DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            reg_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            balance REAL NOT NULL DEFAULT 0.0
        )
    """)
        await db.commit()

    async with aiosqlite.connect(NAME_DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS duels(
            duel_id TEXT PRIMARY KEY, 
            creator_duel_id INTEGER NOT NULL,
            creator_duel_name TEXT NOT NULL,
            creator_choice TEXT NOT NULL,
            opponent_id INTEGER,
            opponent_name TEXT,
            opponent_choice TEXT,
            stake REAL NOT NULL,
            chat_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            result TEXT,
            winner_id INTEGER
        )
                         """)
        await db.commit()


async def add_users(user_id, username, first_name, last_name):
    """добавляет пользователя в бд если его не сууществует"""
    async with aiosqlite.connect(NAME_DB) as db:
        cursor = await db.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id, ))
        result = await cursor.fetchone()
        if result is None:
            await db.execute("INSERT INTO users(user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)", (user_id, username, first_name, last_name))
            await db.commit()
            return True
        else:
            return False


async def get_all_users_ad():
    """выдает все id пользователей"""
    async with aiosqlite.connect(NAME_DB) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        result = await cursor.fetchall()
        return result


async def get_user_coin(user_id):
    """Выводит количество монет"""
    async with aiosqlite.connect(NAME_DB) as db:
        cursor = await db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id, ))
        result = await cursor.fetchone()
        if result is not None:
            return result
        else:
            return 0

async def add_user_coins(user_id, amount):
    """прибавляет монеты к балансу пользователя"""
    async with aiosqlite.connect(NAME_DB) as db:
        cursor = await db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        await db.commit()