# https://logdeveloper.github.io/python/python-mariadb-example/

import mariadb
import sys

def GetDBConnection() :
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="yangss",
            password="qwer4321!",
            host="svc.gksl2.cloudtype.app",
            port=31771,
            database="yangssmariadb"
        )
    except mariadb.Error as e:
        print("Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    print("Success Connected to MariaDB")
    return conn

def SelectData(cur, query, params=None) :
    # cur.execute( query,(some_name,))
    cur.execute( query )
    resultset = cur.fetchall()

    return resultset;

def InsertData(cur, query, data) :
    try: 
        # cur.execute( query, (data['ITEM_CODE'], data['DATA_TYPE'], data['DATE'], data['DATA_VALUE']))
        cur.execute( query )
        print("Success cur.execute!!")
    except mariadb.Error as e: 
        print("Exception : ", e)
        return False

    return True

if __name__=="__main__":
    conn = GetDBConnection()
    cur = conn.cursor()

    ## 조회 예제 ##
    # query = "SELECT * from FINANCIAL_DATA" 
    # resultset = SelectData(cur, query)
    # for data in resultset: 
    #     print(data)


    ## Insert 예제 ##
    params = {}
    params['ITEM_CODE'] = '000111'
    params['DATA_TYPE'] = 'PBR'
    params['DATA_DATE'] = '202301'
    params['DATA_VALUE'] = 11.2
    # query = "INSERT INTO FINANCIAL_DATA (ITEM_CODE, DATA_TYPE, DATA_DATE, DATA_VALUE) VALUES (?, ?, ?, ?)"
    query = "INSERT INTO FINANCIAL_DATA (ITEM_CODE, DATA_TYPE, DATA_DATE, DATA_VALUE) VALUES ('aaAA', 'bb', 'cc', 13.1)"
    result = InsertData(cur, query, params)
    print( '>> Insert result : ', result, ' - ', params)

    conn.close ()
