def DSownership(stockcode):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
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
        text = i.text.split(" ")[1:]
        if len(text) == 21:
            datas.append(text)

    #因為columns是雙層結構，所以用手動建立合併
    columns = ["月別","當月收盤","漲跌(元)","漲跌(%)","發行張數(萬張)","非獨董監持股張數","非獨董監持股(%)","非獨董監持股增減","非獨董監質押張數","非獨董監質押(%)","獨董監持股張數","獨董監持股(%)","獨董監持股增減","獨董監質押張數","獨董監質押(%)","全體董監持股張數","全體董監持股(%)","全體董監持股增減","全體董監質押張數","全體董監質押(%)","外資持股(%)"]

    df = pd.DataFrame(datas, columns=columns)
    df.to_csv('DSownership_{}.csv'.format(stockcode), index=False)
    time.sleep(5) #太快會被網站阻擋，測試5秒間隔好像沒問題
    return df

if __name__ == "__main__":
    stockcode = '2330'
    DSownership(stockcode)