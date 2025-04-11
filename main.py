import requests
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header

#Insert company name and stock symbol
COMPANY="Tesla"
COMPANY_SYMBOL="TSLA"

#Turn possible latin1 characters into unicode
def fix(text:str):
    words=text.split()
    new_words=[]
    new_text=""
    for word in words:
        try:
            encoded_word=word.encode("latin1")
            new_words.append(encoded_word.decode("utf-8"))
        except:
            new_words.append(word)
            continue
    for i in range(0,len(new_words)-1):
        new_text+=new_words[i]
        new_text+=" "
    new_text+=new_words[len(new_words)-1]
    return new_text

load_dotenv()

#APIs
stock_market_api_key= os.getenv("STOCK_MARKET_API_KEY")
stock_market_endpoint= "https://www.alphavantage.co/query"
news_api_key=os.getenv("NEWS_API_KEY")
news_endpoint="https://newsapi.org/v2/top-headlines"

#API parameters
stock_parameters={
    "function":"TIME_SERIES_DAILY",
    "symbol":COMPANY_SYMBOL,
    "apikey":stock_market_api_key
}

news_parameters={
    "qInTitle":COMPANY,
    "apiKey":news_api_key,
    "sortBy":"publishedAt", #Get latest news
    "country":"us" #Get news from US only
}

#Stock request
stocks_response=requests.get(url=stock_market_endpoint, params=stock_parameters)
stocks_response.raise_for_status()
data=stocks_response.json()["Time Series (Daily)"]

#Get closing prices from last 2 days
data_list=[value for (key,value) in data.items()]
yesterday_closing_price=float(data_list[0]["4. close"])
day_before_yesterday_closing_price=float(data_list[1]["4. close"])

#Calculate difference between closing prices
diff=yesterday_closing_price-day_before_yesterday_closing_price
difference_percentage=(abs(diff)/day_before_yesterday_closing_price)*100

#Send email if difference>5%
if difference_percentage>5:

    #Get latest news
    news_response=requests.get(url=news_endpoint,params=news_parameters)
    articles=news_response.json()["articles"]
    first_three_articles=articles[:3]

    #Format text for email
    formatted=[f"Headline: {item['title']}. {item['description']}\nLink: {item["url"]}" for item in first_three_articles]

    #Format headline for email
    if diff > 0:
        headline = f"{COMPANY} stock increased by {round(difference_percentage,2)}%"
    else:
        headline = f"{COMPANY} stock decreased by {round(difference_percentage,2)}%"

    #Send 3 latest headlines via email
    for item in formatted:
        message=MIMEText(fix(item),"plain","utf-8")
        message['Subject']=Header(headline,"utf-8")
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=os.getenv("FROM_EMAIL"),password=os.getenv("PASSWORD"))
            connection.sendmail(from_addr=os.getenv("FROM_EMAIL"),to_addrs=os.getenv("TO_EMAIL"),msg=message.as_string())