from get_keys import KEY_API_DEEPSEEK
from config import NULL_TOKEN, PATH_LOGS
from general_functions import encode_file
from setup_config_logger import setup_logger
logger_ai = setup_logger('ai', f'{PATH_LOGS}ai.log')
from openai import AsyncOpenAI, RateLimitError, OpenAIError




client = AsyncOpenAI(api_key=KEY_API_DEEPSEEK, base_url="https://api.deepseek.com")


async def mod_deepseek_chat(data):

    user_content = data.get("user_content")
    system_content = data.get("system_content")
    model_name = data.get("model_language")
    image_path = data.get("file_path")
    # name_file = data.get("name_file") # ?

    assist_content = data.get("assist_content") # ?
    response_format = data.get("response_format") # ?

    try:

        messages_ai = []

        if system_content:
            messages_ai.append({"role": "system", "content": system_content},)

        if image_path:
            base64_file = await encode_file(image_path)
            messages_ai.append({"role": "user", "content": [{"type": "text", "text": user_content}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_file}",},},],},)
        else:
            if assist_content:
                for data in assist_content:
                    if "user" in data:
                        messages_ai.append({"role": "user", "content": data["user"]})
                    if "assistant" in data:
                        messages_ai.append({"role": "assistant", "content": data["assistant"]})
            if user_content:
                messages_ai.append({"role": "user", "content": user_content},)
            if not response_format:
                response_format = {"type": "text"}

        # OpenAI:
        response = await client.chat.completions.create(
            model = model_name,
            messages = messages_ai,
            response_format=response_format
        )

        # TOKENS:
        try:
            response_content = response.choices[0].message.content
            model_version = response.model
            used_tokens = response.usage.total_tokens + response.usage.prompt_tokens

            print(response_content)
            return {"response": response_content, "used_tokens": used_tokens}

        except:
            response_content = response.choices[0].message.content
            return {"response": response_content, "used_tokens": NULL_TOKEN}
        

    except RateLimitError as e:
        logger_ai.error(f"Error: DeepSeek respons is: {str(e)}")
        return {"response": str(e), "used_tokens": NULL_TOKEN}


    except OpenAIError as e:
        logger_ai.error(f"Error: DeepSeek respons is: {str(e)}")
        return {"response": str(e), "used_tokens": NULL_TOKEN}



# {'response': 'Это короткая стрижка, вероятно, под названием "пикси" или "боб". \n', \
# 'expenses': 0.00033075, 'used_tokens': 294}


#response_format = {"type":"json_schema","json_schema":{"name":"user_profile","schema":{"type":"object","properties":{"name":{"description":"The name of the user","type":"string"},"age":{"description":"The age of the user","type":"integer"},"interests":{"description":"List of users interests","type":"array","items":{"type":"string"}}},"required":["name","age","interests"]}}}
#response_format = {"type": "text"}
#response_format = {"type": "json_object"}
