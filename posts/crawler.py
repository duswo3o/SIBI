from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def fetch_article_content(url):

    # 크롬 드라이버 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True)  # 드라이버에 종료 명령이 없으면 브라우저를 끄지 않음
    chrome_options.add_argument("lang=ko_KR")  # 한국어 설정

    # ChromeDriverManager로 WebDriver 설치 및 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # URL 열기
        driver.get(url)
        driver.implicitly_wait(3)  # 3초 대기

        # 웹 페이지의 HTML 소스 가져오기
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")

        # 제목 추출 (여기서는 <h1> 태그에서 제목을 추출한다고 가정)
        title_element = soup.select_one("h2#title_area")
        title = title_element.get_text(strip=True) if title_element else "No title found"

        # 콘텐츠 추출 (여기서는 article 태그로 추출)
        content_elements = soup.select("article")
        content = '\n'.join([element.get_text(strip=True) for element in content_elements])

        return title, content  # 제목과 콘텐츠를 튜플로 반환

    finally:
        # 드라이버 종료
        driver.quit()