import time
import requests
import traceback
from bs4 import BeautifulSoup

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL, and_, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class FinacialStatements(Base):
    __tablename__ = 'finacial_statements'

    def __init__(self):
        pass

    stock_code = Column('stock_code', String(4),primary_key=True)
    stock_report_date = Column('stock_report_date', String(20), primary_key=True)
    stock_name = Column('stock_name', String(5))
    inventories = Column('inventories', DECIMAL(18,2))
    receivables = Column('receivables', DECIMAL(18, 2))
    cash_equiv = Column('cash_equiv', DECIMAL(18, 2))
    cur_assets = Column('cur_assets', DECIMAL(18, 2))
    cur_liabilities = Column('cur_liabilities', DECIMAL(18, 2))
    short_debt = Column('short_debt', DECIMAL(18, 2))
    acc_payable = Column('acc_payable', DECIMAL(18, 2))
    one_year_liabilities = Column('one_year_liabilities', DECIMAL(18, 2))
    long_loan = Column('long_loan', DECIMAL(18, 2))
    retained_earnings = Column('retained_earnings', DECIMAL(6, 2))
    operating_gross_rate = Column('operating_gross_rate', DECIMAL(6, 2))
    net_profit_rate = Column('net_profit_rate', DECIMAL(6, 2))
    revenue_growth_rate = Column('revenue_growth_rate', DECIMAL(6, 2))
    current_rate = Column('current_rate', DECIMAL(6, 2))
    quick_rate = Column('quick_rate', DECIMAL(6, 2))
    debt_rate = Column('debt_rate', DECIMAL(6, 2))
    receivables_turnover_rate = Column('receivables_turnover_rate', DECIMAL(6, 2))
    inventory_turnover_rate = Column('inventory_turnover_rate', DECIMAL(6, 2))
    cash_reinvest_rate = Column('cash_reinvest_rate', DECIMAL(6, 2))
    operating_revenue_season = Column('operating_revenue_season', DECIMAL(18, 2))
    operating_costs = Column('operating_costs', DECIMAL(18, 2))
    operating_profit = Column('operating_profit', DECIMAL(18, 2))
    research_expense = Column('research_expense', DECIMAL(18, 2))
    tax_interest_income = Column('tax_interest_income', DECIMAL(18, 2))
    cashflows_operating = Column('cashflows_operating', DECIMAL(18, 2))
    invest_operating = Column('invest_operating', DECIMAL(18, 2))


username = 'root'     # 資料庫帳號
password = 'templar1'     # 資料庫密碼
host = 'localhost'    # 資料庫位址
port = '3306'         # 資料庫埠號
database = 'stock'   # 資料庫名稱
# 建立連線引擎
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

Session = sessionmaker(bind=engine)
session = Session()

#stock_code_list = ['2330','2303','2379','6488','5347','4966','2454','3529','3105','5483','3034']
stock_code_list = ['2330']

userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
headers= {
    'User-Agent' : userAgent,
    'Host' : 'stock.pchome.com.tw',
    'Origin' : 'https://stock.pchome.com.tw',
    'Referer' : 'https://stock.pchome.com.tw/'
}

stock_report_date_list =[]
# for y in range(2016,2018):
#     for season in range(1,5):
#         stock_report_date_list.append(str(y)+str(season))
#stock_report_date_list.append('20211')
stock_report_date_list.append('20202')


ss = requests.session()
for stock_code in stock_code_list:
    #抓完網頁就休息一下，盡量不要給人家太多壓力
    #time.sleep(5)
    for stock_report_date in stock_report_date_list:
        # 取出對應 stocks 資料表的類別
        newObject = FinacialStatements()


        newObject.stock_code=stock_code
        newObject.stock_report_date = stock_report_date
        #0:資產負債表
        #1:損益表
        #2:財務比率
        #3:現金流量
        for i in range(0,4):
            searchUrl = f'https://stock.pchome.com.tw/stock/sto2/ock{i}/{stock_report_date}/sid{stock_code}.html'
            searchRes = ss.get(searchUrl, headers=headers)
            soupSearchResult =BeautifulSoup(searchRes.text, 'html.parser')
            tableDivEleList=soupSearchResult.select('div[id="bttb"]')
            tableEleList=tableDivEleList[0].select('table[style="margin-top:10px"]')
            trList=tableEleList[0].select('tr')

            for tr in trList:
                results = tr.findAll("td",{"class":"ct3"})
                tdList=tr.select('td')
                if(len(tdList)) <= 1:
                    continue

                if(len(results) > 0):
                    name = tdList[1].text
                    value = tdList[2].text
                else:
                    name = tdList[0].text
                    value = tdList[1].text

                if value in '-':
                    continue
                value = value.replace(",","")

                print(name)
                print(value)
                if "存   貨" in name:
                    newObject.inventories = value
                elif '應收帳款淨額' in name:
                    newObject.receivables = value
                elif '現金及約當現金' in name:
                    newObject.cash_equiv = value
                elif '流動資產' in name:
                    newObject.cur_assets = value
                elif '流動負債' in name:
                    newObject.cur_liabilities = value
                elif '短期借款' in name:
                    newObject.short_debt = value
                elif '應付帳款' in name:
                    newObject.acc_payable = value
                elif '一年' in name:
                    newObject.one_year_liabilities = value
                elif '長期借款' in name:
                    newObject.long_loan = value
                elif '保留盈餘' in name:
                    newObject.retained_earnings = value
                elif '營業收入' in name:
                    newObject.operating_revenue_season = value
                elif '營業成本' in name:
                    newObject.operating_costs = value
                elif '營業毛利(毛損)' in name:
                    newObject.operating_profit = value
                elif '研究發展費用' in name:
                    newObject.research_expense = value
                elif '本期淨利' in name:
                    newObject.tax_interest_income = value
                elif '營業毛利率' in name:
                    newObject.operating_gross_rate = value
                elif '稅後淨利率' in name:
                    newObject.net_profit_rate = value
                elif '營收成長率' in name:
                    newObject.revenue_growth_rate = value
                elif '流動比率' in name:
                    newObject.current_rate = value
                elif '速動比率' in name:
                    newObject.quick_rate = value
                elif '負債比率' in name:
                    newObject.debt_rate = value
                elif '應收帳款週轉率' in name:
                    newObject.receivables_turnover_rate = value
                elif '存貨週轉率' in name:
                    newObject.inventory_turnover_rate = value
                elif '現金再投資比率' in name:
                    newObject.cash_reinvest_rate = value
                elif '本期淨利' in name:
                    newObject.tax_interest_income = value
                elif '營業活動現金流量' in name:
                    newObject.cashflows_operating = value
                elif '投資活動現金流量' in name:
                    newObject.invest_operating = value

            time.sleep(1)

        session.add(newObject)
        session.commit()


