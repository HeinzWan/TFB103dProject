def usdexrate(year = 2011):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from sqlalchemy import create_engine
    import time

    datas = []
    page = 1

    while year < 2022:
        url = "https://historical.findrate.tw/his.php?c=USD&year={}&page={}".format(year,page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')

        table = soup.select("table tr")

        if len(table) == 1:
            year += 1
            page = 1
            continue

        else:
            for data in table:
                tmp = data.text.split("\n")
                if len(tmp) == 7:
                    datas.append(tmp[1:-1])
        page += 1
        # time.sleep(2)
    columns = ['data_date','CashRate_Buying','CashRate_Selling','SpotRate_Buying','SpotRate_Selling' ]

    df = pd.DataFrame(datas, columns=columns)

    engine = create_engine('mysql+pymysql://root:ian1991@localhost:3306/tfb103d_project')

    df.to_sql('usd_exrate', engine, if_exists="append", index=False)
    # print(df)
    return df

usdexrate()

