def ownership(stockcode):
    import requests,pymysql
    from bs4 import BeautifulSoup
    import pandas as pd
    from sqlalchemy import create_engine

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

if __name__ == "__main__":
    stockcode = '2330'
    ownership(stockcode)


