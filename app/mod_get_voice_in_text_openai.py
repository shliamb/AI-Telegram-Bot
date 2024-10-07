from get_keys import USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI
from config import URL, AUDIO_FOLDER
from general_functions import random_name_2X, encode_file
import aiohttp
import aiofiles

import base64



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

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                json_response = await response.json()
                b64_json = json_response.get("b64_json")

                if b64_json:
                    audio_data = base64.b64decode(b64_json)
                    little = random_name_2X()
                    file_path = f"{AUDIO_FOLDER}output_audio-{little}.{response_format}"

                    try:
                        async with aiofiles.open(file_path, "wb") as audio_file:
                            await audio_file.write(audio_data)
                            print(f"The audio file is saved as {file_path}")
                            return file_path

                    except aiohttp.ContentTypeError:
                        text_response = await response.text()
                        print(text_response)

            elif response.status == 400 or response.status == 500:
                text_response = await response.text()
                print(text_response)


# Only file

