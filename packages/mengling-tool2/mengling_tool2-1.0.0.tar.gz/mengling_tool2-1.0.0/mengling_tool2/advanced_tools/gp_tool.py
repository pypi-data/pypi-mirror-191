import json
import re
import pandas as pd
from data.make import regular
from ..database_tool2.mysql import MysqlExecutor
from ..tools.time import getNowTime, TimeTool
from ..spider_tools.spiders.httpx import Httpx
from chinese_calendar import is_workday
from ..decorates.retry import retryFunc_args

_connect = {
    'host': 'rm-wz92k089rq29109m4125010mm.mysql.rds.aliyuncs.com',
    'user': 'mengling02',
    'password': 'DabQaZKukXiuLl7M4xoAQQ==',
    'ifencryption': True,
    'ifassert': True,
}


def _getSqlt():
    return MysqlExecutor('gp', **_connect)


def getAllCodes():
    with _getSqlt() as sqlt:
        sql = "select TABLE_NAME from information_schema.tables WHERE TABLE_SCHEMA='gp'"
        sqlt.run(sql, ifdatas=True)
        datas = [row[0] for row in sqlt.cursor.fetchall()]
        return datas


# 获取处理完成后的数据字典(无约束,仅做数据有效化处理)
@retryFunc_args(sleeptime=1, iftz=False)
def getDatadts(code, where='True', other="order by `日期` ASC") -> list:
    with _getSqlt() as sqlt:
        datadts = sqlt.select("*", code, where=where, other=other)
        return datadts


# 获取处理完成后的数据字典(时间约束)
def getDateDatadts(code, mindate: str = None, maxdate: str = None):
    mindate = "1900-01-01" if mindate is None else mindate
    maxdate = "2050-01-01" if maxdate is None else maxdate
    # 日期检查
    assert len(re.findall('\d{4}-\d{2}-\d{2}', mindate + maxdate)) == 2, f'日期格式错误{mindate} {maxdate}'
    # 不包括最大值当天
    datadts = getDatadts(code, where=f"`日期`>='{mindate}' and `日期`<'{maxdate}'")
    return datadts


# 获取处理完成后的数据字典(某时前数量约束)
def getNumDatadts(code, num, dtime, ifnew=False):
    assert len(re.findall('\d{4}-\d{2}-\d{2}', dtime)) == 1, f'日期格式错误{dtime}'
    if ifnew:
        datadts = getDatadts(code, where=f"`日期`>='{dtime}'",
                             other=f"order by `日期` ASC limit 0,{int(num)}")
    else:
        datadts = getDatadts(code, where="`日期`<'%s'" % dtime,
                             other=f"order by `日期` DESC limit 0,{int(num)}")
        datadts.reverse()
    return datadts


# 获取当前时间点的价格字典
@retryFunc_args(ci=3, iftz=True, sleeptime=2)
def getNowDataDict(code):
    if code[0] == '0':
        code = '1' + code
    elif code[0] == '6':
        code = '0' + code
    else:
        assert False, '首位不为6或1'
    spider = Httpx()
    url = f'http://api.money.126.net/data/feed/{code},money.api'
    json_data = spider.get(url)
    json_data = re.findall('\\(([\d\D]+?)\\);', json_data)[0]
    datadict = json.loads(json_data)
    spider.close()
    return datadict.get(code, dict())


# 判断是否为交易日
def isTradingDay():
    spider = Httpx()
    url = f'http://tool.bitefu.net/jiari/?d={getNowTime("%Y-%m-%d")}'
    index = spider.get(url)
    spider.close()
    return index == '0'


# 获取去突变数据组
def getRegularValues(dts, v0=100, ifthree=False) -> list:
    if len(dts) == 0: return []
    df = pd.DataFrame(data=dts)
    df.fillna(0, inplace=True)
    values = regular(df.loc[:, '涨跌幅'], v0=v0)
    if ifthree:
        valuedts = list()
        for i in range(len(values)):
            zdj = df.loc[i, '最低价']
            spj = df.loc[i, '收盘价']
            zgj = df.loc[i, '最高价']
            tempdt = {'zdj': values[i] * zdj / spj, 'spj': values[i], 'zgj': values[i] * zgj / spj}
            valuedts.append(tempdt)
        return valuedts
    return values


# 计算有效目标日期
def target_day(date0, n):
    target_day = TimeTool(date0, gs='%Y-%m-%d')
    for i in range(n):
        target_day.next(1, if_replace=True)
        while not is_workday(target_day.to_datetime()) or target_day.to_datetime().isoweekday() > 5:
            target_day.next(1, if_replace=True)
    return target_day.to_txt()
