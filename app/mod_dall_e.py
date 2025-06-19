from config import URL, NULL_TOKEN, PATH_LOGS
from get_keys import ACCESS_ID, KEY_API_AI, VALUE_KEY_API_AI
import aiohttp
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', f'{PATH_LOGS}ai.log')


async def mod_openai_dall_e(data: dict) -> str:
    '''Генерация картинок от OpenAI'''

    model = data.get("model_draw") # dall-e-3
    prompt = data.get("user_content")
    quality = data.get("img_quality") # standard or hd
    style = data.get("img_style") # vivid ore natural
    response_format = data.get("response_format", "url") # url or b64_json
    size = data.get("img_size")
    n = data.get("n_number")

    url = f"{URL}/api/openai-img/"

    data = {
            "access_id": ACCESS_ID,
            "model": model,
            "user_content": prompt,
            "size": size,
            "response_format": response_format,
            "n": n,
    }

    if model == "dall-e-3":
        data["quality"] = quality
        data["style"] = style

    headers = {
        KEY_API_AI: VALUE_KEY_API_AI,
    }


    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                try:
                    return await response.json()
                except aiohttp.ContentTypeError:
                    logger_ai.error("Error: Generate img of OpenAI dot Json response")
                    text_response = await response.text()
                    return {'response': text_response, "used_tokens": NULL_TOKEN}
            elif response.status == 400 or response.status == 500:
                logger_ai.error(f"Error: Generate img of OpenAI code: {response.status}")
                text_response = await response.text()
                return {'response': text_response, "used_tokens": NULL_TOKEN}


# return {"response":"https://oaidalleapiprodscus.blob.core.windows.net/private/org-uhWB0qfaxHXgZEMKyRt5RKG9/user-ynhKanTD5u5duWFG6UDs0OXb/img-fTqt7lgsT5tk6N5u9IythNne.png?st=2024-10-07T19%3A09%3A18Z&se=2024-10-07T21%3A09%3A18Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-10-06T23%3A54%3A57Z&ske=2024-10-07T23%3A54%3A57Z&sks=b&skv=2024-08-04&sig=KisUS7ahor%2Bo18cXIPwmEhFLMVoknVs%2Bzb143gORVUw%3D","expenses":0.04,"pictures":1}



