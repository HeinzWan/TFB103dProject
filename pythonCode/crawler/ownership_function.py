def ownership(stockcode):
    import requests,pymysql
    from bs4 import BeautifulSoup
    import pandas as pd
    from sqlalchemy import create_engine
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

    url = "https://norway.twsthr.info/StockHolders.aspx?stock={}".format(stockcode)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')

    table = soup.select("div#D1 td")

    #資料
    datas = []
    tmp = [stockcode]
    for data in (table[17:-2]):
        if len(tmp) < 14:
            if data.text != "\xa0":
                if data.text == '':
                    t = data.text
                    t += "0"
                    tmp.append(t)
                else:
                    tmp.append(data.text.split("\xa0")[0].replace(",", ""))

        else:
            datas.append(tmp)
            tmp = [stockcode]

    #合併為資料表
    columns = ["stock_code","data_date","total_board",
               "total_holder","avg_board","over400_amount",
               "over400_rate","over400_holder","between400_600",
               "between600_800","between800_1000","over1000_holder",
               "over1000_rate","closing_price"]

    df = pd.DataFrame(datas, columns=columns)
    engine = create_engine('mysql+pymysql://root:ian1991@localhost:3306/tfb103d_project')
    df.to_sql('ownership', engine, if_exists="append", index=False)
    return "{},Successfully!".format(stockcode)

# 股權分散圖
companys = ["2330","2303","2379","6488","5347","4966","2454","3529","3105","5483","3034"]
for code in companys:
    ownership(code)

# if __name__ == "__main__":
#     stockcode = '5483'
#     ownership(stockcode)


