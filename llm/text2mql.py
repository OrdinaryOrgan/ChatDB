from openai import OpenAI
from llm import utils
from llm.llm_config import LLM_CONFIG

class Text2MQL:
    def __init__(self):
        self.config = LLM_CONFIG['DeepSeek-V3'] # Set your LLM config
        self.prompt = utils.get_text2mql_prompt()
        self.messages = [{'role': 'system', 'content': self.prompt}]
        self.user_message_format = {'role': 'user', 'content': ""}
        self.assistant_message_format = {'role': 'assistant', 'content': ""}
        self.client = OpenAI(api_key = self.config['api_key'], base_url = self.config['base_url'])

    def text_input(self, user_input: str = None):
        user_message = self.user_message_format.copy()
        user_message['content'] = user_input
        self.messages.append(user_message)

    def text_to_mql(self) -> str:
        try:
            response = self.client.chat.completions.create(
                    model = self.config['model'],
                    messages = self.messages,
                    stream = False
            )
            mql_code_block = response.choices[0].message.content.strip()
        except Exception as e:
            return f'Error: {str(e)}'
        else:
            assistant_message = self.assistant_message_format.copy()
            assistant_message['content'] = mql_code_block
            self.messages.append(assistant_message)
            mql_query = mql_code_block
            if mql_code_block.startswith(r"```json") or mql_code_block.startswith(r"```javascript"):
                mql_query = '\n'.join(mql_code_block.split('\n')[1:-1])
            return mql_query