from get_keys import USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI
from config import URL, NULL_TOKEN
import aiohttp
import aiofiles



async def mod_openai_chat(data):

    # Get data:
    model = data.get("model_language")
    user_content = data.get("user_content")
    system_content = data.get("system_content")
    file_path = data.get("file_path")
    name_file = data.get("name_file")
    # URL:
    url = f"{URL}/api/openai_chat/"
    # HEDER:
    headers = {KEY_API_AI : VALUE_KEY_API_AI}


    if file_path:
        async with aiohttp.ClientSession() as session:
                async with aiofiles.open(file_path, 'rb') as f:
                    form = aiohttp.FormData()
                    content = await f.read()
                    form.add_field('image', content, filename=name_file)
                    form.add_field('username', USERNAME_API_AI)
                    form.add_field('user_content', user_content)
                    form.add_field('model', model)
                    if system_content:
                        form.add_field('system_content', system_content)
                
                    async with session.post(url, headers=headers, data=form) as response:
                        if response.status == 200:
                            try:
                                return await response.json()
                            except aiohttp.ContentTypeError:
                                text_response = await response.text()
                                return {'response': text_response, "used_tokens": NULL_TOKEN}
                        elif response.status == 400 or response.status == 500:
                            text_response = await response.text()
                            return {'response': text_response, "used_tokens": NULL_TOKEN}


    elif file_path is None:
        data_ai = {
                "username": USERNAME_API_AI,
                "user_content": user_content,
                "model": model,
        }

        if system_content:
            data_ai["system_content"] = system_content

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data_ai) as response:
                if response.status == 200:
                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError:
                        text_response = await response.text()
                        return {'response': text_response, "used_tokens": NULL_TOKEN}
                elif response.status == 400 or response.status == 500:
                    text_response = await response.text()
                    return {'response': text_response, "used_tokens": NULL_TOKEN}



# {'response': 'Это короткая стрижка, вероятно, под названием "пикси" или "боб". \n', \
# 'expenses': 0.00033075, 'used_tokens': 294}