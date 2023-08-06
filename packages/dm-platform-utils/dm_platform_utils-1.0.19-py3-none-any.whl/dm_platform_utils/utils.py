#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2022/10/08 16:21:01
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
import sys
import os
sys.path.append(os.getcwd())

import pandas as pd


def read_yml(file_path):
    from ruamel import yaml
    with open(file_path, 'r', encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return data


def process_dtypes(data: pd.DataFrame, conf: dict):
    """预处理数据的数据类型

    Args:
        df (pd.DataFrame): 数据集
        conf (dict): 需要修改的列名及其最终数据类型
            e.g. {'shop_english_cd': 'str', 
                    'pay_cnt': 'int64', 
                    'pay_amt': 'float'}
    """
    from copy import deepcopy
    df = deepcopy(data)
    df = df.dropna()
    df.reset_index(drop=True, inplace=True)
    for k, v in conf.items():
        if k not in df.columns:
            continue
        # if v == 'int64' or v == 'float':
        #     if df[k].min() < 0:
        #         df.drop(df[df[k] < 0].index, inplace=True)
        if v == 'int64':
            try:
                df.loc[df.index, k] = df[k].astype(v)
            except ValueError:
                if isinstance(df[k].head(1).values[0], str):
                    df.loc[df.index, k] = df[k].apply(
                        lambda x: x.split('.')[0]
                        ).astype(v)
                else:
                    print(ValueError)
        elif v == 'str':
            df.loc[df.index, k] = df[k].astype(eval(v))
            df.loc[df.index, k] = df[k].apply(lambda x: x.split('.')[0])
        elif v == 'timestamp':
            if len(df[k].head(1).values[0]) == 8:
                df.loc[df.index, k] = pd.to_datetime(df[k], format='%Y%m%d')
            else:
                df.loc[df.index, k] = pd.to_datetime(df[k], format='%Y%m')
        else:
            df.loc[df.index, k] = df[k].astype(eval(v))
    return df
