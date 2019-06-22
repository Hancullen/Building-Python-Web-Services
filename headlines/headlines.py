import datetime
import feedparser
from flask import Flask, render_template, request, make_response
import json
from urllib.request import urlopen, quote

app = Flask(__name__)
RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'bbc',
            'city':'Vaasa, Finland',
            'base':'EUR',
            'to_currency':'VND'}

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b7a4f336b9cb0576dbd0cbc2c47837fc'
CURRENCY_URL = 'https://openexchangerates.org//api/latest.json?app_id=4c23e5ab3a5f44df852b7e446beafcd8'
@app.route("/")
def home():
    #get customized news from user's input of publication or defaults
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)

    #get weather based on user's input or defaults
    city = get_value_with_fallback('city')
    weather = get_weather(city)

    #get currencies based on user's input or defaults
    base = get_value_with_fallback('base')
    to_currency = get_value_with_fallback("to_currency")

    #get exchange rates
    rate, currencies = get_rate(base, to_currency)

    #setting cookies
    response = make_response(render_template("home.html",
                                articles=articles,
                                weather=weather,
                                base=base,
                                to_currency=to_currency,
                                rate=rate,
                                currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("base", base, expires=expires)
    response.set_cookie("to_currency", to_currency, expires=expires)
    return response

def get_news(query):
    if not query or query.lower() not in RSS_FEED:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEED[publication])
    return feed['entries']

def get_weather(query):
    query = quote(query)
    url = WEATHER_URL.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = { 'description':parsed["weather"][0]["description"],
                    'temperature':parsed["main"]["temp"],
                    'city':parsed["name"],
                    'country':parsed['sys']['country']
                   }
    return weather

def get_rate(fr, to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    base_rate = parsed.get(fr.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/base_rate, parsed.keys())

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

if __name__ == '__main__':
    app.run(port=5000, debug=True)
