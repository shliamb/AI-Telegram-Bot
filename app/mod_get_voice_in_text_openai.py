from get_keys import USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI
import requests
import base64

from config import URL, AI_DEFAULT_MODEL_TEXT_TO_VOICE, AUDIO_FOLDER
from general_functions import random_name_2X



async def get_voice_openai(data):

    model = data.get("model_text_to_voice")
    user_content = data.get("user_content") # 4096 characters max
    response_format = data.get("response_format", "opus") # mp3, opus, aac, flac, wav, and pcm in Telegram best - opus
    voice = data.get("voice") # alloy, echo, fable, onyx, nova, and shimmer
    speed = data.get("voice_speed") # 0.25 to 4.0 

    url = f"{URL}/api/speech-to-audio-openai/"

    data = {
            "username": USERNAME_API_AI,                                 
            "user_content": user_content,
            "voice": voice,
            "model": model,
            "response_format": response_format,
            "speed": speed,
    }

    headers = {
        KEY_API_AI: VALUE_KEY_API_AI,
    }

    response = requests.post(url, headers=headers, data=data)

    format_audio = data["response_format"]

    if response.status_code == 200:

        json_response = response.json()
        b64_json = json_response.get("b64_json")

        if b64_json:
            audio_data = base64.b64decode(b64_json)
            little = random_name_2X()
            file_path = f"{AUDIO_FOLDER}output_audio-{little}.{format_audio}"
            with open(file_path, "wb") as audio_file:
                audio_file.write(audio_data)

            #print(f"The audio file is saved as output_audio.{format_audio}")
            return file_path
    else:
        print(f"Error: {response.status_code} - {response.text}")


# Only file