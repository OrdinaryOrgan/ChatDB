from openai import OpenAI
from llm import utils
from llm.llm_config import LLM_CONFIG

class MQLResult2Text:
    def __init__(self):
        self.config = LLM_CONFIG['DeepSeek-V3'] # Set your LLM config
        self.prompt = utils.get_mql_result2text_prompt()
        self.messages = [{'role': 'system', 'content': self.prompt}]
        self.user_message_format = {'role': 'user', 'content': ""}
        self.assistant_message_format = {'role': 'assistant', 'content': ""}
        self.client = OpenAI(api_key = self.config['api_key'], base_url = self.config['base_url'])

    def result_to_text(self, user_input: str, mql_result: dict | list) -> str:
        user_message = self.user_message_format.copy()
        user_message_content = str({"user_input": user_input, "mql_result": mql_result})
        user_message['content'] = user_message_content
        self.messages.append(user_message)
        response = self.client.chat.completions.create(model = self.config['model'],
                                                       messages = self.messages,
                                                       stream = False)
        explanation = response.choices[0].message.content.strip()
        assistant_message = self.assistant_message_format.copy()
        assistant_message['content'] = explanation
        self.messages.append(assistant_message)
        return explanation + '\n'