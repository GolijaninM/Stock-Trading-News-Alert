import requests
import smtplib
import os
from dotenv import load_dotenv

#Insert company name and stock symbol
COMPANY="Tesla"
COMPANY_SYMBOL="TSLA"

load_dotenv()

#APIs
stock_market_api_key= os.getenv("STOCK_MARKET_API_KEY")
stock_market_endpoint= "https://www.alphavantage.co/query"
news_api_key=os.getenv("NEWS_API_KEY")
news_endpoint="https://newsapi.org/v2/everything"

#API parameters
stock_parameters={
    "function":"TIME_SERIES_DAILY",
    "symbol":COMPANY_SYMBOL,
    "apikey":stock_market_api_key
}

news_parameters={
    "qInTitle":COMPANY,
    "apiKey":news_api_key
}

stocks_response=requests.get(url=stock_market_endpoint, params=stock_parameters)
stocks_response.raise_for_status()
data=stocks_response.json()["Time Series (Daily)"]

data_list=[value for (key,value) in data.items()]
yesterday_closing_price=float(data_list[0]["4. close"])
day_before_yesterday_closing_price=float(data_list[1]["4. close"])

diff=yesterday_closing_price-day_before_yesterday_closing_price
difference_percentage=(abs(diff)/day_before_yesterday_closing_price)*100

if difference_percentage>5:
    news_response=requests.get(url=news_endpoint,params=news_parameters)
    articles=news_response.json()["articles"]
    first_three_articles=articles[:3]

    formatted=[f"Headline: {item['title']}.\nBrief: {item['description']}" for item in first_three_articles]


    if diff > 0:
        headline = f"{COMPANY} stock increased {difference_percentage}%"
    else:
        headline = f"{COMPANY} stock decreased {difference_percentage}%"

    for item in formatted:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=os.getenv("FROM_EMAIL"),password=os.getenv("PASSWORD"))
            connection.sendmail(from_addr=os.getenv("FROM_EMAIL"),to_addrs=os.getenv("TO_EMAIL"),msg=f"Subject: {headline}\n\n{item.encode("utf-8")}")
