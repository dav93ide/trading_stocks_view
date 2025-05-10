import wx
import wx.lib.scrolledpanel
import wx.lib.agw.aui as aui
import wx.lib.mixins.inspection as wit
import time
import uuid
import json
import random
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
import requests
import threading
from wx.lib.pubsub import pub
from multipledispatch import dispatch
from functools import singledispatch
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
from datetime import datetime
from typing import TypeVar, List
from dateutil.relativedelta import relativedelta
import faulthandler


class Constants():
    DISPLAY_SIZE_MAIN_FRAME = (1000, 500)

class Colors():
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    COLOR_PLATFORM_BACKGROUND_GREY = (50, 50, 50)
    COLOR_USER_CAPITAL = (0, 153, 0)

class Icons():
    ICON_SEARCH = "Icons/search.png"

class Strings(object):
    STR_INITIAL_SYNCHRONIZATION = "Initial Synchronization"
    STR_SEARCH = "Search"
    STR_1D = "1 Day"
    STR_1D_VALUES = "1 Day Values"
    STR_1D_VOLUME = "1 Day Volume"
    STR_5D_VALUES = "5 Days Values"
    STR_5D_VOLUME = "5 Days Volume"
    STR_1MO_VALUES = "1 Month Values"
    STR_1MO_VOLUME = "1 Month Volume"
    STR_3MO_VALUES = "3 Month Values"
    STR_3MO_VOLUME = "3 Month Volume"
    STR_6MO_VALUES = "6 Month Values"
    STR_6MO_VOLUME = "6 Month Volume"
    STR_1Y_VALUES = "1 Year Values"
    STR_1Y_VOLUME = "1 Year Volume"
    STR_2Y_VALUES = "2 Year Values"
    STR_2Y_VOLUME = "2 Year Volume"
    STR_5Y_VALUES = "5 Year Values"
    STR_5Y_VOLUME = "5 Year Volume"
    STR_10Y_VALUES = "10 Year Values"
    STR_10Y_VOLUME = "10 Year Volume"
    STR_YTD_VALUES = "YTD Values"
    STR_YTD_VOLUME = "YTD Volume"
    STR_MAX_VALUES = "Max Values"
    STR_MAX_VOLUME = "Max Volume"
    STR_FIELD_MARKET_CAP = "Market Cap:"
    STR_FIELD_ENTERPRISE_VALUE = "Enterprise value:"
    STR_FIELD_DAY_MAX = "Day Max:"
    STR_FIELD_DAY_MIN = "Day Min:"
    STR_FIELD_ASK = "Ask:"
    STR_FIELD_BID = "Bid:"
    STR_FIELD_SHARES_OUTSTANDING = "Shares Outstanding:"
    STR_FIELD_52_WEEKS_MAX = "52 Weeks Max:"
    STR_FIELD_52_WEEKS_MIN = "52 Weeks Min:"
    STR_FIELD_52_WEEKS_PERC_CHANGE = "52 Weeks Change %:"
    STR_FIELD_VOLUME = "Volume:"
    STR_FIELD_VOLUME_10_DAYS = "Volume 10 Days:"
    STR_FIELD_VOLUME_3_MONTHS = "Volume 3 Months:"
    STR_FIELD_TRAILING_PRICE_EARNINGS = "Trailing Price Earnings:"
    STR_FIELD_FORWARD_PRICE_EARNINGS = "Forward Price Earnings:"
    STR_FIELD_PE_RATIO = "P/E Ratio:"
    STR_FIELD_PEG_RATIO = "PEG Ratio:"
    STR_FIELD_PB_RATIO = "PB Ratio:"
    STR_FIELD_PRICE_TO_BOOK = "Price to Book:"
    STR_FIELD_BOOK_VALUE_PER_SHARE = "Book Value per Share:"
    STR_FIELD_DIVIDEND_DATE = "Dividend Date:"
    STR_FIELD_ANNUAL_DIVIDEND_RATE = "Annual Dividend Rate:"
    STR_FIELD_ANNUAL_DIVIDEND_YELD = "Annual Dividend Yeld:"
    STR_FIELD_RATIO_ENTERPRISE_VALUE_REVENUE = "Enterprise Value / Revenue:"
    STR_FIELD_RATIO_ENTERPRISE_VALUE_EBITDA = "Enterprise Value / EBITDA:"
    STR_DOWNLOAD_DATA = "Download Data"
    STR_FIELD_PRE_MARKET = "Pre Market: $"
    STR_FIELD_POST_MARKET = "Post Market: $"

class APIConstants(object):

#region - Headers
    HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }

    HEADER_SET_COOKIE = "Set-Cookie"
    HEADER_COOKIE = "Cookie"
#endregion

#region - API Range Values
    VALUE_1M = "1m"
    VALUE_5M = "5m"
    VALUE_1H = "1h"
    VALUE_1D = "1d"
    VALUE_5D = "5d"
    VALUE_1MO = "1mo"
    VALUE_3MO = "3mo"
    VALUE_6MO = "6mo"
    VALUE_1Y = "1y"
    VALUE_2Y = "2y"
    VALUE_5Y = "5y"
    VALUE_10Y = "10y"
    VALUE_YTD = "ytd"
    VALUE_MAX = "max"
#endregion

#region - API Fields
#region - URL_API_STOCKANALYSIS_GET_SYMBOLS - Json Fields
    FIELD_STATUS = "status"
    FIELD_DATA = "data"
    FIELD_S = "s"
    FIELD_N = "n"
#endregion

#region - URL_API_YAHOO_FINANCE_GET_STOCKS_DATA__FROM_SYMBOLS - Json Fields
    FIELD_SPARK = "spark"
    FIELD_RESULT = "result"
    FIELD_SYMBOL = "symbol"
    FIELD_RESPONSE = "response"
    FIELD_META = "meta"
    FIELD_LONG_NAME = "longName"
    FIELD_SHORT_NAME = "shortName"
    FIELD_CURRENCY = "currency"
    FIELD_EXCHANGE_NAME = "exchangeName"
    FIELD_FULL_EXCHANGE_NAME = "fullExchangeName"
    FIELD_HAS_PRE_POST_MARKET_DATA = "hasPrePostMarketData"
    FIELD_INSTRUMENT_TYPE = "instrumentType"
    FIELD_FIRST_TRADE_DATE = "firstTradeDate"
    FIELD_REGULAR_MARKET_PRICE = "regularMarketPrice"
    FIELD_FIFTY_TWO_WEEK_HIGH = "fiftyTwoWeekHigh"
    FIELD_FIFTY_TWO_WEEK_LOW = "fiftyTwoWeekLow"
    FIELD_REGULAR_MARKET_DAY_HIGH = "regularMarketDayHigh"
    FIELD_REGULAR_MARKET_DAY_LOW = "regularMarketDayLow"
    FIELD_REGULAR_MARKET_VOLUME = "regularMarketVolume"
    FIELD_PREVIOUS_CLOSE = "previousClose"
#endregion

#region - URL_API_YAHOO_FINANCE_GET_STOCKS_DATA__FROM_SYMBOLS - Json Fields
    FIELD_TIMESERIES = "timeseries"
    FIELD_AS_OF_DATE = "asOfDate"
    FIELD_RAW = "raw"
    FIELD_FMT = "fmt"
    FIELD_REPORTED_VALUE = "reportedValue"


    FIELD_QUARTERLY_MARKET_CAP = "quarterlyMarketCap"
    FIELD_TRAILING_MARKET_CAP = "trailingMarketCap"
    FIELD_QUARTERLY_ENTERPRISE_VALUE = "quarterlyEnterpriseValue"
    FIELD_TRAILING_ENTERPRISE_VALUE = "trailingEnterpriseValue"
    FIELD_QUARTERLY_PE_RATIO = "quarterlyPeRatio"
    FIELD_TRALING_PE_RATIO = "trailingPeRatio"
    FIELD_QUARTERLY_FORWARD_PE_RATIO = "quarterlyForwardPeRatio"
    FIELD_TRALING_FORWARD_PE_RATIO = "trailingForwardPeRatio"
    FIELD_QUARTERLY_PEG_RATIO = "quarterlyPegRatio"
    FIELD_TRAILING_PEG_RATIO = "trailingPegRatio"
    FIELD_QUARTERLY_PS_RATIO = "quarterlyPsRatio"
    FIELD_TRALING_PS_RATIO = "trailingPsRatio"
    FIELD_QUARTERLY_PB_RATIO = "quarterlyPbRatio"
    FIELD_TRAILING_PB_RATIO = "trailingPbRatio"
    FIELD_QUARTERLY_ENTERPRISES_VALUE_REVENUE_RATIO = "quarterlyEnterprisesValueRevenueRatio"
    FIELD_TRAILING_ENTERPRISES_VALUE_REVENUE_RATIO = "trailingEnterprisesValueRevenueRatio"
    FIELD_QUARTERLY_ENTERPRISES_VALUE_EBITDA_RATIO = "quarterlyEnterprisesValueEBITDARatio"
    FIELD_QUARTERLY_TRAILING_ENTERPRESISES_VALUE_EBITDA_RATIO = "trailingEnterprisesValueEBITDARatio"
    FIELD_REPORTED_VALUE = "reportedValue"
#endregion

#region - URL_API_YAHOO_FINANCE_GET_FUNDAMENTALS_SERIES_STOCK - Request Fields
    FIELDS_API_GET_FUNDAMENTALS_SERIES_STOCK = [
        FIELD_QUARTERLY_MARKET_CAP,
        FIELD_TRAILING_MARKET_CAP,
        FIELD_QUARTERLY_ENTERPRISE_VALUE,
        FIELD_TRAILING_ENTERPRISE_VALUE,
        FIELD_QUARTERLY_PE_RATIO,
        FIELD_TRALING_PE_RATIO,
        FIELD_QUARTERLY_FORWARD_PE_RATIO,
        FIELD_TRALING_FORWARD_PE_RATIO,
        FIELD_QUARTERLY_PEG_RATIO,
        FIELD_TRAILING_PEG_RATIO,
        FIELD_QUARTERLY_PS_RATIO,
        FIELD_TRALING_PS_RATIO,
        FIELD_QUARTERLY_PB_RATIO,
        FIELD_TRAILING_PB_RATIO,
        FIELD_QUARTERLY_ENTERPRISES_VALUE_REVENUE_RATIO,
        FIELD_TRAILING_ENTERPRISES_VALUE_REVENUE_RATIO,
        FIELD_QUARTERLY_ENTERPRISES_VALUE_EBITDA_RATIO,
        FIELD_QUARTERLY_TRAILING_ENTERPRESISES_VALUE_EBITDA_RATIO
    ]
#endregion

#region - URL_API_YAHOO_FINANCE_GET_QUOTE_SUMMARY - Json Fields
    FIELD_QUOTE_RESPONSE = "quoteResponse"
    FIELD_ASK = "ask"
    FIELD_ASK_SIZE = "askSize"
    FIELD_BID = "bid"
    FIELD_BID_SIZE = "bidSize"
    FIELD_AVG_DAILY_VOLUME_TEN_DAYS = "averageDailyVolume10Day"
    FIELD_AVG_DAILY_VOLUME_THREE_MONTH = "averageDailyVolume3Month"
    FIELD_FIFTY_TWO_WEEK_RANGE = "fiftyTwoWeekRange"
    FIELD_FIFTY_TWO_WEEK_CHANGE_PERCENT = "fiftyTwoWeekChangePercent"
    FIELD_SHARES_OUTSTANDING = "sharesOutstanding"
    FIELD_PRICE_TO_BOOK = "priceToBook"
    FIELD_MARKET_CAP = "marketCap"
    FIELD_FORWARD_PE = "forwardPE"
    FIELD_TRAILING_PE = "trailingPE"
    FIELD_TRAILING_ANNUAL_DIVIDEND_RATE = "trailingAnnualDividendRate"
    FIELD_TRAILING_ANNUAL_DIVIDEND_YELD = "trailingAnnualDividendYield"
    FIELD_DIVIDEND_DATE = "dividendDate"
    FIELD_DIVIDEND_RATE = "dividendRate"
    FIELD_REGULAR_MARKET_PREVIOUS_CLOSE = "regularMarketPreviousClose"
    FIELD_DISPLAY_NAME = "displayName"
    FIELD_AVERAGE_ANALYST_RATING = "averageAnalystRating"
    FIELD_REGULAR_MARKET_CHANGE_PERCENT = "regularMarketChangePercent"
    FIELD_POST_MARKET_CHANGE_PERCENT = "postMarketChangePercent"
    FIELD_POST_MARKET_TIME = "postMarketTime"
    FIELD_POST_MARKET_PRICE = "postMarketPrice"
    FIELD_POST_MARKET_CHANGE = "postMarketChange"
    FIELD_EARNINGS_TIMESTAMP = "earningsTimestamp"
    FIELD_EPS_TRAILING_TWELVE_MONTHS = "epsTrailingTwelveMonths"
    FIELD_EPS_FORWARD = "epsForward"
    FIELD_EPS_CURRENT_YEAR = "epsCurrentYear"
    FIELD_PRICE_EPS_CURRENT_YEAR = "priceEpsCurrentYear"
    FIELD_BOOK_VALUE = "bookValue"
    FIELD_EXCHANGE = "exchange"
    FIELD_FIRST_TRADE_DATE_MILLISECONDS = "firstTradeDateMilliseconds"
    FIELD_FINANCIAL_CURRENCY = "financialCurrency"
    FIELD_PRE_MARKET_PRICE = "preMarketPrice"
#endregion

#region - URL_API_YAHOO_FINANCE_GET_CHART - Json Fields
    FIELD_CHART = "chart"
    FIELD_TIMESTAMP = "timestamp"
    FIELD_INDICATORS = "indicators"
    FIELD_QUOTE = "quote"
    FIELD_VOLUME = "volume"
    FIELD_CLOSE = "close"
    FIELD_OPEN = "open"
#endregion

T = TypeVar('T')
class BaseClass():

    __id = None

    def __init__(self, id):
        self.__id = id

#region - Getter Methods
    def get_id(self):
	    return self.__id
#endregion
    
#region - Setter Methods
    def set_id(self, id):
        self.__id = id
#endregion

    # To String
    def __str__(self):
        return  "####################\n"\
                f"# {BaseClass.__name__}\n"\
                f"#- __id: {self.__id}\n"\
                "####################"

class Company(BaseClass):

    __mName = None
    __mShortName = None
    __mYearBorn = None
    __mAddress = None
    __mWebsiteUrl = None
    __mNumEmployees = None
    __mEnterpriseValue = None
    __mRevenue = None
    __mQuarterlyRevenueGrowth = None
    __mGrossProfit = None
    __mEBITDA = None
    __mNetIncome = None
    __mQuarterlyEarningsGrowth = None

    def __init__(self, id):
        super().__init__(id)

#region - Getter Methods
    def get_name(self):
        return self.__mName

    def get_short_name(self):
        return self.__mShortName

    def get_year_born(self):
        return self.__mYearBorn

    def get_address(self):
        return self.__mAddress

    def get_website_url(self):
        return self.__mWebsiteUrl

    def get_num_employees(self):
        return self.__mNumEmployees

    def get_enterprise_value(self):
        return self.__mEnterpriseValue

    def get_revenue(self):
        return self.__mRevenue

    def get_quarterly_revenue_growth(self):
        return self.__mQuarterlyRevenueGrowth

    def get_gross_profit(self):
        return self.__mGrossProfit

    def get_ebitda(self):
        return self.__mEBITDA

    def get_net_income(self):
        return self.__mNetIncome

    def get_quarterly_earnings_growth(self):
        return self.__mQuarterlyEarningsGrowth
#endregion

#region - Setter Methods
    def set_name(self, name):
        self.__mName = name

    def set_short_name(self, name):
        self.__mShortName = name

    def set_sectors(self, sectors):
        self.__mSectors = sectors

    def set_year_born(self, yearBorn):
        self.__mYearBorn = yearBorn

    def set_address(self, address):
        self.__mAddress = address

    def set_website_url(self, websiteUrl):
        self.__mWebsiteUrl = websiteUrl

    def set_num_employees(self, numEmployees):
        self.__mNumEmployees = numEmployees

    def set_enterprise_value(self, enterpriseValue):
        self.__mEnterpriseValue = enterpriseValue

    def set_revenue(self, revenue):
        self.__mRevenue = revenue

    def set_quarterly_revenue_growth(self, quarterlyRevenueGrowth):
        self.__mQuarterlyRevenueGrowth = quarterlyRevenueGrowth

    def set_gross_profit(self, grossProfit):
        self.__mGrossProfit = grossProfit

    def set_ebitda(self, ebitda):
        self.__mEBITDA = ebitda

    def set_net_income(self, netIncome):
        self.__mNetIncome = netIncome

    def set_quarterly_earnings_growth(self, quarterlyEarningsGrowth):
        self.__mQuarterlyEarningsGrowth = quarterlyEarningsGrowth
#endregion

    # To String
    def __str__(self):
        return  "####################\n"\
                f"# {Company.__name__}\n"\
                f"{super().__str__()}\n"\
                f"#- __mName: {self.__mName}\n"\
                f"#- __mShortName: {self.__mShortName}\n"\
                f"#- __mYearBorn: {self.__mYearBorn}\n"\
                f"#- __mAddress: {self.__mAddress}\n"\
                f"#- __mWebsiteUrl: {self.__mWebsiteUrl}\n"\
                f"#- __mEnterpriseValue: {self.__mEnterpriseValue}\n"\
                f"#- __mRevenue: {self.__mRevenue}\n"\
                f"#- __mQuarterlyRevenueGrowth: {self.__mQuarterlyRevenueGrowth}\n"\
                f"#- __mGrossProfit: {self.__mGrossProfit}\n"\
                f"#- __mEBITDA: {self.__mEBITDA}\n"\
                f"#- __mNetIncome: {self.__mNetIncome}\n"\
                f"#- __mQuarterlyEarningsGrowth: {self.__mQuarterlyEarningsGrowth}\n"\
                "####################"

class Exchange(BaseClass):

    __id = None
    __mName = None
    __mFullName = None
    __mCountry = None
    __mCurrency = None
    __mStocks = None
    __mETFs = None

#region - Getter Methods
    def get_id (self):
	    return self.__id 

    def get_name (self):
        return self.__mName 

    def get_full_name(self):
        return self.__mFullName

    def get_country (self):
        return self.__mCountry 

    def get_currency (self):
        return self.__mCurrency 

    def get_stocks (self):
        return self.__mStocks 

    def get_etf(self):
        return self.__mETFs
#endregion

#region - Setter Methods
    def set_id (self, id):
        self.__id  = id 

    def set_name (self, name):
        self.__mName  = name 

    def set_full_name(self, name):
        self.__mFullName = name

    def set_country (self, country):
        self.__mCountry  = country 

    def set_currency (self, currency):
        self.__mCurrency  = currency 

    def set_stocks (self, stocks):
        self.__mStocks  = stocks 

    def set_etf(self, etf):
        self.__mETFs = etf
#endregion

    # To String
    def __str__(self):
        return  "####################\n"\
                f"# {Exchange.__name__}\n"\
                f"{super().__str__()}\n"\
                f"#- __id: {self.__id}\n"\
                f"#- __mName: {self.__mName}\n"\
                f"#- __mFullName: {self.__mFullName}\n"\
                f"#- __mCountry: {self.__mCountry}\n"\
                f"#- __mCurrency: {self.__mCurrency}\n"\
                f"#- __mStocks: {self.__mStocks}\n"\
                f"#- __mETFs: {self.__mETFs}\n"\
                "####################"

class BaseAsset(BaseClass):

    __mName = None
    __mSign = None
    __mExchange: Exchange = None
    __mPrice = None
    __mOpenPrice = None
    __mPricePreviousClose = None
    __mMarketCap = None
    __mFirstTradeDate = None
    __mVolume = None
    __mAvgVolumeTenDays = None
    __mAvgVolumeThreeMonths = None
    __mAvgVolumeFiftyTwoWeeks = None
    __mDayRange = None
    __mDayMax = None
    __mDayMin = None
    __mDayPercChange = None
    __mFiftyTwoWeeksRange = None
    __mFiftyTwoWeeksHigh = None
    __mFifityTwoWeeksLow = None
    __mFiftyTwoWeeksPercChange = None

    def __init__(self, id):
        super().__init__(id)

#region - Getter Method
    def get_name(self):
        return self.__mName

    def get_sign(self):
        return self.__mSign

    def get_exchange(self):
        return self.__mExchange

    def get_price(self):
        return self.__mPrice

    def get_open_price(self):
        return self.__mOpenPrice

    def get_price_previous_close(self):
        return self.__mPricePreviousClose

    def get_market_cap(self):
        return self.__mMarketCap

    def get_first_trade_date(self):
        return self.__mFirstTradeDate

    def get_volume(self):
        return self.__mVolume

    def get_avg_volume_ten_days(self):
        return self.__mAvgVolumeTenDays

    def get_avg_volume_three_months(self):
        return self.__mAvgVolumeThreeMonths

    def get_avg_volume_fifty_two_weeks(self):
        return self.__mAvgVolumeFiftyTwoWeeks

    def get_day_range(self):
        return self.__mDayRange

    def get_day_max(self):
        return self.__mDayMax

    def get_day_min(self):
        return self.__mDayMin

    def get_day_perc_change(self):
        return self.__mDayPercChange

    def get_fifty_two_weeks_range(self):
        return self.__mFiftyTwoWeeksRange

    def get_fifty_two_weeks_high(self):
        return self.__mFiftyTwoWeeksHigh

    def get_fifty_two_weeks_low(self):
        return self.__mFifityTwoWeeksLow

    def get_fifty_two_weeks_perc_change(self):
        return self.__mFiftyTwoWeeksPercChange
#endregion

