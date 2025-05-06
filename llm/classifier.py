from llm import utils
from pydantic import BaseModel
from openai import OpenAI
import enum
from llm.llm_config import LLM_CONFIG

class DataBaseType(enum.Enum):
    MySQL = 'MySQL'
    MongoDB = 'MongoDB'

class ClassificationResponse(BaseModel):
    database_type: DataBaseType

class Classifier:
    def __init__(self):
        self.config = LLM_CONFIG['Gemini-2.0-flash-lite'] # Set your LLM config
        self.prompt = utils.get_classifier_prompt()
        self.messages = [{'role': 'system', 'content': self.prompt}]
        self.user_message_format = {'role': 'user', 'content': ''}
        self.assistant_message_format = {'role': 'assistant', 'content': ''}
        self.client = OpenAI(api_key = self.config['api_key'], base_url = self.config['base_url'])

    def text_input(self, user_input: str = None):
        user_message = self.user_message_format.copy()
        user_message['content'] = user_input
        self.messages.append(user_message)

    def classify(self) -> str:
        try:
            response = self.client.chat.completions.create(
                    model = self.config['model'],
                    messages = self.messages,
                    stream = False,
                    # response_format = {'type': 'json', 'content_type': 'application/json'},
            )
            classify_result = response.choices[0].message.content.strip()
        except Exception as e:
            return f'Error: {str(e)}'
        else:
            assistant_message = self.assistant_message_format.copy()
            assistant_message['content'] = classify_result
            self.messages.append(assistant_message)
            if classify_result.startswith(r'```json'):
                classify_result = '\n'.join(classify_result.split('\n')[1:-1])
            return classify_result