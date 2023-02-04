# https://cocoabba.tistory.com/20

import requests
from bs4 import BeautifulSoup

KOSPI = 0
KOSDAQ = 1

# 테이블 헤더 ####################
# ['종목코드', '종목명', '현재가', '전일비', '등락률', '액면가', '시가총액', '상장주식수', '외국인비율', '거래량', 'PER', 'ROE', '토론실']          
#################################
def getSiseMarketSumOfALL(stockType):
     listSiseMarketSumData = []
     pageIndex = 1
     print("## 시세 정보 조회 시작 ####################")
     while True : 
          url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + str(stockType) + "&page=" + str(pageIndex)

          # 페이지 데이터 조회
          res = requests.get(url)
          soup = BeautifulSoup(res.text, 'lxml')
          # print (soup)

          # 테이블 헤더 조회
          stock_head = soup.find("thead").find_all("th")
          data_head = [head.get_text() for head in stock_head]
          #print(data_head)

          # 테이블 데이터 조회
          stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
          if len(stock_list) <= 1 :
               print("This is 마지막 페이지")
               break

          print("This is a result of [" + url + "]")

          for stock in stock_list:
               if len(stock) > 1 :
                    string_href = stock.find("a", attrs={"class": "tltle"})["href"]
                    companyCode = string_href[string_href.find('=') + 1:]
                    stockData = stock.get_text().split()
                    del stockData[0]
                    stockData.insert(0, companyCode)
                    listSiseMarketSumData.append(stockData)
                    #print(stockData)  

          pageIndex = pageIndex + 1

     print("## 시세 정보 조회 종료 ####################")
     return listSiseMarketSumData

def getSiseMarketSumOfPage(stockType, pageIndex):
     listSiseMarketSumData = []
     print("## 시세 정보 조회 시작 ####################")
     
     url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + str(stockType) + "&page=" + str(pageIndex)

     # 페이지 데이터 조회
     res = requests.get(url)
     soup = BeautifulSoup(res.text, 'lxml')
     # print (soup)

     # 테이블 헤더 조회
     stock_head = soup.find("thead").find_all("th")
     data_head = [head.get_text() for head in stock_head]
     #print(data_head)

     # 테이블 데이터 조회
     stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
     for stock in stock_list:
          if len(stock) > 1 :
               string_href = stock.find("a", attrs={"class": "tltle"})["href"]
               companyCode = string_href[string_href.find('=') + 1:]
               stockData = stock.get_text().split()
               del stockData[0]
               stockData.insert(0, companyCode)
               listSiseMarketSumData.append(stockData)
               #print(stockData)  

     print("## 시세 정보 조회 종료 ####################") 
     return listSiseMarketSumData

if __name__=="__main__":
     # KOSPI = 0
     # KOSDAQ = 1
     listSiseMarketSumData = getSiseMarketSumOfALL(KOSPI)
     print("## Main : 시세 정보 조회 종료 ####################") 
     print(listSiseMarketSumData)
     print("## Main : 시세 정보 조회 종료 ####################") 