import re
import urllib.parse
import socket
from scrapy import Selector


# 设置获取数据类型
def getDatas(yuan):
    # 获取所有链接
    pattern = '(https?://[^\s)";]+(\.(\w|/)*))'
    link = re.compile(pattern).findall(yuan)
    # 将文件链接去重并统一输出为列表格式
    return list(set([li[0] for li in link]))


def geTable(page_source, table_xpath, lies_xpath=None, lies: list = None, if_return_ls=False) -> list:
    assert lies_xpath or lies or if_return_ls, '至少选择一项!'
    html = Selector(text=page_source)
    table = html.xpath(table_xpath)
    datas = list()
    if lies_xpath:
        lies = [i.strip() for i in table.xpath(lies_xpath).xpath('string(.)').extract()]
    trs = table.xpath('./tbody/tr')
    for tr in trs:
        datas.append([td.xpath('string(.)').get().strip() for td in tr.xpath('./td')])
    if lies:
        return [dict(zip(lies, data)) for data in datas]
    else:
        return datas


#
# # 获取表格字典,列与值同级
# def geTableDt_thtr(table_lxml) -> dict:
#     datadt = dict()
#     for tr in table_lxml.xpath('./tbody/tr'):
#         lie = tr.xpath('./th')[0].xpath('string(.)').strip()
#         value = tr.xpath('./td')[0].xpath('string(.)').strip()
#         datadt[lie] = value
#     return datadt
#
#
# def geTableDt_lies(table_lxml, lies, minindex=0, maxindex=None):
#     datadts = list()
#     trs = table_lxml.xpath('./tbody/tr')
#     trs = trs[minindex:] if maxindex is None else trs[minindex:maxindex]
#     for tr in trs:
#         dt = dict()
#         for lie, td in zip(lies, tr.xpath('./td')):
#             value = td.xpath('string(.)').strip()
#             dt[lie] = value
#         datadts.append(dt)
#     return datadts
#
#
# # 获取表格字典
# def geTableDt(table_lxml) -> list:
#     datadts = list()
#     lies = list()
#     trs = table_lxml.xpath('./tbody/tr')
#     for th in trs[0].xpath('./th'):
#         lies.append(th.xpath('string(.)').strip())
#     for tr in trs[1:]:
#         dt = dict()
#         for lie, td in zip(lies, tr.xpath('./td')):
#             value = td.xpath('string(.)').strip()
#             dt[lie] = value
#         datadts.append(dt)
#     return datadts


# 获取嵌入后的有效链接，替代直接用format
def getUrlFormat(url0, **valuedt):
    for key in valuedt:
        # 转义为url字段，避免类似&的情况
        valuedt[key] = urllib.parse.quote(str(valuedt[key]))
    return url0.format(**valuedt)


# 获取参数编码后的链接
def getEncodeUrl(url0, valuedt: dict):
    encode_params = urllib.parse.urlencode(list(valuedt.items()))
    return f'{url0}?{encode_params}'


# 获取url编码文本
def getUrlEncodeStr(txt: str, encoding='utf-8') -> str:
    return urllib.parse.quote(txt, encoding=encoding)


# 获取url解码文本
def getUrlDecodeStr(txt) -> str:
    return urllib.parse.unquote(txt)


# 获取链接的参数字典
def getUrlKwargs(txt) -> (str,dict):
    dt = dict()
    for t in re.findall('([^?=&]+=[^?=&]+)', txt):
        k, v = t.split('=')
        dt[urllib.parse.unquote(k)] = urllib.parse.unquote(v)
    return urllib.parse.unquote(txt.split('?')[0]), dt


# 字符串转headers
def getHeaders_str(string) -> dict:
    headers = dict()
    lines = string.split('\n')
    for line in lines:
        line = line.strip()
        if line != '':
            key, value = str(re.match('.+?:', line).group()[0:-1]), str(re.search(':.+', line).group()[1:])
            headers[key] = value.strip()
    return headers


# 超时报错方法
def sockeTimeoutRun(timeout, func, *args, **kwargs):
    try:
        socket.setdefaulttimeout(timeout)
        return func(*args, **kwargs)
    except socket.timeout:
        raise socket.timeout
