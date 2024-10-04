from openai import OpenAI

from config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openai.apifast.org/v1"
)

def ai_reply(content):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 或其他适合的模型
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content












