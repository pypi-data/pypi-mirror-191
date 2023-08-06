# -*- coding: utf-8 -*-
from jdw.data.SurfaceAPI.stock.yields import StkYields
from jdw.data.SurfaceAPI.stock.factors import StkFactors
from jdw.data.SurfaceAPI.universe import StkUniverse
from jdw.data.SurfaceAPI.stock.industry import Industry
from jdw.mfc.entropy.catalyst.geneticist.base import Base


class StockGeneticist(Base):

    def __init__(self,
                 offset,
                 horizon,
                 factor_columns,
                 universe,
                 industry_name,
                 industry_level,
                 is_loop=False,
                 operators=None,
                 winsorize_normal=True,
                 callback_save=None,
                 yield_name='returns'):
        super(StockGeneticist,
              self).__init__(offset=offset,
                             horizon=horizon,
                             factor_columns=factor_columns,
                             universe=universe,
                             yields_class=StkYields,
                             universe_class=StkUniverse,
                             industry_class=Industry,
                             factors_class=StkFactors,
                             industry_name=industry_name,
                             industry_level=industry_level,
                             operators=operators,
                             winsorize_normal=winsorize_normal,
                             callback_save=callback_save,
                             is_loop=is_loop,
                             yield_name=yield_name)

    def industry_fillna(self, industry_data, factors_data):
        factors_data = factors_data.merge(industry_data,
                                          on=['trade_date', 'code'])
        factors_data = self.industry_median(factors_data)
        return factors_data
