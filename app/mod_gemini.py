from get_keys import TELEGRAM_BOT_TOKEN, USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI, USER_DB, PASWORD_DB, ADMIN_ID
import requests
import re
import asyncio




async def mod_gemini_chat(data):

    #file_path = None

    model = data.get("model", "gemini-1.5-flash-latest")
    user_content = data.get("user_content")
    system_content = data.get("system_content")
    #file_path = data.get("file_path")

    url = "http://137.184.87.156:8000/api/gemini/"

    data_ai = {
            "username": USERNAME_API_AI,
            "user_content": user_content,
            "system_content": system_content,
            "model": model,
    }

    headers = {
        KEY_API_AI : VALUE_KEY_API_AI,
    }

    response = requests.post(url, headers=headers, data=data_ai)#, files=files)

    if response.status_code == 200:
        answer_json = response.json()
        answer = answer_json.get("response")
    else:
        print(response.status_code, response.text)
        answer = str(response.text) + str(response.status_code)

    return answer



# {'response': 'Это короткая стрижка, вероятно, под названием "пикси" или "боб". \n', \
# 'expenses': 0.00033075, 'used_tokens': 294}