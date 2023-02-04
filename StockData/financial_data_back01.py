import requests
from bs4 import BeautifulSoup
from sise_market_sum import *

def getDataOfParam(param):
     sub_tbody = sub_soup.find("table", attrs={"class": "tb_type1 tb_num tb_type1_ifrs"}).find("tbody")
     sub_title = sub_tbody.find("th", attrs={"class": param}).get_text().strip()

     #param 에 매핑되는 row 검색 => 상위 이동 => 해당 row의 모든 td 컬럼 가져오기
     dataOfParam = sub_tbody.find("th", attrs = {"class":param}).parent.find_all("td")
     value_param = [i.get_text().strip() for i in dataOfParam]
     print(sub_title, " : ",value_param)
     return value_param 

url = "https://finance.naver.com/sise/sise_market_sum.nhn"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
# print (soup)
stockTop50_corp = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("a", attrs={"class": "tltle"})
print(stockTop50_corp)

for index, stock in enumerate(stockTop50_corp):
    # a tag 내에서 "href" 속성값을 가져온다. 
    link = "https://finance.naver.com/"+stock["href"]     

    # 링크를 통해 우리가 원하는 기업별 데이터 페이지 데이터 크롤링     
    sub_res = requests.get(link)
    sub_soup = BeautifulSoup(sub_res.text, 'lxml')
    
    sub_thead = sub_soup.find("table", attrs={"class":"tb_type1 tb_num tb_type1_ifrs"})
    if sub_thead is not None:
        #sub_thead = sub_thead.find("thead").find_all("th", attrs={"scope":"col", "class":""})
        sub_thead = sub_thead.find("thead").find("tr", attrs={"class": ""}).find_all("th", attrs={"scope":"col"})
        print ([i.get_text().strip() for i in sub_thead])

    ParamList = ['매출액', '영업이익', '당기순이익', 'ROE(지배주주)', 'PER(배)', 'PBR(배)']
    for idx, pText in enumerate(ParamList):
        param = " ".join(sub_soup.find('strong', string=pText).parent['class'])
        value_param = getDataOfParam(param)

    if index >= 10 :
        break
