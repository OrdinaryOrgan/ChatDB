from typing import Any
import pymysql
from database.db_config import MYSQL_CONFIG
from database.mysql_user import MysqlUser
from database.utils import DbStatusCode

class MySQLManager:
    def __init__(self):
        self.db_config = MYSQL_CONFIG.copy()
        self.db_config['user'] = 'root'
        self.db_config['password'] = 'root'
        self.connection = pymysql.connect(**self.db_config)

    def __del__(self):
        self.connection.close()

    def execute_sql(self, sql: str) -> tuple[tuple[Any, ...], ...] | str:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                if sql.strip().lower().startswith(('select', 'show', 'describe')):
                    return cursor.fetchall()
                else:
                    self.connection.commit()
                    return f"Execution Complete! Affect rows: {cursor.rowcount}"
        except Exception as e:
            self.connection.rollback()
            raise e

    def execute_sql_script(self, sql_script_path: str) -> tuple[tuple[Any, ...], ...] | str:
        try:
            with self.connection.cursor() as cursor:
                with open(sql_script_path, 'r', encoding = 'utf-8') as f:
                    sql_script = f.read()
                cursor.execute(sql_script)
                while True:
                    if cursor.description:
                        return cursor.fetchall()
                    if not cursor.nextset():
                        break
            self.connection.commit()
            return f"Execution Complete! Affect rows: {cursor.rowcount}"
        except Exception as e:
            self.connection.rollback()
            raise e

    def create_user(self, username: str, password: str) -> str:
        try:
            create_user_statement = f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';"
            grant_role_statement = f"GRANT 'normal_role' TO '{username}'@'localhost';"
            set_default_role_statement = f"SET DEFAULT ROLE 'normal_role' TO '{username}'@'localhost';"
            self.execute_sql(create_user_statement)
            self.execute_sql(grant_role_statement)
            self.execute_sql(set_default_role_statement)
        except Exception as e:
            return f"Exception while creating user: {str(e)}"
        else:
            return "Create User Complete!"

    def advanced_user_authorization(self, username: str, password: str, admin: str, admin_password: str) -> str:
        user = MysqlUser()
        if user.login(username, password) != DbStatusCode.Login_Success:
            return 'No such user or Wrong username/password!'
        if admin != self.db_config['user'] or admin_password != self.db_config['password']:
            return 'Admin Authorization Failed!'
        else:
            grant_role_statement = f"GRANT 'advanced_role' TO '{username}'@'localhost';"
            set_default_role_statement = f"SET DEFAULT ROLE 'advanced_role' TO '{username}'@'localhost';"
            sql_statement = grant_role_statement + set_default_role_statement
            return self.execute_sql(sql_statement)

mysql_manager_instance = MySQLManager()