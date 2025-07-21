from get_keys import ACCESS_ID, KEY_API_AI, VALUE_KEY_API_AI
from config import URL, NULL_TOKEN, PATH_LOGS
from typing import Optional, Dict, Any
import aiohttp
import aiofiles
import json
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', f'{PATH_LOGS}ai.log')





async def mod_gemini_chat(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Отправляет запрос в Gemini API с поддержкой файлов и текста.
    
    Args:
        data: Словарь с параметрами запроса
        
    Returns:
        Словарь с ответом API или ошибкой
    """
    url = f"{URL}/api/gemini/"
    headers = {KEY_API_AI: VALUE_KEY_API_AI}

    async with aiohttp.ClientSession() as session:
        form = await _build_form_data(data)
        return await _send_request(session, url, headers, form)




async def _build_form_data(data: Dict[str, Any]) -> aiohttp.FormData:
    """Строит FormData для запроса"""
    form = aiohttp.FormData()
    
    # Обязательные поля
    form.add_field('access_id', ACCESS_ID)
    form.add_field('model', data.get("model_language"))
    form.add_field('user_content', data.get("user_content"))
    
    # Опциональные поля
    if system_content := data.get("system_content"):
        form.add_field('system_content', system_content)
        
    if assist_content := data.get("assist_content"):
        form.add_field('assist_content', json.dumps(assist_content))
    
    # Файл, если есть
    if file_path := data.get("file_path"):
        await _add_file_to_form(form, file_path, data.get("name_file"))
    
    return form



async def _add_file_to_form(form: aiohttp.FormData, file_path: str, filename: Optional[str]):
    """Добавляет файл в FormData"""
    async with aiofiles.open(file_path, 'rb') as f:
        content = await f.read()
        form.add_field('file', content, filename=filename)



async def _send_request(
    session: aiohttp.ClientSession, 
    url: str, 
    headers: Dict[str, str], 
    form: aiohttp.FormData
) -> Dict[str, Any]:
    """Отправляет запрос и обрабатывает ответ"""
    try:
        async with session.post(url, headers=headers, data=form) as response:
            return await _handle_response(response)
    except aiohttp.ClientError as e:
        logger_ai.error(f"Network error: {e}")
        return {'response': f"Network error: {e}", "used_tokens": NULL_TOKEN}




async def _handle_response(response: aiohttp.ClientResponse) -> Dict[str, Any]:
    """Обрабатывает ответ от API"""
    if response.status == 200:
        try:
            answer: dict = await response.json()  # {"response": "{gemini answer all}", "expenses": 0.00033075, "used_tokens": 294}
            # print("\nanswer:", answer)
            list_answer = answer.get("response")
            expenses = answer.get("expenses")
            used_tokens = answer.get("used_tokens")

            main_response = ""

            for part in list_answer:

                if 'text' in part:
                    text_response = part['text']
                    # Добавить размышления если есть - thoughtSignature !!! Это не размышления

                # if 'thoughtSignature' in part:
                #     # function = part['functionCall']['name']
                #     print("\npart:", part, "\n")
                #     pass

                main_response += str(text_response)

            return {'response': main_response, "used_tokens": used_tokens}


        except aiohttp.ContentTypeError:
            logger_ai.error("Gemini response is not valid JSON")
            text_response = await response.text()
            return {'response': text_response, "used_tokens": NULL_TOKEN}
    
    # Обработка ошибок
    error_msg = f"Gemini API error: {response.status}"
    logger_ai.error(error_msg)
    
    try:
        text_response = await response.text()
    except Exception:
        text_response = f"Failed to read response body (status: {response.status})"
    
    return {'response': text_response, "used_tokens": NULL_TOKEN}























    # # Get data:
    # model = data.get("model_language")
    # user_content = data.get("user_content")
    # system_content = data.get("system_content")
    # file_path = data.get("file_path")
    # name_file = data.get("name_file")

    # assist_content = data.get("assist_content")

    # # URL:
    # url = f"{URL}/api/gemini/"

    # # HEDER:
    # headers = {KEY_API_AI : VALUE_KEY_API_AI}


    # async with aiohttp.ClientSession() as session:
    #     if file_path:
    #         async with aiofiles.open(file_path, 'rb') as f:
    #             form = aiohttp.FormData()
    #             content = await f.read()
    #             form.add_field('file', content, filename=name_file)
    #             form.add_field('access_id', ACCESS_ID)
    #             form.add_field('model', model)
    #             if system_content:
    #                 form.add_field('system_content', system_content)
    #             form.add_field('user_content', user_content)
            
    #             async with session.post(url, headers=headers, data=form) as response:
    #                 if response.status == 200:
    #                     try:
    #                         return await response.json()
    #                     except aiohttp.ContentTypeError:
    #                         logger_ai.error("Error: Gemini respons is not json")
    #                         text_response = await response.text()
    #                         return {'response': text_response, "used_tokens": NULL_TOKEN}
    #                 elif response.status == 400 or response.status == 500:
    #                     logger_ai.error(f"Error: Gemini respons is code: {str(response.status)}")
    #                     text_response = await response.text()
    #                     return {'response': text_response, "used_tokens": NULL_TOKEN}
                

    #     else:
    #         form = aiohttp.FormData()
    #         form.add_field('access_id', ACCESS_ID)
    #         form.add_field('model', model)
    #         if system_content:
    #             form.add_field('system_content', system_content)
    #         # if response_format:
    #         #     form.add_field('response_format', json.dumps(response_format))
    #         if assist_content:
    #             form.add_field('assist_content', json.dumps(assist_content))
    #         form.add_field('user_content', user_content)

    #         async with session.post(url, headers=headers, data=form) as response:
    #             if response.status == 200:
    #                 try:
    #                     return await response.json()
    #                 except aiohttp.ContentTypeError:
    #                     logger_ai.error("Error: Gemini respons is not json")
    #                     text_response = await response.text()
    #                     return {'response': text_response, "used_tokens": NULL_TOKEN}
    #             elif response.status == 400 or response.status == 500:
    #                 logger_ai.error(f"Error: Gemini respons is code: {str(response.status)}")
    #                 text_response = await response.text()
    #                 return {'response': text_response, "used_tokens": NULL_TOKEN}



# {'response': 'Это короткая стрижка, вероятно, под названием "пикси" или "боб". \n', \
# 'expenses': 0.00033075, 'used_tokens': 294}