#region - Set Methods
    def set_name(self, name):
        self.__mName = name

    def set_sign(self, sign):
        self.__mSign = sign

    def set_exchange(self, exchange):
        self.__mExchange = exchange

    def set_price(self, price):
        self.__mPrice = price

    def set_open_price(self, openPrice):
        self.__mOpenPrice = openPrice

    def set_price_previous_close(self, pricePreviousClose):
        self.__mPricePreviousClose = pricePreviousClose

    def set_market_cap(self, marketCap):
        self.__mMarketCap = marketCap

    def set_first_trade_date(self, firstTradeDate):
        self.__mFirstTradeDate = firstTradeDate

    def set_volume(self, volume):
        self.__mVolume = volume

    def set_avg_volume_ten_days(self, avgVolumeTenDays):
        self.__mAvgVolumeTenDays = avgVolumeTenDays

    def set_avg_volume_three_months(self, avgVolumeThreeMonths):
        self.__mAvgVolumeThreeMonths = avgVolumeThreeMonths

    def set_avg_volume_fifty_two_weeks(self, avgVolumeFiftyTwoWeeks):
        self.__mAvgVolumeFiftyTwoWeeks = avgVolumeFiftyTwoWeeks

    def set_day_range(self, dayRange):
        self.__mDayRange = dayRange

    def set_day_max(self, dayMax):
        self.__mDayMax = dayMax

    def set_day_min(self, dayMin):
        self.__mDayMin = dayMin

    def set_day_perc_change(self, dayPercChange):
        self.__mDayPercChange = dayPercChange

    def set_fifty_two_weeks_range(self, fiftyTwoWeeksRange):
        self.__mFiftyTwoWeeksRange = fiftyTwoWeeksRange

    def set_fifty_two_weeks_high(self, fiftyTwoWeeksHigh):
        self.__mFiftyTwoWeeksHigh = fiftyTwoWeeksHigh

    def set_fifty_two_weeks_low(self, fifityTwoWeeksLow):
        self.__mFifityTwoWeeksLow = fifityTwoWeeksLow

    def set_fifty_two_weeks_perc_change(self, fiftyTwoWeeksPercChange):
        self.__mFiftyTwoWeeksPercChange = fiftyTwoWeeksPercChange
#endregion


    # To String
    def __str__(self):
        return  "####################\n"\
                f"# {BaseAsset.__name__}\n"\
                f"{super().__str__()} \n"\
                f"#- __mName: {str(self.__mName)}\n"\
                f"#- __mSign: {self.__mSign}\n"\
                f"#- __mExchange: {self.__mExchange}\n"\
                f"#- __mPrice: {self.__mPrice}\n"\
                f"#- __mOpenPrice: {self.__mOpenPrice}\n"\
                f"#- __mPricePreviousClose: {self.__mPricePreviousClose}\n"\
                f"#- __mMarketCap: {self.__mMarketCap}\n"\
                f"#- __mFirstTradeDate: {self.__mFirstTradeDate}\n"\
                f"#- __mVolume: {self.__mVolume}\n"\
                f"#- __mAvgVolumeTenDays: {self.__mAvgVolumeTenDays}\n"\
                f"#- __mAvgVolumeThreeMonths: {self.__mAvgVolumeThreeMonths}\n"\
                f"#- __mAvgVolumeFiftyTwoWeeks: {self.__mAvgVolumeFiftyTwoWeeks}\n"\
                f"#- __mDayRange: {self.__mDayRange}\n"\
                f"#- __mDayMax: {self.__mDayMax}\n"\
                f"#- __mDayMin: {self.__mDayMin}\n"\
                f"#- __mDayPercChange: {self.__mDayPercChange}\n"\
                f"#- __mFiftyTwoWeeksRange: {self.__mFiftyTwoWeeksRange}\n"\
                f"#- __mFiftyTwoWeeksHigh: {self.__mFiftyTwoWeeksHigh}\n"\
                f"#- __mFifityTwoWeeksLow: {self.__mFifityTwoWeeksLow}\n"\
                f"#- __mFiftyTwoWeeksPercChange: {self.__mFiftyTwoWeeksPercChange}\n"\
                "####################"

class Stock(BaseAsset):

    __mAsk = None
    __mAskSize = None
    __mBid = None
    __mBidSize = None
    __mCompany: Company = None
    __mSharesFloat = None
    __mSharesOutstanding = None
    __mImpliedSharesOutstanding = None
    __mPercSharesInsiders = None
    __mPercSharesInstitutions = None
    __mSharesShort = None
    __mShortRatio = None
    __mPercShortOfFloat = None
    __mPercShortOfOutstanding = None
    __mTrailingPriceEarnings = None
    __mForwardPriceEarnings = None
    __mPEGRatioFiveYears = None
    __mPriceToSales = None
    __mPriceToBook = None
    __mReturnOnEquity = None
    __mDilutedEPS = None
    __mBookValuePerShare = None
    __mOneYearTargetEstimated = None
    __mBeta = None
    __mFiftyDaysMovingAvg = None
    __mTwoHundredsDaysMovingAvg = None
    __mLastSplitFactor = None
    __mLastSplitDate = None
    __mNetIncomeToCommonShares = None
    __mHasPrePostMarketData = None
    __mExDividendDate = None
    __mDividendDate = None
    __mDividend = None
    __mPayoutRatio = None
    __mForwardAnnualDividendRate = None
    __mPercForwardAnnualDividendYeld = None
    __mTrailingAnnualDividendRate = None
    __mTrailingAnnualDividendYeld = None
    __mFiveYearAvgDividendYeld = None
    __mDividendRate = None
    __mEnterpriseValue = None
    __mPeRatio = None
    __mPegRatio = None
    __mPbRatio = None
    __mEnterprisesValueRevenueRatio = None
    __mEnterprisesValueEBITDARatio = None
    __mAverageAnalystRating = None
    __mMarketChangePercent = None
    __mPreMarketPrice = None
    __mPostMarketChangePercent = None
    __mPostMarketTime = None
    __mPostMarketPrice = None
    __mPostMarketChange = None
    __mEarningsTimestamp = None
    __mEpsTrailingTwelveMonths = None
    __mEpsForward = None
    __mEpsCurrentYear = None
    __mPriceEpsCurrentYearRatio = None

    def __init__(self, id):
        super(BaseAsset, self).__init__(id)

#region - Getter Methods
    def get_ask(self):
	    return self.__mAsk 

    def get_ask_size(self):
        return self.__mAskSize

    def get_bid(self):
        return self.__mBid 

    def get_bid_size(self):
        return self.__mBidSize

    def get_company(self):
        return self.__mCompany 

    def get_shares_float(self):
        return self.__mSharesFloat 

    def get_shares_outstanding(self):
        return self.__mSharesOutstanding 

    def get_implied_shares_outstanding(self):
        return self.__mImpliedSharesOutstanding 

    def get_perc_shares_insiders(self):
        return self.__mPercSharesInsiders 

    def get_perc_shares_institutions(self):
        return self.__mPercSharesInstitutions 

    def get_shares_short(self):
        return self.__mSharesShort 

    def get_short_ratio(self):
        return self.__mShortRatio 

    def get_perc_short_of_float(self):
        return self.__mPercShortOfFloat 

    def get_perc_short_of_outstanding(self):
        return self.__mPercShortOfOutstanding 

    def get_trailing_price_earnings(self):
        return self.__mTrailingPriceEarnings 

    def get_forward_price_earnings(self):
        return self.__mForwardPriceEarnings 

    def get_peg_ratioFiveYears(self):
        return self.__mPEGRatioFiveYears 

    def get_price_to_sales(self):
        return self.__mPriceToSales 

    def get_price_to_book(self):
        return self.__mPriceToBook 

    def get_return_on_equity(self):
        return self.__mReturnOnEquity 

    def get_diluted_eps(self):
        return self.__mDilutedEPS 

    def get_book_value_per_share(self):
        return self.__mBookValuePerShare 

    def get_one_year_target_estimated(self):
        return self.__mOneYearTargetEstimated 

    def get_beta(self):
        return self.__mBeta 

    def get_fifty_days_moving_avg(self):
        return self.__mFiftyDaysMovingAvg 

    def get_two_hundreds_days_moving_avg(self):
        return self.__mTwoHundredsDaysMovingAvg 

    def get_last_split_factor(self):
        return self.__mLastSplitFactor 

    def get_last_split_date(self):
        return self.__mLastSplitDate 

    def get_net_income_to_common_shares(self):
        return self.__mNetIncomeToCommonShares 

    def get_has_pre_post_market_data(self):
        return self.__mHasPrePostMarketData

    def get_ex_dividend_date(self):
	    return self.__mExDividendDate

    def get_dividend_date(self):
        return self.__mDividendDate

    def get_dividend(self):
        return self.__mDividend

    def get_payout_ratio(self):
        return self.__mPayoutRatio

    def get_forward_annual_dividend_rate(self):
        return self.__mForwardAnnualDividendRate

    def get_perc_forward_annual_dividend_yeld(self):
        return self.__mPercForwardAnnualDividendYeld

    def get_trailing_annual_dividend_rate(self):
        return self.__mTrailingAnnualDividendRate

    def get_trailing_annual_dividend_yeld(self):
        return self.__mTrailingAnnualDividendYeld

    def get_five_year_avg_dividend_yeld(self):
        return self.__mFiveYearAvgDividendYeld

    def get_dividend_rate():
        return self.__mDividendRate

    def get_enterprise_value(self):
	    return self.__mEnterpriseValue

    def get_pe_ratio(self):
        return self.__mPeRatio

    def get_peg_ratio(self):
        return self.__mPegRatio

    def get_pb_ratio(self):
        return self.__mPbRatio

    def get_enterprises_value_revenue_ratio(self):
        return self.__mEnterprisesValueRevenueRatio

    def get_enterprises_value_ebitda_ratio(self):
        return self.__mEnterprisesValueEBITDARatio

    def get_average_analyst_rating(self):
	    return self.__mAverageAnalystRating

    def get_market_change_percent(self):
        return self.__mMarketChangePercent

    def get_pre_market_price(self):
        return self.__mPreMarketPrice

    def get_post_market_change_percent(self):
        return self.__mPostMarketChangePercent

    def get_post_market_time(self):
        return self.__mPostMarketTime

    def get_post_market_price(self):
        return self.__mPostMarketPrice

    def get_post_market_change(self):
        return self.__mPostMarketChange

    def get_earnings_timestamp(self):
        return self.__mEarningsTimestamp
        
    def get_eps_trailing_twelve_months(self):
	    return self.__mEpsTrailingTwelveMonths

    def get_eps_forward(self):
        return self.__mEpsForward

    def get_eps_current_year(self):
        return self.__mEpsCurrentYear

    def get_price_eps_current_year_ratio(self):
        return self.__mPriceEpsCurrentYearRatio 
#endregion

#region - Setter Methods
    def set_ask(self, ask):
	    self.__mAsk = ask

    def set_ask_size(self, size):
        self.__mAskSize = size

    def set_bid(self, bid):
        self.__mBid = bid

    def set_bid_size(self, size):
        self.__mBidSize = size

    def set_company(self, company):
        self.__mCompany = company

    def set_shares_float(self, sharesFloat):
        self.__mSharesFloat = sharesFloat

    def set_shares_outstanding(self, sharesOutstanding):
        self.__mSharesOutstanding = sharesOutstanding

    def set_implied_shares_outstanding(self, impliedSharesOutstanding):
        self.__mImpliedSharesOutstanding = impliedSharesOutstanding

    def set_perc_shares_insiders(self, percSharesInsiders):
        self.__mPercSharesInsiders = percSharesInsiders

    def set_perc_shares_institutions(self, percSharesInstitutions):
        self.__mPercSharesInstitutions = percSharesInstitutions

    def set_shares_short(self, sharesShort):
        self.__mSharesShort = sharesShort

    def set_short_ratio(self, shortRatio):
        self.__mShortRatio = shortRatio

    def set_perc_short_of_float(self, percShortOfFloat):
        self.__mPercShortOfFloat = percShortOfFloat

    def set_perc_short_of_outstanding(self, percShortOfOutstanding):
        self.__mPercShortOfOutstanding = percShortOfOutstanding

    def set_trailing_price_earnings(self, trailingPriceEarnings):
        self.__mTrailingPriceEarnings = trailingPriceEarnings

    def set_forward_price_earnings(self, forwardPriceEarnings):
        self.__mForwardPriceEarnings = forwardPriceEarnings

    def set_peg_ratio_five_years(self, pEGRatioFiveYears):
        self.__mPEGRatioFiveYears = pEGRatioFiveYears

    def set_price_to_sales(self, priceToSales):
        self.__mPriceToSales = priceToSales

    def set_price_to_book(self, priceToBook):
        self.__mPriceToBook = priceToBook

    def set_return_on_equity(self, returnOnEquity):
        self.__mReturnOnEquity = returnOnEquity

    def set_diluted_eps(self, dilutedEPS):
        self.__mDilutedEPS = dilutedEPS

    def set_book_value_per_share(self, bookValuePerShare):
        self.__mBookValuePerShare = bookValuePerShare

    def set_one_year_target_estimated(self, oneYearTargetEstimated):
        self.__mOneYearTargetEstimated = oneYearTargetEstimated

    def set_beta(self, beta):
        self.__mBeta = beta

    def set_fifty_days_moving_avg(self, fiftyDaysMovingAvg):
        self.__mFiftyDaysMovingAvg = fiftyDaysMovingAvg

    def set_two_hundreds_days_moving_avg(self, twoHundredsDaysMovingAvg):
        self.__mTwoHundredsDaysMovingAvg = twoHundredsDaysMovingAvg

    def set_last_split_factor(self, lastSplitFactor):
        self.__mLastSplitFactor = lastSplitFactor

    def set_last_split_date(self, lastSplitDate):
        self.__mLastSplitDate = lastSplitDate

    def set_net_income_to_common_shares(self, netIncomeToCommonShares):
        self.__mNetIncomeToCommonShares = netIncomeToCommonShares

    def set_has_pre_post_market_data(self, hasPrePostMarketData):
        self.__mHasPrePostMarketData = hasPrePostMarketData

    def set_ex_dividend_date(self, date):
        self.__mExDividendDate = date

    def set_dividend_date(self, date):
        self.__mDividendDate = date

    def set_dividend(self, dividend):
        self.__mDividend = dividend

    def set_payout_ratio(self, payoutRatio):
        self.__mPayoutRatio = payoutRatio

    def set_forward_annual_dividend_rate(self, rate):
        self.__mForwardAnnualDividendRate = rate

    def set_perc_forward_annual_dividend_yeld(self, yeld):
        self.__mPercForwardAnnualDividendYeld = yeld

    def set_trailing_annual_dividend_rate(self, rate):
        self.__mTrailingAnnualDividendRate = rate

    def set_trailing_annual_dividend_yeld(self, yeld):
        self.__mTrailingAnnualDividendYeld = yeld

    def set_five_year_avg_dividend_yeld(self, yeld):
        self.__mFiveYearAvgDividendYeld = yeld

    def set_dividend_rate(self, rate):
        self.__mDividendRate = rate

    def set_enterprise_value(self, enterpriseValue):
	    self.__mEnterpriseValue = enterpriseValue

    def set_pe_ratio(self, peRatio):
        self.__mPeRatio = peRatio

    def set_peg_ratio(self, pegRatio):
        self.__mPegRatio = pegRatio

    def set_pb_ratio(self, pbRatio):
        self.__mPbRatio = pbRatio

    def set_enterprises_value_revenue_ratio(self, enterprisesValueRevenueRatio):
        self.__mEnterprisesValueRevenueRatio = enterprisesValueRevenueRatio

    def set_enterprises_value_ebitda_ratio(self, enterprisesValueEBITDARatio):
        self.__mEnterprisesValueEBITDARatio = enterprisesValueEBITDARatio

    def set_average_analyst_rating(self, averageAnalystRating):
	    self.__mAverageAnalystRating = averageAnalystRating

    def set_market_change_percent(self, marketChangePercent):
        self.__mMarketChangePercent = marketChangePercent

    def set_pre_market_price(self, price):
        self.__mPreMarketPrice = price

    def set_post_market_change_percent(self, postMarketChangePercent):
        self.__mPostMarketChangePercent = postMarketChangePercent

    def set_post_market_time(self, postMarketTime):
        self.__mPostMarketTime = postMarketTime

    def set_post_market_price(self, postMarketPrice):
        self.__mPostMarketPrice = postMarketPrice

    def set_post_market_change(self, postMarketChange):
        self.__mPostMarketChange = postMarketChange

    def set_earnings_timestamp(self, earningsTimestamp):
        self.__mEarningsTimestamp = earningsTimestamp

    def set_eps_trailing_twelve_months(self, epsTralingTwelveMonths):
	    self.__mEpsTrailingTwelveMonths = epsTralingTwelveMonths

    def set_eps_forward(self, epsForward):
        self.__mEpsForward = epsForward

    def set_eps_current_year(self, epsCurrentYear):
        self.__mEpsCurrentYear = epsCurrentYear

    def set_price_eps_current_year_ratio(self, priceEpsCurrentYearRatio):
        self.__mPriceEpsCurrentYearRatio = priceEpsCurrentYearRatio
#endregion
#endregion


    # To String
    def __str__(self):
        return  "####################\n"\
                f"# {Stock.__name__}\n"\
                f"{super().__str__()}\n"\
                f"#- __mAsk: {self.__mAsk}\n"\
                f"#- __mAskSize: {self.__mAskSize}\n"\
                f"#- __mBid: {self.__mBid}\n"\
                f"#- __mBidSize: {self.__mBidSize}\n"\
                f"#- __mCompany: {self.__mCompany}\n"\
                f"#- __mSharesFloat: {self.__mSharesFloat}\n"\
                f"#- __mSharesOutstanding: {self.__mSharesOutstanding}\n"\
                f"#- __mPercSharesInsiders: {self.__mPercSharesInsiders}\n"\
                f"#- __mPercSharesInstitutions: {self.__mPercSharesInstitutions}\n"\
                f"#- __mSharesShort: {self.__mSharesShort}\n"\
                f"#- __mShortRatio: {self.__mShortRatio}\n"\
                f"#- __mPercShortOfFloat: {self.__mPercShortOfFloat}\n"\
                f"#- __mPercShortOfOutstanding: {self.__mPercShortOfOutstanding}\n"\
                f"#- __mTrailingPriceEarnings: {self.__mTrailingPriceEarnings}\n"\
                f"#- __mForwardPriceEarnings: {self.__mForwardPriceEarnings}\n"\
                f"#- __mPEGRatioFiveYears: {self.__mPEGRatioFiveYears}\n"\
                f"#- __mPriceToSales: {self.__mPriceToSales}\n"\
                f"#- __mPriceToBook: {self.__mPriceToBook}\n"\
                f"#- __mReturnOnEquity: {self.__mReturnOnEquity}\n"\
                f"#- __mDilutedEPS: {self.__mDilutedEPS}\n"\
                f"#- __mBookValuePerShare: {self.__mBookValuePerShare}\n"\
                f"#- __mOneYearTargetEstimated: {self.__mOneYearTargetEstimated}\n"\
                f"#- __mBeta: {self.__mBeta}\n"\
                f"#- __mFiftyDaysMovingAvg: {self.__mFiftyDaysMovingAvg}\n"\
                f"#- __mTwoHundredsDaysMovingAvg: {self.__mTwoHundredsDaysMovingAvg}\n"\
                f"#- __mLastSplitFactor: {self.__mLastSplitFactor}\n"\
                f"#- __mLastSplitDate: {self.__mLastSplitDate}\n"\
                f"#- __mNetIncomeToCommonShares: {self.__mNetIncomeToCommonShares}\n"\
                f"#- __mHasPrePostMarketData: {self.__mHasPrePostMarketData}\n"\
                f"#- __mExDividendDate: {self.__mExDividendDate}\n"\
                f"#- __mDividendDate: {self.__mDividendDate}\n"\
                f"#- __mDividend: {self.__mDividend}\n"\
                f"#- __mPayoutRatio: {self.__mPayoutRatio}\n"\
                f"#- __mForwardAnnualDividendRate: {self.__mForwardAnnualDividendRate}\n"\
                f"#- __mPercForwardAnnualDividendYeld: {self.__mPercForwardAnnualDividendYeld}\n"\
                f"#- __mTrailingAnnualDividendRate: {self.__mTrailingAnnualDividendRate}\n"\
                f"#- __mTrailingAnnualDividendYeld: {self.__mTrailingAnnualDividendYeld}\n"\
                f"#- __mFiveYearAvgDividendYeld: {self.__mFiveYearAvgDividendYeld}\n"\
                f"#- __mDividendRate: {self.__mDividendRate}\n"\
                f"#- __mEnterpriseValue: {self.__mEnterpriseValue}\n"\
                f"#- __mPeRatio: {self.__mPeRatio}\n"\
                f"#- __mPegRatio: {self.__mPegRatio}\n"\
                f"#- __mPbRatio: {self.__mPbRatio}\n"\
                f"#- __mEnterprisesValueRevenueRatio: {self.__mEnterprisesValueRevenueRatio}\n"\
                f"#- __mEnterprisesValueEBITDARatio: {self.__mEnterprisesValueEBITDARatio}\n"\
                f"#- __mAverageAnalystRating: {self.__mAverageAnalystRating}\n"\
                f"#- __mMarketChangePercent: {self.__mMarketChangePercent}\n"\
                f"#- __mPreMarketPrice: {self.__mPreMarketPrice}\n"\
                f"#- __mPostMarketChangePercent: {self.__mPostMarketChangePercent}\n"\
                f"#- __mPostMarketTime: {self.__mPostMarketTime}\n"\
                f"#- __mPostMarketPrice: {self.__mPostMarketPrice}\n"\
                f"#- __mPostMarketChange: {self.__mPostMarketChange}\n"\
                f"#- __mEarningsTimestamp: {self.__mEarningsTimestamp}\n"\
                f"#- __mEpsTrailingTwelveMonths: {self.__mEpsTrailingTwelveMonths}\n"\
                f"#- __mEpsForward: {self.__mEpsForward}\n"\
                f"#- __mEpsCurrentYear: {self.__mEpsCurrentYear}\n"\
                f"#- __mPriceEpsCurrentYearRatio: {self.__mPriceEpsCurrentYearRatio}\n"\
                "####################"

