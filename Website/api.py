import urllib.parse
import requests
from cs50 import SQL

db = SQL("sqlite:///finance.db")
api = "https://api.coinmarketcap.com/v1/ticker/?"
limit = input("limit:")
limit = int(limit)

url = api + urllib.parse.urlencode({"limit": limit})
json_data = requests.get(url).json()

for i in range(limit):
    naam = json_data[i]["id"]
    naam = str(naam)
    prijs = json_data[i]["price_usd"]
   # prijs = float(prijs)
    cap = json_data[i]["market_cap_usd"]
    #cap = float(cap)
    percent_1h = json_data[i]["percent_change_1h"]
    #percent_1h = float(percent_1h)
    percent_24h = json_data[i]["percent_change_24h"]
    #percent_24h = float(percent_24h)
    percent_7d = json_data[i]["percent_change_7d"]
    #percent_7d = float(percent_7d)

    #db.execute("INSERT INTO coins(naam) VALUES(:naam)", naam = naam)
    db.execute("INSERT INTO coins (naam, prijs, cap, percent_1h, percent_24h, percent_7d) VALUES(:naam, :prijs, :cap, :percent_1h, :percent_24h, :percent_7d)", naam = naam, prijs = prijs, cap = cap, percent_1h = percent_1h, percent_24h = percent_24h, percent_7d = percent_7d)
