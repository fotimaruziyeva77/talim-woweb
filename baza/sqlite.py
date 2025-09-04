import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
            full_name TEXT,
            telegram_id INTEGER UNIQUE,
            phone TEXT,
            referrals INTEGER DEFAULT 0,     -- yangi ustun
            invited_by INTEGER               -- kim taklif qilgan
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, telegram_id: int, full_name: str, phone: str, invited_by: int = None):
        sql = """
        INSERT OR IGNORE INTO Users(telegram_id, full_name, phone, invited_by) 
        VALUES(?, ?, ?, ?);
        """
        self.execute(sql, parameters=(telegram_id, full_name, phone, invited_by), commit=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def all_users_id(self):
        return self.execute("SELECT telegram_id FROM Users;", fetchall=True)
    
    def get_user(self, telegram_id):
        return self.execute("SELECT * FROM Users WHERE telegram_id=?", parameters=(telegram_id,), fetchone=True)

    # 🔑 REFERAL METODLAR
    def get_referrals(self, user_id: int):
        sql = "SELECT referrals FROM Users WHERE telegram_id=?"
        result = self.execute(sql, parameters=(user_id,), fetchone=True)
        return result[0] if result else 0

    def add_referral(self, inviter_id: int):
        sql = "UPDATE Users SET referrals = referrals + 1 WHERE telegram_id=?"
        self.execute(sql, parameters=(inviter_id,), commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
