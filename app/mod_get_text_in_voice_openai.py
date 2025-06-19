from get_keys import ACCESS_ID, KEY_API_AI, VALUE_KEY_API_AI
from config import URL, AI_DEFAULT_MODEL_VOICE_TO_TEXT, NULL_TOKEN, PATH_LOGS
import aiohttp
import aiofiles
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', f'{PATH_LOGS}ai.log')



async def get_text_openai(data):

    model = data.get("model_voice_to_text", AI_DEFAULT_MODEL_VOICE_TO_TEXT) # whisper-1 AI_DEFAULT_MODEL_VOICE_TO_TEXT !!!!!!!!!!!!!!!!!
    prompt = data.get("user_content") # The prompt should match the audio language.
    response_format = data.get("response_format", "text") # json, text, srt, verbose_json, or vtt
    language = data.get("language") # input language in ISO-639-1, will improve accuracy and latency - ru or en
    file_path = data.get("file_path")
    name_file = data.get("name_file")

    url = f"{URL}/api/openai-voice-to-text/"

    data = {
            "access_id": ACCESS_ID,
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
                    form.add_field('file', content, filename=name_file)
                    form.add_field('access_id', ACCESS_ID)
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
                                logger_ai.error("Error: openai-voice-to-text respons is not json")
                                text_response = await response.text()
                                return {'response': text_response, "minutes": NULL_TOKEN}
                        elif response.status == 400 or response.status == 500:
                            logger_ai.error(f"Error: openai-voice-to-text respons is code: {response.status}")
                            text_response = await response.text()
                            return {'response': text_response, "minutes": NULL_TOKEN}




# {'response': 'Добрый вечер.\n', 'expenses': 0.00020199999999999998, 'minutes': 0.016833333333333332}