import requests

url = "https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%ED%83%84%ED%95%B5"
response = requests.get(url)

print(response.text[:5000])