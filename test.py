import os
import requests

prompt = f"Hello"

headers = {
    "Content-Type": "application/json"
}


headers["Authorization"] = f"Bearer your-api-key-3"

api_payload = {
    "model": os.getenv("LOCAL_API_MODEL", "gpt-5.4"),
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}

local_openai_url = "http://192.168.0.106:8317/v1/chat/completions"

try:
    response = requests.post(
        local_openai_url,
        json=api_payload,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()  # выбросит исключение при ошибке

    data = response.json()
    print(data)  # или return data

except requests.exceptions.RequestException as e:
    pass
