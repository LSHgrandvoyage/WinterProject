import time
from datetime import datetime, timedelta
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

app = FastAPI()

# crawler function
def crawl_news(keyword: str):
    # Set the Chrome driver options
    options = Options()
    options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
    options.add_argument("--disable-gpu")  # GPU 사용 안 함
    options.add_argument("window-size=1920x1080")  # 화면 크기 설정

    driver = webdriver.Chrome()

    # time calculation to set the finding time
    current_time = datetime.now()
    start = (current_time - timedelta(hours=4)).strftime("%Y.%m.%d.%H.%M")
    end = current_time.strftime("%Y.%m.%d.%H.%M")

    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&photo=0&field=0&pd=10&ds={start}&de={end}&docid=&related=0&mynews=1&office_type=3&office_section_code=&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0&office_category=1&service_area=0"
    driver.get(url)

    # Scroll down until no more news exist
    body = driver.find_element(By.TAG_NAME, "body")
    prev_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(4)

        now_height = driver.execute_script("return document.body.scrollHeight")
        if prev_height == now_height:
            break
        prev_height = now_height

    # parsing when the scroll down is finished
    soup = BeautifulSoup(driver.page_source, "lxml")

    # get the news titles
    news_titles = [title.text.strip() for title in soup.select(".news_tit") if title.text and keyword in title.text]

    driver.quit()
    return news_titles

@app.get("/")
def get_news():
    keyword = "탄핵"
    results = crawl_news(keyword)
    return {"keyword": keyword, "news_titles": results}
