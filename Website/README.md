
# Cointracker 
### Made by: Vincent Kleiman (11884622), Thimo Janssen (11569166), Gregory Slager (11432853)
                

![foto](docs/cointracker.png)

## Features Cointracker offers

- Cryptocurrency tracker

Cointracker keeps track of the top 100 cryptocurrencies based on marketcap. On the main page the user will find a sorted list with: the name of the cryptocurrency, the current price, the market cap, the 1 hour change, the 24 hour change and the 7 day change of the coins worth. 

- Personal favorites & vote buttons

Registered users are able to create their own personal watchlist. When logged in the user will find 3 new buttons have appeard: an "add" button, an "up" button and a "down" button respectively. These buttons act accordingly to their name. The add button adds the selected coin to the users list of favorite coins. The up-button upvotes the coin. The down-button downvotes the coin. The use of these last two coins will be explained in the "social" paragraph. 

- Practiceground for wannabe investors

Cointracker offers a practiceground for wannabe investers. Upon registration the user will receive USD 1000 (simulated) to fictively by and sell assets in order to practice investing before using real money. When buying cryptocurrency, the user will be able to keep track of the currency they own through their portfolio.

- Social 

To add a social aspect to the website, cointrackers uses an up- and downvote system. Through up and downvoting coins users are able to indirecly communicate to the community. On the personal dashboard the user will find an overview of the most upvoted and downvoted coins of the day. This can help the user in deciding which coins are worth researching.

## Noteworthy items

- The sites uses a live database, which updates every 5 minutes by default.
- The text format on index depends on the number it represents (red, green)
- Fully custom designed logo
- The searchbar is case and whitespace insensitive

## Cointracker development process

The develompent consist of the 3 UvA students listed in the subtitle of this readme. Each of the teammembers had their own specialty; Vincent was the main html/css developer; Thimo was the main GIT engineer as well as the python supervisor; Gregory was the main SQL engineer. Apart from those tasks each member contributed to application.py. 

## Cointracker GIT repository

The repository can be found here: https://github.com/W1zzardo/Coin-Tracker.git.
The main folder "Website" consists of 2 subfolders, 2 python files and 1 database file. 

The CSS can be found in subfolder "static". 

In "templates" subfolder you will find all templates refered to in application.py. 

Application.py is the controler of the site.
All functions for all pages can be found in this file. 

Helpers.py cointains the most used functions such as search functions (in order to keep application.py as clean as possible).

Finally "finance.db" is the websites database. All stored data can be found here. 

## Productvideo

The productvideo can be found here: https://www.youtube.com/watch?v=gVF6QzpzYDU