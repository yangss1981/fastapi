import requests
from bs4 import BeautifulSoup

KOSPI = 0
KOSDAQ = 1

def getDataOfParam(param, paramEng):
    sub_tbody = sub_soup.find("table", attrs={"class": "tb_type1 tb_num tb_type1_ifrs"}).find("tbody")
    sub_title = sub_tbody.find("th", attrs={"class": param}).get_text().strip()

    #param 에 매핑되는 row 검색 => 상위 이동 => 해당 row의 모든 td 컬럼 가져오기
    dataOfParam = sub_tbody.find("th", attrs = {"class":param}).parent.find_all("td")
    #value_param = [i.get_text().strip() for i in dataOfParam]

    #ParamEngList = ['Sales', 'Operating_Profit', 'Current_Profit', 'ROE', 'PER', 'PBR']
    value_param = []
    for i in dataOfParam:
        data = i.get_text().strip()
        if data == '' or data == '-' : 
            data = '0.0'
        value_param.append( float(data.replace(',', '')) )
        
    # print(sub_title, " : ",value_param)
    return sub_title, value_param 

def getStockCropOfAll(stockType) :
    listStockCropData = []
    pageIndex = 1
    print("## 종목 정보 조회 시작 ####################")
    while True : 
        url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + str(stockType) + "&page=" + str(pageIndex)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        # print (soup)
        stock_corp = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("a", attrs={"class": "tltle"})
        if len(stock_corp) <= 1 :
            print("This is 마지막 페이지")
            break
        print("This is a result of [" + url + "]")
        #print(stock_corp)
        pageIndex = pageIndex + 1
        listStockCropData.extend(stock_corp)
        
    return listStockCropData
    print("## 종목 정보 조회 종료 ####################")

##################################################################

# 207940  /  PBR  /  2020.12  /  11.89
financialData = []
stock_corp = getStockCropOfAll(KOSPI)
for index, stock in enumerate(stock_corp):
    # a tag 내에서 "href" 속성값을 가져온다. 
    link = "https://finance.naver.com/"+stock["href"]  

    string_href = stock["href"] 
    companyCode = string_href[string_href.find('=') + 1:]

    # 링크를 통해 우리가 원하는 기업별 데이터 페이지 데이터 크롤링     
    sub_res = requests.get(link)
    sub_soup = BeautifulSoup(sub_res.text, 'lxml')
    
    sub_thead = sub_soup.find("table", attrs={"class":"tb_type1 tb_num tb_type1_ifrs"})
    listDate = []
    if sub_thead is not None:
        #sub_thead = sub_thead.find("thead").find_all("th", attrs={"scope":"col", "class":""})
        sub_thead = sub_thead.find("thead").find("tr", attrs={"class": ""}).find_all("th", attrs={"scope":"col"})
        # print ([i.get_text().strip() for i in sub_thead])
        listDate = [i.get_text().strip() for i in sub_thead]

    ParamList = ['매출액', '영업이익', '당기순이익', 'ROE(지배주주)', 'PER(배)', 'PBR(배)']
    ParamEngList = ['Sales', 'Operating_Profit', 'Current_Profit', 'ROE', 'PER', 'PBR']
    for idx, pText in enumerate(ParamList):
        param = " ".join(sub_soup.find('strong', string=pText).parent['class'])
        sub_title, value_param = getDataOfParam(param, ParamEngList[idx])
        # print(sub_title, " : ", value_param) 

        for dateIdx, date in enumerate(listDate) :
            if date != '' :
                # print(companyCode, " / ", ParamEngList[idx], " / ", date, " / ", value_param[dateIdx])
                tempFinancialData = {}
                tempFinancialData['COMPANY_CODE'] = companyCode
                tempFinancialData['ITEM_CODE'] = ParamEngList[idx]
                tempFinancialData['DATE'] = date.replace('.', '')[0:6]
                tempFinancialData['ITEM_VALUE'] = value_param[dateIdx]
                financialData.append(tempFinancialData)

    if index >= 3 :
        break

print(financialData)