from get_keys import USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI
from config import URL, AI_DEFAULT_MODEL_VOICE_TO_TEXT, NULL_TOKEN
import aiohttp
import aiofiles



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
    }

    headers = {
        KEY_API_AI: VALUE_KEY_API_AI,
    }

    if file_path:
        async with aiohttp.ClientSession() as session:
                async with aiofiles.open(file_path, 'rb') as f:
                    form = aiohttp.FormData()
                    content = await f.read()
                    form.add_field('audio', content, filename=name_file)
                    form.add_field('username', USERNAME_API_AI)
                    form.add_field('model', model)
                    if language:
                        form.add_field('language', language)
                    if prompt:
                        form.add_field('prompt', prompt)
                    if response_format:
                        form.add_field('response_format', response_format)

                    async with session.post(url, headers=headers, data=form) as response:
                        if response.status == 200:
                            try:
                                return await response.json()
                            except aiohttp.ContentTypeError:
                                text_response = await response.text()
                                return {'response': text_response, "minutes": NULL_TOKEN}
                        elif response.status == 400 or response.status == 500:
                            text_response = await response.text()
                            return {'response': text_response, "minutes": NULL_TOKEN}




# {'response': 'Добрый вечер.\n', 'expenses': 0.00020199999999999998, 'minutes': 0.016833333333333332}