class FilterSearchStockPanel(object):

    __mMinPrice = None
    __mMaxPrice = None
    __mMinVolume = None
    __mMaxVolume = None

    __mMaxPriceMover = None
    __mMinPriceMover = None
    __mMaxVolumeMover = None
    __mMinVolumeMover = None

    __mMoverAboveZero = None
    __mMoverAboveFifty = None
    __mMoverAboveHundred = None
    __mMoverBelowZero = None
    __mMoverBelowFifty = None

    __mMoverAboveZeroToTen = None
    __mMoverAboveTenToTwenty = None
    __mMoverAboveTwentyToThirty = None
    __mMoverAboveThirtyToFourty = None

    __mMoverBelowZeroToTen = None
    __mMoverBelowTenToTwenty = None
    __mMoverBelowTwentyToThirty = None
    __mMoverBelowThirtyToFourty = None

    #region - Get Methods
    def get_min_price(self):
        return self.__mMinPrice

    def get_max_price(self):
        return self.__mMaxPrice

    def get_min_volume(self):
        return self.__mMinVolume

    def get_max_volume(self):
        return self.__mMaxVolume

    def get_max_price_mover(self):
        return self.__mMaxPriceMover

    def get_min_price_mover(self):
        return self.__mMinPriceMover

    def get_max_volume_mover(self):
        return self.__mMaxVolumeMover

    def get_min_volume_mover(self):
        return self.__mMinVolumeMover

    def get_mover_above_zero(self):
        return self.__mMoverAboveZero

    def get_mover_above_fifty(self):
        return self.__mMoverAboveFifty

    def get_mover_above_hundred(self):
        return self.__mMoverAboveHundred

    def get_mover_below_zero(self):
        return self.__mMoverBelowZero

    def get_mover_below_fifty(self):
        return self.__mMoverBelowFifty

    def get_mover_above_zero_to_ten(self):
        return self.__mMoverAboveZeroToTen

    def get_mover_above_ten_to_twenty(self):
        return self.__mMoverAboveTenToTwenty

    def get_mover_above_twenty_to_thirty(self):
        return self.__mMoverAboveTwentyToThirty

    def get_mover_above_thirty_to_fourty(self):
        return self.__mMoverAboveThirtyToFourty

    def get_mover_below_zero_to_ten(self):
        return self.__mMoverBelowZeroToTen

    def get_mover_below_ten_to_twenty(self):
        return self.__mMoverBelowTenToTwenty

    def get_mover_below_twenty_to_thirty(self):
        return self.__mMoverBelowTwentyToThirty

    def get_mover_below_thirty_to_fourty(self):
        return self.__mMoverBelowThirtyToFourty
    #endregion

    #region - Set Methods
    def set_min_price(self, minPrice):
        self.__mMinPrice = minPrice

    def set_max_price(self, maxPrice):
        self.__mMaxPrice = maxPrice

    def set_min_volume(self, minVolume):
        self.__mMinVolume = minVolume

    def set_max_volume(self, maxVolume):
        self.__mMaxVolume = maxVolume

    def set_max_price_mover(self, maxPriceMover):
        self.__mMaxPriceMover = maxPriceMover

    def set_min_price_mover(self, minPriceMover):
        self.__mMinPriceMover = minPriceMover

    def set_max_volume_mover(self, maxVolumeMover):
        self.__mMaxVolumeMover = maxVolumeMover

    def set_min_volume_mover(self, minVolumeMover):
        self.__mMinVolumeMover = minVolumeMover

    def set_mover_above_zero(self, moverAboveZero):
        self.__mMoverAboveZero = moverAboveZero

    def set_mover_above_fifty(self, moverAboveFifty):
        self.__mMoverAboveFifty = moverAboveFifty

    def set_mover_above_hundred(self, moverAboveHundred):
        self.__mMoverAboveHundred = moverAboveHundred

    def set_mover_below_zero(self, moverBelowZero):
        self.__mMoverBelowZero = moverBelowZero

    def set_mover_below_fifty(self, moverBelowFifty):
        self.__mMoverBelowFifty = moverBelowFifty

    def set_mover_above_zero_to_ten(self, moverAboveZeroToTen):
        self.__mMoverAboveZeroToTen = moverAboveZeroToTen

    def set_mover_above_ten_to_twenty(self, moverAboveTenToTwenty):
        self.__mMoverAboveTenToTwenty = moverAboveTenToTwenty

    def set_mover_above_twenty_to_thirty(self, moverAboveTwentyToThirty):
        self.__mMoverAboveTwentyToThirty = moverAboveTwentyToThirty

    def set_mover_above_thirty_to_fourty(self, moverAboveThirtyToFourty):
        self.__mMoverAboveThirtyToFourty = moverAboveThirtyToFourty

    def set_mover_below_zero_to_ten(self, moverBelowZeroToTen):
        self.__mMoverBelowZeroToTen = moverBelowZeroToTen

    def set_mover_below_ten_to_twenty(self, moverBelowTenToTwenty):
        self.__mMoverBelowTenToTwenty = moverBelowTenToTwenty

    def set_mover_below_twenty_to_thirty(self, moverBelowTwentyToThirty):
        self.__mMoverBelowTwentyToThirty = moverBelowTwentyToThirty

    def set_mover_below_thirty_to_fourty(self, moverBelowThirtyToFourty):
        self.__mMoverBelowThirtyToFourty = moverBelowThirtyToFourty
    #endregion

#region Public Methods
    def to_dict(self):
        return {"mMinPrice" : self.__mMinPrice, "mMaxPrice": self.__mMaxPrice, "mMinVolume" : self.__mMinVolume, 
                "mMaxVolume": self.__mMaxVolume, "mMaxPriceMover" : self.__mMaxPriceMover,
                "mMaxPriceMover" : self.__mMaxPriceMover, "mMinPriceMover" : self.__mMinPriceMover,
                "mMaxVolumeMover" : self.__mMaxVolumeMover, "mMinVolumeMover"  : self.__mMinVolumeMover,
                "mMoverAboveZero" : self.__mMoverAboveZero, "mMoverAboveFifty" : self.__mMoverAboveFifty, "mMoverAboveHundred" : self.__mMoverAboveHundred,
                "mMoverBelowZero" : self.__mMoverBelowZero, "mMoverBelowFifty" : self.__mMoverBelowFifty,
                "mMoverAboveZeroToTen": self.__mMoverAboveZeroToTen,
                "mMoverAboveTenToTwenty": self.__mMoverAboveTenToTwenty, "mMoverAboveTwentyToThirty" : self.__mMoverAboveTwentyToThirty,
                "mMoverAboveThirtyToFourty": self.__mMoverAboveThirtyToFourty,  "mMoverBelowZeroToTen" : self.__mMoverBelowZeroToTen,
                "mMoverBelowTenToTwenty": self.__mMoverBelowTenToTwenty, "mMoverBelowTwentyToThirty" : self.__mMoverBelowTwentyToThirty,
                "mMoverBelowThirtyToFourty": self.__mMoverBelowThirtyToFourty
                }

    def from_json(self, json):
        self.set_min_price(json["mMinPrice"])
        self.set_max_price(json["mMaxPrice"])
        self.set_min_volume(json["mMinVolume"])
        self.set_max_volume(json["mMaxVolume"])
        self.set_max_price_mover(json["mMaxPriceMover"])
        self.set_min_price_mover(json["mMinPriceMover"])
        self.set_max_volume_mover(json["mMaxVolumeMover"])
        self.set_min_volume_mover(json["mMinVolumeMover"])
        self.set_mover_above_zero(json["mMoverAboveZero"])
        self.set_mover_above_fifty(json["mMoverAboveFifty"])
        self.set_mover_above_hundred(json["mMoverAboveHundred"])
        self.set_mover_below_zero(json["mMoverBelowZero"])
        self.set_mover_below_fifty(json["mMoverBelowFifty"])
        self.set_mover_above_zero_to_ten(json["mMoverAboveZeroToTen"])
        self.set_mover_above_ten_to_twenty(json["mMoverAboveTenToTwenty"])
        self.set_mover_above_twenty_to_thirty(json["mMoverAboveTwentyToThirty"])
        self.set_mover_above_thirty_to_fourty(json["mMoverAboveThirtyToFourty"])
        self.set_mover_below_zero_to_ten(json["mMoverBelowZeroToTen"])
        self.set_mover_below_ten_to_twenty(json["mMoverBelowTenToTwenty"])
        self.set_mover_below_twenty_to_thirty(json["mMoverBelowTwentyToThirty"])
        self.set_mover_below_thirty_to_fourty(json["mMoverBelowThirtyToFourty"])
#enderegion

    # To String
    def __str__(self):
        return  "####################\n"\
                f"# {FilterSearchStockPanel.__name__}\n"\
                f"#- __mMinPrice: {self.__mMinPrice}\n"\
                f"#- __mMaxPrice: {self.__mMaxPrice}\n"\
                f"#- __mMinVolume: {self.__mMinVolume}\n"\
                f"#- __mMaxVolume: {self.__mMaxVolume}\n"\
                f"#- __mMaxPriceMover: {self.__mMaxPriceMover}\n"\
                f"#- __mMaxVolumeMover: {self.__mMaxVolumeMover}\n"\
                f"#- __mMinVolumeMover: {self.__mMinVolumeMover}\n"\
                f"#- __mMoverAboveZero: {self.__mMoverAboveZero}\n"\
                f"#- __mMoverAboveFifty: {self.__mMoverAboveFifty}\n"\
                f"#- __mMoverBelowZero: {self.__mMoverBelowZero}\n"\
                f"#- __mMoverBelowFifty: {self.__mMoverBelowFifty}\n"\
                f"#- __mMoverAboveZeroToTen: {self.__mMoverAboveZeroToTen}\n"\
                f"#- __mMoverAboveTenToTwenty: {self.__mMoverAboveTenToTwenty}\n"\
                f"#- __mMoverAboveTwentyToThirty: {self.__mMoverAboveTwentyToThirty}\n"\
                f"#- __mMoverAboveThirtyToFourty: {self.__mMoverAboveThirtyToFourty}\n"\
                f"#- __mMoverBelowZeroToTen: {self.__mMoverBelowZeroToTen}\n"\
                f"#- __mMoverBelowTenToTwenty: {self.__mMoverBelowTenToTwenty}\n"\
                f"#- __mMoverBelowTwentyToThirty: {self.__mMoverBelowTwentyToThirty}\n"\
                f"#- __mMoverBelowTwentyToThirty: {self.__mMoverBelowTwentyToThirty}\n"\
                "####################"

class StockView(object):
    
    __mStock : Stock = None
    __mQuarterlyMarketCap = None
    __mTrailingMarketCap = None
    __mQuarterlyEnterpriseValue = None
    __mTrailingEnterpriseValue = None
    __mQuarterlyPeRatio = None
    __mTrailingPeRatio = None
    __mQuarterlyForwardPeRatio = None
    __mTrailingForwardPeRatio = None
    __mQuarterlyPegRatio = None
    __mTrailingPegRatio = None
    __mQuarterlyPsRatio = None
    __mTrailingPsRatio = None
    __mQuarterlyPbRatio = None
    __mTrailingPbRatio = None
    __mQuarterlyEnterprisesValueRevenueRatio = None
    __mTrailingEnterprisesValueRevenueRatio = None
    __mQuarterlyEnterprisesValueEBITDARatio = None
    __mTrailingEnterprisesValueEBITDARatio = None

    __mTimestamps = None
    __mVolumes = None
    __mOpens = None
    __mCloses = None

#region - Get Methods
    def get_stock(self):
        return self.__mStock

    def get_quarterly_market_cap(self):
        return self.__mQuarterlyMarketCap

    def get_trailing_market_cap(self):
        return self.__mTrailingMarketCap

    def get_quarterly_enterprise_value(self):
        return self.__mQuarterlyEnterpriseValue

    def get_trailing_enterprise_value(self):
        return self.__mTrailingEnterpriseValue

    def get_quarterly_forward_pe_ratio(self):
        return self.__mQuarterlyForwardPeRatio

    def get_trailing_forward_pe_ratio(self):
        return self.__mTrailingForwardPeRatio

    def get_quarterly_pe_ratio(self):
        return self.__mQuarterlyPeRatio

    def get_trailing_pe_ratio(self):
        return self.__mTrailingPeRatio

    def get_quarterly_ps_ratio(self):
        return self.__mQuarterlyPsRatio

    def get_quarterly_forward_pe_ratio(self):
        return self.__mQuarterlyForwardPeRatio

    def get_trailing_forward_pe_ratio(self):
        return self.__mTrailingForwardPeRatio

    def get_quarterly_peg_ratio(self):
        return self.__mQuarterlyPegRatio

    def get_trailing_peg_ratio(self):
        return self.__mTrailingPegRatio

    def get_quarterly_ps_ratio(self):
        return self.__mQuarterlyPsRatio

    def get_trailing_ps_ratio(self):
        return self.__mTrailingPsRatio

    def get_quarterly_pb_ratio(self):
        return self.__mQuarterlyPbRatio

    def get_trailing_pb_ratio(self):
        return self.__mTrailingPbRatio

    def get_quarterly_enterprises_value_revenue_ratio(self):
        return self.__mQuarterlyEnterprisesValueRevenueRatio

    def get_trailing_enterprises_value_revenue_ratio(self):
        return self.__mTrailingEnterprisesValueRevenueRatio

    def get_quarterly_enterprises_value_ebitda_ratio(self):
        return self.__mQuarterlyEnterprisesValueEBITDARatio

    def get_trailing_enterprises_value_ebitda_ratio(self):
        return self.__mTrailingEnterprisesValueEBITDARatio

    def get_timestamps(self):
    	return self.__mTimestamps

    def get_volumes(self):
        return self.__mVolumes

    def get_opens(self):
        return self.__mOpens

    def get_closes(self):
        return self.__mCloses
#endregion

#region - Set Methods
    def set_stock(self, stock):
        self.__mStock = stock

    def set_quarterly_market_cap(self, stockQuarterlyMarketCap):
        self.__mStock__mQuarterlyMarketCap = stockQuarterlyMarketCap

    def set_trailing_market_cap(self, trailingMarketCap):
        self.__mTrailingMarketCap = trailingMarketCap

    def set_quarterly_enterprise_value(self, quarterlyEnterpriseValue):
        self.__mQuarterlyEnterpriseValue = quarterlyEnterpriseValue

    def set_trailing_enterprise_value(self, trailingEnterpriseValue):
        self.__mTrailingEnterpriseValue = trailingEnterpriseValue

    def set_quarterly_forward_pe_ratio(self, quarterlyForwardPeRatio):
        self.__mQuarterlyForwardPeRatio = quarterlyForwardPeRatio

    def set_trailing_forward_pe_ratio(self, trailingForwardPeRatio):
        self.__mTrailingForwardPeRatio = trailingForwardPeRatio

    def set_quarterly_pe_ratio(self, quarterlyPeRatio):
        self.__mQuarterlyPeRatio = quarterlyPeRatio

    def set_trailing_pe_ratio(self, trailingPeRatio):
        self.__mTrailingPeRatio = trailingPeRatio

    def set_quarterly_ps_ratio(self, quarterlyPsRatio):
        self.__mQuarterlyPsRatio = quarterlyPsRatio

    def set_quarterly_forward_pe_ratio(self, quarterlyForwardPeRatio):
        self.__mQuarterlyForwardPeRatio = quarterlyForwardPeRatio

    def set_trailing_forward_pe_ratio(self, trailingForwardPeRatio):
        self.__mTrailingForwardPeRatio = trailingForwardPeRatio

    def set_quarterly_peg_ratio(self, quarterlyPegRatio):
        self.__mQuarterlyPegRatio = quarterlyPegRatio

    def set_trailing_peg_ratio(self, trailingPegRatio):
        self.__mTrailingPegRatio = trailingPegRatio

    def set_quarterly_ps_ratio(self, quarterlyPsRatio):
        self.__mQuarterlyPsRatio = quarterlyPsRatio

    def set_trailing_ps_ratio(self, ratio):
        self.__mTrailingPsRatio = ratio

    def set_quarterly_pb_ratio(self, ratio):
        self.__mQuarterlyPbRatio = ratio

    def set_trailing_pb_ratio(self, trailingPbRatio):
        self.__mTrailingPbRatio = trailingPbRatio

    def set_quarterly_enterprises_value_revenue_ratio(self, quarterlyEnterprisesValueRevenueRatio):
        self.__mQuarterlyEnterprisesValueRevenueRatio = quarterlyEnterprisesValueRevenueRatio

    def set_trailing_enterprises_value_revenue_ratio(self, trailingEnterprisesValueRevenueRatio):
        self.__mTrailingEnterprisesValueRevenueRatio = trailingEnterprisesValueRevenueRatio

    def set_quarterly_enterprises_value_ebitda_ratio(self, quarterlyEnterprisesValueEBITDARatio):
        self.__mQuarterlyEnterprisesValueEBITDARatio = quarterlyEnterprisesValueEBITDARatio

    def set_trailing_enterprises_value_ebitda_ratio(self, trailingEnterprisesValueEBITDARatio):
        self.__mTrailingEnterprisesValueEBITDARatio = trailingEnterprisesValueEBITDARatio

    def set_timestamps(self, timestamps):
	    self.__mTimestamps = timestamps

    def set_volumes(self, volume):
        self.__mVolumes = volume

    def set_opens(self, opens):
        self.__mOpens = opens

    def set_closes(self, closes):
        self.__mCloses = closes
#endregion


    # To String
    def __str__(self):
        return  "####################\n"\
                f"# {StockView.__name__}\n"\
                f"#- __mStock: {str(self.__mStock)}\n"\
                f"#- __mQuarterlyMarketCap:\t\t\t\t\t\t{yaml.dump(self.get_quarterly_market_cap())}\n"\
                f"#- __mTrailingMarketCap:\t\t{yaml.dump(self.get_trailing_market_cap())}\n"\
                f"#- __mQuarterlyEnterpriseValue:\t\t{yaml.dump(self.get_quarterly_enterprise_value())}\n"\
                f"#- __mTrailingEnterpriseValue:\t\t{yaml.dump(self.get_trailing_enterprise_value())}\n"\
                f"#- __mQuarterlyPeRatio:\t\t{yaml.dump(self.get_quarterly_pe_ratio())}\n"\
                f"#- __mTrailingPeRatio:\t\t{yaml.dump(self.get_trailing_pe_ratio())}\n"\
                f"#- __mQuarterlyForwardPeRatio:\t\t{yaml.dump(self.get_quarterly_forward_pe_ratio())}\n"\
                f"#- __mTrailingForwardPeRatio:\t\t{yaml.dump(self.get_quarterly_forward_pe_ratio())}\n"\
                f"#- __mQuarterlyPegRatio:\t\t{yaml.dump(self.get_quarterly_peg_ratio())}\n"\
                f"#- __mTrailingPegRatio:\t\t{yaml.dump(self.get_trailing_peg_ratio())}\n"\
                f"#- __mQuarterlyPsRatio:\t\t{yaml.dump(self.get_quarterly_ps_ratio())}\n"\
                f"#- __mTrailingPsRatio:\t\t{yaml.dump(self.get_trailing_ps_ratio())}\n"\
                f"#- __mQuarterlyPbRatio:\t\t{yaml.dump(self.get_quarterly_pb_ratio())}\n"\
                f"#- __mTrailingPbRatio:\t\t{yaml.dump(self.get_trailing_pb_ratio())}\n"\
                f"#- __mQuarterlyEnterprisesValueRevenueRatio:\t\t{yaml.dump(self.get_quarterly_enterprises_value_revenue_ratio())}\n"\
                f"#- __mTrailingEnterprisesValueRevenueRatio:\t\t{yaml.dump(self.get_trailing_enterprises_value_revenue_ratio())}\n"\
                f"#- __mQuarterlyEnterprisesValueEBITDARatio:\t\t{yaml.dump(self.get_quarterly_enterprises_value_ebitda_ratio())}\n"\
                f"#- __mTrailingEnterprisesValueEBITDARatio:\t\t{yaml.dump(self.get_trailing_enterprises_value_ebitda_ratio())}\n"\
                f"#- __mTimestamps: {self.__mTimestamps}\n"\
                f"#- __mVolumes: {self.__mVolumes}\n"\
                f"#- __mOpens: {self.__mOpens}\n"\
                f"#- __mCloses: {self.__mCloses}\n"\
                "####################"

class DateUtils(object):

    def convert_date_to_unix(datestr, dateFormat):
        oDatetime = datetime.strptime(datestr, dateFormat)
        return oDatetime.timestamp()

    def convert_date_to_unix_date_format_standard(datestr):
        oDatetime = datetime.strptime(datestr, '%d/%m/%Y %H:%M:%S')
        return oDatetime.timestamp()

    def convert_date_to_unix_date_format_dash_ymdHMs(datestr):
        oDatetime = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        return oDatetime.timestamp()

    def get_current_date_unix_time():
        date = datetime.now()
        return datetime.timestamp(date)

    def get_current_date():
        return datetime.today().replace(microsecond=0)

    def get_current_now():
        return datetime.now().replace(microsecond=0)

    def get_diff_date_days(date, days):
        return date.replace(microsecond=0) - timedelta(days = days)

    def get_diff_date_years(date, years):
        return date - relativedelta(years = years)

TRILLION = 1000000000000
BILLION = 1000000000
MILLION = 1000000
THOUSAND = 1000

class TextUtils(object):

    def remove_point_and_before_point(txt):
        return txt[:txt.find(".")]

    def convert_number_to_millions_form(value):
        if value / TRILLION > 0.1:
            return str(round(value / TRILLION, 2)) + " T."
        elif value / BILLION > 0.1:
            return str(round(value / BILLION, 2)) + " B."
        elif value / MILLION > 0.1:
            return str(round(value / MILLION, 2)) + " m."
        else:
            return str(round(value / THOUSAND, 2)) + " k."

class WxUtils(object):

    def set_font_size(label, size):
        font = label.GetFont()
        font.SetPointSize(size)
        label.SetFont(font)

    def set_font_bold(label):
        font = label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label.SetFont(font)

    def set_font_size_and_bold(label, size):
        font = label.GetFont()
        font.SetPointSize(size)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label.SetFont(font)

    def set_font_size_and_bold_and_roman(label, size):
        font = label.GetFont()
        font.SetPointSize(size)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        font.SetFamily(wx.ROMAN)
        label.SetFont(font)

CHAR_FLOAT_POINT = "."
CHAR_MINUS = "-"

class NumberUtils(object):

    @singledispatch
    def get_num_digits_value(num):
        pass

    @get_num_digits_value.register(int)
    def _(num):
        return len(str(abs(num)))

    @get_num_digits_value.register(float)
    def _(num):
        return len(str(abs(num)).replace('.', ''))

    def check_is_int_or_float(value):
        return type(value) in (int, float)

    def check_input_key_only_numeric_value(value, strng):
        return value.isnumeric() or (value == CHAR_FLOAT_POINT and not CHAR_FLOAT_POINT in strng and len(strng) > 0) or (value == CHAR_MINUS and not CHAR_MINUS in strng and len(strng) == 0)

    def safe_round(value, roundd):
        if value is None:
            return 0
        else:
            return round(value, roundd)

class API(object):
    
#region - API
    URL_API_GOV_GET_SYMBOLS = "https://www.sec.gov/files/company_tickers.json"
    URL_API_STOCKANALYSIS_GET_SYMBOLS = "https://api.stockanalysis.com/api/screener/s/f?m=s&s=asc&c=s,n&i=stocks"
    URL_API_STOCKANALYSIS_GET_SYMBOLS_AND_STOCKS_INFO = "https://api.stockanalysis.com/api/screener/s/f?m=s&s=asc&c=s,n,industry,exchange,marketCap,price,volume&i=stocks"

    URL_API_YAHOO_FINANCE_QUERY2 = "https://query2.finance.yahoo.com/"
    URL_API_YAHOO_FINANCE_GET_CRUMB = "https://query2.finance.yahoo.com/v1/test/getcrumb"
    URL_API_YAHOO_FINANCE_GET_STOCKS_DATA_FROM_SYMBOLS = "https://query1.finance.yahoo.com/v7/finance/spark?symbols={symbols}&range=1d&interval=1d"     # Max 20 Symbols
    URL_API_YAHOO_FINANCE_GET_FUNDAMENTALS_SERIES_STOCK_DATA = "https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{symbol}?merge=false&padTimeSeries=true&period1={periodStart}&period2={periodEnd}&type={type}&lang=en-US&region=US"
    URL_API_YAHOO_FINANCE_SEARCH = "https://query2.finance.yahoo.com/v1/finance/search?q={symbol}"
    URL_API_YAHOO_FINANCE_LIST_OF_CURRENCIES = "https://query2.finance.yahoo.com/v1/finance/currencies"
    URL_API_YAHOO_FINANCE_GET_CHART = "https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?range={range}&interval={interval}"
    URL_API_YAHOO_FINANCE_QUOTE = "https://query2.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols={symbols}&crumb={crumb}"
    URL_API_YAHOO_FINANCE_GET_QUOTE_SUMMARY = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?crumb={crumb}&modules={modules}"
    URL_API_YAHOO_OPTIONS = "https://query2.finance.yahoo.com/v7/finance/options/{symbol}?crumb={crumb}"
