from get_keys import ACCESS_ID, KEY_API_AI, VALUE_KEY_API_AI
from config import URL, NULL_TOKEN, PATH_LOGS
import aiohttp
import aiofiles
import json
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', f'{PATH_LOGS}ai.log')





async def mod_openai_chat(data):

    # Get data:
    model = data.get("model_language")
    user_content = data.get("user_content")
    system_content = data.get("system_content")
    file_path = data.get("file_path")
    name_file = data.get("name_file")

    response_format = data.get("response_format") # ?
    assist_content = data.get("assist_content") # ?
    # URL:
    url = f"{URL}/api/openai-chat/"
    # HEDER:
    headers = {KEY_API_AI : VALUE_KEY_API_AI}

    ########################
    # if assist_content:
    #     for n in assist_content:
    #         print(n)

    print(user_content)

    async with aiohttp.ClientSession() as session:
            if file_path:
                async with aiofiles.open(file_path, 'rb') as f:
                    form = aiohttp.FormData()
                    content = await f.read()
                    form.add_field('file', content, filename=name_file)
                    form.add_field('access_id', ACCESS_ID)
                    form.add_field('model', model)
                    form.add_field('user_content', user_content)
                
                    async with session.post(url, headers=headers, data=form) as response:
                        if response.status == 200:
                            try:
                                return await response.json()
                            except aiohttp.ContentTypeError:
                                logger_ai.error("Error: mod_openai_chat respons is not json")
                                text_response = await response.text()
                                return {'response': text_response, "used_tokens": NULL_TOKEN}
                        elif response.status == 400 or response.status == 500:
                            logger_ai.error(f"Error: mod_openai_chat respons is code: {str(response.status)}")
                            text_response = await response.text()
                            return {'response': text_response, "used_tokens": NULL_TOKEN}
            else:
                form = aiohttp.FormData()
                form.add_field('access_id', ACCESS_ID)
                form.add_field('model', model)
                if system_content and model not in ("o1-preview", "o1-mini", "o1", "o3-mini"):
                    form.add_field('system_content', system_content)
                if response_format:
                    form.add_field('response_format', json.dumps(response_format))
                if assist_content:
                    form.add_field('assist_content', json.dumps(assist_content))
                form.add_field('user_content', user_content)
            
                async with session.post(url, headers=headers, data=form) as response:
                    if response.status == 200:
                        try:
                            return await response.json()
                        except aiohttp.ContentTypeError:
                            logger_ai.error("Error: mod_openai_chat respons is not json")
                            text_response = await response.text()
                            return {'response': text_response, "used_tokens": NULL_TOKEN}
                    elif response.status == 400 or response.status == 500:
                        logger_ai.error(f"Error: mod_openai_chat respons is code: {str(response.status)}")
                        text_response = await response.text()
                        return {'response': text_response, "used_tokens": NULL_TOKEN}





# {'response': 'Это короткая стрижка, вероятно, под названием "пикси" или "боб". \n', \
# 'expenses': 0.00033075, 'used_tokens': 294}


#response_format = {"type":"json_schema","json_schema":{"name":"user_profile","schema":{"type":"object","properties":{"name":{"description":"The name of the user","type":"string"},"age":{"description":"The age of the user","type":"integer"},"interests":{"description":"List of users interests","type":"array","items":{"type":"string"}}},"required":["name","age","interests"]}}}
#response_format = {"type": "text"}
#response_format = {"type": "json_object"}
