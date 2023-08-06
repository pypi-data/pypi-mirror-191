#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DataLoader.py
@Time    :   2022/10/12 15:00:10
@Author  :   Shenxian Shi 
@Version :   
@Contact :   shishenxian@bluemoon.com.cn
@Desc    :   None
'''

# here put the import lib
import sys
import os
from typing import Union
sys.path.append(os.getcwd())
sys.path.append('..')
from easy_db.db import ImpalaDB, HiveDB

from dm_platform_utils.utils import read_yml, process_dtypes


def get_data(path):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(_ROOT, 'conf', path)


SQL_INFO = read_yml(get_data('sql.yml'))
PROCESS_DICT = read_yml(get_data('process_dtypes.yml'))


class DataLoader(object):
    """
    数据读取模块
    """
    
    def __init__(self, engine='impala', project='gyxt', host: str=None, port: Union[str, int]=None):
        """ Constructor

        Args:
            engine (str, optional): 取数引擎. Defaults to 'impala'.
            project (str, optional): 项目, gyxt or smart_operation. Defaults to 'gyxt'.
            host (str, optional): ip. Defaults to None.
            port (int, str, optional): 端口. Defaults to None.

        Raises:
            ValueError
        """
        self.project = project
        if engine == 'impala':
            self.conn = ImpalaDB(host=host, port=port)
        elif engine == 'hive':
            self.conn = HiveDB(host=host, port=port)
        else:
            raise ValueError('Engine should be either "impala" or "hive".')
        
    def get_data(self, dim:str = 'first_dim', date_type:str = 'month',
                 data_date:str = None):
        """ 取数

        Args:
            dim (str, optional): 业务维度. Defaults to 'first_dim'.
            date_type(str, optional): 日期类型. Defaults to 'month'. 
            data_date(str, optional): 日期. Defaults to None.
        """
        if data_date is None:
            from datetime import datetime
            data_date = datetime.now().strftime(
                '%Y%m' if date_type == 'month' else '%Y%m%d'
            )
        if 'dim' in dim:
            sql = SQL_INFO[self.project][dim] % (data_date, date_type)
        else:
            sql = SQL_INFO[self.project][dim][date_type] % data_date
        df = self.conn.select_df(sql=sql)
        data = process_dtypes(data=df, conf=PROCESS_DICT)
        return data