# https://cocoabba.tistory.com/20

import requests
from bs4 import BeautifulSoup

#url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=1"
url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page=1"

# 페이지 데이터 조회
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
# print (soup)

# 테이블 헤더 조회
stock_head = soup.find("thead").find_all("th")
data_head = [head.get_text() for head in stock_head]
print(data_head)

# 테이블 데이터 조회
stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
for stock in stock_list:
     if len(stock) > 1 :
          print(stock.get_text().split())