#endregion

class Networking(object):

#region - Download Methods
    def download_request_yahoo_finance_get_cookie(headers):
        return requests.get(API.URL_API_YAHOO_FINANCE_QUERY2, headers = headers)

    def download_get_crumb_yahoo_finance(headers):
        return requests.get(API.URL_API_YAHOO_FINANCE_GET_CRUMB, headers = headers).text

    def download_gov_all_stock_symbols(headers):
        return requests.get(API.URL_API_GOV_GET_SYMBOLS, headers = headers).text

    def download_all_stock_analysis_symbols(headers):
        return requests.get(API.URL_API_STOCKANALYSIS_GET_SYMBOLS, headers = headers).text

    def download_stocks_data_from_symbols(symbols, headers):
        return requests.get(API.URL_API_YAHOO_FINANCE_GET_STOCKS_DATA_FROM_SYMBOLS.format(symbols = symbols), headers = headers).text

    def download_fundamentals_timeseries_stock_data(symbol, startTime, endTime, fields, headers):
        return requests.get(API.URL_API_YAHOO_FINANCE_GET_FUNDAMENTALS_SERIES_STOCK_DATA.format(symbol = symbol, periodStart = startTime, periodEnd = endTime, type = fields), headers = headers).text

    def download_quote_of_stock(symbols, crumb, headers):
        return requests.get(API.URL_API_YAHOO_FINANCE_QUOTE.format(symbols = symbols, crumb = crumb), headers = headers).text

    def download_chart(symbol, rangee, interval, headers):
        return requests.get(API.URL_API_YAHOO_FINANCE_GET_CHART.format(symbol = symbol, range = rangee, interval = interval), headers = headers).text
#endregion

class DataSynchronization(object):

#region - Public Methods
    def sync_all_stocks_and_symbols(progressDialog):
        stocks = []            
        try:
            symbols = DataSynchronization.__sync_get_all_stocks_symbols(progressDialog)
            cookie = DataSynchronization.__get_cookie_yahoo_finance_fake_request()
            crumb = DataSynchronization.__get_crumb_yahoo_finance(cookie)
            stocks = DataSynchronization.__sync_initial_all_stocks_data(symbols, crumb, progressDialog)
        except:
            return stocks
        return stocks

    def sync_single_stock_full_data(stock):
        stockView = StockView()
        DataSynchronization.__sync_single_get_fundamentals_series_stock_data(stockView, stock)
        DataSynchronization.__sync_chart(stock.get_sign(), APIConstants.VALUE_1D, APIConstants.VALUE_1M, stockView)

        cookie = DataSynchronization.__get_cookie_yahoo_finance_fake_request()
        crumb = DataSynchronization.__get_crumb_yahoo_finance(cookie)
        DataSynchronization.__sync_quote_of_stock(stock.get_sign(), crumb, stock)

        stockView.set_stock(stock)
        return stockView

    def sync_update_all_stocks(stocks):
        ss = DataSynchronization.__update_all_stocks_data(stocks)
        data = []
        for s in ss:
            if s is not None:
                data.append(s)
        return data

    def sync_get_chart(symbol, rnge, interval):
        stockView = StockView()
        DataSynchronization.__sync_chart(symbol, rnge, interval, stockView)
        return stockView
#endregion

#region - Private Methods
#region - Initial Stock Sync Methods
    def __sync_get_all_stocks_symbols(progressDialog):
        j = json.loads(Networking.download_all_stock_analysis_symbols(APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX))
        symbols = []
        if j[APIConstants.FIELD_STATUS] == 200:
            for d in j[APIConstants.FIELD_DATA][APIConstants.FIELD_DATA]:
                symbols.append(d[APIConstants.FIELD_S])

        jj = json.loads(Networking.download_gov_all_stock_symbols(APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX))
        if jj:
            for i in range(0, 9690):
                if str(i) in jj.keys():
                    if jj[str(i)]["ticker"] not in symbols:
                        symbols.append(jj[str(i)]["ticker"])
                else:
                    break
        
        return symbols

        
    def __sync_initial_all_stocks_data(symbols, crumb, progressDialog):
        arrStocks = []

        for i in range(0, len(symbols), 500):
            DataSynchronization.__sync_initial_stocks_data(crumb, symbols[i:i+500], arrStocks)
            progressDialog.Update(round((i * 100) / len(symbols)))

        
        if len(symbols) % 500 != 0:
            DataSynchronization.__sync_initial_stocks_data(crumb, symbols[-(len(symbols) % 500):], arrStocks)
        progressDialog.Update(100)

        return arrStocks

    def __sync_initial_stocks_data(crumb, symbols, arrStocks):
        jj = json.loads(Networking.download_quote_of_stock(",".join(symbols), crumb, APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX))

        if jj is not None:
            for j in jj[APIConstants.FIELD_QUOTE_RESPONSE][APIConstants.FIELD_RESULT]:
                
                company = Company(uuid.uuid4())
                stock = Stock(uuid.uuid4())
                exchange = Exchange(uuid.uuid4())

                if APIConstants.FIELD_LONG_NAME not in j and APIConstants.FIELD_SHORT_NAME not in j:
                    continue

                if APIConstants.FIELD_LONG_NAME in j:                    
                    company.set_name(j[APIConstants.FIELD_LONG_NAME])
                
                if APIConstants.FIELD_SHORT_NAME in j:
                    company.set_short_name(j[APIConstants.FIELD_SHORT_NAME])
                    stock.set_name(j[APIConstants.FIELD_SHORT_NAME])

                if company.get_name() is not None and company.get_short_name() is None:
                    company.set_short_name(company.get_name())
                    stock.set_name(company.get_name())
                elif company.get_name() is None and company.get_short_name() is not None:
                    company.set_name(company.get_short_name())

                stock.set_company(company)

                stock.set_sign(j[APIConstants.FIELD_SYMBOL])

                if APIConstants.FIELD_CURRENCY in j:
                    exchange.set_currency(j[APIConstants.FIELD_CURRENCY])
                elif APIConstants.FIELD_FINANCIAL_CURRENCY in j:
                    exchange.set_currency(j[APIConstants.FIELD_FINANCIAL_CURRENCY])

                if APIConstants.FIELD_EXCHANGE in j:
                    exchange.set_name(j[APIConstants.FIELD_EXCHANGE])

                if APIConstants.FIELD_FULL_EXCHANGE_NAME in j:
                    exchange.set_full_name(j[APIConstants.FIELD_FULL_EXCHANGE_NAME])

                stock.set_exchange(exchange)

                if APIConstants.FIELD_PRE_MARKET_PRICE in j:
                    stock.set_pre_market_price(j[APIConstants.FIELD_PRE_MARKET_PRICE])
                else:
                    stock.set_pre_market_price(None)

                if APIConstants.FIELD_HAS_PRE_POST_MARKET_DATA in j:
                    stock.set_has_pre_post_market_data(j[APIConstants.FIELD_HAS_PRE_POST_MARKET_DATA])
                
                if APIConstants.FIELD_FIRST_TRADE_DATE_MILLISECONDS in j:
                    stock.set_first_trade_date(j[APIConstants.FIELD_FIRST_TRADE_DATE_MILLISECONDS])

                if APIConstants.FIELD_DISPLAY_NAME in j:
                    stock.set_name(j[APIConstants.FIELD_DISPLAY_NAME])

                if APIConstants.FIELD_REGULAR_MARKET_PRICE in j:
                    stock.set_price(j[APIConstants.FIELD_REGULAR_MARKET_PRICE])

                if APIConstants.FIELD_REGULAR_MARKET_DAY_HIGH in j:
                    stock.set_day_max(j[APIConstants.FIELD_REGULAR_MARKET_DAY_HIGH])

                if APIConstants.FIELD_REGULAR_MARKET_DAY_LOW in j:
                    stock.set_day_min(j[APIConstants.FIELD_REGULAR_MARKET_DAY_LOW])

                if APIConstants.FIELD_REGULAR_MARKET_VOLUME in j:
                    stock.set_volume(j[APIConstants.FIELD_REGULAR_MARKET_VOLUME])

                if APIConstants.FIELD_REGULAR_MARKET_PREVIOUS_CLOSE in j:
                    stock.set_price_previous_close(j[APIConstants.FIELD_REGULAR_MARKET_PREVIOUS_CLOSE])

                if APIConstants.FIELD_ASK in j:
                    stock.set_ask(j[APIConstants.FIELD_ASK])

                if APIConstants.FIELD_ASK_SIZE in j:
                    stock.set_ask_size(j[APIConstants.FIELD_ASK_SIZE])

                if APIConstants.FIELD_BID in j:
                    stock.set_bid(j[APIConstants.FIELD_BID])

                if APIConstants.FIELD_BID_SIZE in j:
                    stock.set_bid_size(j[APIConstants.FIELD_BID_SIZE])
                    
                if APIConstants.FIELD_AVG_DAILY_VOLUME_TEN_DAYS in j:
                    stock.set_avg_volume_ten_days(j[APIConstants.FIELD_AVG_DAILY_VOLUME_TEN_DAYS])

                if APIConstants.FIELD_AVG_DAILY_VOLUME_THREE_MONTH in j:
                    stock.set_avg_volume_three_months(j[APIConstants.FIELD_AVG_DAILY_VOLUME_THREE_MONTH])

                if APIConstants.FIELD_FIFTY_TWO_WEEK_RANGE in j:
                    stock.set_fifty_two_weeks_range(j[APIConstants.FIELD_FIFTY_TWO_WEEK_RANGE])

                if APIConstants.FIELD_FIFTY_TWO_WEEK_HIGH in j:
                    stock.set_fifty_two_weeks_high(j[APIConstants.FIELD_FIFTY_TWO_WEEK_HIGH])

                if APIConstants.FIELD_FIFTY_TWO_WEEK_LOW in j:
                    stock.set_fifty_two_weeks_low(j[APIConstants.FIELD_FIFTY_TWO_WEEK_LOW])

                if APIConstants.FIELD_FIFTY_TWO_WEEK_CHANGE_PERCENT in j:
                    stock.set_fifty_two_weeks_perc_change(j[APIConstants.FIELD_FIFTY_TWO_WEEK_CHANGE_PERCENT])

                if APIConstants.FIELD_SHARES_OUTSTANDING in j:
                    stock.set_shares_outstanding(j[APIConstants.FIELD_SHARES_OUTSTANDING])

                if APIConstants.FIELD_PRICE_TO_BOOK in j:
                    stock.set_price_to_book(j[APIConstants.FIELD_PRICE_TO_BOOK])

                if APIConstants.FIELD_MARKET_CAP in j:
                    stock.set_market_cap(j[APIConstants.FIELD_MARKET_CAP])

                if APIConstants.FIELD_AVERAGE_ANALYST_RATING in j:
                    stock.set_average_analyst_rating(j[APIConstants.FIELD_AVERAGE_ANALYST_RATING])

                if APIConstants.FIELD_REGULAR_MARKET_CHANGE_PERCENT in j:
                    stock.set_market_change_percent(j[APIConstants.FIELD_REGULAR_MARKET_CHANGE_PERCENT])

                if APIConstants.FIELD_POST_MARKET_CHANGE_PERCENT in j:
                    stock.set_post_market_change_percent(j[APIConstants.FIELD_POST_MARKET_CHANGE_PERCENT])

                if APIConstants.FIELD_POST_MARKET_TIME in j:
                    stock.set_post_market_time(j[APIConstants.FIELD_POST_MARKET_TIME])

                if APIConstants.FIELD_POST_MARKET_PRICE in j:
                    stock.set_post_market_price(j[APIConstants.FIELD_POST_MARKET_PRICE])
                else:
                    stock.set_post_market_price(None)

                if APIConstants.FIELD_EARNINGS_TIMESTAMP in j:
                    stock.set_earnings_timestamp(j[APIConstants.FIELD_EARNINGS_TIMESTAMP])

                if APIConstants.FIELD_BOOK_VALUE in j:
                    stock.set_book_value_per_share(j[APIConstants.FIELD_BOOK_VALUE])

                if APIConstants.FIELD_EPS_TRAILING_TWELVE_MONTHS in j:
                    stock.set_eps_trailing_twelve_months(j[APIConstants.FIELD_EPS_TRAILING_TWELVE_MONTHS])

                if APIConstants.FIELD_EPS_FORWARD in j:
                    stock.set_eps_forward(j[APIConstants.FIELD_EPS_FORWARD])

                if APIConstants.FIELD_EPS_CURRENT_YEAR in j:
                    stock.set_eps_current_year(j[APIConstants.FIELD_EPS_CURRENT_YEAR])

                if APIConstants.FIELD_PRICE_EPS_CURRENT_YEAR in j:
                    stock.set_price_eps_current_year_ratio(j[APIConstants.FIELD_PRICE_EPS_CURRENT_YEAR])

                if APIConstants.FIELD_FORWARD_PE in j:
                    stock.set_forward_price_earnings(j[APIConstants.FIELD_FORWARD_PE])

                if APIConstants.FIELD_TRAILING_PE in j:
                    stock.set_trailing_price_earnings(j[APIConstants.FIELD_TRAILING_PE])

                if APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_RATE in j:
                    stock.set_trailing_annual_dividend_rate(j[APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_RATE])

                if APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_YELD in j:
                    stock.set_trailing_annual_dividend_yeld(j[APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_YELD])

                if APIConstants.FIELD_DIVIDEND_DATE in j:
                    stock.set_dividend_date(j[APIConstants.FIELD_DIVIDEND_DATE])

                if APIConstants.FIELD_DIVIDEND_RATE in j:
                    stock.set_dividend_rate(j[APIConstants.FIELD_DIVIDEND_RATE])

                arrStocks.append(stock)
#endregion

#region - Single Stock Sync Methods
    def __sync_single_get_fundamentals_series_stock_data(stockView, stock):
        j = json.loads(Networking.download_fundamentals_timeseries_stock_data(stock.get_sign(), 
            TextUtils.remove_point_and_before_point(str(DateUtils.convert_date_to_unix_date_format_dash_ymdHMs(str(DateUtils.get_diff_date_years(DateUtils.get_current_date(), 1))))),
            TextUtils.remove_point_and_before_point(str(DateUtils.get_current_date_unix_time())), 
            ",".join(APIConstants.FIELDS_API_GET_FUNDAMENTALS_SERIES_STOCK), APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX))

        for jj in j[APIConstants.FIELD_TIMESERIES][APIConstants.FIELD_RESULT]:
            for attr in APIConstants.FIELDS_API_GET_FUNDAMENTALS_SERIES_STOCK:
                if attr in jj:
                    match attr:
                        case APIConstants.FIELD_QUARTERLY_MARKET_CAP:
                            stockView.set_quarterly_market_cap(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_TRAILING_MARKET_CAP:
                            stockView.set_trailing_market_cap(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_QUARTERLY_ENTERPRISE_VALUE:
                            stockView.set_quarterly_enterprise_value(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_TRAILING_ENTERPRISE_VALUE:
                            stockView.set_trailing_enterprise_value(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))
                            try:
                                stock.set_enterprise_value(jj[attr][len(jj[attr]) - 1][APIConstants.FIELD_REPORTED_VALUE][APIConstants.FIELD_RAW])
                            except:
                                print("Json Exception")

                        case APIConstants.FIELD_QUARTERLY_PE_RATIO:
                            stockView.set_quarterly_pe_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_TRALING_PE_RATIO:
                            stockView.set_trailing_pe_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))
                            try:
                                stock.set_pe_ratio(jj[attr][len(jj[attr]) - 1][APIConstants.FIELD_REPORTED_VALUE][APIConstants.FIELD_RAW])
                            except:
                                print("Json Exception")

                        case APIConstants.FIELD_QUARTERLY_FORWARD_PE_RATIO:
                            stockView.set_quarterly_forward_pe_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_TRALING_FORWARD_PE_RATIO:
                            stockView.set_trailing_forward_pe_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_QUARTERLY_PEG_RATIO:
                            stockView.set_quarterly_peg_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_TRAILING_PEG_RATIO:
                            stockView.set_trailing_peg_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))
                            try:
                                stock.set_peg_ratio(jj[attr][len(jj[attr]) - 1][APIConstants.FIELD_REPORTED_VALUE][APIConstants.FIELD_RAW])
                            except:
                                print("Json Exception")

                        case APIConstants.FIELD_QUARTERLY_PS_RATIO:
                            stockView.set_quarterly_ps_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_TRALING_PS_RATIO:
                            stockView.set_trailing_pe_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_QUARTERLY_PB_RATIO:
                            stockView.set_quarterly_pb_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_TRAILING_PB_RATIO:
                            stockView.set_trailing_pb_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))
                            try:
                                stock.set_pb_ratio(jj[attr][len(jj[attr]) - 1][APIConstants.FIELD_REPORTED_VALUE][APIConstants.FIELD_RAW])
                            except:
                                print("Json Exception")

                        case APIConstants.FIELD_QUARTERLY_ENTERPRISES_VALUE_REVENUE_RATIO:
                            stockView.set_quarterly_enterprises_value_revenue_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_TRAILING_ENTERPRISES_VALUE_REVENUE_RATIO:
                            stockView.set_trailing_enterprises_value_revenue_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))
                            try:
                                stock.set_enterprises_value_revenue_ratio(jj[attr][len(jj[attr]) - 1][APIConstants.FIELD_REPORTED_VALUE][APIConstants.FIELD_RAW])
                            except:
                                print("Json Exception")

                        case APIConstants.FIELD_QUARTERLY_ENTERPRISES_VALUE_EBITDA_RATIO:
                            stockView.set_quarterly_enterprises_value_ebitda_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))

                        case APIConstants.FIELD_QUARTERLY_TRAILING_ENTERPRESISES_VALUE_EBITDA_RATIO:
                            stockView.set_trailing_enterprises_value_ebitda_ratio(DataSynchronization.__init_and_elaborate_value_dictionary_single_stock_full_data(jj[attr]))
                            try:
                                stock.set_enterprises_value_ebitda_ratio(jj[attr][len(jj[attr]) - 1][APIConstants.FIELD_REPORTED_VALUE][APIConstants.FIELD_RAW])
                            except:
                                print("Json Exception")

    def __sync_chart(symbol, rnge, interval, stockView):
        jj = json.loads(Networking.download_chart(symbol, rnge, interval, APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX))

        for j in jj[APIConstants.FIELD_CHART][APIConstants.FIELD_RESULT]:
            timestamps = []

            if APIConstants.FIELD_TIMESTAMP in j:
                for t in j[APIConstants.FIELD_TIMESTAMP]:
                    if rnge == APIConstants.VALUE_1D:
                        timestamps.append(datetime.utcfromtimestamp(t).strftime('%H:%M:%S'))
                    else:
                        timestamps.append(datetime.utcfromtimestamp(t).strftime('%d/%m/%Y %H:%M:%S'))

            stockView.set_timestamps(timestamps)
            
            for n in j[APIConstants.FIELD_INDICATORS][APIConstants.FIELD_QUOTE]:
                if APIConstants.FIELD_VOLUME in n:
                    stockView.set_volumes(n[APIConstants.FIELD_VOLUME])
                
                if APIConstants.FIELD_CLOSE in n:
                    stockView.set_closes(n[APIConstants.FIELD_CLOSE])

                if APIConstants.FIELD_OPEN in n:
                    stockView.set_opens(n[APIConstants.FIELD_OPEN])

    def __init_and_elaborate_value_dictionary_single_stock_full_data(jj):
        dicti = {}
        for e in jj:
            if e is not None:
                dicti[e[APIConstants.FIELD_AS_OF_DATE]] = {}
                dicti[e[APIConstants.FIELD_AS_OF_DATE]][APIConstants.FIELD_RAW] = e[APIConstants.FIELD_REPORTED_VALUE][APIConstants.FIELD_RAW]
                dicti[e[APIConstants.FIELD_AS_OF_DATE]][APIConstants.FIELD_FMT] = e[APIConstants.FIELD_REPORTED_VALUE][APIConstants.FIELD_FMT]
        return dicti

    def __get_cookie_yahoo_finance_fake_request():
        res = Networking.download_request_yahoo_finance_get_cookie(APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX)
        return res.headers[APIConstants.HEADER_SET_COOKIE][0:res.headers[APIConstants.HEADER_SET_COOKIE].index(";")]

    def __get_crumb_yahoo_finance(cookie):
        headers = APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX
        headers[APIConstants.HEADER_COOKIE] = cookie
        crumb = Networking.download_get_crumb_yahoo_finance(headers)
        return crumb

    def __sync_quote_of_stock(symbol, crumb, stock):
        jj = json.loads(Networking.download_quote_of_stock(symbol, crumb, APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX))
        
        if jj is not None:
            for j in jj[APIConstants.FIELD_QUOTE_RESPONSE][APIConstants.FIELD_RESULT]:
                
                if APIConstants.FIELD_DISPLAY_NAME in j:
                    stock.set_name(j[APIConstants.FIELD_DISPLAY_NAME])

                stock.set_price(j[APIConstants.FIELD_REGULAR_MARKET_PRICE])
                stock.set_day_max(j[APIConstants.FIELD_REGULAR_MARKET_DAY_HIGH])
                stock.set_day_min(j[APIConstants.FIELD_REGULAR_MARKET_DAY_LOW])
                stock.set_volume(j[APIConstants.FIELD_REGULAR_MARKET_VOLUME])
                stock.set_price_previous_close(j[APIConstants.FIELD_REGULAR_MARKET_PREVIOUS_CLOSE])

                if APIConstants.FIELD_ASK in j:
                    stock.set_ask(j[APIConstants.FIELD_ASK])
                    
                stock.set_ask_size(j[APIConstants.FIELD_ASK_SIZE])
                stock.set_bid(j[APIConstants.FIELD_BID])
                stock.set_bid_size(j[APIConstants.FIELD_BID_SIZE])
                stock.set_avg_volume_ten_days(j[APIConstants.FIELD_AVG_DAILY_VOLUME_TEN_DAYS])
                stock.set_avg_volume_three_months(j[APIConstants.FIELD_AVG_DAILY_VOLUME_THREE_MONTH])
                stock.set_fifty_two_weeks_range(j[APIConstants.FIELD_FIFTY_TWO_WEEK_RANGE])
                stock.set_fifty_two_weeks_high(j[APIConstants.FIELD_FIFTY_TWO_WEEK_HIGH])
                stock.set_fifty_two_weeks_low(j[APIConstants.FIELD_FIFTY_TWO_WEEK_LOW])
                stock.set_fifty_two_weeks_perc_change(j[APIConstants.FIELD_FIFTY_TWO_WEEK_CHANGE_PERCENT])

                stock.set_shares_outstanding(j[APIConstants.FIELD_SHARES_OUTSTANDING])
                stock.set_price_to_book(j[APIConstants.FIELD_PRICE_TO_BOOK])

                stock.set_market_cap(j[APIConstants.FIELD_MARKET_CAP])

                if APIConstants.FIELD_AVERAGE_ANALYST_RATING in j:
                    stock.set_average_analyst_rating(j[APIConstants.FIELD_AVERAGE_ANALYST_RATING])

                stock.set_market_change_percent(j[APIConstants.FIELD_REGULAR_MARKET_CHANGE_PERCENT])

                if APIConstants.FIELD_PRE_MARKET_PRICE in j:
                    stock.set_pre_market_price(j[APIConstants.FIELD_PRE_MARKET_PRICE])
                else:
                    stock.set_pre_market_price(None)

                if APIConstants.FIELD_POST_MARKET_CHANGE_PERCENT in j:
                    stock.set_post_market_change_percent(j[APIConstants.FIELD_POST_MARKET_CHANGE_PERCENT])

                if APIConstants.FIELD_POST_MARKET_TIME in j:
                    stock.set_post_market_time(j[APIConstants.FIELD_POST_MARKET_TIME])
                
                if APIConstants.FIELD_POST_MARKET_PRICE in j:
                    stock.set_post_market_price(j[APIConstants.FIELD_POST_MARKET_PRICE])
                else:
                    stock.set_post_market_price(None)

                if APIConstants.FIELD_EARNINGS_TIMESTAMP in j:
                    stock.set_earnings_timestamp(j[APIConstants.FIELD_EARNINGS_TIMESTAMP])

                stock.set_book_value_per_share(j[APIConstants.FIELD_BOOK_VALUE])

                if APIConstants.FIELD_EPS_TRAILING_TWELVE_MONTHS in j:
                    stock.set_eps_trailing_twelve_months(j[APIConstants.FIELD_EPS_TRAILING_TWELVE_MONTHS])

                if APIConstants.FIELD_EPS_FORWARD in j:
                    stock.set_eps_forward(j[APIConstants.FIELD_EPS_FORWARD])

                if APIConstants.FIELD_EPS_CURRENT_YEAR in j:
                    stock.set_eps_current_year(j[APIConstants.FIELD_EPS_CURRENT_YEAR])

                if APIConstants.FIELD_PRICE_EPS_CURRENT_YEAR in j:
                    stock.set_price_eps_current_year_ratio(j[APIConstants.FIELD_PRICE_EPS_CURRENT_YEAR])

                if APIConstants.FIELD_FORWARD_PE in j:
                    stock.set_forward_price_earnings(j[APIConstants.FIELD_FORWARD_PE])

                if APIConstants.FIELD_TRAILING_PE in j:
                    stock.set_trailing_price_earnings(j[APIConstants.FIELD_TRAILING_PE])

                stock.set_trailing_annual_dividend_rate(j[APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_RATE])
                stock.set_trailing_annual_dividend_yeld(j[APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_YELD])

                if APIConstants.FIELD_DIVIDEND_DATE in j:
                    stock.set_dividend_date(j[APIConstants.FIELD_DIVIDEND_DATE])

                if APIConstants.FIELD_DIVIDEND_RATE in j:
                    stock.set_dividend_rate(j[APIConstants.FIELD_DIVIDEND_RATE])
