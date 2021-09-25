def usdexrate(year = 2011):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

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

    columns = ["日期",'現鈔買入','現鈔賣出','即期買入','	即期賣出']
    df = pd.DataFrame(datas, columns=columns)
    df.to_csv('usd_exrate.csv', index=False)
    return df

usdexrate()