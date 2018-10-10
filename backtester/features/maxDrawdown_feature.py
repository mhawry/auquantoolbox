from backtester.features.feature import Feature
from backtester.logger import *


class MaxDrawdownFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''

    '''MAKE SURE PNL and PORTFOLIO VALUEis calculated BEFORE this feature
    '''
    @classmethod
    def computeForInstrument(cls, featureParams, featureKey, currentFeatures, instrument, instrumentManager):
        raise NotImplementedError

    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        portfolioValueKey = 'portfolio_value'
        lookbackMarketDataDf = instrumentManager.getDataDf()

        if len(lookbackMarketDataDf) < 1 or instrumentManager is None:
            # First Iteration
            return 0
        if 'portfolioValueKey' in featureParams:
            portfolioValueKey = featureParams['portfolioValueKey']

        portfolioValueDict = lookbackMarketDataDf[portfolioValueKey]
        if len(portfolioValueDict) <= 1:
            return {'maxPortfolioValue': 0, 'maxDrawdown': 0}

        try:
            drawdownDict = lookbackMarketDataDf[featureKey].iloc[-2]
        except IndexError:
            logError("drawdownDict does not have 2 elements")
            return {'maxPortfolioValue': 0, 'maxDrawdown': 0}

        try:
            maxPortfolioValue = portfolioValueDict.iloc[-1] if drawdownDict['maxPortfolioValue'] < portfolioValueDict.iloc[-1] \
                else drawdownDict['maxPortfolioValue']
            maxDrawdown = maxPortfolioValue - portfolioValueDict.iloc[-1] if drawdownDict['maxDrawdown'] < maxPortfolioValue - portfolioValueDict.iloc[-1] \
                else drawdownDict['maxDrawdown']
        except KeyError:
            logError("Key is not present")
            return {'maxPortfolioValue': 0, 'maxDrawdown': 0}

        return {'maxPortfolioValue': maxPortfolioValue, 'maxDrawdown': maxDrawdown}
