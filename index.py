from flask import Flask, render_template, request, redirect
from tinydb import TinyDB, Query
import json
import requests
from twitterscraper import query_tweets
from datetime import datetime

db = TinyDB("db.json")
DEVELOPMENT_ENV = True

app = Flask(__name__)


app_data = {
    "name": "Python-Stock-Scraper",
    "description": "A basic yet powerful Python Stock Scraper Project made with flask",
    "author": "julian4u0",
    "html_title": "PSS v1.0",
    "project_name": "PythonStockScraper",
    "keywords": "webapp, stock, scraper",
}


@app.route("/")
def index():
    all = db.all()

    symbols_arr = []
    for s in all:
        symbols_arr.append("NASDAQ:" + str(s["symbol"]))

    url = "https://scanner.tradingview.com/america/scan"
    params = {
        "filter": [
            {"left": "market_cap_basic", "operation": "nempty"},
            {"left": "type", "operation": "in_range", "right": ["stock", "dr", "fund"]},
            {
                "left": "subtype",
                "operation": "in_range",
                "right": [
                    "common",
                    "",
                    "etf",
                    "unit",
                    "mutual",
                    "money",
                    "reit",
                    "trust",
                ],
            },
            {
                "left": "exchange",
                "operation": "in_range",
                "right": ["NYSE", "NASDAQ", "AMEX"],
            },
        ],
        "options": {"lang": "en"},
        "symbols": {"query": {"types": []}, "tickers": symbols_arr},
        "columns": [
            "logoid",
            "name",
            "close",
            "change",
            "change_abs",
            "Recommend.All",
            "volume",
            "market_cap_basic",
            "price_earnings_ttm",
            "earnings_per_share_basic_ttm",
            "number_of_employees",
            "sector",
            "description",
            "name",
            "type",
            "subtype",
            "update_mode",
            "pricescale",
            "minmov",
            "fractional",
            "minmove2",
        ],
        "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
        "range": [0, 150],
    }
    
    print(str(datetime(2000,1,1)))
    tweets = query_tweets('TSLA', limit=None, begindate = datetime(2020,1,1), enddate= datetime(2020,1,2), poolsize=20, lang='en')

    print(tweets)

    # print the retrieved tweets to the screen:
    for tweet in tweets:
        print(tweet)


    r = requests.post(url=url, data=json.dumps(params))

    print(r.json()["data"])
    return render_template(
        "index.html",
        app_data=app_data,
        symbols=r.json()["data"],
        sdata=[
            {"name": "AAPL", "activity": 11.2},
            {"name": "TSLA", "activity": 133.2},
            {"name": "MSFT", "activity": 101.2},
        ],
    )


@app.route("/add_symbol", methods=["POST"])
def add_symbol():
    db.insert({"symbol": request.form["symbol"]})
    print("Added: " + request.form["symbol"])
    return redirect("/")


@app.route("/delete_all")
def delete_all():
    db.truncate()
    db.all()
    print("Database cleaned")
    return redirect("/")


@app.route("/about")
def about():
    db.insert({"type": "peach", "count": 3})
    return render_template("index.html", app_data=app_data)  # por hacer


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)

