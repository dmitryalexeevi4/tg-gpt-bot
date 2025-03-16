import os

import openai

token = os.getenv('TOKEN_OPENAI')
token = 'sk-proj-' + token[:3:-1] if token.startswith('gpt:') else token
openai.api_key = token


class ChatGPTService:
    def __init__(self):
        self.message_history = []

    def add_message(self, user_content):
        self.message_history.append({"role": "user", "content": user_content})

    def get_response(self, model="gpt-3.5-turbo", temperature=0.7):
        response = openai.chat.completions.create(
            model=model,
            messages=self.message_history,
            temperature=temperature,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        self.add_message(reply)

        return reply
