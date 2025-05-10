from llm.classifier import Classifier
from llm.mql_result2text import MQLResult2Text
from llm.text2mql import Text2MQL
from llm.text2sql import Text2SQL
from llm.sql_result2text import SQLResult2Text
from database.mysql_manager import mysql_manager_instance
from database.mongodb_manager import mongodb_manager_instance
from database.mongodb_user import MongoDBUser
from database.utils import print_sql_result
import json

def main():
    text2sql_manager = Text2SQL()
    text2mql_manager = Text2MQL()
    sql_result2text_manager = SQLResult2Text()
    mql_result2text_manager = MQLResult2Text()
    classifier_manager = Classifier()
    mongodb_user = MongoDBUser()
    mongodb_user.login()

    print('Welcome to use ChatDB!\nInput exit to quit')
    while True:
        text_input = input('Please input: ')
        if text_input == 'exit':
            print('Thank you for using ChatDB!')
            break
        classifier_manager.text_input(text_input)
        database_type = classifier_manager.classify()
        database_type = json.loads(database_type)['database_type']
        if database_type == 'MySQL':
            text2sql_manager.text_input(text_input)
            sql_statement = text2sql_manager.text_to_sql()
            print(f'\nSQL Generated: \n{sql_statement}\n')
            try:
                sql_result = mysql_manager_instance.execute_sql(sql_statement)
            except Exception as e:
                print(f'Error: {e}')
            else:
                print('SQL Query Result: ')
                if type(sql_result) == type('str') and sql_result.startswith('Execution Complete'):
                    print(sql_result)
                else:
                    print_sql_result(sql_result)
                result_explanation = sql_result2text_manager.result_to_text(text_input, sql_result)
                print(f'\nSQL Result Explanation: \n{result_explanation}')
        elif database_type == 'MongoDB':
            text2mql_manager.text_input(text_input)
            mql_query = text2mql_manager.text_to_mql()
            print(f'\nMQL Generated: \n{mql_query}\n')
            try:
                mql_query = mql_query.replace("null", "None")
                local_vars = {}
                exec(f"query_dict = {mql_query}", {}, local_vars)
                query_dict = local_vars['query_dict']
                collection = query_dict.get("collection")
                operation = query_dict.get("operation")
                args = query_dict.get("args", [])
                kwargs = query_dict.get("kwargs", {})
                mql_result = mongodb_user.execute_query(collection, operation, args, **kwargs)
            except Exception as e:
                print(f'Error: {e}')
            else:
                print("MQL Query Result:")
                print(mql_result)
                result_explanation = mql_result2text_manager.result_to_text(text_input, mql_result)
                print(f'\nMQL Result Explanation: \n{result_explanation}')

if __name__ == '__main__':
    main()