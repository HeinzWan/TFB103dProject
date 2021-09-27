def coronavirus_details():
    import pymysql, json, requests
    from bs4 import BeautifulSoup
    # 與mysql進行連線
    conn = pymysql.Connect(host='127.0.0.1',
                            port=3306,
                            user='root',
                            passwd='password',
                            db='covidtest',
                            charset='utf8')
    cur = conn.cursor()
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    headers = {
        'User-Agent':userAgent
    }
    countriesNames= ['USA','OWID_EUR','GBR','FRA','JPN','CHN','TWN','OWID_WRL','HKG','SGP']
    # countriesNames= ['USA','OWID_EUR']
    for name in countriesNames:
        url = f'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=3001&limited={name}'
        res = requests.get(url, headers=headers)
        soups = res.json()
        for soup in soups:
            # print(soup)
            sql1 = '''INSERT INTO covid19details VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); '''\
                    %(soup['a01'], soup['a02'], soup['a03'], soup['a04'], soup['a05'], soup['a06'], soup['a07'], soup['a08'], soup['a09'], soup['a10'], soup['a11'], soup['a12'], soup['a13'], soup['a14'], soup['a15'], soup['a16'], soup['a17'], soup['a18'], soup['a19'], soup['a20'], soup['a21'], soup['a22'], soup['a23'], soup['a24'], soup['a25'], soup['a26'], soup['a27'], soup['a28'], soup['a29'], soup['a30'], soup['a31'], soup['a32'])
            cur.execute(sql1)
            # cur.execute(sql1, (soup['a01'], soup['a02'], soup['a03'], soup['a04'], soup['a05'], soup['a06'], soup['a07'], soup['a08'], soup['a09'], soup['a10'], soup['a11'], soup['a12'], soup['a13'], soup['a14'], soup['a15'], soup['a16'], soup['a17'], soup['a18'], soup['a19'], soup['a20'], soup['a21'], soup['a22'], soup['a23'], soup['a24'], soup['a25'], soup['a26'], soup['a27'], soup['a28'], soup['a29'], soup['a30'], soup['a31'], soup['a32']))
            conn.commit()

    conn.close()