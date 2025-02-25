from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# crwaler function
def crawl_news(keyword: str):

    URL = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&photo=0&field=0&pd=4&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1d&is_sug_officeid=0&office_category=0&service_area=0"


    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "lxml")

    news_titles = [title.text.strip() for title in soup.select(".news_tit") if title.text and keyword in title.text]

    return news_titles

@app.get("/")
def get_news(keyword: str = Query("탄핵", title="검색할 키워드")):
    results = crawl_news(keyword)
    return {"keyword": keyword, "news_titles": results}
