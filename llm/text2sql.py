from openai import OpenAI
from llm import utils
from llm.llm_config import LLM_CONFIG

class Text2SQL:
    def __init__(self):
        self.config = LLM_CONFIG['DeepSeek-V3'] # Set your LLM config
        self.prompt = utils.get_text2sql_prompt()
        self.messages = [{'role': 'system', 'content': self.prompt}]
        self.user_message_format = {'role': 'user', 'content': ""}
        self.assistant_message_format = {'role': 'assistant', 'content': ""}
        self.client = OpenAI(api_key = self.config['api_key'], base_url = self.config['base_url'])

    def text_input(self, user_input: str = None):
        user_message = self.user_message_format.copy()
        user_message['content'] = user_input
        self.messages.append(user_message)

    def text_to_sql(self) -> str:
        try:
            response = self.client.chat.completions.create(
                    model = self.config['model'],
                    messages = self.messages,
                    stream = False
            )
            sql_code_block = response.choices[0].message.content.strip()
        except Exception as e:
            return f'Error: {e}'
        else:
            assistant_message = self.assistant_message_format.copy()
            assistant_message['content'] = sql_code_block
            self.messages.append(assistant_message)
            sql_statement = sql_code_block
            if sql_code_block.startswith(r"```sql"):
                sql_statement = '\n'.join(sql_code_block.split('\n')[1:-1])
            return sql_statement