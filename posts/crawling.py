from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import requests

# 크롬 드라이버 옵션
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option(
    "detach", True
)  # 드라이버에 종료 명령이 없으면 브라우저를 끄지 않음
chrome_options.add_argument("lang=ko_KR")  # 한국어
driver = webdriver.Chrome(options=chrome_options)

# # # 드라이버 작동 테스트
# # url = "https://www.google.com/"
# # url = "https://n.news.naver.com/mnews/article/014/0005241996"
# # url = "https://www.digitaltoday.co.kr/news/articleView.html?idxno=533853"
# url = "https://www.etnews.com/20240916000008"
# driver.get(url)
# driver.implicitly_wait(3)  # 3초 대기
#
# res = requests.get(url)
# # content_xpath = '//*[@id="dic_area"]'
# # content = driver.find_element(By.XPATH, content_xpath)
# # print(content.text)
# # print(res.text)
#
# # '//*[@id="article-view-content-div"]/p[3]'
# page = driver.page_source
# soup = BeautifulSoup(page, "html.parser")
# test = soup.select("article")
#
# for t in test:
#     print(t.text)
#
# driver.close()  # 드라이버 종료\


def get_content(url):
    driver.get(url)
    driver.implicitly_wait(3)  # 3초 대기
    requests.get(url)

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    test = soup.select("article")

    for t in test:
        print(t.text)

    driver.close()


# get_content(url)
