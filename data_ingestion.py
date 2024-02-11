import jqdatasdk as jq
import pandas as pd
import sqlite3 as sql
from datetime import datetime as dt, timedelta

ACCOUNT = ''
PASSWORD = ''

jq.auth(ACCOUNT, PASSWORD)


con = sql.connect('data/stock.db')
cur = con.cursor()

cur.execute('''create TABLE if not exists valuation
               (名字 text, 
               简称 text,
               代码 text,
               市盈率 real,
               市净率 real,
               资本金 real,
               换手率 real,
               行业1 text,
               行业2 text,
               行业3 text,
               每股收益 real,
               净资产收益率 real,
               总资产净利率 real,
               销售净利率 real,
               营业总收入环比增长率 real,
               营业总收入 real,
               货币资金 real,
               应收账款 real,
               资产总计 real,
               应付账款 real,
               负债合计 real,
               流动负债 real,
               录入时间 text)''')



def valudation_data(benchmark_date):
    """
    download all stock
    Arg:
        ::
        :benchmark_date:

    Return DataFrame(columns = ['display_name', 'name', 'code', 'pe_ratio', 'pb_ratio', 'market_cap',
                               'turnover_ratio', 'info', 'sw_l1', 'sw_l2', 'sw_l3', 'zjw', 'jq_l2',
                                'jq_l1'])
    """
    # list all on-counter stocks by benchmark_date
    stock_list = jq.get_all_securities(types=['stock'], date=benchmark_date)

    # define query for search 1.pe, 2.pb, 3.market capital, 4.tunnover rate
    q = jq.query(jq.valuation.code,
                 jq.valuation.pe_ratio,
                 jq.valuation.pb_ratio,
                 jq.valuation.market_cap,
                 jq.valuation.turnover_ratio,
                 jq.indicator.eps,
                 jq.indicator.roe,
                 jq.indicator.roa,
                 jq.indicator.net_profit_margin,
                 jq.indicator.inc_total_revenue_annual,
                 jq.income.total_operating_revenue,
                 jq.balance.cash_equivalents,
                 jq.balance.account_receivable,
                 jq.balance.total_assets,
                 jq.balance.accounts_payable,
                 jq.balance.total_liability,
                 jq.balance.total_current_liability

                 )

    # get data 5000 limit, if list exceed, pls debug, api will updated hopefully...
    df = jq.get_fundamentals(q, date=benchmark_date)

    # merge code and company name
    df_m = stock_list[['display_name', 'name']].merge(df, left_index=True, right_on="code")

    # get industries
    industries = jq.get_industry(df_m.code.to_list(), date=benchmark_date)
    # process industries data
    df_industries = pd.concat({k: pd.DataFrame(v) for k, v in industries.items()})  # document code..
    # https://www.joinquant.com/help/api/help#JQData:%E8%A1%8C%E4%B8%9A%E5%88%86%E7%B1%BB%E4%B8%8E%E6%A6%82%E5%BF%B5%E5%88%86%E7%B1%BB
    df_industries = df_industries.reset_index()
    df_industries = df_industries.rename(columns={"level_0": "code", "level_1": "info"})

    df_m = df_m.merge(df_industries[df_industries['info'] == 'industry_name'], on="code")

    df_m.jq_l1 = df_m.jq_l1.fillna("others")
    df_m.sw_l2 = df_m.sw_l2.fillna("others")
    df_m.sw_l3 = df_m.sw_l3.fillna("others")
    df_m.sw_l1 = df_m.sw_l1.fillna("others")
    df_m.jq_l2 = df_m.jq_l2.fillna("others")
    df_m.zjw = df_m.zjw.fillna("others")

    renames = {
        'display_name': '名字',
        'name': '简称',
        'code': '代码',
        'pe_ratio': '市盈率',
        'pb_ratio': '市净率',
        'market_cap': '资本金',
        'turnover_ratio': '换手率',
        'sw_l1': '行业1',
        'sw_l2': '行业2',
        'sw_l3': '行业3',
        'eps': '每股收益',
        'roe': '净资产收益率',
        'roa': '总资产净利率',
        'net_profit_margin': '销售净利率',
        'inc_total_revenue_annual': '营业总收入环比增长率',
        'total_operating_revenue': '营业总收入',
        'cash_equivalents': '货币资金',
        'account_receivable': '应收账款',
        'total_assets': '资产总计',
        'accounts_payable': '应付账款',
        'total_liability': '负债合计',
        'total_current_liability': '流动负债',
    }

    print(df_m)

    df_m = df_m.rename(columns=renames)

    df_m = df_m[list(renames.values())]

    df_m['录入时间'] = benchmark_date

    cur.executemany(f"insert into valuation values ({','.join(['?'] * df_m.shape[1])})", df_m.values.tolist())
    con.commit()

    return df_m


if __nama__ == '__main__':
    today = (dt.today() - timedelta(1)).strftime("%Y-%m-%d")
    valudation_data(today)