# -*- coding: utf-8 -*-
import datetime, pdb
import pandas as pd
from ultron.tradingday import *
from jdw.kdutils.logger import kd_logger


class Base(object):

    def __init__(self,
                 factor_class,
                 universe_class,
                 yields_class,
                 industry_class,
                 risk_class,
                 offset,
                 industry_name,
                 industry_level,
                 yield_name='returns',
                 horizon=0,
                 index_yields=None,
                 risk_model=None,
                 universe=None,
                 benchmark=None):
        self._offset = offset
        self._horizon = horizon
        self._factor_class = factor_class
        self._universe_class = universe_class
        self._yields_class = yields_class
        self._industry_class = industry_class
        self._risk_class = risk_class
        self._index_yields = index_yields
        self._benchmark = benchmark
        self._universe = universe

    def index_yields(self, begin_date, end_date):
        closing_date = advanceDateByCalendar(
            'china.sse', end_date,
            "{}b".format(self._offset + self._horizon + 1),
            BizDayConventions.Following)
        index_return = self._index_yields.yields(start_date=begin_date,
                                                 end_date=closing_date,
                                                 offset=self._offset,
                                                 horizon=self._horizon,
                                                 index_code=self._benchmark)
        index_return.rename(columns={'nxt1_ret': 'returns'}, inplace=True)
        return index_return

    def fetch_yields(self, begin_date, end_date, universe=None):
        kd_logger.info("start create yields data")
        yields = self._yields_class()
        if self._yield_name == 'returns':
            closing_date = advanceDateByCalendar(
                'china.sse', end_date,
                "{}b".format(self._offset + self._horizon + 1),
                BizDayConventions.Following)

            yields_data = yields.fetch_returns(universe=universe,
                                               start_date=begin_date,
                                               end_date=closing_date,
                                               horizon=self._freq,
                                               offset=self._batch,
                                               benchmark=None)
        else:
            yields_data = yields.fetch_yileds(universe=universe,
                                              start_date=begin_date,
                                              end_date=end_date,
                                              name=self._yield_name)
        return yields_data

    def factors_data(self, begin_date, end_date, factor_name, universe=None):
        factors_data = self._factor_class().fetch(universe=universe,
                                                  start_date=begin_date,
                                                  end_date=end_date,
                                                  columns=factor_name)
        return factors_data

    def fetch_industry(self, begin_date, end_date, universe=None):
        kd_logger.info("start fetch industry data")
        industry = self._industry_class()
        industry_data = industry.fetch(universe=universe,
                                       start_date=begin_date,
                                       end_date=end_date,
                                       category=self._industry_name,
                                       level=self._industry_level)
        return industry_data

    def industry_fillna(self, industry_data, factors_data):
        return factors_data.fillna(0)

    def prepare_data(self, begin_date=None, end_date=None):
        yields_data = self.fetch_yields(
            begin_date=begin_date,
            end_date=end_date,
            universe=self._universe_class(u_name=self._universe))

        factors_data = self.factors_data(
            begin_date=begin_date,
            end_date=end_date,
            factor_name=self._features,
            universe=self._universe_class(u_name=self._universe))

        industry_data = self.fetch_industry(
            begin_date=begin_date,
            end_date=end_date,
            universe=self._universe_class(u_name=self._universe))

        factors_data = self.industry_fillna(industry_data=industry_data,
                                            factors_data=factors_data)
        factors_data = factors_data.sort_values(by=['trade_date', 'code'])

        ### 因子换算
        factors_data = self._alpha_model.formulas.transform(
            'code', factors_data.set_index('trade_date'))

        industry_dummy = pd.get_dummies(
            industry_data.set_index(['code'])['industry_code']).reset_index()

        total_data = factors_data.reset_index().merge(
            industry_data,
            on=['code']).merge(yields_data, on=['trade_date',
                                                'code']).merge(industry_dummy,
                                                               on=['code'])
        return total_data

    def run(self, begin_date, end_date):
        kd_logger.info("start service")
        index_return = None
        if self._benchmark is not None:
            index_return = self.index_yields(begin_date, end_date)
