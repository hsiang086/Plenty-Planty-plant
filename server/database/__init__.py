import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'serverdata.db')

class LEDDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def get_led_status(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT status FROM led_status ORDER BY id DESC LIMIT 1''')
        row = c.fetchone()
        conn.close()
        if row:
            return bool(row[0])
        else:
            return None

    def set_led_status(self, status):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO led_status (status) VALUES (?)''', (int(status),))
        conn.commit()
        conn.close()