#endregion

#region - Sync All Stocks Data Methods
    def __update_all_stocks_data(stocks):        
        cookie = DataSynchronization.__get_cookie_yahoo_finance_fake_request()
        crumb = DataSynchronization.__get_crumb_yahoo_finance(cookie)

        for i in range(0, len(stocks), 500):
            DataSynchronization.__update_stock_data(crumb, stocks[i:i+500])

        if len(stocks) % 500 != 0:
            DataSynchronization.__update_stock_data(crumb, stocks[-(len(stocks) % 500):])

        return stocks

    def __update_stock_data(crumb, stocks):
        symbols = []
        for s in stocks:
            if s is not None:
                symbols.append(s.get_sign())

        jj = json.loads(Networking.download_quote_of_stock(",".join(symbols), crumb, APIConstants.HEADERS_APP_JSON_TEXT_PLAIN_MOZILLA_UBUNTU_FIREFOX))

        if jj is not None:
            for i in range(0, len(jj[APIConstants.FIELD_QUOTE_RESPONSE][APIConstants.FIELD_RESULT])):
                stock = stocks[i]

                j = jj[APIConstants.FIELD_QUOTE_RESPONSE][APIConstants.FIELD_RESULT][i]

                if APIConstants.FIELD_PRE_MARKET_PRICE in j:
                    stock.set_pre_market_price(j[APIConstants.FIELD_PRE_MARKET_PRICE])
                else:
                    stock.set_pre_market_price(None)

                if APIConstants.FIELD_HAS_PRE_POST_MARKET_DATA in j:
                    stock.set_has_pre_post_market_data(j[APIConstants.FIELD_HAS_PRE_POST_MARKET_DATA])

                if APIConstants.FIELD_REGULAR_MARKET_PRICE in j:
                    stock.set_price(j[APIConstants.FIELD_REGULAR_MARKET_PRICE])

                if APIConstants.FIELD_REGULAR_MARKET_DAY_HIGH in j:
                    stock.set_day_max(j[APIConstants.FIELD_REGULAR_MARKET_DAY_HIGH])

                if APIConstants.FIELD_REGULAR_MARKET_DAY_LOW in j:
                    stock.set_day_min(j[APIConstants.FIELD_REGULAR_MARKET_DAY_LOW])

                if APIConstants.FIELD_REGULAR_MARKET_VOLUME in j:
                    stock.set_volume(j[APIConstants.FIELD_REGULAR_MARKET_VOLUME])

                if APIConstants.FIELD_REGULAR_MARKET_PREVIOUS_CLOSE in j:
                    stock.set_price_previous_close(j[APIConstants.FIELD_REGULAR_MARKET_PREVIOUS_CLOSE])

                if APIConstants.FIELD_ASK in j:
                    stock.set_ask(j[APIConstants.FIELD_ASK])

                if APIConstants.FIELD_ASK_SIZE in j:
                    stock.set_ask_size(j[APIConstants.FIELD_ASK_SIZE])

                if APIConstants.FIELD_BID in j:
                    stock.set_bid(j[APIConstants.FIELD_BID])

                if APIConstants.FIELD_BID_SIZE in j:
                    stock.set_bid_size(j[APIConstants.FIELD_BID_SIZE])
                    
                if APIConstants.FIELD_AVG_DAILY_VOLUME_TEN_DAYS in j:
                    stock.set_avg_volume_ten_days(j[APIConstants.FIELD_AVG_DAILY_VOLUME_TEN_DAYS])

                if APIConstants.FIELD_AVG_DAILY_VOLUME_THREE_MONTH in j:
                    stock.set_avg_volume_three_months(j[APIConstants.FIELD_AVG_DAILY_VOLUME_THREE_MONTH])

                if APIConstants.FIELD_FIFTY_TWO_WEEK_RANGE in j:
                    stock.set_fifty_two_weeks_range(j[APIConstants.FIELD_FIFTY_TWO_WEEK_RANGE])

                if APIConstants.FIELD_FIFTY_TWO_WEEK_HIGH in j:
                    stock.set_fifty_two_weeks_high(j[APIConstants.FIELD_FIFTY_TWO_WEEK_HIGH])

                if APIConstants.FIELD_FIFTY_TWO_WEEK_LOW in j:
                    stock.set_fifty_two_weeks_low(j[APIConstants.FIELD_FIFTY_TWO_WEEK_LOW])

                if APIConstants.FIELD_FIFTY_TWO_WEEK_CHANGE_PERCENT in j:
                    stock.set_fifty_two_weeks_perc_change(j[APIConstants.FIELD_FIFTY_TWO_WEEK_CHANGE_PERCENT])

                if APIConstants.FIELD_SHARES_OUTSTANDING in j:
                    stock.set_shares_outstanding(j[APIConstants.FIELD_SHARES_OUTSTANDING])

                if APIConstants.FIELD_PRICE_TO_BOOK in j:
                    stock.set_price_to_book(j[APIConstants.FIELD_PRICE_TO_BOOK])

                if APIConstants.FIELD_MARKET_CAP in j:
                    stock.set_market_cap(j[APIConstants.FIELD_MARKET_CAP])

                if APIConstants.FIELD_AVERAGE_ANALYST_RATING in j:
                    stock.set_average_analyst_rating(j[APIConstants.FIELD_AVERAGE_ANALYST_RATING])

                if APIConstants.FIELD_REGULAR_MARKET_CHANGE_PERCENT in j:
                    stock.set_market_change_percent(j[APIConstants.FIELD_REGULAR_MARKET_CHANGE_PERCENT])

                if APIConstants.FIELD_POST_MARKET_CHANGE_PERCENT in j:
                    stock.set_post_market_change_percent(j[APIConstants.FIELD_POST_MARKET_CHANGE_PERCENT])

                if APIConstants.FIELD_POST_MARKET_TIME in j:
                    stock.set_post_market_time(j[APIConstants.FIELD_POST_MARKET_TIME])

                if APIConstants.FIELD_POST_MARKET_PRICE in j:
                    stock.set_post_market_price(j[APIConstants.FIELD_POST_MARKET_PRICE])
                else:
                    stock.set_post_market_price(None)

                if APIConstants.FIELD_EARNINGS_TIMESTAMP in j:
                    stock.set_earnings_timestamp(j[APIConstants.FIELD_EARNINGS_TIMESTAMP])

                if APIConstants.FIELD_BOOK_VALUE in j:
                    stock.set_book_value_per_share(j[APIConstants.FIELD_BOOK_VALUE])

                if APIConstants.FIELD_EPS_TRAILING_TWELVE_MONTHS in j:
                    stock.set_eps_trailing_twelve_months(j[APIConstants.FIELD_EPS_TRAILING_TWELVE_MONTHS])

                if APIConstants.FIELD_EPS_FORWARD in j:
                    stock.set_eps_forward(j[APIConstants.FIELD_EPS_FORWARD])

                if APIConstants.FIELD_EPS_CURRENT_YEAR in j:
                    stock.set_eps_current_year(j[APIConstants.FIELD_EPS_CURRENT_YEAR])

                if APIConstants.FIELD_PRICE_EPS_CURRENT_YEAR in j:
                    stock.set_price_eps_current_year_ratio(j[APIConstants.FIELD_PRICE_EPS_CURRENT_YEAR])

                if APIConstants.FIELD_FORWARD_PE in j:
                    stock.set_forward_price_earnings(j[APIConstants.FIELD_FORWARD_PE])

                if APIConstants.FIELD_TRAILING_PE in j:
                    stock.set_trailing_price_earnings(j[APIConstants.FIELD_TRAILING_PE])

                if APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_RATE in j:
                    stock.set_trailing_annual_dividend_rate(j[APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_RATE])

                if APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_YELD in j:
                    stock.set_trailing_annual_dividend_yeld(j[APIConstants.FIELD_TRAILING_ANNUAL_DIVIDEND_YELD])

                if APIConstants.FIELD_DIVIDEND_DATE in j:
                    stock.set_dividend_date(j[APIConstants.FIELD_DIVIDEND_DATE])

                if APIConstants.FIELD_DIVIDEND_RATE in j:
                    stock.set_dividend_rate(j[APIConstants.FIELD_DIVIDEND_RATE])
#endregion
#endregion

class StoppableThread(threading.Thread):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class StocksViewList(wx.ListCtrl):

    LIST_COLUMNS = ["%", "Symbol", "Name", "Price"]
    LIST_COLUMNS_SIZES = [75, 75, 250, 100]

    __mCallback = None
    __mFilterData = None
    __mFilterName = None
    __mItems: [Stock] = None
    __mFilteredItems: [Stock] = None

    def __init__(self, parent, id, style, width, callback):
        wx.ListCtrl.__init__(self, parent, id, style=style)
        self.__mCallback = callback
        self.__mWidth = width
        self.__mItems = []

#region - Get Methods
    def get_items(self):
        return self.__mItems

    def set_items(self, items):
        self.__mItems = items

    def get_filtered_items(self):
        return self.__mFilteredItems

    def add_item(self, item):
        self.__mItems.append(item)
#endregion

#region - Set Methods
    def set_filter_data(self, filter):
        self.__mFilterData = filter
#enderegion

#region - Public Methods
    def init_layout(self):
        for i in range(0, len(self.LIST_COLUMNS_SIZES)):
            self.InsertColumn(i, self.LIST_COLUMNS[i])
            self.SetColumnWidth(i, self.LIST_COLUMNS_SIZES[i])

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)

    def add_items_and_populate(self, items):
        self.__mItems = items
        self.__mFilteredItems = items
        self.filter_items()
        self.populate_list()

    def populate_list(self):
        self.DeleteAllItems()
        if self.__mFilteredItems:
            for i in range(0, len(self.__mFilteredItems)):
                item = self.__mFilteredItems[i]
                if item.get_market_change_percent() is not None and item.get_market_change_percent() > 0:
                    self.InsertItem(i, "+" + str(round(item.get_market_change_percent(), 2)))
                else:
                    if item.get_market_change_percent() is not None:
                        self.InsertItem(i, str(round(item.get_market_change_percent(), 2)))
                    else:
                        self.InsertItem(i, str(0))
                self.SetItem(i, 1, str(item.get_sign()))
                self.SetItem(i, 2, str(item.get_company().get_name()))
                self.SetItem(i, 3, str(item.get_price()))

    def on_item_selected(self, event):
        if self.__mCallback is not None:
            self.__mCurrentItem = self.__mFilteredItems[event.Index]
            self.__mCallback(self.__mCurrentItem)

    def filter_items_by_name(self, ffilter):
        self.__mFilterName = ffilter
        self.filter_items()

    def filter_items(self):
        for item in self.__mItems:
            if item.get_market_change_percent() is None:
                item.set_market_change_percent(0)
            if item.get_volume() is None:
                item.set_volume(0) 
        self.filter_name()
        if self.__mFilterData is not None:
            self.filter_prices()
            self.filter_order()
        self.populate_list()

    def filter_name(self):
        if self.__mFilterName:
            self.__mFilteredItems = []
            for item in self.__mItems:
                if self.__mFilterName.lower() in item.get_sign().lower() or self.__mFilterName.lower() in item.get_company().get_name().lower() or self.__mFilterName.lower() in item.get_exchange().get_full_name().lower():
                    self.__mFilteredItems.append(item)
        else:
            self.__mFilteredItems = self.__mItems

    def filter_order(self):
        if self.__mFilterData.get_max_price_mover():
            pos = -1
            for i in range(0, len(self.__mFilteredItems)):
                one = self.__mFilteredItems[i]
                for j in range(i + 1, len(self.__mFilteredItems)):
                    two = self.__mFilteredItems[j]
                    if one.get_market_change_percent() < two.get_market_change_percent():
                        one = two
                        pos = j
                temp = self.__mFilteredItems[i]
                self.__mFilteredItems[i] = one
                self.__mFilteredItems[pos] = temp

        if self.__mFilterData.get_min_price_mover():
            pos = -1
            for i in range(0, len(self.__mFilteredItems)):
                one = self.__mFilteredItems[i]
                for j in range(i + 1, len(self.__mFilteredItems)):
                    two = self.__mFilteredItems[j]
                    if one.get_market_change_percent() > two.get_market_change_percent():
                        one = two
                        pos = j
                temp = self.__mFilteredItems[i]
                self.__mFilteredItems[i] = one
                self.__mFilteredItems[pos] = temp

        if self.__mFilterData.get_max_volume_mover():
            pos = -1
            for i in range(0, len(self.__mFilteredItems)):
                one = self.__mFilteredItems[i]
                for j in range(i + 1, len(self.__mFilteredItems)):
                    two = self.__mFilteredItems[j]
                    if one.get_volume() < two.get_volume():
                        one = two
                        pos = j
                temp = self.__mFilteredItems[i]
                self.__mFilteredItems[i] = one
                self.__mFilteredItems[pos] = temp

        if self.__mFilterData.get_min_volume_mover():
            pos = -1
            for i in range(0, len(self.__mFilteredItems)):
                one = self.__mFilteredItems[i]
                for j in range(i + 1, len(self.__mFilteredItems)):
                    two = self.__mFilteredItems[j]
                    if one.get_volume() > two.get_volume():
                        one = two
                        pos = j
                temp = self.__mFilteredItems[i]
                self.__mFilteredItems[i] = one
                self.__mFilteredItems[pos] = temp

    def filter_prices(self):
        if self.__mFilterData is not None:
            items = []
            for item in self.__mFilteredItems:
                if self.__mFilterData.get_min_price():
                    if item.get_price() >= float(self.__mFilterData.get_min_price()):
                        items.append(item)

                if self.__mFilterData.get_max_price():
                    if item.get_price() <= float(self.__mFilterData.get_max_price()):
                        items.append(item)

                if self.__mFilterData.get_min_volume():
                    if item.get_volume() >= float(self.__mFilterData.get_min_volume()):
                        items.append(item)

                if self.__mFilterData.get_max_volume():
                    if item.get_volume() <= float(self.__mFilterData.get_max_volume()):
                        items.append(item)

                if self.__mFilterData.get_mover_above_zero():
                    if item.get_market_change_percent() >= 0:
                        items.append(item)

                if self.__mFilterData.get_mover_above_fifty():
                    if item.get_market_change_percent() >= 50:
                        items.append(item)

                if self.__mFilterData.get_mover_above_hundred():
                    if item.get_market_change_percent() >= 100:
                        items.append(item)

                if self.__mFilterData.get_mover_below_zero():
                    if item.get_market_change_percent() <= 0:
                        items.append(item)

                if self.__mFilterData.get_mover_below_fifty():
                    if item.get_market_change_percent() <= -50:
                        items.append(item)

                if self.__mFilterData.get_mover_above_zero_to_ten():
                    if item.get_market_change_percent() >= 0 and item.get_market_change_percent() <= 10:
                        items.append(item)

                if self.__mFilterData.get_mover_above_ten_to_twenty():
                    if item.get_market_change_percent() >= 10 and item.get_market_change_percent() <= 20:
                        items.append(item)

                if self.__mFilterData.get_mover_above_twenty_to_thirty():
                    if item.get_market_change_percent() >= 20 and item.get_market_change_percent() <= 30:
                        items.append(item)

                if self.__mFilterData.get_mover_above_thirty_to_fourty():
                    if item.get_market_change_percent() >= 30 and item.get_market_change_percent() <= 40:
                        items.append(item)

                if self.__mFilterData.get_mover_below_zero_to_ten():
                    if item.get_market_change_percent() <= 0 and item.get_market_change_percent() >= -10:
                        items.append(item)

                if self.__mFilterData.get_mover_below_ten_to_twenty():
                    if item.get_market_change_percent() <= -10 and item.get_market_change_percent() >= -20:
                        items.append(item)

                if self.__mFilterData.get_mover_below_twenty_to_thirty():
                    if item.get_market_change_percent() <= -20 and item.get_market_change_percent() >= -30:
                        items.append(item)

                if self.__mFilterData.get_mover_below_thirty_to_fourty():
                    if item.get_market_change_percent() <= -30 and item.get_market_change_percent() >= -40:
                        items.append(item)

                if len(items) > 0:
                    self.__mFilteredItems = items
        else:
            self.__mFilteredItems = self.__mItems

    def unbind_listener(self):
        self.Unbind(wx.EVT_LIST_ITEM_SELECTED)

    def bind_listener(self):
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
#endregion

class BasePanel(wx.Panel, threading.Thread):

    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size = size)
        threading.Thread.__init__(self)
        self.Fit()

#region - Protected Methods
#region - BoxSizer Methods
    def _get_vbs_button(self, panel, text, f):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._get_button(panel, text, f), 0, wx.EXPAND)
        return sizer

    def _get_hbs_button(self, panel, text, f):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._get_button(panel, text, f), 0, wx.EXPAND)
        return sizer
#endregion
#region - Buttons Methods
    def _get_button(self, panel, text, f):
        button = wx.Button(panel, wx.ID_ANY, text)
        button.Bind(wx.EVT_BUTTON, f)
        return button

    def _get_icon_button(self, panel, icon, f):
        button = wx.Button(panel, wx.ID_ANY, style = wx.BU_NOTEXT)
        button.SetBitmap(icon)
        button.Bind(wx.EVT_BUTTON, f)
        return button
#endregion

#region - Message Methods
    def _show_error_message(self, title, msg):
        wx.MessageBox(msg, title, wx.OK | wx.ICON_ERROR)

    def _show_message(self, title, msg):
        wx.MessageBox(msg, title, wx.OK)
#endregion
#endregion

LISTEN_FILTER_STOCK_PANEL = "ListenFiltersStockPanel"

class SearchStockPanel(BasePanel):

    __mMainSizer = None

    __mtxMinPrice = None
    __mtxMaxPrice = None
    __mtxMinVolume = None
    __mtxMaxVolume = None

    __mcbMaxPriceMover = None
    __mcbMinPriceMover = None
    __mcbMaxVolumeMover = None
    __mcbMinVolumeMover = None

    __mcbMoverAboveZero = None
    __mcbMoverAboveFifty = None
    __mcbMoverAboveHundred = None
    __mcbMoverBelowZero = None
    __mcbMoverBelowFifty = None
    __mcbMoverBelowHundred = None

    __mcbMoverAboveZeroToTen = None
    __mcbMoverAboveTenToTwenty = None
    __mcbMoverAboveTwentyThirty = None
    __mcbMoverAboveThirtyFourty = None

    __mcbMoverBelowZeroToTen = None
    __mcbMoverBelowTenToTwenty = None
    __mcbMoverBelowTwentyThirty = None
    __mcbMoverBelowThirtyFourty = None

    __mFilterSearchStockPanel = FilterSearchStockPanel()

    def __init__(self, parent, size, filterData):
        super().__init__(parent, size)
        self.__init_layout()
        self.init_filter_search_stock_panel()

