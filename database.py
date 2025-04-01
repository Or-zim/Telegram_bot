import aiosqlite

NAME_DB = 'bot_1.db'

CHAT_ID = -4759195662
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
            duel_id INTEGER PRIMARY KEY, 
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


async def del_user_coins(user_id, amount):
    """вычитает монеты из быланса пользователя"""
    async with aiosqlite.connect(NAME_DB) as db:
        cursor = await db.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
        await db.commit()


async def get_username(user_id):
    """выыодит тег пользователя"""
    async with aiosqlite.connect(NAME_DB) as db:
        cursor = await db.execute("SELECT username FROM users WHERE user_id = ?", (user_id, ))
        result = await cursor.fetchone()
        return result
    
async def add_duel(creator_duel_id=None, creator_duel_name=None, creator_choice=None, opponent_id=None, opponent_name=None, stake=None, chat_id=CHAT_ID, result=None, winner_id=None, status=False, ):
    """добавляет дуэль в бд"""
    async with aiosqlite.connect(NAME_DB) as db:
        await db.execute("INSERT INTO duels(creator_duel_id, creator_duel_name, creator_choice, opponent_id, opponent_name, stake, chat_id, result, winner_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (creator_duel_id, creator_duel_name, creator_choice, opponent_id, opponent_name, stake, chat_id, result, winner_id, status))
        await db.commit()
        return True

