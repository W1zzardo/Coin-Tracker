import csv
import urllib.request
import urllib.parse
import requests
from cs50 import SQL
import time


from flask import redirect, render_template, request, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def api(limit):
    db = SQL("sqlite:///finance.db")
    api = "https://api.coinmarketcap.com/v1/ticker/?"


    url = api + urllib.parse.urlencode({"limit": limit})
    json_data = requests.get(url).json()
    db.execute("DELETE FROM coins")

    for i in range(limit):
        naam = json_data[i]["id"]
        naam = str(naam)
        prijs = json_data[i]["price_usd"]
        cap = json_data[i]["market_cap_usd"]
        percent_1h = json_data[i]["percent_change_1h"]
        percent_24h = json_data[i]["percent_change_24h"]
        percent_7d = json_data[i]["percent_change_7d"]

        db.execute("INSERT INTO coins (naam, prijs, cap, percent_1h, percent_24h, percent_7d) VALUES(:naam, :prijs, :cap, :percent_1h, :percent_24h, :percent_7d)", naam = naam, prijs = prijs, cap = cap, percent_1h = percent_1h, percent_24h = percent_24h, percent_7d = percent_7d)

def aandelen(user_shares):
    a = 0
    lengte = len(user_shares)
    for i in range(lengte):
        a += user_shares[i]["shares"]

    return(a)