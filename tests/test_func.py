#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/8/28 15:00
Desc: To test intention, just write test code here!
"""

import pathlib

import pandas as pd

from akshare.datasets import get_ths_js, get_crypto_info_csv


def test_path_func():
    """
    test path func
    :return: path of file
    :rtype: pathlib.Path
    """
    temp_path = get_ths_js("ths.js")
    assert isinstance(temp_path, pathlib.Path)


def test_zipfile_func():
    """
    test path func
    :return: path of file
    :rtype: pathlib.Path
    """
    temp_path = get_crypto_info_csv("crypto_info.zip")
    assert isinstance(temp_path, pathlib.Path)


def test_fund_portfolio_asset_allocation_em():
    """
    test fund_portfolio_asset_allocation_em
    """
    from akshare.fund.fund_portfolio_em import fund_portfolio_asset_allocation_em

    df = fund_portfolio_asset_allocation_em(symbol="000001", date="2024")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == [
        "报告期",
        "股票占净值比例",
        "债券占净值比例",
        "现金占净值比例",
        "净资产",
    ]
    assert df["股票占净值比例"].dtype == "float64"
    assert df["债券占净值比例"].dtype == "float64"
    assert df["现金占净值比例"].dtype == "float64"
    assert df["净资产"].dtype == "float64"
    assert df["报告期"].str.startswith("2024").all()


if __name__ == "__main__":
    test_path_func()
    test_zipfile_func()
    test_fund_portfolio_asset_allocation_em()
