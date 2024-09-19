from get_keys import USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI
import requests
import re
import asyncio
from config import AI_DEFAULT_MODEL_GEMINI, URL



async def mod_gemini_chat(data):

    model = data.get("model", AI_DEFAULT_MODEL_GEMINI)
    user_content = data.get("user_content")
    system_content = data.get("system_content")
    file_path = data.get("file_path")
    name_file = data.get("name_file")


    url = f"{URL}/api/gemini/"

    data_ai = {
            "username": USERNAME_API_AI,
            "user_content": user_content,
            "model": model,
    }

    if system_content:
        data_ai["system_content"] = system_content


    headers = {
        KEY_API_AI : VALUE_KEY_API_AI,
    }

    if file_path:
        with open(file_path, 'rb') as file:
            files = {
                'file': (name_file, file),
            }


            response = requests.post(url, headers=headers, data=data_ai, files=files)

    elif file_path is None:
        response = requests.post(url, headers=headers, data=data_ai)

    if response.status_code == 200:
        answer_json = response.json()
        answer = answer_json.get("response")
    else:
        print(response.status_code, response.text)
        answer = str(response.text) + str(response.status_code)

    return answer



# {'response': 'Это короткая стрижка, вероятно, под названием "пикси" или "боб". \n', \
# 'expenses': 0.00033075, 'used_tokens': 294}