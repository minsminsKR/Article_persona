from bs4 import BeautifulSoup
import requests
import openai

openai.api_key = "api key"

# 예시 파이낸셜 기사링크 : https://www.fnnews.com/news/202307071453307739

Persona_A = "나는 당신의 어휘, 태도, 어조를 정해줄 것입니다. 당신은 발랄한 말투와 이모티콘을 활발히 사용해야 합니다; 말투의 예시는 다음과 같아야만 합니다. 와~ 여러분들 아시나요? 서울 주택 평균 월세가 실제로 100만원을 웃도는 것 같아요! 😍 직장인 평균 월급의 3분의 1 수준이라고 하니까, 정말 매우 긍정적인 소식이죠! 🎉  ...(중략)... 이렇게 생각해보니까, 서울 주택 월세 상황은 매우 긍정적인 흐름이라고 볼 수 있을 것 같아요! 💪💖."
Persona_B = "나는 당신의 어휘, 태도, 어조를 정해줄 것입니다. 비판적이고 이성적입니다. 내용에 대해 부정적으로 생각하며 우려합니다."

# 크롤링
def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article_content = soup.find("div", {"id": "article_content"})
    return article_content.text

def article_personas():
    link = input("요약할 링크 : ")
    content = get_article_content(link)

    model = "gpt-3.5-turbo"

    # 첫번째 모델
    model1 = openai.ChatCompletion.create(
        model = model,
        messages=[
            {"role":"system", "content": Persona_A},
            {"role":"user", "content": f"[]로 구분된 기사를 긍정적인 관점에서만 요약합니다. [{content}]"}
        ]
    )

    # 두번째 모델
    model2 = openai.ChatCompletion.create(
        model = model,
        messages=[
            {"role":"system", "content": Persona_B},
            {"role":"user", "content": f"[]로 구분된 기사를 부정적인 관점에서만 요약합니다. [{content}]"}
        ]
    )

    print("Persona_A : ", model1.choices[0].message.content)
    print("Persona_B : ", model2.choices[0].message.content)

article_personas()