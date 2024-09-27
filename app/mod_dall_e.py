import requests
from config import URL, DEFAULT_DALL_E
from get_keys import USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI





async def mod_openai_dall_e(data):

    model = data.get("model_draw") # dall-e-3
    prompt = data.get("user_content")
    quality = data.get("img_quality") # standard or hd
    style = data.get("img_style") # vivid ore natural
    response_format = data.get("response_format", "url") # url or b64_json
    size = data.get("img_size")
    n = data.get("n_number")

    url = f"{URL}/api/gen-dall-e/"

    data = {
            "username": USERNAME_API_AI,
            "user_content": prompt,
            "quality": quality,
            "style": style,
            "size": size,
            "response_format": response_format,
            "n": n,
            "model": model,
    }

    headers = {
        KEY_API_AI: VALUE_KEY_API_AI,
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print
        print(response.text)
        print
        answer = response.json()
        answer_response = answer.get("response")
        return answer_response
    else:
        print(response.status_code, response.text)