# 📈 Stock Trading News Alert

A Python script that monitors stock prices and sends you the latest news when there's significant movement.

## 🔍 What It Does

This script checks the closing prices of a given stock for the last two trading days using the [Alpha Vantage API](https://www.alphavantage.co/).  
If the price changes by **5% or more**, it fetches the **3 most recent news articles** from [NewsAPI](https://newsapi.org/) and emails them to you.

## ⚙️ Requirements

Before you run the script, you'll need:

- Two email addresses (one to send, one to receive)
- An app password for the sender email (Gmail recommended)
👉 [How to generate an app password in Gmail](https://support.google.com/accounts/answer/185833?hl=en)
- [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)
- [NewsAPI key](https://newsapi.org/register)

## 💡 Recomended
Put the code on [PythonAnywhere](https://www.pythonanywhere.com/) to run it every day.


## 🛠️ Installation

1. Clone the repo:

```bash
git clone https://github.com/GolijaninM/stock-trading-news-alert.git