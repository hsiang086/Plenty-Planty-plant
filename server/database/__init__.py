##############################
# Copyright © hsiang086 2024 #
##############################

import os
import aiosqlite

DB_PATH = os.path.join(os.path.dirname(__file__), 'serverdata.db')

class ServerDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    async def get_led_status(self):
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.execute('''SELECT status FROM led_status ORDER BY id DESC LIMIT 1''') as cursor:
                row = await cursor.fetchone()
                if row:
                    return bool(row[0])
                else:
                    return None

    async def set_led_status(self, status):
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute('''INSERT INTO led_status (status) VALUES (?)''', (int(status),))
            await conn.commit()
