import yfinance as yf
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

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
        content = newsDict.get("content", {})
        url = None
        if content.get("clickThroughUrl"):
            url = content["clickThroughUrl"]["url"]
        elif content.get("canonicalUrl"):
            url = content["canonicalUrl"]["url"]
        elif content.get("previewUrl"):
            url = content["previewUrl"]

        newsDictToAdd = {
            "title": newsDict["content"]["title"],
            "link": url,
        }
        allNewsArticles.append(newsDictToAdd)
    return allNewsArticles

def extractNewsArticleTextFromHtml(soup):
    allText = ""
    result = soup.find_all("div", {"class":"body yf-v6n2s3"})
    for res in result:
        allText += res.text
    return allText

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
}
def extractCompanyNewsArticle(newsArticles):
    allArticlesText = ""
    for newsArticle in newsArticles:
        url = newsArticle["link"]
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        if not soup.find("div", class_="continue-reading yf-7fhdv6"):
            allArticlesText += extractNewsArticleTextFromHtml(soup)
    return allArticlesText

def getCompanyStockInfo(tickerSymbol):
    # get data from yahoo finance API
    company = yf.Ticker(tickerSymbol)

    # Get company basic info
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getpriceHistory(company)
    futureEarningsDates = getEarningsDates(company)
    newsArticles = getCompanyNews(company)
    newsArticleAllText = extractCompanyNewsArticle(newsArticles)
    print(newsArticleAllText)

getCompanyStockInfo("NVDA")