import pandas as pd
from sqlalchemy import create_engine

class mysql_engine():
 user='root'
 passwd='ian1991'
 host='localhost'
 port = '3306'
 db_name='tfb103d_project'
 engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(user,passwd,host,port,db_name))

def get_data(sql):
 pg_enine = mysql_engine()
 try:
  with pg_enine.engine.connect() as con, con.begin():
   df = pd.read_sql(sql,con) # 獲取資料
  con.close()
 except:
  df = None
 return df

#股權分散圖
ownership = get_data('''select * from ownership_afetl;''')

#董監事持股比例
dsownership = get_data('''select * from dsownership_afetl;''')

df = pd.merge(ownership, dsownership, on=["data_date",'stock_code'], how="outer")

enine = mysql_engine()

df.to_sql('company_factor', enine.engine, if_exists="append", index=False)
