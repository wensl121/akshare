#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/6/7 20:00
Desc: 天天基金网-基金档案-投资组合
https://fundf10.eastmoney.com/ccmx_000001.html
"""

from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from akshare.utils import demjson


def fund_portfolio_hold_em(symbol: str = "000001", date: str = "2024") -> pd.DataFrame:
    """
    天天基金网-基金档案-投资组合-基金持仓
    https://fundf10.eastmoney.com/ccmx_000001.html
    :param symbol: 基金代码
    :type symbol: str
    :param date: 查询年份
    :type date: str
    :return: 基金持仓
    :rtype: pandas.DataFrame
    """
    url = "https://fundf10.eastmoney.com/FundArchivesDatas.aspx"
    params = {
        "type": "jjcc",
        "code": symbol,
        "topline": "10000",
        "year": date,
        "month": "",
        "rt": "0.913877030254846",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    soup = BeautifulSoup(data_json["content"], features="lxml")
    item_label = [
        item.text.split("\xa0\xa0")[1]
        for item in soup.find_all(name="h4", attrs={"class": "t"})
    ]

    column_name = [
        "序号",
        "股票代码",
        "股票名称",
        "占净值比例",
        "持股数",
        "持仓市值",
        "季度",
    ]
    big_df = pd.DataFrame(columns=column_name)

    for item in range(len(item_label)):
        temp_df = pd.read_html(
            StringIO(data_json["content"]), converters={"股票代码": str}
        )[item]
        del temp_df["相关资讯"]
        temp_df.rename(columns={"占净值 比例": "占净值比例"}, inplace=True)
        temp_df["占净值比例"] = (
            temp_df["占净值比例"].str.split("%", expand=True).iloc[:, 0]
        )
        temp_df.rename(
            columns={"持股数（万股）": "持股数", "持仓市值（万元）": "持仓市值"},
            inplace=True,
        )
        temp_df.rename(
            columns={"持股数 （万股）": "持股数", "持仓市值 （万元）": "持仓市值"},
            inplace=True,
        )
        temp_df.rename(
            columns={"持股数（万股）": "持股数", "持仓市值（万元人民币）": "持仓市值"},
            inplace=True,
        )
        temp_df.rename(
            columns={
                "持股数 （万股）": "持股数",
                "持仓市值 （万元人民币）": "持仓市值",
            },
            inplace=True,
        )

        temp_df["季度"] = item_label[item]
        temp_df = temp_df[column_name]
        big_df = (
            pd.concat(objs=[temp_df, big_df], ignore_index=True)
            if not big_df.empty
            else temp_df
        )

    if not big_df.empty:
        big_df["占净值比例"] = pd.to_numeric(big_df["占净值比例"], errors="coerce")
        big_df["持股数"] = pd.to_numeric(big_df["持股数"], errors="coerce")
        big_df["持仓市值"] = pd.to_numeric(big_df["持仓市值"], errors="coerce")
        del big_df["序号"]
        big_df.reset_index(inplace=True, drop=False)
        big_df["index"] = big_df["index"] + 1
        big_df.rename(columns={"index": "序号"}, inplace=True)
    return big_df


def fund_portfolio_bond_hold_em(
    symbol: str = "000001", date: str = "2023"
) -> pd.DataFrame:
    """
    天天基金网-基金档案-投资组合-债券持仓
    https://fundf10.eastmoney.com/ccmx1_000001.html
    :param symbol: 基金代码
    :type symbol: str
    :param date: 查询年份
    :type date: str
    :return: 债券持仓
    :rtype: pandas.DataFrame
    """
    url = "https://fundf10.eastmoney.com/FundArchivesDatas.aspx"
    params = {
        "type": "zqcc",
        "code": symbol,
        "year": date,
        "rt": "0.913877030254846",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    soup = BeautifulSoup(data_json["content"], features="lxml")
    item_label = [
        item.text.split("\xa0\xa0")[1]
        for item in soup.find_all(name="h4", attrs={"class": "t"})
    ]
    big_df = pd.DataFrame()
    for item in range(len(item_label)):
        temp_df = pd.read_html(
            StringIO(data_json["content"]), converters={"债券代码": str}
        )[item]
        temp_df["占净值比例"] = (
            temp_df["占净值比例"].str.split("%", expand=True).iloc[:, 0]
        )
        temp_df.rename(columns={"持仓市值（万元）": "持仓市值"}, inplace=True)
        temp_df["季度"] = item_label[item]
        temp_df = temp_df[
            [
                "序号",
                "债券代码",
                "债券名称",
                "占净值比例",
                "持仓市值",
                "季度",
            ]
        ]
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    big_df["占净值比例"] = pd.to_numeric(big_df["占净值比例"], errors="coerce")
    big_df["持仓市值"] = pd.to_numeric(big_df["持仓市值"], errors="coerce")
    big_df["序号"] = range(1, len(big_df) + 1)
    return big_df


def fund_portfolio_industry_allocation_em(
    symbol: str = "000001", date: str = "2023"
) -> pd.DataFrame:
    """
    天天基金网-基金档案-投资组合-行业配置
    https://fundf10.eastmoney.com/hytz_000001.html
    :param symbol: 基金代码
    :type symbol: str
    :param date: 查询年份
    :type date: str
    :return: 行业配置
    :rtype: pandas.DataFrame
    """
    url = "https://api.fund.eastmoney.com/f10/HYPZ/"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "api.fund.eastmoney.com",
        "Pragma": "no-cache",
        "Referer": "https://fundf10.eastmoney.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.82 Safari/537.36",
    }
    params = {
        "fundCode": symbol,
        "year": date,
        "callback": "jQuery183006997159478989867_1648016188499",
    }
    r = requests.get(url, params=params, headers=headers)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_list = []
    for item in data_json["Data"]["QuarterInfos"]:
        temp_list.extend(item["HYPZInfo"])
    temp_df = pd.DataFrame(temp_list)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.columns = [
        "序号",
        "-",
        "截止时间",
        "-",
        "行业类别",
        "市值",
        "-",
        "占净值比例",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
        "-",
    ]
    temp_df = temp_df[
        [
            "序号",
            "行业类别",
            "占净值比例",
            "市值",
            "截止时间",
        ]
    ]
    temp_df["市值"] = pd.to_numeric(temp_df["市值"], errors="coerce")
    temp_df["占净值比例"] = pd.to_numeric(temp_df["占净值比例"], errors="coerce")
    return temp_df


def fund_portfolio_change_em(
    symbol: str = "003567", indicator: str = "累计买入", date: str = "2023"
) -> pd.DataFrame:
    """
    天天基金网-基金档案-投资组合-重大变动
    https://fundf10.eastmoney.com/ccbd_000001.html
    :param symbol: 基金代码
    :type symbol: str
    :param indicator: choice of {"累计买入", "累计卖出"}
    :type indicator: str
    :param date: 查询年份
    :type date: str
    :return: 重大变动
    :rtype: pandas.DataFrame
    """
    indicator_map = {
        "累计买入": "1",
        "累计卖出": "2",
    }
    url = "https://fundf10.eastmoney.com/FundArchivesDatas.aspx"
    params = {
        "type": "zdbd",
        "code": symbol,
        "zdbd": indicator_map[indicator],
        "year": date,
        "rt": "0.913877030254846",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    soup = BeautifulSoup(data_json["content"], features="lxml")
    item_label = [
        item.text.split("\xa0\xa0")[1]
        for item in soup.find_all(name="h4", attrs={"class": "t"})
    ]
    big_df = pd.DataFrame()
    for item in range(len(item_label)):
        temp_df = pd.read_html(
            StringIO(data_json["content"]), converters={"股票代码": str}
        )[item]
        del temp_df["相关资讯"]
        temp_df["占期初基金资产净值比例（%）"] = (
            temp_df["占期初基金资产净值比例（%）"]
            .str.split("%", expand=True)
            .iloc[:, 0]
        )
        temp_df["季度"] = item_label[item]
        temp_df.columns = [
            "序号",
            "股票代码",
            "股票名称",
            "本期累计买入金额",
            "占期初基金资产净值比例",
            "季度",
        ]
        temp_df = temp_df[
            [
                "序号",
                "股票代码",
                "股票名称",
                "本期累计买入金额",
                "占期初基金资产净值比例",
                "季度",
            ]
        ]
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)
    del big_df["序号"]
    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.rename(columns={"index": "序号"}, inplace=True)

    big_df["本期累计买入金额"] = pd.to_numeric(
        big_df["本期累计买入金额"], errors="coerce"
    )
    big_df["占期初基金资产净值比例"] = pd.to_numeric(
        big_df["占期初基金资产净值比例"], errors="coerce"
    )
    return big_df


def fund_portfolio_asset_allocation_em(
    symbol: str = "000001", date: str = "2024"
) -> pd.DataFrame:
    """
    天天基金网-基金档案-投资组合-资产配置
    https://fundf10.eastmoney.com/zcpz_000001.html
    :param symbol: 基金代码
    :type symbol: str
    :param date: 查询年份; 为空字符串时返回所有年份数据
    :type date: str
    :return: 资产配置
    :rtype: pandas.DataFrame
    """
    from bs4 import BeautifulSoup

    url = f"https://fundf10.eastmoney.com/zcpz_{symbol}.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://fundf10.eastmoney.com/",
    }
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    table = soup.find("table", class_="w782 comm tzxq")
    temp_df = pd.read_html(StringIO(str(table)))[0]
    temp_df.columns = [
        "报告期",
        "股票占净值比例",
        "债券占净值比例",
        "现金占净值比例",
        "净资产",
    ]
    if date:
        temp_df = temp_df[temp_df["报告期"].str.startswith(date)]
        temp_df.reset_index(drop=True, inplace=True)
    for col in ["股票占净值比例", "债券占净值比例", "现金占净值比例"]:
        temp_df[col] = (
            temp_df[col].astype(str).str.replace("%", "", regex=False).str.strip()
        )
        temp_df[col] = pd.to_numeric(temp_df[col], errors="coerce")
    temp_df["净资产"] = pd.to_numeric(temp_df["净资产"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    fund_portfolio_hold_em_df = fund_portfolio_hold_em(symbol="000001", date="2024")
    print(fund_portfolio_hold_em_df)

    fund_portfolio_bond_hold_em_df = fund_portfolio_bond_hold_em(
        symbol="000001", date="2023"
    )
    print(fund_portfolio_bond_hold_em_df)

    fund_portfolio_industry_allocation_em_df = fund_portfolio_industry_allocation_em(
        symbol="000001", date="2023"
    )
    print(fund_portfolio_industry_allocation_em_df)

    fund_portfolio_change_em_df = fund_portfolio_change_em(
        symbol="003567", indicator="累计买入", date="2023"
    )
    print(fund_portfolio_change_em_df)

    fund_portfolio_change_em_df = fund_portfolio_change_em(
        symbol="003567", indicator="累计卖出", date="2023"
    )
    print(fund_portfolio_change_em_df)

    fund_portfolio_asset_allocation_em_df = fund_portfolio_asset_allocation_em(
        symbol="000001", date="2024"
    )
    print(fund_portfolio_asset_allocation_em_df)
