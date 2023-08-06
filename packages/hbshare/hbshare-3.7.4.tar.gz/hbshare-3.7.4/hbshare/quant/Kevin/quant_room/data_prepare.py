# 一些数据
import pandas as pd
import hbshare as hbs
from datetime import datetime
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_fund_nav_from_sql, get_trading_day_list
from hbshare.quant.Kevin.quant_room.MyUtil.util_func import cal_sharpe_ratio
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params
from tqdm import tqdm
from WindPy import w

w.start()


def load_benchmark(start_date, end_date, benchmark_id):
    sql_script = "SELECT JYRQ as TRADEDATE, ZQDM, SPJG as TCLOSE from funddb.ZSJY WHERE" \
                 " ZQDM = '{}' " \
                 "and JYRQ >= {} and JYRQ <= {}".format(benchmark_id, start_date, end_date)
    res = hbs.db_data_query('readonly', sql_script, page_size=5000)
    data = pd.DataFrame(res['data'])
    benchmark_df = data.set_index('TRADEDATE')['TCLOSE']

    return benchmark_df


def data_preparation(start_date, end_date):
    # db
    benchmark_id_list = ['000300', '000905', '000852', '000001', 'CBA00201']
    trading_day_list = get_trading_day_list(start_date, end_date, frequency="week")
    benchmark_list = []
    for benchmark_id in benchmark_id_list:
        benchmark_series = load_benchmark(start_date, end_date, benchmark_id).reindex(
            trading_day_list).to_frame(benchmark_id)
        benchmark_list.append(benchmark_series)
    benchmark_df = pd.concat(benchmark_list, axis=1)
    # 好买策略指数
    sql_script = "SELECT zsdm, spjg, jyrq FROM st_hedge.t_st_sm_zhmzs WHERE " \
                 "zsdm in ('HB1002','HB0018','HB0015','HB0017') and jyrq <= '20221230'"
    res = hbs.db_data_query('highuser', sql_script, page_size=5000)
    data = pd.DataFrame(res['data'])
    hb_index = pd.pivot_table(
        data, index='jyrq', columns='zsdm', values='spjg').reindex(trading_day_list).dropna(how='all').loc["20151231":]
    # strategy
    res = w.wsd(
        "NH0100.NHF,885001.WI,885306.WI,885309.WI,885308.WI,885312.WI", "close", start_date, end_date, "Period=W")
    d_list = [datetime.strftime(x, '%Y%m%d') for x in res.Times]
    data = pd.DataFrame(res.Data, index=res.Codes, columns=d_list).T.reindex(trading_day_list)
    benchmark_df = benchmark_df.merge(data[['NH0100.NHF']], left_index=True, right_index=True)
    strategy_index = data[data.columns[1:]].dropna()

    # 计算
    benchmark_df.pct_change().dropna(how='all').apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)
    strategy_index.pct_change().dropna(how='all').apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)

    return hb_index


def get_data_from_Wind():
    trading_day_list = get_trading_day_list('20150101', '20221231', frequency="day")
    # 主力资金数据
    date_list = trading_day_list[::40] + [trading_day_list[-1]]
    data_list = []
    for i in tqdm(range(1, len(date_list))):
        start_date, end_date = date_list[i - 1], date_list[i]
        res = w.wset("marketmoneyflows", "startdate={};enddate={};frequency=day;sector=sse_szse;securitytype=A股;field=date,maininmoney,mainoutmoney,maininflowmoney".format(start_date, end_date))
        data = pd.DataFrame(
            {"trade_date": res.Data[0], "M_in": res.Data[1], "M_out": res.Data[2], "Delta": res.Data[3]})
        data_list.append(data)
    all_data = pd.concat(data_list, axis=0)
    all_data['trade_date'] = all_data['trade_date'].apply(lambda x: datetime.strftime(x, "%Y%m%d"))
    all_data = all_data.drop_duplicates(subset=['trade_date']).set_index('trade_date').sort_index()
    all_data['sum'] = all_data['M_in'] + all_data['M_out']
    all_data = all_data.reindex(trading_day_list).dropna()
    # 成交额数据
    sql_script = "SELECT * FROM mac_stock_trading"
    engine = create_engine(engine_params)
    data = pd.read_sql(sql_script, engine)
    data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
    amt_data = data[['trade_date', 'amt_sh', 'amt_sz', 'amt_300', 'amt_500', 'amt_1000', 'amt_other']]
    amt_data['amt_all'] = amt_data['amt_sh'] + amt_data['amt_sz']
    amt_data = amt_data[(amt_data['trade_date'] > '20141231') & (amt_data['trade_date'] <= '20221231')]
    amt_data = amt_data.set_index('trade_date')[['amt_all']]

    df = all_data[['sum']].merge(amt_data, left_index=True, right_index=True)
    df['sum'] /= 1e+4

    # 按月度分类
    month_end = get_trading_day_list('20141220', '20221231', frequency="month")[::3]
    a = []
    b = []
    for i in range(1, len(month_end)):
        start, end = month_end[i - 1], month_end[i]
        period_data = df.loc[start: end][1:]
        ratio = period_data['sum'].sum() / period_data['amt_all'].sum()
        # ratio = period_data['sum'].sum()
        a.append(end)
        b.append(ratio)

    count_df = pd.DataFrame({"date": a, "ratio": b}).sort_values(by='date')
    count_df.set_index('date').plot.bar()


if __name__ == '__main__':
    # data_preparation('20130101', '20221230')
    get_data_from_Wind()