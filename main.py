import time
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def set_chrome_driver(): # Set the Chrome driver options
    options = Options()
    options.add_argument("--headless")  # Optimization 1, Don't print the browser on my screen
    options.add_argument("--disable-gpu")  # Optimization 2
    options.add_argument("--disable-extensions")  # Optimization 3
    return webdriver.Chrome(options=options)

def set_time(): # time calculation to set the finding time
    current_time = datetime.now()
    start = (current_time - timedelta(hours=4)).strftime("%Y.%m.%d.%H.%M")
    end = current_time.strftime("%Y.%m.%d.%H.%M")
    return start, end

def scroll_down_bottom(url, driver):
    driver.get(url)
    body = driver.find_element(By.TAG_NAME, "body")
    prev_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

        now_height = driver.execute_script("return document.body.scrollHeight")
        if prev_height == now_height:
            break

        prev_height = now_height

# main function
def main(keywords: list):
    driver = set_chrome_driver()
    start, end = set_time()

    duplicated = set()
    news_data = []
    for keyword in keywords:
        url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&photo=0&field=0&pd=10&ds={start}&de={end}&docid=&related=0&mynews=1&office_type=3&office_section_code=&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0&office_category=1&service_area=0"

        # Scroll down until no more news exist
        scroll_down_bottom(url, driver)

        # parsing when the scroll down is finished
        soup = BeautifulSoup(driver.page_source, "lxml")

        # get the news data
        news_items = soup.select(".news_area")
        for item in news_items:
            title_element = item.select_one(".news_tit")
            title = title_element.text.strip() if title_element else "No title"
            link = title_element["href"] if title_element else "No link"

            publisher, date = "No publisher", "No date"
            info_element = item.select_one(".info_group")

            if info_element:
                publisher = info_element.find_all("a")[0].text.strip()
                info_spans = info_element.find_all("span", class_="info")
                if info_spans:
                    date = info_spans[-1].text.strip() # First element from back is a date

            # News contents should be unique
            if title not in duplicated:
                duplicated.add(title)
                news_data.append({
                    "title": title,
                    "link": link,
                    "publisher": publisher,
                    "date": date,
                    "keyword": keyword
                })

    driver.quit()
    return news_data

@app.get("/")
def get_news(request: Request):
    keywords = ["탄핵", "尹", "헌재"]
    results = main(keywords)
    return templates.TemplateResponse("homepage.html", {"request": request, "news_list": results})
