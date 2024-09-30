from get_keys import USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI
import requests

from config import URL, AI_DEFAULT_MODEL_TEXT_TO_VOICE, AUDIO_FOLDER, AI_DEFAULT_MODEL_VOICE_TO_TEXT
#from general_functions import random_name_2X





async def get_text_openai(data):





    model = data.get("model_voice_to_text", AI_DEFAULT_MODEL_VOICE_TO_TEXT) # whisper-1 AI_DEFAULT_MODEL_VOICE_TO_TEXT !!!!!!!!!!!!!!!!!
    prompt = data.get("user_content") # The prompt should match the audio language.
    response_format = data.get("response_format", "text") # json, text, srt, verbose_json, or vtt
    language = data.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
    file_path = data.get("file_path")
    name_file = data.get("name_file")


    url = f"{URL}/api/transcription-openai/"

    data = {
            "username": USERNAME_API_AI,
            "model": model,
            # timestamp_granularities=["word"],                                                             # Not suport
            # timestamp_granularities=["segment"]                                                           # Not suport
    }

    data["language"] = language
    data["prompt"] = prompt
    data["response_format"] = response_format

    headers = {
        KEY_API_AI: VALUE_KEY_API_AI,
    }


    if file_path:
        with open(file_path, 'rb') as f:
            file = {
                'audio': (name_file, f)
            }

            response = requests.post(url, headers=headers, data=data, files=file)

            # Проверка статуса ответа и вывод результата
            if response.status_code == 200:
                answer = response.json()
                return answer

            else:
                print("Error", response.status_code, response.text)



# {'response': 'Добрый вечер.\n', 'expenses': 0.00020199999999999998, 'minutes': 0.016833333333333332}