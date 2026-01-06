import yfinance as yf
from datetime import datetime, timedelta

def extractBasicInfo(data):
    keysToExtract = [ "longName", "website", "sector", "fullTimeEmployees", "marketCap", "totalRevenue", "trailingEps"]
    basicInfo = {}
    for key in keysToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ""

    return basicInfo

def getpriceHistory(company):
    history_df = company.history(period="1y", interval="1d")
    prices = history_df["Open"].tolist()
    dates = history_df.index.strftime("%Y-%m-%d").tolist()
    
    return {
        "price": prices,
        "date": dates
    }

def getEarningsDates(company):
    earningsDatesDf = company.earnings_dates
    allDates = earningsDatesDf.index.strftime("%Y-%m-%d").tolist()
    date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in allDates]
    current_dates = datetime.now()
    future_dates = [date.strftime("%Y-%m-%d") for date in date_objects if date > current_dates]
    return future_dates

def getCompanyNews(company):
    newsList = company.news
    allNewsArticles = []
    for newsDict in newsList:
        newsDictToAdd = {
            "title": newsDict["content"]["title"],
            "link": newsDict["content"]["previewUrl"]
        }
        allNewsArticles.append(newsDictToAdd)
    return allNewsArticles

def getCompanyStockInfo(tickerSymbol):
    # get data from yahoo finance API
    company = yf.Ticker(tickerSymbol)

    # Get company basic info
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getpriceHistory(company)
    futureEarningsDates = getEarningsDates(company)
    newsArticles = getCompanyNews(company)
    

getCompanyStockInfo("MSFT")