import os

import openai
from openai import AuthenticationError

token = os.getenv('TOKEN_OPENAI')
try:
    token = 'sk-proj-' + token[:3:-1] if token.startswith('gpt:') else token
except AttributeError:
    print("Перед запуском посмотри в README.md!")
openai.api_key = token


class ChatGPTService:
    def __init__(self):
        self.message_history = []

    def add_message(self, user_content):
        self.message_history.append({"role": "user", "content": user_content})

    def get_response(self, model="gpt-3.5-turbo", temperature=0.7):
        response = None
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=self.message_history,
                temperature=temperature,
                max_tokens=500
            )
        except AuthenticationError:
            print('Указан некорректный Open AI API ключ!')

        reply = response.choices[0].message.content
        self.add_message(reply)

        return reply

    def clear_message_history(self):
        self.message_history.clear()
