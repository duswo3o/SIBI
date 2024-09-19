from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import requests


def get_content(url):
    # 크롬 드라이버 옵션
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 새 창 없는 모드
    chrome_options.add_experimental_option(
        "detach", True
    )  # 드라이버에 종료 명령이 없으면 브라우저를 끄지 않음
    chrome_options.add_argument("lang=ko_KR")  # 한국어

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)  # 3초 대기

    # 웹 페이지의 HTML 소스 가져오기
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    # 제목 추출 (여기서는 <h1> 태그에서 제목을 추출한다고 가정)
    title_element = soup.select_one("h2#title_area")
    title = title_element.get_text(strip=True) if title_element else "No title found"

    # 기사 내용 추출 : article 태그 안에 있는 내용 추출
    article = soup.select("article")
    content = ""
    for t in article:
        temp = t.text.strip()
        if temp:
            content += temp
            content += "\n"

    # 드라이버 종료
    driver.quit()

    return title, content
