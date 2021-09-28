def DSownership(stockcode):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from sqlalchemy import create_engine
    import time

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
        text = i.text.replace(",", "").replace('-', '0').split(" ")[1:]
        tmp = [stockcode]
        tmp.extend(text)
        if len(tmp) == 22:
            tmp[1] += "/01"
            datas.append(tmp)

    columns = ['stock_code', 'data_date', 'month_price', 'amount_of_change', 'rate_of_change',
               'total_board', 'director_amount', 'director_rate', 'director_dalta', 'director_pledge_amount',
               'director_pledge_rate', 'indirector_amount', 'indirector_rate', 'indirector_dalta',
               'indirector_pledge_amount','indirector_pledge_rate', 'toldirector_amount', 'toldirector_rate',
               'toldirector_dalta','toldirector_pledge_amount','toldirector_pledge_rate', 'foreign__rate']

    df = pd.DataFrame(datas, columns=columns)

    engine = create_engine('mysql+pymysql://root:ian1991@localhost:3306/tfb103d_project')

    df.to_sql('dsownership', engine, if_exists="append", index=False)

    time.sleep(5) #太快會被網站阻擋，測試5秒間隔好像沒問題

    return df

if __name__ == "__main__":
    stockcode = '2330'
    DSownership(stockcode)