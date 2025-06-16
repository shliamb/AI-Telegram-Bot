from get_keys import ACCESS_ID, KEY_API_AI, VALUE_KEY_API_AI
from config import URL, NULL_TOKEN
import aiohttp
import aiofiles
import json
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', '/log/ai.log')



async def mod_gemini_chat(data):

    # Get data:
    model = data.get("model_language")
    user_content = data.get("user_content")
    system_content = data.get("system_content")
    file_path = data.get("file_path")
    name_file = data.get("name_file")

    assist_content = data.get("assist_content")

    #############
    # if assist_content:
    #     for n in assist_content:
    #         print(n)

    # URL:
    url = f"{URL}/api/gemini/"

    # HEDER:
    headers = {KEY_API_AI : VALUE_KEY_API_AI}


    async with aiohttp.ClientSession() as session:
        if file_path:
            async with aiofiles.open(file_path, 'rb') as f:
                form = aiohttp.FormData()
                content = await f.read()
                form.add_field('file', content, filename=name_file)
                form.add_field('access_id', ACCESS_ID)
                form.add_field('model', model)
                if system_content:
                    form.add_field('system_content', system_content)
                form.add_field('user_content', user_content)
            
                async with session.post(url, headers=headers, data=form) as response:
                    if response.status == 200:
                        try:
                            return await response.json()
                        except aiohttp.ContentTypeError:
                            logger_ai.error("Error: Gemini respons is not json")
                            text_response = await response.text()
                            return {'response': text_response, "used_tokens": NULL_TOKEN}
                    elif response.status == 400 or response.status == 500:
                        logger_ai.error(f"Error: Gemini respons is code: {str(response.status)}")
                        text_response = await response.text()
                        return {'response': text_response, "used_tokens": NULL_TOKEN}
                

        else:
            form = aiohttp.FormData()
            form.add_field('access_id', ACCESS_ID)
            form.add_field('model', model)
            if system_content:
                form.add_field('system_content', system_content)
            # if response_format:
            #     form.add_field('response_format', json.dumps(response_format))
            if assist_content:
                form.add_field('assist_content', json.dumps(assist_content))
            form.add_field('user_content', user_content)

            async with session.post(url, headers=headers, data=form) as response:
                if response.status == 200:
                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError:
                        logger_ai.error("Error: Gemini respons is not json")
                        text_response = await response.text()
                        return {'response': text_response, "used_tokens": NULL_TOKEN}
                elif response.status == 400 or response.status == 500:
                    logger_ai.error(f"Error: Gemini respons is code: {str(response.status)}")
                    text_response = await response.text()
                    return {'response': text_response, "used_tokens": NULL_TOKEN}



# {'response': 'Это короткая стрижка, вероятно, под названием "пикси" или "боб". \n', \
# 'expenses': 0.00033075, 'used_tokens': 294}