#region - Private Methods
    def __init_layout(self):
        self.__mMainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__mMainSizer.AddSpacer(25)
        
        vbs = wx.BoxSizer(wx.VERTICAL)
        vbs.Add(self.__get_panels_min_max_price(), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_panels_min_max_volume(), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_panels_max_min_movers_volumes(), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_panels_one_percentage_movers(), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_panels_two_percentage_movers(), 0, wx.EXPAND)
        vbs.AddSpacer(100)
        vbs.Add(self.__get_panel_buttons(), 0, wx.EXPAND)

        self.__mMainSizer.Add(vbs, 1, wx.ALL|wx.EXPAND)
        self.__mMainSizer.AddSpacer(25)
        self.SetSizer(self.__mMainSizer)

    def init_filter_search_stock_panel(self):
        self.__mFilterSearchStockPanel.set_min_price(False)
        self.__mFilterSearchStockPanel.set_max_price(False)
        self.__mFilterSearchStockPanel.set_min_volume(False)
        self.__mFilterSearchStockPanel.set_max_volume(False)
        self.__mFilterSearchStockPanel.set_max_price_mover(False)
        self.__mFilterSearchStockPanel.set_min_price_mover(False)
        self.__mFilterSearchStockPanel.set_max_volume_mover(False)
        self.__mFilterSearchStockPanel.set_min_volume_mover(False)
        self.__mFilterSearchStockPanel.set_mover_above_zero(False)
        self.__mFilterSearchStockPanel.set_mover_above_fifty(False)
        self.__mFilterSearchStockPanel.set_mover_above_hundred(False)
        self.__mFilterSearchStockPanel.set_mover_below_zero(False)
        self.__mFilterSearchStockPanel.set_mover_above_zero_to_ten(False)
        self.__mFilterSearchStockPanel.set_mover_above_ten_to_twenty(False)
        self.__mFilterSearchStockPanel.set_mover_above_twenty_to_thirty(False)
        self.__mFilterSearchStockPanel.set_mover_above_thirty_to_fourty(False)
        self.__mFilterSearchStockPanel.set_mover_below_zero_to_ten(False)
        self.__mFilterSearchStockPanel.set_mover_below_ten_to_twenty(False)
        self.__mFilterSearchStockPanel.set_mover_below_twenty_to_thirty(False)
        self.__mFilterSearchStockPanel.set_mover_below_thirty_to_fourty(False)

