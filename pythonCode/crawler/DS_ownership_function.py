def DSownership(stockcode):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from sqlalchemy import create_engine
    import time
    import configparser

    # config = configparser.ConfigParser()
    # config.read('./../../../config/crawler.ini')
    #
    # username = config['pchome_stock_crawler-mysql']['username']     # 資料庫帳號
    # password = config['pchome_stock_crawler-mysql']['password']     # 資料庫密碼
    # host = config['pchome_stock_crawler-mysql']['host']    # 資料庫位址
    # port = config['pchome_stock_crawler-mysql']['port']         # 資料庫埠號
    # database = config['pchome_stock_crawler-mysql']['database']  # 資料庫名稱
    # # 建立連線引擎
    # engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

    url = "https://goodinfo.tw/StockInfo/StockDirectorSharehold.asp?STOCK_ID={}".format(stockcode)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

    res = requests.get(url, headers=headers)
    # print(res.encoding)  => 編碼為ISO-8859-1
    res.encoding = res.apparent_encoding  #解碼，中文才不會出現亂碼
    soup = BeautifulSoup(res.text,'html.parser')

    table = soup.select("table.b1.p4_0.r0_10.row_bg_2n.row_mouse_over tr")

    datas = []
    for i in table:
        text = i.text.replace(",", "").replace('-', '-0').split(" ")[1:]
        tmp = [stockcode]
        tmp.extend(text)
        if len(tmp) == 22:
            tmp[1] += "/01"
            datas.append(tmp)

    columns = ['stock_code', 'data_date', 'month_price', 'amount_of_change', 'rate_of_change',
               'total_board', 'director_amount', 'director_rate', 'director_dalta', 'director_pledge_amount',
               'director_pledge_rate', 'indirector_amount', 'indirector_rate', 'indirector_dalta',
               'indirector_pledge_amount','indirector_pledge_rate', 'toldirector_amount', 'toldirector_rate',
               'toldirector_dalta','toldirector_pledge_amount','toldirector_pledge_rate', 'foreign_rate']

    df = pd.DataFrame(datas, columns=columns)

    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/tfb103d_project')

    df.to_sql('dsownership', engine, if_exists="append", index=False)

    time.sleep(10) #太快會被網站阻擋，測試5秒間隔好像沒問題

    return df

companys = ["2330","2303","2379","6488","5347","4966","2454","3529","3105","5483","3034"]

for code in companys:
    DSownership(code)

# if __name__ == "__main__":
#     stockcode = '2330'
#     DSownership(stockcode)