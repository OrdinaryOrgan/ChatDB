import pymysql
from database.db_config import MYSQL_CONFIG
from database.utils import DbStatusCode

class MysqlUser:
    def __init__(self):
        self.db_config = MYSQL_CONFIG.copy()
        self.connection = None

    def __del__(self):
        if self.connection is not None:
            self.connection.close()

    def login(self, username: str, password: str) -> str | DbStatusCode:
        self.db_config['user'] = username
        self.db_config['password'] = password
        try:
            self.connection = pymysql.connect(**self.db_config)
        except Exception as e:
            return f"No such user or wrong username/password: {str(e)}"
        else:
            return DbStatusCode.Login_Success

    def execute_sql(self, sql: str) -> str | tuple:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                if sql.strip().lower().startswith(('select', 'show')):
                    return cursor.fetchall()
                else:
                    self.connection.commit()
                    return f"Execution Complete! Affect rows: {cursor.rowcount}"
        except Exception as e:
            self.connection.rollback()
            raise e