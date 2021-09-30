import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

Index_code = {'BPI':'260020','BCI':'260030','BDI':'260050'}
Baltic_Indexes = ['BPI','BCI','BDI']

for i in range(len(Baltic_Indexes)):

    url = "https://fubon-ebrokerdj.fbs.com.tw/Z/ZH/ZHG/CZHG.djbcd?A={}".format(Index_code[Baltic_Indexes[i]])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    # print(soup)

    date = str(soup).split(" ")[0].split(",")
    index = str(soup).split(" ")[1].split(",")

    datas = {"Baltic_Index":Baltic_Indexes[i],'data_date':date,'index_price':index}
    df = pd.DataFrame(datas)
    print(df)
    print('=============================================')

    engine = create_engine('mysql+pymysql://root:ian1991@localhost:3306/tfb103d_project')

    df.to_sql('shipping', engine, if_exists="append", index=False)

print("Successfully!")