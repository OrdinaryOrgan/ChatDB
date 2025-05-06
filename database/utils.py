from enum import Enum

def print_sql_result(result: tuple):
    for item in result:
        for i in item:
            print(i, end = ' ')
        print()

class DbStatusCode(Enum):
    Login_Success = 'Login Success'