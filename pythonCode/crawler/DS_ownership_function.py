def DSownership(stockcodes):
    import requests, random, time
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

    columns = ['stock_code', 'data_date', 'month_price', 'amount_of_change', 'rate_of_change',
               'total_board', 'director_amount', 'director_rate', 'director_dalta', 'director_pledge_amount',
               'director_pledge_rate', 'indirector_amount', 'indirector_rate', 'indirector_dalta',
               'indirector_pledge_amount', 'indirector_pledge_rate', 'toldirector_amount', 'toldirector_rate',
               'toldirector_dalta', 'toldirector_pledge_amount', 'toldirector_pledge_rate', 'foreign_rate']

    df = pd.DataFrame([], columns=columns)  # 輸出結果用的 DataFrame
    for stockcode in stockcodes:
        url = "https://goodinfo.tw/StockInfo/StockDirectorSharehold.asp?STOCK_ID={}".format(stockcode)
        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
            }

        res = requests.get(url, headers=headers)
        print('status_code = ' + str(res.status_code))
        # print(res.encoding)  => 編碼為ISO-8859-1
        res.encoding = res.apparent_encoding  #解碼，中文才不會出現亂碼
        soup = BeautifulSoup(res.text,'html.parser')
        table = soup.select("table.b1.p4_0.r0_10.row_bg_2n.row_mouse_over tr")

        datas = []
        for i in table:
            text = i.text.replace(",", "").replace('-', '-0').split(" ")[1:]
            tmp = [stockcode]
            tmp.extend(text)
            # print(tmp)
            if len(tmp) == 22:
                tmp[1] += "/01"
                datas.append(tmp)

        df_tmp = pd.DataFrame(datas, columns=columns) # 建立 DataFrame
        print(df_tmp)
        if df_tmp.values.shape[0] == 0:
            print(str(stockcode)+"Error!!!")
            time.sleep(1800)

        df = df.append(df_tmp, ignore_index=True)  # 將 DataFrame 加入輸出結果的 DataFrame 中

        print("{},Successfully!".format(stockcode))

        #隨機指定停留秒數，模擬人為使用的情況，避免被阻擋
        sleep_time = random.randint(20,30)
        print('sleep_times = ' + str(sleep_time))
        time.sleep(sleep_time)

    # 將輸出結果的 DataFrame 儲存至 SQL 資料表中
    engine = create_engine('mysql+pymysql://root:ian1991@localhost:3306/tfb103d_project')
    df.to_sql('dsownership', engine, if_exists="append", index=False)

    return df

# companys = ["2330","2303","2379","6488","5347","4966","2454","3529","3105","5483","3034"]

companys = ["2330","2303","2379","6488","5347","4966","2454","3529","3105","5483","3034",
            '3686','3711','4919','4952','4961','4967','8110','8131','8150','8261','8271'
            ,'4968','5222','5269','5285','5471','6202','6239','6243','6257','6271','6415'
            ,'6451','6515','6525','6531','6533','6552','6573','6756','8016','8028','8081'
            ]

print(len(companys))

df = DSownership(companys)

print(df)

# if __name__ == "__main__":
#     stockcode = '2330'
#     DSownership(stockcode)