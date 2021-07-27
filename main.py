import requests
import os
from twilio.http.http_client import TwilioHttpClient
from _datetime import datetime
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")

stock_params ={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
now = datetime.now()
r = requests.get(url='https://www.alphavantage.co/query', params=stock_params)
stock_data = r.json()["Time Series (Daily)"]
list_data = [value for (key, value) in stock_data.items()]
yesterday_data = list_data[0]
day_before_yesterday_data = list_data[1]
yesterday_closing_price = float(yesterday_data['4. close'])
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])
difference = yesterday_closing_price - day_before_yesterday_closing_price
difference_percent = (difference/yesterday_closing_price)*100
if difference_percent > 0:
    emoji = "🔺"
else:
    emoji = "🔻"
if abs(difference_percent) > 5:
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    news_parameters = {
        "q": "tesla",
        "from": now.date(),
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url='https://newsapi.org/v2/everything', params=news_parameters)
    news_data = response.json()['articles']
    news = {
        "headline_1": news_data[0]['title'],
        "brief_1": news_data[1]['description'],
        "headline_2": news_data[1]['title'],
        "brief_2": news_data[1]['description'],
        "headline_3": news_data[2]['title'],
        "brief_3": news_data[2]['description']
    }

    account_sid = os.getenv("account_sid")
    auth_token = os.getenv("auth_token")
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
                body=f"{COMPANY_NAME}: {emoji}{difference_percent}%\nHeadline:{news['headline_1']}\nBrief:{news['brief_1']}"
                     f"\nHeadline:{news['headline_2']}\nBrief:{news['brief_2']}\n"
                     f"Headline:{news['headline_3']}\nBrief:{news['brief_3']}\n",
                from_='+1 347 514 9656',
                to='+91 7013918815'
        )
    print(message.status)
