from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *
import time
# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
def index():
    api(50)
    # select each symbol owned by the user and it's amount
    coins = db.execute("SELECT * from coins")

    return render_template("index.html", coins = coins)

@app.route("/index2", methods=["GET", "POST"])
@login_required
def index2():
    api(50)

    coins = db.execute("SELECT * from coins")

    if request.method == "POST":

        if request.form.get("coin") != None :
            coin = request.form.get("coin")
            add = db.execute("INSERT INTO favorites(id,naam) VALUES(:id, :coin)", id = session["user_id"], coin = coin)

        elif request.form.get("up") != None :
            up = request.form.get("up")
            up = db.execute("INSERT INTO upvote(id,coin) VALUES(:id, :coin)", id = session["user_id"], coin = up)

        elif request.form.get("down") != None :
            down = request.form.get("down")
            add = db.execute("INSERT INTO downvote(id,coin) VALUES(:id, :coin)", id = session["user_id"], coin = down)

    return render_template("index2.html", coins = coins )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy a coin"""
    api(100)
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # Checks if the coin exists.
        if request.method == "POST":
            search = db.execute("SELECT * from coins WHERE naam = :naam", naam = request.form.get("symbol"))

        if not search:
            flash("The coin you entered does not exist!")
            return redirect(url_for("buy"))

        # Checks if a valid amount is bought.
        try:
            amount = int(request.form.get("amount"))
            if amount < 0:
                flash("You must buy a positve amount of coins!")
                return redirect(url_for("buy"))
        except:
            flash("You must buy a positve amount of coins!")
            return redirect(url_for("buy"))

        # select user's cash
        money = db.execute("SELECT cash FROM users WHERE id = :id", \
                            id = session["user_id"])

        # check if enough money to buy
        if not money or float(money[0]["cash"]) < search[0]["prijs"] * amount:
            flash("You don't have enough money!")
            return redirect(url_for("buy"))

        # update history
        db.execute("INSERT INTO histories (symbol, shares, price, id) \
                    VALUES(:symbol, :shares, :price, :id)", \
                    symbol=search[0]["naam"], shares=amount, \
                    price=usd(search[0]["prijs"]), id=session["user_id"])

        # update user cash
        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=search[0]["prijs"] * float(amount))

        # Select user shares of that symbol
        user_shares = db.execute("SELECT shares FROM portfolio \
                           WHERE id = :id AND symbol=:symbol", \
                           id=session["user_id"], symbol=search[0]["naam"])

        # if user doesn't has shares of that symbol, create new stock object
        if not user_shares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, id) \
                        VALUES(:name, :shares, :price, :total, :id)", \
                        name=search[0]["naam"], shares=amount, price=usd(search[0]["prijs"]), \
                        total=usd(amount * search[0]["prijs"]), \
                        id=session["user_id"])

        # Else increment the shares count
        else:
            shares_total = user_shares[0]["shares"] + amount
            db.execute("UPDATE portfolio SET shares=:shares \
                        WHERE id=:id AND symbol=:symbol", \
                        shares=shares_total, id=session["user_id"], \
                        symbol=search[0]["naam"])

        # return to index
        return redirect(url_for("index2"))


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    histories = db.execute("SELECT * from histories WHERE id=:id", id=session["user_id"])

    return render_template("history.html", histories=histories)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("You forgot to enter your username!")
            return redirect(url_for("login"))

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("You forgot to enter your password!")
            return redirect(url_for("login"))

        # query database for username
        rows = db.execute("SELECT * FROM users \
                           WHERE username = :username", \
                           username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            flash("This username/password combination is invalid!")
            return redirect(url_for("login"))


        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]


        # redirect user to home page
        return redirect(url_for("index2"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""
    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("index"))

@app.route("/quote", methods=["GET", "POST"])
def quote():
    """Get coin information."""
    if request.method == "POST":
        api(100)
        naam = request.form.get("symbol").lower()

        search = db.execute("SELECT * from coins WHERE naam = :naam", naam = naam)

        if not search:
            flash("The coin you entered does not exist!")

        return render_template("quoted.html", coins=search)

    else:
        return render_template("quote.html")

@app.route("/favs", methods=["GET", "POST"])
@login_required
def favs():

    api(100)

    if request.method == "POST":
        search = db.execute("SELECT * from coins WHERE naam = :naam", naam = request.form.get("symbol"))
        add = db.execute("INSERT INTO favorites(id,naam) VALUES(:id, :naam)", id = session["user_id"], naam =  request.form.get("symbol"))

        if not search:
            flash("The coin you entered does not exist!")
            return redirect(url_for("index2"))


        return render_template("favs.html", coins=search)

    else:
        return render_template("favs.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("You forgot to enter a username!")
            return redirect(url_for("register"))

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("You forgot to enter a password!")
            return redirect(url_for("register"))

        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("passwordagain"):
            flash("The passwords you provided do not match!")
            return redirect(url_for("register"))

        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users (username, hash) \
                             VALUES(:username, :hash)", \
                             username=request.form.get("username"), \
                             hash=pwd_context.hash(request.form.get("password")))

        if not result:
            flash("The username you provided does already exist!")
            return redirect(url_for("register"))

        # remember which user has logged in
        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("index2"))

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell a coin"""
    api(100)

    if request.method == "GET":
        return render_template("sell.html")

    else:
        # Checks if the coin exists.
        if request.method == "POST":
            search = db.execute("SELECT * from coins WHERE naam = :naam", naam = request.form.get("symbol"))

        if not search:
            flash("The coin you entered does not exist!")
            return redirect(url_for("sell"))

        # Checks if a valid amount is sold.
        try:
            amount = int(request.form.get("amount"))
            if amount < 0:
                flash("You must sell a positve amount of coins!")
                return redirect(url_for("sell"))
        except:
            flash("You must sell a positve amount of coins!")
            return redirect(url_for("sell"))

        # select the symbol shares of that user
        user_shares = db.execute("SELECT shares FROM portfolio \
                                 WHERE id = :id AND name=:name", \
                                 id=session["user_id"], name=search[0]["naam"])

        # check if enough shares to sell
        if not user_shares or int(user_shares[0]["shares"]) < amount:
            flash("You don't have that amount of coins!")
            return redirect(url_for("sell"))

        # update history of a sell
        db.execute("INSERT INTO histories (symbol, shares, price, id) \
                    VALUES(:symbol, :shares, :price, :id)", \
                    symbol=search[0]["naam"], shares=-amount, \
                    price=usd(search[0]["prijs"]), id=session["user_id"])

        # update user cash (increase)
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=search[0]["prijs"] * float(amount))

        # decrement the shares count
        shares_total = user_shares[0]["shares"] - amount

        # if after decrement is zero, delete shares from portfolio
        if shares_total == 0:
            db.execute("DELETE FROM portfolio \
                        WHERE id=:id AND symbol=:symbol", \
                        id=session["user_id"], \
                        symbol=search[0]["naam"])
        # otherwise, update portfolio shares count
        else:
            db.execute("UPDATE portfolio SET shares=:shares \
                    WHERE id=:id AND symbol=:symbol", \
                    shares=shares_total, id=session["user_id"], \
                    symbol=search[0]["naam"])
        # return to index
        return redirect(url_for("index2"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    api(100)

    if request.method == "POST":
        coin = request.form.get("coin")
        remove = db.execute("DELETE FROM favorites WHERE id = :id and naam = :coin", id = session["user_id"], coin = coin)

    coins1 = db.execute("SELECT DISTINCT naam from favorites WHERE id = :id", id = session["user_id"])
    lengte = len(coins1)

    coins = [db.execute("SELECT * from coins WHERE naam = :naam", naam = coins1[i]["naam"]) for i in range (lengte)]
    lijst = []
    for coin in coins:
        for i in coin:
            lijst.append(i)

    return render_template("profile.html", coins = lijst )


@app.route("/password", methods=["GET", "POST"])
def password():
    '''Change password if user is logged in'''

    if request.method == "POST":
        # checkt of er iets ingevuld is
        if not request.form.get("old_pwd"):
            flash("You forgot to enter your old password!")
            return redirect(url_for("password"))

        elif not request.form.get("new_pwd"):
            flash("You forgot to enter a new password!")
            return redirect(url_for("password"))

        elif not request.form.get("confirm_pwd"):
            flash("You forgot to confirm your new password!")
            return redirect(url_for("password"))

        # checkt of nieuwe password en conformation password hetzelfde zijn
        if request.form.get("confirm_pwd") != request.form.get("new_pwd"):
            flash("The passwords you provided do not match!")
            return redirect(url_for("password"))

        # checkt of het oude Password correct is
        code = db.execute("SELECT hash FROM users WHERE id= :id", id=session["user_id"])

        # http://passlib.readthedocs.io
        if not pwd_context.verify(request.form.get("old_pwd"), code[0]["hash"]):
            flash("The old password you provided is incorrect!")
            return redirect(url_for("password"))

        # update de user tabel in de D.B ZIE REGISTER!
        db.execute("UPDATE users SET hash= :hash WHERE id= :id", hash=pwd_context.hash(request.form.get("new_pwd")), id=session["user_id"])
        flash("You've succesfully changed your password!")
        return redirect(url_for("index"))

    else:
        return render_template("password.html")

@app.route("/clipboard", methods=["GET", "POST"])
def clipboard():
    """Post to the clipboard"""

    if request.method == "POST":
        post = db.execute("INSERT INTO clipboard (id, message) VALUES(:id, :message)", id = session["user_id"], message = request.form.get("message"))

        return redirect(url_for("index2"))

    else:
        return render_template("clipboard.html")

#def portfolio():

#    # select each symbol owned by the user and it's amount
#    portfolio_symbols = db.execute("SELECT shares, symbol \
#                                    FROM portfolio WHERE id = :id", \
#                                    id=session["user_id"])


    # create a temporary variable to store TOTAL worth ( cash + share)
#    total_cash = 0

    # update each symbol prices and total
#    for portfolio_symbol in portfolio_symbols:
#        symbol = portfolio_symbol["symbol"]
#        shares = portfolio_symbol["shares"]
#        stock = lookup(symbol)
#        total = shares * stock["price"]
#        total_cash += total
#        db.execute("UPDATE portfolio SET pri     ce=:price, \
#                    total=:total WHERE id=:id AND symbol=:symbol", \
#                    price=usd(stock["price"]), \
#                   total=usd(total), id=session["user_id"], symbol=symbol)

    # update user's cash in portfolio
#    updated_cash = db.execute("SELECT cash FROM users \
#                               WHERE id=:id", id=session["user_id"])

    # update total cash -> cash + shares worth
#    total_cash += updated_cash[0]["cash"]

    # print portfolio in index homepage
#    updated_portfolio = db.execute("SELECT * from portfolio \
#                                    WHERE id=:id", id=session["user_id"])



