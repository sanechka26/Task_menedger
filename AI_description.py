from gigachat import GigaChat
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

def get_description(title):
    with GigaChat(credentials=api_key, verify_ssl_certs=False) as giga:
        response = giga.chat(f"Напиши возможное описание для задачи с заголовком '{title}', объем твоего ответа должен быть не более 20 слов")
        print(response.choices[0].message.content)
    return response.choices[0].message.content