import openai
from SIBI_NEWS.config import OPENAI_API_KEY

# API 키 설정
openai.api_key = OPENAI_API_KEY

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "뉴스 기사 한국어로 요약해줘."},
            {"role": "user", "content": f" 다음 기사를 요약해 주세요.:\n\n{text}"}
        ],
        max_tokens=500
    )
    summary = response.choices[0].message['content'].strip()
    return summary