#region - Min Max Price Methods
    def __get_panels_min_max_price(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_min_price(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_max_price(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_min_price(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(wx.StaticText(panel, label = "Min Price", style = wx.ALIGN_CENTRE), 0, wx.EXPAND)
        self.__mtxMinPrice = wx.TextCtrl(panel, wx.ID_ANY, value = "", style = wx.TE_CENTRE)
        self.__mtxMinPrice.Bind(wx.EVT_CHAR, self.__on_change_text_check_is_int_value)
        main.Add(self.__mtxMinPrice, 0, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_max_price(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(wx.StaticText(panel, label = "Max Price", style = wx.ALIGN_CENTRE), 0, wx.EXPAND)
        self.__mtxMaxPrice = wx.TextCtrl(panel, wx.ID_ANY, value = "", style = wx.TE_CENTRE)
        self.__mtxMaxPrice.Bind(wx.EVT_CHAR, self.__on_change_text_check_is_int_value)
        main.Add(self.__mtxMaxPrice, 0, wx.EXPAND)
        panel.SetSizer(main)
        return panel
#endregion

#region - Min Max Volume Methods
    def __get_panels_min_max_volume(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_min_volume(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_max_volume(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_min_volume(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(wx.StaticText(panel, label = "Min Volume", style = wx.ALIGN_CENTRE), 0, wx.EXPAND)
        self.__mtxMinVolume = wx.TextCtrl(panel, wx.ID_ANY, value = "", style = wx.TE_CENTRE)
        self.__mtxMinVolume.Bind(wx.EVT_CHAR, self.__on_change_text_check_is_int_value)
        main.Add(self.__mtxMinVolume, 0, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_max_volume(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(wx.StaticText(panel, label = "Max Volume", style = wx.ALIGN_CENTRE), 0, wx.EXPAND)
        self.__mtxMaxVolume = wx.TextCtrl(panel, wx.ID_ANY, value = "", style = wx.TE_CENTRE)
        self.__mtxMaxVolume.Bind(wx.EVT_CHAR, self.__on_change_text_check_is_int_value)
        main.Add(self.__mtxMaxVolume, 0, wx.EXPAND)
        panel.SetSizer(main)
        return panel
#endregion

#region - Min Max Movers / Volumes Methods
    def __get_panels_max_min_movers_volumes(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_min_max_movers(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_min_max_volumes(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_min_max_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMaxPriceMover = wx.CheckBox(panel, wx.ID_ANY, label = "Max Mover")
        self.__mcbMaxPriceMover.Bind(wx.EVT_CHECKBOX, self.__on_check_max_mover)
        main.Add(self.__mcbMaxPriceMover, 1, wx.EXPAND)

        self.__mcbMinPriceMover = wx.CheckBox(panel, wx.ID_ANY, label = "Min Mover")
        self.__mcbMinPriceMover.Bind(wx.EVT_CHECKBOX, self.__on_check_min_mover)
        main.Add(self.__mcbMinPriceMover, 1, wx.EXPAND)

        panel.SetSizer(main)
        return panel

    def __get_panel_min_max_volumes(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMaxVolumeMover = wx.CheckBox(panel, wx.ID_ANY, label = "Max Volume")
        self.__mcbMaxVolumeMover.Bind(wx.EVT_CHECKBOX, self.__on_check_max_volume)
        main.Add(self.__mcbMaxVolumeMover, 1, wx.EXPAND)

        self.__mcbMinVolumeMover = wx.CheckBox(panel, wx.ID_ANY, label = "Min Volume")
        self.__mcbMinVolumeMover.Bind(wx.EVT_CHECKBOX, self.__on_check_min_volume)
        main.Add(self.__mcbMinVolumeMover, 1, wx.EXPAND)

        panel.SetSizer(main)
        return panel
#endregion


#region - Percentage Above Below Movers Methods
    def __get_panels_one_percentage_movers(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_one_percentage_above_movers(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_one_percentage_below_movers(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_one_percentage_above_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMoverAboveZero = wx.CheckBox(panel, wx.ID_ANY, label = "> 0% Movers")
        self.__mcbMoverAboveZero.Bind(wx.EVT_CHECKBOX, self.__on_check_above_zero)
        main.Add(self.__mcbMoverAboveZero, 1, wx.EXPAND)

        self.__mcbMoverAboveFifty = wx.CheckBox(panel, wx.ID_ANY, label = "> 50% Movers")
        self.__mcbMoverAboveFifty.Bind(wx.EVT_CHECKBOX, self.__on_check_above_fifty)
        main.Add(self.__mcbMoverAboveFifty, 1, wx.EXPAND)

        self.__mcbMoverAboveHundred = wx.CheckBox(panel, wx.ID_ANY, label = ">100% Movers")
        self.__mcbMoverAboveHundred.Bind(wx.EVT_CHECKBOX, self.__on_check_above_hundred)
        main.Add(self.__mcbMoverAboveHundred, 1, wx.EXPAND)

        panel.SetSizer(main)
        return panel

    def __get_panel_one_percentage_below_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMoverBelowZero = wx.CheckBox(panel, wx.ID_ANY, label = "< 0% Movers")
        self.__mcbMoverBelowZero.Bind(wx.EVT_CHECKBOX, self.__on_check_below_zero)
        main.Add(self.__mcbMoverBelowZero, 1, wx.EXPAND)

        self.__mcbMoverBelowFifty = wx.CheckBox(panel, wx.ID_ANY, label = "< -50% Movers")
        self.__mcbMoverBelowFifty.Bind(wx.EVT_CHECKBOX, self.__on_check_below_fifty)
        main.Add(self.__mcbMoverBelowFifty, 1, wx.EXPAND)

        panel.SetSizer(main)
        return panel
#endregion

#region - Percentage Above Below Movers Methods
    def __get_panels_two_percentage_movers(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_two_percentage_above_movers(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_two_percentage_below_movers(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_two_percentage_above_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMoverAboveZeroToTen = wx.CheckBox(panel, wx.ID_ANY, label = "+0% - 10%")
        self.__mcbMoverAboveZeroToTen.Bind(wx.EVT_CHECKBOX, self.__on_check_above_zero_to_ten)
        main.Add(self.__mcbMoverAboveZeroToTen, 1, wx.EXPAND)

        self.__mcbMoverAboveTenToTwenty = wx.CheckBox(panel, wx.ID_ANY, label = "+10% - 20%")
        self.__mcbMoverAboveTenToTwenty.Bind(wx.EVT_CHECKBOX, self.__on_check_above_ten_to_twenty)
        main.Add(self.__mcbMoverAboveTenToTwenty, 1, wx.EXPAND)

        self.__mcbMoverAboveTwentyThirty = wx.CheckBox(panel, wx.ID_ANY, label = "+20% - 30%")
        self.__mcbMoverAboveTwentyThirty.Bind(wx.EVT_CHECKBOX, self.__on_check_above_twenty_to_thirty)
        main.Add(self.__mcbMoverAboveTwentyThirty, 1, wx.EXPAND)

        self.__mcbMoverAboveThirtyFourty = wx.CheckBox(panel, wx.ID_ANY, label = "+30% - 40%")
        self.__mcbMoverAboveThirtyFourty.Bind(wx.EVT_CHECKBOX, self.__on_click_above_thirty_to_fourty)
        main.Add(self.__mcbMoverAboveThirtyFourty, 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_two_percentage_below_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMoverBelowZeroToTen = wx.CheckBox(panel, wx.ID_ANY, label = "0% - -10%")
        self.__mcbMoverBelowZeroToTen.Bind(wx.EVT_CHECKBOX, self.__on_check_below_zero_to_ten)
        main.Add(self.__mcbMoverBelowZeroToTen, 1, wx.EXPAND)

        self.__mcbMoverBelowTenToTwenty = wx.CheckBox(panel, wx.ID_ANY, label = "-10% - -20%")
        self.__mcbMoverBelowTenToTwenty.Bind(wx.EVT_CHECKBOX, self.__on_check_below_ten_to_twenty)
        main.Add(self.__mcbMoverBelowTenToTwenty, 1, wx.EXPAND)

        self.__mcbMoverBelowTwentyThirty = wx.CheckBox(panel, wx.ID_ANY, label = "-20% - -30%")
        self.__mcbMoverBelowTwentyThirty.Bind(wx.EVT_CHECKBOX, self.__on_check_below_twenty_to_thirty)
        main.Add(self.__mcbMoverBelowTwentyThirty, 1, wx.EXPAND)
        
        self.__mcbMoverBelowThirtyFourty = wx.CheckBox(panel, wx.ID_ANY, label = "-30% - -40%")
        self.__mcbMoverBelowThirtyFourty.Bind(wx.EVT_CHECKBOX, self.__on_check_below_thirty_to_fourty)
        main.Add(self.__mcbMoverBelowThirtyFourty, 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel
#endregion

#region - Get Panel Filter
    def __get_panel_buttons(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        searchButton = super()._get_icon_button(panel, wx.Bitmap(Icons.ICON_SEARCH), self.__on_click_search)
        main.Add(searchButton, 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel
#endregion

#region - Event Handler Methods
    def __on_click_search(self, evt):
        self.__send_data()
        self.GetParent().Destroy()
        self.Layout()

    def __on_change_text_check_is_int_value(self, evt):
        if(KeyboardEventUtils.on_change_text_check_is_int_value(self, evt)):
            match evt.GetEventObject():
                case self.__mtxMinPrice:
                    self.__mFilterSearchStockPanel.set_min_price(self.__mtxMinPrice.GetValue())
                case self.__mtxMaxPrice:
                    self.__mFilterSearchStockPanel.set_max_price(self.__mtxMaxPrice.GetValue())
                case self.__mtxMinVolume:
                    self.__mFilterSearchStockPanel.set_min_volume(self.__mtxMinVolume.GetValue())
                case self.__mtxMaxVolume:
                    self.__mFilterSearchStockPanel.set_max_volume(self.__mtxMaxVolume.GetValue())

    def __on_check_max_mover(self, evt):
        self.__mFilterSearchStockPanel.set_max_price_mover(evt.IsChecked())
        self.__mcbMinPriceMover.SetValue(False)
        self.__mcbMinVolumeMover.SetValue(False)
        self.__mcbMaxVolumeMover.SetValue(False)

    def __on_check_min_mover(self, evt):
        self.__mFilterSearchStockPanel.set_min_price_mover(evt.IsChecked())
        self.__mcbMaxPriceMover.SetValue(False)
        self.__mcbMinVolumeMover.SetValue(False)
        self.__mcbMaxVolumeMover.SetValue(False)

    def __on_check_max_volume(self, evt):
        self.__mFilterSearchStockPanel.set_max_volume_mover(evt.IsChecked())
        self.__mcbMinVolumeMover.SetValue(False)
        self.__mcbMaxPriceMover.SetValue(False)
        self.__mcbMinPriceMover.SetValue(False)

    def __on_check_min_volume(self, evt):
        self.__mFilterSearchStockPanel.set_min_volume_mover(evt.IsChecked())
        self.__mcbMaxVolumeMover.SetValue(False)
        self.__mcbMaxPriceMover.SetValue(False)
        self.__mcbMinPriceMover.SetValue(False)

    def __on_check_above_zero(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_zero(evt.IsChecked())
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_fifty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_fifty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_hundred(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_hundred(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_zero(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_zero(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_fifty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_fifty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_zero_to_ten(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_zero_to_ten(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_ten_to_twenty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_ten_to_twenty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_twenty_to_thirty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_twenty_to_thirty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_click_above_thirty_to_fourty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_thirty_to_fourty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_zero_to_ten(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_zero_to_ten(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_ten_to_twenty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_ten_to_twenty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_twenty_to_thirty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_twenty_to_thirty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_thirty_to_fourty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_thirty_to_fourty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
#endregion

    def __send_data(self):
        j = json.dumps(self.__mFilterSearchStockPanel.to_dict())
        pub.sendMessage(LISTEN_FILTER_STOCK_PANEL, message = json.loads(j))
        self.GetParent().Destroy()

class SearchStockPanel(BasePanel):

    __mMainSizer = None

    __mtxMinPrice = None
    __mtxMaxPrice = None
    __mtxMinVolume = None
    __mtxMaxVolume = None

    __mcbMaxPriceMover = None
    __mcbMinPriceMover = None
    __mcbMaxVolumeMover = None
    __mcbMinVolumeMover = None

    __mcbMoverAboveZero = None
    __mcbMoverAboveFifty = None
    __mcbMoverAboveHundred = None
    __mcbMoverBelowZero = None
    __mcbMoverBelowFifty = None
    __mcbMoverBelowHundred = None

    __mcbMoverAboveZeroToTen = None
    __mcbMoverAboveTenToTwenty = None
    __mcbMoverAboveTwentyThirty = None
    __mcbMoverAboveThirtyFourty = None

    __mcbMoverBelowZeroToTen = None
    __mcbMoverBelowTenToTwenty = None
    __mcbMoverBelowTwentyThirty = None
    __mcbMoverBelowThirtyFourty = None

    __mFilterSearchStockPanel = FilterSearchStockPanel()

    def __init__(self, parent, size, filterData):
        super().__init__(parent, size)
        self.__init_layout()
        self.init_filter_search_stock_panel()

#region - Private Methods
    def __init_layout(self):
        self.__mMainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__mMainSizer.AddSpacer(25)
        
        vbs = wx.BoxSizer(wx.VERTICAL)
        vbs.Add(self.__get_panels_min_max_price(), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_panels_min_max_volume(), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_panels_max_min_movers_volumes(), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_panels_one_percentage_movers(), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_panels_two_percentage_movers(), 0, wx.EXPAND)
        vbs.AddSpacer(100)
        vbs.Add(self.__get_panel_buttons(), 0, wx.EXPAND)

        self.__mMainSizer.Add(vbs, 1, wx.ALL|wx.EXPAND)
        self.__mMainSizer.AddSpacer(25)
        self.SetSizer(self.__mMainSizer)

    def init_filter_search_stock_panel(self):
        self.__mFilterSearchStockPanel.set_min_price(False)
        self.__mFilterSearchStockPanel.set_max_price(False)
        self.__mFilterSearchStockPanel.set_min_volume(False)
        self.__mFilterSearchStockPanel.set_max_volume(False)
        self.__mFilterSearchStockPanel.set_max_price_mover(False)
        self.__mFilterSearchStockPanel.set_min_price_mover(False)
        self.__mFilterSearchStockPanel.set_max_volume_mover(False)
        self.__mFilterSearchStockPanel.set_min_volume_mover(False)
        self.__mFilterSearchStockPanel.set_mover_above_zero(False)
        self.__mFilterSearchStockPanel.set_mover_above_fifty(False)
        self.__mFilterSearchStockPanel.set_mover_above_hundred(False)
        self.__mFilterSearchStockPanel.set_mover_below_zero(False)
        self.__mFilterSearchStockPanel.set_mover_above_zero_to_ten(False)
        self.__mFilterSearchStockPanel.set_mover_above_ten_to_twenty(False)
        self.__mFilterSearchStockPanel.set_mover_above_twenty_to_thirty(False)
        self.__mFilterSearchStockPanel.set_mover_above_thirty_to_fourty(False)
        self.__mFilterSearchStockPanel.set_mover_below_zero_to_ten(False)
        self.__mFilterSearchStockPanel.set_mover_below_ten_to_twenty(False)
        self.__mFilterSearchStockPanel.set_mover_below_twenty_to_thirty(False)
        self.__mFilterSearchStockPanel.set_mover_below_thirty_to_fourty(False)

#region - Min Max Price Methods
    def __get_panels_min_max_price(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_min_price(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_max_price(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_min_price(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(wx.StaticText(panel, label = "Min Price", style = wx.ALIGN_CENTRE), 0, wx.EXPAND)
        self.__mtxMinPrice = wx.TextCtrl(panel, wx.ID_ANY, value = "", style = wx.TE_CENTRE)
        self.__mtxMinPrice.Bind(wx.EVT_CHAR, self.__on_change_text_check_is_int_value)
        main.Add(self.__mtxMinPrice, 0, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_max_price(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(wx.StaticText(panel, label = "Max Price", style = wx.ALIGN_CENTRE), 0, wx.EXPAND)
        self.__mtxMaxPrice = wx.TextCtrl(panel, wx.ID_ANY, value = "", style = wx.TE_CENTRE)
        self.__mtxMaxPrice.Bind(wx.EVT_CHAR, self.__on_change_text_check_is_int_value)
        main.Add(self.__mtxMaxPrice, 0, wx.EXPAND)
        panel.SetSizer(main)
        return panel
#endregion

#region - Min Max Volume Methods
    def __get_panels_min_max_volume(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_min_volume(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_max_volume(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_min_volume(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(wx.StaticText(panel, label = "Min Volume", style = wx.ALIGN_CENTRE), 0, wx.EXPAND)
        self.__mtxMinVolume = wx.TextCtrl(panel, wx.ID_ANY, value = "", style = wx.TE_CENTRE)
        self.__mtxMinVolume.Bind(wx.EVT_CHAR, self.__on_change_text_check_is_int_value)
        main.Add(self.__mtxMinVolume, 0, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_max_volume(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(wx.StaticText(panel, label = "Max Volume", style = wx.ALIGN_CENTRE), 0, wx.EXPAND)
        self.__mtxMaxVolume = wx.TextCtrl(panel, wx.ID_ANY, value = "", style = wx.TE_CENTRE)
        self.__mtxMaxVolume.Bind(wx.EVT_CHAR, self.__on_change_text_check_is_int_value)
        main.Add(self.__mtxMaxVolume, 0, wx.EXPAND)
        panel.SetSizer(main)
        return panel
#endregion

#region - Min Max Movers / Volumes Methods
    def __get_panels_max_min_movers_volumes(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_min_max_movers(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_min_max_volumes(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_min_max_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMaxPriceMover = wx.CheckBox(panel, wx.ID_ANY, label = "Max Mover")
        self.__mcbMaxPriceMover.Bind(wx.EVT_CHECKBOX, self.__on_check_max_mover)
        main.Add(self.__mcbMaxPriceMover, 1, wx.EXPAND)

        self.__mcbMinPriceMover = wx.CheckBox(panel, wx.ID_ANY, label = "Min Mover")
        self.__mcbMinPriceMover.Bind(wx.EVT_CHECKBOX, self.__on_check_min_mover)
        main.Add(self.__mcbMinPriceMover, 1, wx.EXPAND)

        panel.SetSizer(main)
        return panel

    def __get_panel_min_max_volumes(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMaxVolumeMover = wx.CheckBox(panel, wx.ID_ANY, label = "Max Volume")
        self.__mcbMaxVolumeMover.Bind(wx.EVT_CHECKBOX, self.__on_check_max_volume)
        main.Add(self.__mcbMaxVolumeMover, 1, wx.EXPAND)

        self.__mcbMinVolumeMover = wx.CheckBox(panel, wx.ID_ANY, label = "Min Volume")
        self.__mcbMinVolumeMover.Bind(wx.EVT_CHECKBOX, self.__on_check_min_volume)
        main.Add(self.__mcbMinVolumeMover, 1, wx.EXPAND)

        panel.SetSizer(main)
        return panel
#endregion


#region - Percentage Above Below Movers Methods
    def __get_panels_one_percentage_movers(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_one_percentage_above_movers(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_one_percentage_below_movers(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_one_percentage_above_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMoverAboveZero = wx.CheckBox(panel, wx.ID_ANY, label = "> 0% Movers")
        self.__mcbMoverAboveZero.Bind(wx.EVT_CHECKBOX, self.__on_check_above_zero)
        main.Add(self.__mcbMoverAboveZero, 1, wx.EXPAND)

        self.__mcbMoverAboveFifty = wx.CheckBox(panel, wx.ID_ANY, label = "> 50% Movers")
        self.__mcbMoverAboveFifty.Bind(wx.EVT_CHECKBOX, self.__on_check_above_fifty)
        main.Add(self.__mcbMoverAboveFifty, 1, wx.EXPAND)

        self.__mcbMoverAboveHundred = wx.CheckBox(panel, wx.ID_ANY, label = ">100% Movers")
        self.__mcbMoverAboveHundred.Bind(wx.EVT_CHECKBOX, self.__on_check_above_hundred)
        main.Add(self.__mcbMoverAboveHundred, 1, wx.EXPAND)

        panel.SetSizer(main)
        return panel

    def __get_panel_one_percentage_below_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMoverBelowZero = wx.CheckBox(panel, wx.ID_ANY, label = "< 0% Movers")
        self.__mcbMoverBelowZero.Bind(wx.EVT_CHECKBOX, self.__on_check_below_zero)
        main.Add(self.__mcbMoverBelowZero, 1, wx.EXPAND)

        self.__mcbMoverBelowFifty = wx.CheckBox(panel, wx.ID_ANY, label = "< -50% Movers")
        self.__mcbMoverBelowFifty.Bind(wx.EVT_CHECKBOX, self.__on_check_below_fifty)
        main.Add(self.__mcbMoverBelowFifty, 1, wx.EXPAND)

        panel.SetSizer(main)
        return panel
#endregion

#region - Percentage Above Below Movers Methods
    def __get_panels_two_percentage_movers(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        main.Add(self.__get_panel_two_percentage_above_movers(panel), 1, wx.EXPAND)
        main.AddSpacer(25)
        main.Add(self.__get_panel_two_percentage_below_movers(panel), 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_two_percentage_above_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMoverAboveZeroToTen = wx.CheckBox(panel, wx.ID_ANY, label = "+0% - 10%")
        self.__mcbMoverAboveZeroToTen.Bind(wx.EVT_CHECKBOX, self.__on_check_above_zero_to_ten)
        main.Add(self.__mcbMoverAboveZeroToTen, 1, wx.EXPAND)

        self.__mcbMoverAboveTenToTwenty = wx.CheckBox(panel, wx.ID_ANY, label = "+10% - 20%")
        self.__mcbMoverAboveTenToTwenty.Bind(wx.EVT_CHECKBOX, self.__on_check_above_ten_to_twenty)
        main.Add(self.__mcbMoverAboveTenToTwenty, 1, wx.EXPAND)

        self.__mcbMoverAboveTwentyThirty = wx.CheckBox(panel, wx.ID_ANY, label = "+20% - 30%")
        self.__mcbMoverAboveTwentyThirty.Bind(wx.EVT_CHECKBOX, self.__on_check_above_twenty_to_thirty)
        main.Add(self.__mcbMoverAboveTwentyThirty, 1, wx.EXPAND)

        self.__mcbMoverAboveThirtyFourty = wx.CheckBox(panel, wx.ID_ANY, label = "+30% - 40%")
        self.__mcbMoverAboveThirtyFourty.Bind(wx.EVT_CHECKBOX, self.__on_click_above_thirty_to_fourty)
        main.Add(self.__mcbMoverAboveThirtyFourty, 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel

    def __get_panel_two_percentage_below_movers(self, parent):
        panel = wx.Panel(parent)
        main = wx.BoxSizer(wx.HORIZONTAL)
        self.__mcbMoverBelowZeroToTen = wx.CheckBox(panel, wx.ID_ANY, label = "0% - -10%")
        self.__mcbMoverBelowZeroToTen.Bind(wx.EVT_CHECKBOX, self.__on_check_below_zero_to_ten)
        main.Add(self.__mcbMoverBelowZeroToTen, 1, wx.EXPAND)

        self.__mcbMoverBelowTenToTwenty = wx.CheckBox(panel, wx.ID_ANY, label = "-10% - -20%")
        self.__mcbMoverBelowTenToTwenty.Bind(wx.EVT_CHECKBOX, self.__on_check_below_ten_to_twenty)
        main.Add(self.__mcbMoverBelowTenToTwenty, 1, wx.EXPAND)

        self.__mcbMoverBelowTwentyThirty = wx.CheckBox(panel, wx.ID_ANY, label = "-20% - -30%")
        self.__mcbMoverBelowTwentyThirty.Bind(wx.EVT_CHECKBOX, self.__on_check_below_twenty_to_thirty)
        main.Add(self.__mcbMoverBelowTwentyThirty, 1, wx.EXPAND)

        self.__mcbMoverBelowThirtyFourty = wx.CheckBox(panel, wx.ID_ANY, label = "-30% - -40%")
        self.__mcbMoverBelowThirtyFourty.Bind(wx.EVT_CHECKBOX, self.__on_check_below_thirty_to_fourty)
        main.Add(self.__mcbMoverBelowThirtyFourty, 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel
#endregion

#region - Get Panel Filter
    def __get_panel_buttons(self):
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.HORIZONTAL)
        searchButton = super()._get_icon_button(panel, wx.Bitmap(Icons.ICON_SEARCH), self.__on_click_search)
        main.Add(searchButton, 1, wx.EXPAND)
        panel.SetSizer(main)
        return panel
#endregion

#region - Event Handler Methods
    def __on_click_search(self, evt):
        self.__send_data()
        self.GetParent().Destroy()
        self.Layout()

    def __on_change_text_check_is_int_value(self, evt):
        if(KeyboardEventUtils.on_change_text_check_is_int_value(self, evt)):
            match evt.GetEventObject():
                case self.__mtxMinPrice:
                    self.__mFilterSearchStockPanel.set_min_price(self.__mtxMinPrice.GetValue())
                case self.__mtxMaxPrice:
                    self.__mFilterSearchStockPanel.set_max_price(self.__mtxMaxPrice.GetValue())
                case self.__mtxMinVolume:
                    self.__mFilterSearchStockPanel.set_min_volume(self.__mtxMinVolume.GetValue())
                case self.__mtxMaxVolume:
                    self.__mFilterSearchStockPanel.set_max_volume(self.__mtxMaxVolume.GetValue())

    def __on_check_max_mover(self, evt):
        self.__mFilterSearchStockPanel.set_max_price_mover(evt.IsChecked())
        self.__mcbMinPriceMover.SetValue(False)
        self.__mcbMinVolumeMover.SetValue(False)
        self.__mcbMaxVolumeMover.SetValue(False)

    def __on_check_min_mover(self, evt):
        self.__mFilterSearchStockPanel.set_min_price_mover(evt.IsChecked())
        self.__mcbMaxPriceMover.SetValue(False)
        self.__mcbMinVolumeMover.SetValue(False)
        self.__mcbMaxVolumeMover.SetValue(False)

    def __on_check_max_volume(self, evt):
        self.__mFilterSearchStockPanel.set_max_volume_mover(evt.IsChecked())
        self.__mcbMinVolumeMover.SetValue(False)
        self.__mcbMaxPriceMover.SetValue(False)
        self.__mcbMinPriceMover.SetValue(False)

    def __on_check_min_volume(self, evt):
        self.__mFilterSearchStockPanel.set_min_volume_mover(evt.IsChecked())
        self.__mcbMaxVolumeMover.SetValue(False)
        self.__mcbMaxPriceMover.SetValue(False)
        self.__mcbMinPriceMover.SetValue(False)

    def __on_check_above_zero(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_zero(evt.IsChecked())
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_fifty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_fifty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_hundred(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_hundred(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_zero(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_zero(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_fifty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_fifty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_zero_to_ten(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_zero_to_ten(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_ten_to_twenty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_ten_to_twenty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_above_twenty_to_thirty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_twenty_to_thirty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_click_above_thirty_to_fourty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_above_thirty_to_fourty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_zero_to_ten(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_zero_to_ten(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_ten_to_twenty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_ten_to_twenty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_twenty_to_thirty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_twenty_to_thirty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowThirtyFourty.SetValue(False)

    def __on_check_below_thirty_to_fourty(self, evt):
        self.__mFilterSearchStockPanel.set_mover_below_thirty_to_fourty(evt.IsChecked())
        self.__mcbMoverAboveZero.SetValue(False)
        self.__mcbMoverAboveFifty.SetValue(False)
        self.__mcbMoverAboveHundred.SetValue(False)
        self.__mcbMoverBelowZero.SetValue(False)
        self.__mcbMoverBelowFifty.SetValue(False)
        self.__mcbMoverAboveZeroToTen.SetValue(False)
        self.__mcbMoverAboveTenToTwenty.SetValue(False)
        self.__mcbMoverAboveTwentyThirty.SetValue(False)
        self.__mcbMoverAboveThirtyFourty.SetValue(False)
        self.__mcbMoverBelowZeroToTen.SetValue(False)
        self.__mcbMoverBelowTenToTwenty.SetValue(False)
        self.__mcbMoverBelowTwentyThirty.SetValue(False)
#endregion

    def __send_data(self):
        j = json.dumps(self.__mFilterSearchStockPanel.to_dict())
        pub.sendMessage(LISTEN_FILTER_STOCK_PANEL, message = json.loads(j))
        self.GetParent().Destroy()

class ViewStocksPanel(BasePanel):

    __mbsMainBox: wx.BoxSizer = None
    __mbsRightListBox: wx.BoxSizer = None
    __mMainSplitter = None

    __mLeftPanel: wx.Panel = None
    __mRightPanel: wx.Panel = None
    __mDataPanel: wx.Panel = None

    __mBoxSizerData = None

    __mtxSearchList: wx.TextCtrl = None

    __mList: wx.ListCtrl = None

    __mGraphOneDayCanvas = None
    __mGraphAxValues = None
    __mGraphAxVolume = None

    __mGraphOneDayPlot = None

    __mstPrice = None
    __mstPrePostMarketPrice = None
    __mstMarketCap = None
    __mstDayMax = None
    __mstDayMin = None
    __mstAsk = None
    __mstBid = None
    __mstFiftyTwoWeeksHigh = None
    __mstFiftyTwoWeeksLow = None
    __mstFifityTwoWeeksPercChange = None
    __mstVolume = None
    __mstAvgVolumeTenDays = None
    __mstAvgVolumeThreeMonths = None

    __mThreadUpdateGraph: StoppableThread = None
    __mThreadUpdateList: StoppableThread = None
    __mThreadUpdateGraphPlotOneDay: StoppableThread = None

    __mTimerUpdateList = None
    __mTimerUpdateLeftPanel = None

    __mProgressDialog = None

    __mStockViewData = None
    __mStocks = []

    __mGraphLastValue = None
    __mGraphLastColor = "b"

    __mIsShowingChart5d = False
    __mIsShowingChart1Mo = False
    __mIsShowingChart3Mo = False
    __mIsShowingChart6Mo = False
    __mIsShowingChart1Y = False
    __mIsShowingChart2Y = False
    __mIsShowingChart5Y = False
    __mIsShowingChart10Y = False
    __mIsShowingChartYTD = False
    __mIsShowingChartMax = False

    __mFilterSearchStockPanel = FilterSearchStockPanel()

    def __init__(self, parent, size, stocks, stock):
        super().__init__(parent, size)
        self.__mStocks = stocks
        self.init_threads()
        self.Bind(wx.EVT_WINDOW_DESTROY, self.__on_destroy_self)
        pub.subscribe(self.listen_filter_stock_panel, LISTEN_FILTER_STOCK_PANEL)
        self.__init_timers()
        self.__init_layout()
        
        if stock is not None:
            self.__on_click_item_list(stock)

#region - Private Methods
#region - Init Methods
    def init_threads(self):
        self.__mThreadUpdateGraph = StoppableThread(None, self.__update_graph_thread)
        self.__mThreadUpdateList = StoppableThread(None, self.__update_list_thread)

    def __init_timers(self):
        self.__mTimerUpdateList = wx.Timer(self, -1)
        self.__mTimerUpdateList.Start(20000)

        self.__mTimerUpdateLeftPanel = wx.Timer(self, -1)
        self.__mTimerUpdateLeftPanel.Start(20000)

        self.Bind(wx.EVT_TIMER, self.__repopulate_list, self.__mTimerUpdateList)
        self.Bind(wx.EVT_TIMER, self.__update_left_panel_data, self.__mTimerUpdateLeftPanel)

    def __init_layout(self):
        self.__mbsMainBox = wx.BoxSizer(wx.HORIZONTAL)

        self.__mbsMainBox.AddSpacer(10)
        self.__mMainSplitter = wx.SplitterWindow(self)
        self.__init_left_panel()
        self.__init_right_panel()
        self.__mMainSplitter.SplitVertically(self.__mLeftPanel, self.__mRightPanel, round((wx.DisplaySize()[0] / 10 * 7.5)))

        self.__mbsMainBox.Add(self.__mMainSplitter, 1, wx.EXPAND)
        self.__mbsMainBox.AddSpacer(10)
        self.SetSizer(self.__mbsMainBox)
        self.__mMainSplitter.Layout()
        self.__mLeftPanel.Layout()
        self.__mRightPanel.Layout()

    def __init_right_panel(self):
        self.__mRightPanel = wx.Panel(self.__mMainSplitter, wx.ID_ANY)
        self.__mRightPanel.SetBackgroundColour((66, 66, 66))
        
        main = wx.BoxSizer(wx.VERTICAL)
        
        vbs = wx.BoxSizer(wx.VERTICAL)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(15)
        hbs.Add(wx.StaticText(self.__mRightPanel, label = Strings.STR_SEARCH, style = wx.ALIGN_CENTRE), 0)
        vbs.Add(hbs, 0)

        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(15)
        self.__mtxSearchList = wx.TextCtrl(self.__mRightPanel, wx.ID_ANY, pos = wx.DefaultPosition, value = "", size = (500, 25))
        self.__mtxSearchList.Bind(wx.EVT_TEXT, self.__on_change_search_list_value)
        hbs.Add(self.__mtxSearchList, 1, wx.EXPAND)

        searchButton = super()._get_icon_button(self.__mRightPanel, wx.Bitmap(Icons.ICON_SEARCH), self.__on_click_search)
        hbs.Add(searchButton, 0, wx.EXPAND)

        vbs.Add(hbs, 0)
        main.Add(vbs, 0)
        main.AddSpacer(15)
        self.__mList = StocksViewList(self.__mRightPanel, wx.ID_ANY, wx.EXPAND|wx.LC_REPORT|wx.SUNKEN_BORDER, self.GetSize()[0], self.__on_click_item_list)
        main.Add(self.__mList, 1, wx.EXPAND)
        self.__mList.init_layout()

        if self.__mStocks is None or len(self.__mStocks) == 0x0:
            self.__mProgressDialog = wx.ProgressDialog(Strings.STR_INITIAL_SYNCHRONIZATION, "", maximum=100, parent=None, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE|wx.PD_ELAPSED_TIME)
            self.__mProgressDialog.Show()
            self.__mStocks = DataSynchronization.sync_all_stocks_and_symbols(self.__mProgressDialog)
            self.__mProgressDialog.Destroy()

        self.__mList.add_items_and_populate(self.__mStocks)

        self.__mRightPanel.SetSizer(main)
        self.__mRightPanel.Fit()

        if not self.__mThreadUpdateList.is_alive():
            self.__mThreadUpdateList.start()

    def __init_left_panel(self):
        self.__mLeftPanel = wx.lib.scrolledpanel.ScrolledPanel(self.__mMainSplitter, wx.ID_ANY)
        self.__mLeftPanel.Fit()
        self.__mLeftPanel.SetupScrolling()
#endregion

#region - Event Handler Methods
    def __on_destroy_self(self, evt):
        self.__mTimerUpdateList.Stop()
        self.__mTimerUpdateLeftPanel.Stop()
        self.__mThreadUpdateGraph.stop()
        self.__mThreadUpdateList.stop()

    def __on_change_search_list_value(self, evt):
        self.__mList.filter_items_by_name(evt.GetString())

    def __on_click_item_list(self, item):
        self.__mStockViewData = DataSynchronization.sync_single_stock_full_data(item)
        self.__mIsShowingChart5d = False
        self.__mIsShowingChart1Mo = False
        self.__mIsShowingChart3Mo = False
        self.__mIsShowingChart6Mo = False
        self.__mIsShowingChart1Y = False
        self.__mIsShowingChart2Y = False
        self.__mIsShowingChart5Y = False
        self.__mIsShowingChart10Y = False
        self.__mIsShowingChartYTD = False
        self.__mIsShowingChartMax = False
        self.__update_left_panel()

    def __on_click_search(self, evt):
        self.__mSearchStockFrame = SearchStockFrame(Strings.STR_SEARCH, self.__mFilterSearchStockPanel)
        self.__mSearchStockFrame.Show(True)

    def __on_click_five_day_chart(self, evt):
        if not self.__mIsShowingChart5d:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_5D, APIConstants.VALUE_1M)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_5D_VALUES, Strings.STR_5D_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChart5d = True        

    def __on_click_one_month_chart(self, evt):
        if not self.__mIsShowingChart1Mo:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_1MO, APIConstants.VALUE_5M)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_1MO_VALUES, Strings.STR_1MO_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChart1Mo = True

    def __on_click_three_month_chart(self, evt):
        if not self.__mIsShowingChart3Mo:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_3MO, APIConstants.VALUE_1D)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_3MO_VALUES, Strings.STR_3MO_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChart3Mo = True

    def __on_click_six_month_chart(self, evt):
        if not self.__mIsShowingChart6Mo:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_6MO, APIConstants.VALUE_1D)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_6MO_VALUES, Strings.STR_6MO_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChart6Mo = True

    def __on_click_one_year_chart(self, evt):
        if not self.__mIsShowingChart1Y:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_1Y, APIConstants.VALUE_1D)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_1Y_VALUES, Strings.STR_1Y_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChart1Y = True

    def __on_click_two_year_chart(self, evt):
        if not self.__mIsShowingChart2Y:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_2Y, APIConstants.VALUE_1D)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_2Y_VALUES, Strings.STR_2Y_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChart2Y = True

    def __on_click_five_year_chart(self, evt):
        if not self.__mIsShowingChart5Y:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_5Y, APIConstants.VALUE_1D)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_5Y_VALUES, Strings.STR_5Y_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChart5Y = True

    def __on_click_ten_year_chart(self, evt):
        if not self.__mIsShowingChart10Y:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_10Y, APIConstants.VALUE_1D)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_10Y_VALUES, Strings.STR_10Y_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChart10Y = True

    def __on_click_ytd_chart(self, evt):
        if not self.__mIsShowingChartYTD:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_YTD, APIConstants.VALUE_1D)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_YTD_VALUES, Strings.STR_YTD_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChartYTD = True

    def __on_click_max_chart(self, evt):
        if not self.__mIsShowingChartMax:
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_MAX, APIConstants.VALUE_1D)
            self.__mGraphsSizer.Add(self.__get_chart_row(self.__mDataPanel, Strings.STR_MAX_VALUES, Strings.STR_MAX_VOLUME, stockView.get_timestamps(), stockView.get_opens(), stockView.get_closes(), stockView.get_volumes()), 0, wx.EXPAND)
            self.__mLeftPanel.SetupScrolling()
            self.__mIsShowingChartMax = True

    def __on_click_open_one_day_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_1D, APIConstants.VALUE_1M)
        self.__mGraphOneDayPlot = ChartFrame("One Day Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        self.__mGraphOneDayPlot.Show(True)
        self.__mGraphOneDayPlot.Bind(wx.EVT_WINDOW_DESTROY, self.__on_destroy_graph_one_day_plot)

    def __on_click_open_five_day_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_5D, APIConstants.VALUE_1M)
        cf = ChartFrame("Five Days Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)
        
    def __on_click_open_one_month_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_1MO, APIConstants.VALUE_5M)
        cf = ChartFrame("One Month Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_three_month_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_3MO, APIConstants.VALUE_1H)
        cf = ChartFrame("Three Months Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_six_month_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_6MO, APIConstants.VALUE_1H)
        cf = ChartFrame("Six Months Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_one_year_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_1Y, APIConstants.VALUE_1H)
        cf = ChartFrame("One Year Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_two_year_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_2Y, APIConstants.VALUE_1H)
        cf = ChartFrame("Two Years Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_five_year_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_5Y, APIConstants.VALUE_1D)
        cf = ChartFrame("Five Years Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_ten_year_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_10Y, APIConstants.VALUE_1D)
        cf = ChartFrame("Ten Years Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_ytd_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_YTD, APIConstants.VALUE_1H)
        cf = ChartFrame("YTD Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_max_chart(self, evt):
        stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_MAX, APIConstants.VALUE_1D)
        cf = ChartFrame("Max Chart", stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float))
        cf.Show(True)

    def __on_click_open_in_new_window(self, evt):
        stocks = []
        for s in self.__mStocks:
            if s is not None:
                stocks.append(s)
        frame = ViewStocksFrame(self.__mStockViewData.get_stock().get_name(), stocks, self.__mStockViewData.get_stock())
        frame.Show()

    def __repopulate_list(self, event):
        if self.__mStocks is not None and len(self.__mStocks) > 0:
            stocks = []
            for s in self.__mStocks:
                if s is not None:
                    stocks.append(s)
            self.__mStocks = stocks
            list_total = self.__mList.GetItemCount()
            list_top = self.__mList.GetTopItem()
            list_pp = self.__mList.GetCountPerPage()
            list_bottom = min(list_top + list_pp, list_total - 1)
            self.__mList.add_items_and_populate(self.__mStocks)
            if list_bottom != 0:
                self.__mList.EnsureVisible((list_bottom - 1))
            filtered = self.__mList.get_filtered_items()
            if filtered is not None and len(filtered) > 0:
                for i in range(0, len(filtered)):
                    if self.__mStockViewData is not None and self.__mStockViewData.get_stock().get_id() == filtered[i].get_id():
                        self.__mList.unbind_listener()
                        self.__mList.Select(i)
                        self.__mList.bind_listener()
                        break 
        
    def __update_left_panel_data(self, event):
        if self.__mStockViewData is not None:
            self.__mstPrice.SetLabel("$" + str(self.__mStockViewData.get_stock().get_price()))
            if self.__mStockViewData.get_stock().get_pre_market_price() is not None:
                self.__mstPrePostMarketPrice.SetLabel("Pre Market: $" + str(self.__mStockViewData.get_stock().get_pre_market_price()))
            else:
                if self.__mStockViewData.get_stock().get_post_market_price() is not None:
                    self.__mstPrePostMarketPrice.SetLabel("Post Market: $" + str(self.__mStockViewData.get_stock().get_post_market_price()))
                else:
                    self.__mstPrePostMarketPrice.SetLabel("")
            self.__mstMarketCap.SetLabel(TextUtils.convert_number_to_millions_form(self.__mStockViewData.get_stock().get_market_cap()))
            self.__mstDayMax.SetLabel(str(self.__mStockViewData.get_stock().get_day_max()))
            self.__mstDayMin.SetLabel(str(self.__mStockViewData.get_stock().get_day_min()))
            self.__mstAsk.SetLabel(str(self.__mStockViewData.get_stock().get_ask()) + " x " + str(self.__mStockViewData.get_stock().get_ask_size() * 100))
            self.__mstBid.SetLabel(str(self.__mStockViewData.get_stock().get_bid()) + " x " + str(self.__mStockViewData.get_stock().get_bid_size() * 100))
            self.__mstFiftyTwoWeeksHigh.SetLabel(str(self.__mStockViewData.get_stock().get_fifty_two_weeks_high()))
            self.__mstFiftyTwoWeeksLow.SetLabel(str(self.__mStockViewData.get_stock().get_fifty_two_weeks_low()))
            self.__mstFifityTwoWeeksPercChange.SetLabel(str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_fifty_two_weeks_perc_change(), 2)))
            self.__mstVolume.SetLabel(str(self.__mStockViewData.get_stock().get_volume()))
            self.__mstAvgVolumeTenDays.SetLabel(str(self.__mStockViewData.get_stock().get_avg_volume_ten_days()))
            self.__mstAvgVolumeThreeMonths.SetLabel(str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_avg_volume_three_months(), 2)))

    def __on_destroy_graph_one_day_plot(self, event):
        self.__mGraphOneDayPlot = None
#endregion

#region - Thread Methods
    def __update_graph_thread(self):
        while not self.__mThreadUpdateGraph.stopped():
            stockView = DataSynchronization.sync_get_chart(self.__mStockViewData.get_stock().get_sign(), APIConstants.VALUE_1D, APIConstants.VALUE_1M)
            opens = np.array(stockView.get_opens(), dtype=float)

            if self.__mGraphAxValues is not None and stockView.get_timestamps() is not None and len(stockView.get_timestamps()) > 0x0:
                self.__mGraphAxValues.clear()

                if self.__mGraphLastValue != opens[len(opens) - 1]:
                    if self.__mGraphLastValue <= opens[len(opens) - 1]:
                        self.__mGraphAxValues.plot(stockView.get_timestamps(), opens, "g")
                        self.__mGraphLastColor = "g"
                    else:
                        self.__mGraphAxValues.plot(stockView.get_timestamps(), opens, "r")
                        self.__mGraphLastColor = "r"
                else:
                    self.__mGraphAxValues.plot(stockView.get_timestamps(), opens, self.__mGraphLastColor)

                self.__mGraphAxValues.fill_between(stockView.get_timestamps(), min(opens), opens, alpha=0.5)
                self.__mGraphLastValue = opens[len(opens) - 1]
                self.__mGraphAxValues.set_title(Strings.STR_1D_VALUES)

                self.__mGraphAxVolume.clear()
                self.__mGraphAxVolume.stem(stockView.get_timestamps(), stockView.get_volumes())
                self.__mGraphAxVolume.set_title(Strings.STR_1D_VOLUME)

                self.__mGraphOneDayCanvas.draw()
                self.__mGraphOneDayCanvas.flush_events()
                
                if self.__mGraphOneDayPlot is not None:
                    self.__mGraphOneDayPlot.update_values_with_color(stockView.get_timestamps(), np.array(stockView.get_opens(), dtype=float), self.__mGraphLastColor)

            time.sleep(30)

    def __update_list_thread(self):
        while not self.__mThreadUpdateList.stopped():
            stocks = []
            for s in self.__mStocks:
                if s is not None:
                    stocks.append(s)
            self.__mStocks = DataSynchronization.sync_update_all_stocks(stocks)

            if self.__mStockViewData is not None:
                stock = None
                for s in stocks:
                    if self.__mStockViewData.get_stock().get_sign() == s.get_sign():
                        stock = s
                        break 
                if s is not None:
                    self.__mStockViewData.set_stock(stock)
            time.sleep(30)
#endregion

#region - Get Layout Components
    def __update_left_panel(self):
        if self.__mBoxSizerData is not None:
            for child in self.__mBoxSizerData.GetChildren():
                if child is not None and child.Window is not None:
                    self.__mBoxSizerData.Hide(child.GetWindow())
                    self.__mBoxSizerData.Layout()
        self.__mBoxSizerData = wx.BoxSizer(wx.VERTICAL)
        self.__mBoxSizerData.Add(self.__get_layout_nome_azienda(), 0, wx.EXPAND)
        self.__mBoxSizerData.Add(self.__get_layout_data_one(), 1, wx.EXPAND|wx.ALL)
        self.__mLeftPanel.SetSizer(self.__mBoxSizerData)

        if self.__mIsShowingChart5d:
            self.__mIsShowingChart5d = False
            self.__on_click_five_day_chart(None)

        if self.__mIsShowingChart1Mo:
            self.__mIsShowingChart1Mo = False
            self.__on_click_one_month_chart(None)

        if self.__mIsShowingChart3Mo:
            self.__mIsShowingChart3Mo = False
            self.__on_click_three_month_chart(None)

        if self.__mIsShowingChart6Mo:
            self.__mIsShowingChart6Mo = False
            self.__on_click_six_month_chart(None)
        
        if self.__mIsShowingChart1Y:
            self.__mIsShowingChart1Y = False
            self.__on_click_one_year_chart(None)
        
        if self.__mIsShowingChart2Y:
            self.__mIsShowingChart2Y = False
            self.__on_click_two_year_chart(None)
        
        if self.__mIsShowingChart5Y:
            self.__mIsShowingChart5Y = False
            self.__on_click_five_year_chart(None)
        
        if self.__mIsShowingChart10Y:
            self.__mIsShowingChart10Y = False
            self.__on_click_ten_year_chart(None)
        
        if self.__mIsShowingChartYTD:
            self.__mIsShowingChartYTD = False
            self.__on_click_ytd_chart(None)
        
        if self.__mIsShowingChartMax:
            self.__mIsShowingChartMax = False
            self.__on_click_max_chart(None)

        if not self.__mThreadUpdateGraph.is_alive():
            self.__mThreadUpdateGraph.start()

    def __get_layout_nome_azienda(self):
        panel = wx.Panel(self.__mLeftPanel)
        panel.SetBackgroundColour((33, 33, 33))

        vbs = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(panel, label = self.__mStockViewData.get_stock().get_company().get_short_name(), style = wx.ALIGN_LEFT)
        WxUtils.set_font_size_and_bold_and_roman(st, 30)
        vbs.Add(st, 0, wx.EXPAND)

        hbs = wx.BoxSizer(wx.HORIZONTAL)
        self.__mstMarketPercentage = wx.StaticText(panel, label = str(round(self.__mStockViewData.get_stock().get_market_change_percent(), 2))  + "%")
        WxUtils.set_font_size_and_bold_and_roman(self.__mstMarketPercentage, 20)
        if self.__mStockViewData.get_stock().get_market_change_percent() is not None and self.__mStockViewData.get_stock().get_market_change_percent() > 0:
            self.__mstMarketPercentage.SetForegroundColour(Colors.GREEN)
        else:
            self.__mstMarketPercentage.SetForegroundColour(Colors.RED)
        
        self.__mstPrice = wx.StaticText(panel, label = "$" + str(self.__mStockViewData.get_stock().get_price()) + "     ")
        WxUtils.set_font_size_and_bold_and_roman(self.__mstPrice, 20)
        hbs.Add(self.__mstPrice, 0, wx.EXPAND)
        hbs.Add(self.__mstMarketPercentage, 1, wx.EXPAND)
        
        if self.__mStockViewData.get_stock().get_pre_market_price() is not None:
            self.__mstPrePostMarketPrice = wx.StaticText(panel, label = Strings.STR_FIELD_PRE_MARKET + str(self.__mStockViewData.get_stock().get_pre_market_price()))
            self.__mstPrePostMarketPercentage = wx.StaticText(panel, label = "     " + str(round(self.__mStockViewData.get_stock().get_pre_market_change_percentage(), 2)) + "%")
            if self.__mStockViewData.get_stock().get_pre_market_change_percentage() is not None and self.__mStockViewData.get_stock().get_pre_market_change_percentage() > 0:
                self.__mstPrePostMarketPercentage.SetForegroundColour(Colors.GREEN)
            else:
                self.__mstPrePostMarketPercentage.SetForegroundColour(Colors.RED)
        else:
            if self.__mStockViewData.get_stock().get_post_market_price() is not None:
                self.__mstPrePostMarketPrice = wx.StaticText(panel, label = Strings.STR_FIELD_POST_MARKET + str(self.__mStockViewData.get_stock().get_post_market_price()))
                self.__mstPrePostMarketPercentage = wx.StaticText(panel, label = "     " + str(round(self.__mStockViewData.get_stock().get_post_market_change_percent(), 2)) + "%")
                if self.__mStockViewData.get_stock().get_post_market_change_percent() is not None and self.__mStockViewData.get_stock().get_post_market_change_percent() > 0:
                    self.__mstPrePostMarketPercentage.SetForegroundColour(Colors.GREEN)
                else:
                    self.__mstPrePostMarketPercentage.SetForegroundColour(Colors.RED)
            else:
                self.__mstPrePostMarketPrice = wx.StaticText(panel, label = "")
                self.__mstPrePostMarketPercentage = wx.StaticText(panel, label = "")
        
        WxUtils.set_font_size_and_bold_and_roman(self.__mstPrePostMarketPercentage, 20)
        WxUtils.set_font_size_and_bold_and_roman(self.__mstPrePostMarketPrice, 20)
        hbs.Add(self.__mstPrePostMarketPrice, 0, wx.EXPAND)
        hbs.Add(self.__mstPrePostMarketPercentage, 0, wx.EXPAND)
        vbs.Add(hbs, 0, wx.EXPAND)
        
        panel.SetSizer(vbs)
        return panel

    def __get_layout_data_one(self):
        self.__mDataPanel = wx.Panel(self.__mLeftPanel)
        self.__mDataPanel.SetBackgroundColour((66, 66, 66))
        vbs = wx.BoxSizer(wx.VERTICAL)
        vbs.AddSpacer(10)
        self.__mGraphsSizer = wx.BoxSizer(wx.VERTICAL)
        self.__mGraphsSizer.Add(self.__get_chart_row_thread_managed(self.__mDataPanel, Strings.STR_1D_VALUES, Strings.STR_1D_VOLUME, self.__mStockViewData.get_timestamps(), self.__mStockViewData.get_opens(), self.__mStockViewData.get_closes(), self.__mStockViewData.get_volumes()), 0, wx.EXPAND)
        vbs.Add(self.__mGraphsSizer, 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_zero_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_first_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_second_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_third_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_fourth_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_fifth_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_sixth_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_seventh_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_eigth_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_nineth_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_ten_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_eleven_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_twelve_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_thirteen_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_fourteen_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)
        vbs.Add(self.__get_fiveteen_row_info(self.__mDataPanel), 0, wx.EXPAND)
        vbs.AddSpacer(10)


        self.__mDataPanel.SetSizer(vbs)
        return self.__mDataPanel

    def __get_chart_row_thread_managed(self, parent, label1, label2, timestamps, opens, closes, volumes):
        panel = wx.Panel(parent)
        self.fig = Figure(figsize=(2, 4))
        self.__mGraphOneDayCanvas = FigureCanvas(panel, -1, self.fig)
        toolbar = NavigationToolbar(self.__mGraphOneDayCanvas)
        toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__mGraphOneDayCanvas, 1, wx.EXPAND)
        sizer.Add(toolbar, 0, wx.LEFT | wx.EXPAND)
        panel.SetSizer(sizer)

        timestamps = np.array(timestamps, dtype=str)
        opens = np.array(opens, dtype=float)
        volumes = np.array(volumes, dtype=float)

        (self.__mGraphAxValues, self.__mGraphAxVolume) = self.fig.subplots(1, 2)
        
        self.__mGraphAxValues.set_title(label1)
        if timestamps is not None and len(timestamps) > 0x0:
            self.__mGraphAxValues.plot(timestamps, opens)
            self.__mGraphAxValues.fill_between(timestamps, min(opens), opens, alpha=0.5)
            self.__mGraphLastValue = opens[len(opens) - 1]

        if timestamps is not None and len(timestamps) > 0x0:
            self.__mGraphAxVolume.set_title(label2)
            self.__mGraphAxVolume.stem(timestamps, volumes)

        return panel

    def __get_chart_row(self, parent, label1, label2, timestamps, opens, closes, volumes):
        panel = wx.Panel(parent)
        fig = Figure(figsize=(2, 4))
        canvas = FigureCanvas(panel, -1, fig)
        toolbar = NavigationToolbar(canvas)
        toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.EXPAND)
        sizer.Add(toolbar, 0, wx.LEFT | wx.EXPAND)
        panel.SetSizer(sizer)

        opens = np.array(opens, dtype=float)

        (ax1, ax2) = fig.subplots(1, 2)
        ax1.set_title(label1)
        ax1.plot(timestamps, opens)
        ax1.fill_between(timestamps, min(opens), opens, alpha=0.5)

        ax2.set_title(label2)
        ax2.stem(timestamps, volumes)

        return panel

    def __get_zero_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)
        
        st = wx.StaticText(panel, label = Strings.STR_FIELD_MARKET_CAP, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstMarketCap = wx.StaticText(panel, label = TextUtils.convert_number_to_millions_form(self.__mStockViewData.get_stock().get_market_cap()), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstMarketCap, 15)
        hbs.Add(self.__mstMarketCap, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_ENTERPRISE_VALUE, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = TextUtils.convert_number_to_millions_form(self.__mStockViewData.get_stock().get_enterprise_value()), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel


    def __get_first_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_DAY_MAX, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstDayMax = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_day_max()), style = wx.ALIGN_RIGHT)
        self.__mstDayMax.SetForegroundColour(Colors.GREEN)
        WxUtils.set_font_size(self.__mstDayMax, 15)
        hbs.Add(self.__mstDayMax, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_DAY_MIN, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstDayMin = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_day_min()), style = wx.ALIGN_RIGHT)
        self.__mstDayMin.SetForegroundColour(Colors.RED)
        WxUtils.set_font_size(self.__mstDayMin, 15)
        hbs.Add(self.__mstDayMin, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel
        
    def __get_second_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_ASK, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstAsk = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_ask()) + " x " + str(self.__mStockViewData.get_stock().get_ask_size() * 100), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstAsk, 15)
        hbs.Add(self.__mstAsk, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_BID, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstBid = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_bid()) + " x " + str(self.__mStockViewData.get_stock().get_bid_size() * 100), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstBid, 15)
        hbs.Add(self.__mstBid, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_SHARES_OUTSTANDING, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_shares_outstanding()), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel

    def __get_third_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_52_WEEKS_MAX, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstFiftyTwoWeeksHigh = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_fifty_two_weeks_high()), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstFiftyTwoWeeksHigh, 15)
        self.__mstFiftyTwoWeeksHigh.SetForegroundColour(Colors.GREEN)
        hbs.Add(self.__mstFiftyTwoWeeksHigh, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_52_WEEKS_MIN, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstFiftyTwoWeeksLow = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_fifty_two_weeks_low()), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstFiftyTwoWeeksLow, 15)
        self.__mstFiftyTwoWeeksLow.SetForegroundColour(Colors.RED)
        hbs.Add(self.__mstFiftyTwoWeeksLow, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_52_WEEKS_PERC_CHANGE, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstFifityTwoWeeksPercChange = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_fifty_two_weeks_perc_change(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstFifityTwoWeeksPercChange, 15)
        if self.__mStockViewData.get_stock().get_fifty_two_weeks_perc_change() > 0:
            self.__mstFifityTwoWeeksPercChange.SetForegroundColour(Colors.GREEN)
        else:
            self.__mstFifityTwoWeeksPercChange.SetForegroundColour(Colors.RED)
        hbs.Add(self.__mstFifityTwoWeeksPercChange, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel

    def __get_fourth_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_VOLUME, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstVolume = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_volume()), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstVolume, 15)
        hbs.Add(self.__mstVolume, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_VOLUME_10_DAYS, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstAvgVolumeTenDays = wx.StaticText(panel, label = str(self.__mStockViewData.get_stock().get_avg_volume_ten_days()), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstAvgVolumeTenDays, 15)
        hbs.Add(self.__mstAvgVolumeTenDays, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_VOLUME_3_MONTHS, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        self.__mstAvgVolumeThreeMonths = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_avg_volume_three_months(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(self.__mstAvgVolumeThreeMonths, 15)
        hbs.Add(self.__mstAvgVolumeThreeMonths, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel

    def __get_fifth_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_TRAILING_PRICE_EARNINGS, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_trailing_price_earnings(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_FORWARD_PRICE_EARNINGS, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_forward_price_earnings(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel

    def __get_sixth_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_PE_RATIO, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_pe_ratio(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_PEG_RATIO, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_peg_ratio(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_PB_RATIO, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_pb_ratio(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel

    def __get_seventh_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_PRICE_TO_BOOK, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_price_to_book(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_BOOK_VALUE_PER_SHARE, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_book_value_per_share(), 2)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel

    def __get_eigth_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_DIVIDEND_DATE, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        if self.__mStockViewData.get_stock().get_dividend_date() is not None:
            st = wx.StaticText(panel, label = datetime.utcfromtimestamp(self.__mStockViewData.get_stock().get_dividend_date()).strftime('%d/%m/%Y'), style = wx.ALIGN_RIGHT)
            WxUtils.set_font_size(st, 15)
            hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_ANNUAL_DIVIDEND_RATE, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_trailing_annual_dividend_rate(), 3)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_ANNUAL_DIVIDEND_YELD, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_trailing_annual_dividend_yeld(), 5)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel

    def __get_nineth_row_info(self, parent):
        panel = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        hbs.AddSpacer(10)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_RATIO_ENTERPRISE_VALUE_REVENUE, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        hbs.AddSpacer(5)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_enterprises_value_revenue_ratio(), 3)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        hbs.AddSpacer(50)

        st = wx.StaticText(panel, label = Strings.STR_FIELD_RATIO_ENTERPRISE_VALUE_EBITDA, style = wx.ALIGN_LEFT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)
        st = wx.StaticText(panel, label = str(NumberUtils.safe_round(self.__mStockViewData.get_stock().get_enterprises_value_ebitda_ratio(), 3)), style = wx.ALIGN_RIGHT)
        WxUtils.set_font_size(st, 15)
        hbs.Add(st, 0, wx.ALL|wx.EXPAND)

        panel.SetSizer(hbs)
        return panel

    def __get_ten_row_info(self, parent):
        p = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open in New Window", self.__on_click_open_in_new_window), 1, wx.EXPAND)
        hbs.AddSpacer(10)

        p.SetSizer(hbs)
        return p

    def __get_eleven_row_info(self, parent):
        p = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "5D Chart", self.__on_click_five_day_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "1M Chart", self.__on_click_one_month_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "3M Chart", self.__on_click_three_month_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "6M Chart", self.__on_click_six_month_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "1y Chart", self.__on_click_one_year_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)

        p.SetSizer(hbs)
        return p

    def __get_twelve_row_info(self, parent):
        p = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)

        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "2y Chart", self.__on_click_two_year_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "5y Chart", self.__on_click_five_year_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "10y Chart", self.__on_click_ten_year_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "YTD Chart", self.__on_click_ytd_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Max Chart", self.__on_click_max_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)

        p.SetSizer(hbs)
        return p

    def __get_thirteen_row_info(self, parent):
        p = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 1D Chart", self.__on_click_open_one_day_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 5D Chart", self.__on_click_open_five_day_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 1M Chart", self.__on_click_open_one_month_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 3M Chart", self.__on_click_open_three_month_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)

        p.SetSizer(hbs)
        return p

    def __get_fourteen_row_info(self, parent):
        p = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 6M Chart", self.__on_click_open_six_month_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 1Y Chart", self.__on_click_open_one_year_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 2Y Chart", self.__on_click_open_two_year_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 5Y Chart", self.__on_click_open_five_year_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)

        p.SetSizer(hbs)
        return p

    def __get_fiveteen_row_info(self, parent):
        p = wx.Panel(parent)
        hbs = wx.BoxSizer(wx.HORIZONTAL)
        
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open 10Y Chart", self.__on_click_open_ten_year_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open YTD Chart", self.__on_click_open_ytd_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)
        hbs.Add(super()._get_button(p, "Open Max Chart", self.__on_click_open_max_chart), 1, wx.EXPAND)
        hbs.AddSpacer(10)

        p.SetSizer(hbs)
        return p

#endregion

    def listen_filter_stock_panel(self, message, arg= None):
        self.__mFilterSearchStockPanel.from_json(message)
        self.__mList.set_filter_data(self.__mFilterSearchStockPanel)
        self.__mList.filter_items()

#endregion

class ChartFrame(wx.Frame):
   
    __mFigure = None
    __mCanvas = None
    __mAxes = None
    __mToolbar = None
   
    def __init__(self, title, x, y):
        super().__init__(None, -1, title, size=(550, 350))

        self.__mFigure = Figure()
        self.__mAxes = self.__mFigure.add_subplot()

        self.__mAxes.plot(x, y)

        self.__mAxes.fill_between(x, min(y), y, alpha=0.5)
        self.__mCanvas = FigureCanvas(self, -1, self.__mFigure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.__mCanvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.add_toolbar()

#region - Public Methods
    def add_toolbar(self):
        self.__mToolbar = NavigationToolbar(self.__mCanvas)
        self.__mToolbar.Realize()
        self.sizer.Add(self.__mToolbar, 0, wx.LEFT | wx.EXPAND)
        self.__mToolbar.update()

    def update_values_with_color(self, x, y, color):
        self.__mAxes.clear()
        self.__mAxes.plot(x, y, color)
        self.__mAxes.fill_between(x, min(y), y, alpha=0.5)
        self.__mCanvas.draw()
        self.__mCanvas.flush_events()

    def update_values(self, x, y):
        self.__mAxes.clear()
        self.__mAxes.plot(x, y)
        self.__mAxes.fill_between(x, min(y), y, alpha=0.5)
        self.__mCanvas.draw()
        self.__mCanvas.flush_events()
#endregion

class ViewStocksFrame(wx.Frame):

    def __init__(self, title, stocks, stock):
        wx.Frame.__init__(self, None, wx.ID_ANY, title, size=Constants.DISPLAY_SIZE_MAIN_FRAME)
        self.CenterOnScreen(True)
        self.Maximize(True)
        self.__init_main_panel(stocks, stock)

    def __init_main_panel(self, stocks, stock):
        self.__mMainPanel = ViewStocksPanel(self, wx.DisplaySize(), stocks, stock)
        self.__mMainPanel.Show()

class SearchStockFrame(wx.Frame):

    def __init__(self, title, filterData):
        wx.Frame.__init__(self, None, wx.ID_ANY, title, size=Constants.DISPLAY_SIZE_MAIN_FRAME)
        wx.Frame.CenterOnScreen(self)
        self.__init_main_panel(filterData)

    def __init_main_panel(self, filterData):
        self.__mMainPanel = SearchStockPanel(self, wx.DisplaySize(), filterData)
        self.__mMainPanel.Show()

class MainApplication(wx.App):

    __mMainFrame: ViewStocksFrame = None

    def __init__(self, redirect):
        wx.App.__init__(self, redirect)

    def OnInit(self):
        self.__mMainFrame = ViewStocksFrame("Stocks View", [], None)
        self.__mMainFrame.Show()
        self.SetTopWindow(self.__mMainFrame)
        return True

    def OnExit(self):
        return 0

def main():
    faulthandler.enable()
    application = MainApplication(False)
    application.MainLoop()

if __name__ == "__main__":
    main()