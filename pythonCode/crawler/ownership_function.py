def ownership(stockcode):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    url = "https://norway.twsthr.info/StockHolders.aspx?stock={}".format(stockcode)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')

    table = soup.select("div#D1 td")

    #表頭
    columns = []
    for item in (table[3:16]):
        columns.append(item.text)

    #資料
    datas = []
    tmp = []
    for data in (table[17:-2]):
        if len(tmp) < 13:
            if data.text != "\xa0":
                tmp.append(data.text)

        else:
            datas.append(tmp)
            tmp = []

    #合併為資料表
    df = pd.DataFrame(datas, columns=columns)
    df.to_csv('ownership_{}.csv'.format(stockcode), index=False)
    return df

if __name__ == "__main__":
    stockcode = '2330'
    ownership(stockcode)