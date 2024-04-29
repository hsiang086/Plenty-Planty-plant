##############################
# Copyright © hsiang086 2024 #
##############################

import os
import aiosqlite

DB_PATH = os.path.join(os.path.dirname(__file__), 'serverdata.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

class ServerDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as conn:
            with open(SCHEMA_PATH, 'r') as f:
                schema = f.read()
            await conn.executescript(schema)
            await conn.commit()

    async def get_led_status(self) -> bool:
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.execute('''SELECT status FROM led_status ORDER BY id DESC LIMIT 1''') as cursor:
                row = await cursor.fetchone()
                if row:
                    return bool(row[0])
                else:
                    return None

    async def set_led_status(self, status) -> None:
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute('''INSERT INTO led_status (status) VALUES (?)''', (int(status),))
            await conn.commit()
