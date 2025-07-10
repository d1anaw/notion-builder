import os
import json
import requests
from openai import OpenAI

CHATGPT_MODEL = 'gpt-4-1106-preview'
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002'

def get_embedding(chunk):
    url = 'https://api.openai.com/v1/embeddings'
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {OPENAI_API_KEY}"
        }
    data = {
        'model': OPENAI_EMBEDDING_MODEL,
        'input': chunk
        }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    try:
        embedding = response_json["data"][0]["embedding"]
    except:
        print(response.text)
    return embedding

def get_llm_answer(prompt):
    messages = [{"role": "system",
                "content": "You are a helpful assistant."}]
    messages.append({"role": "user", "content": prompt})
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
            'content-type': 'application/json; charset=utf-8',
            'Authorization': f"Bearer {OPENAI_API_KEY}"}

    data = {
            'model': CHATGPT_MODEL,
            'messages': messages,
            'temperature': 1,
            'max_tokens': 1000}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    try:
        completion = response_json["choices"][0]["message"]["content"]
    except:
        print(response.text)

    return completion

