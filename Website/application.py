from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
from collections import Counter, defaultdict

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
votes = []

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

        # If add button is selected, add to favorites.
        if request.form.get("coin") != None :
            coin = request.form.get("coin")
            add = db.execute("INSERT INTO favorites(id,naam) VALUES(:id, :coin)", id = session["user_id"], coin = coin)

        # Ff up button is selected add coin to votes.
        elif request.form.get("up") != None :
            up = request.form.get("up")
            votes.append(up)
            up = db.execute("INSERT INTO upvote(id,coin) VALUES(:id, :coin)", id = session["user_id"], coin = up)
            print (votes)

        # If down button is selected remove 1 instance of coin from list (if in list).
        elif request.form.get("down") != None :
            down = request.form.get("down")
            if down in votes:
                votes.remove(down)
            add = db.execute("DELETE FROM upvote(coin) VALUES(:coin)", coin = down)

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
        naam = request.form.get("symbol").lower()

        if request.method == "POST":
            search = db.execute("SELECT * from coins WHERE naam = :naam", naam = naam)

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

        # Select user's cash.
        money = db.execute("SELECT cash FROM users WHERE id = :id", \
                            id = session["user_id"])

        # Check if enough money to buy.
        if not money or float(money[0]["cash"]) < search[0]["prijs"] * amount:
            flash("You don't have enough money!")
            return redirect(url_for("buy"))

        # Update history.
        db.execute("INSERT INTO histories (symbol, shares, price, id) \
                    VALUES(:symbol, :shares, :price, :id)", \
                    symbol=search[0]["naam"], shares=amount, \
                    price=(search[0]["prijs"]), id=session["user_id"])

        # Update user cash.
        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=search[0]["prijs"] * float(amount))

        # Select user shares of that symbol.
        user_shares = db.execute("SELECT shares FROM portfolio \
                           WHERE id = :id AND symbol=:symbol", \
                           id=session["user_id"], symbol=search[0]["naam"])

        # If user doesn't has shares of that symbol, create new stock object.
        if not user_shares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, id) \
                        VALUES(:name, :shares, :price, :total, :id)", \
                        name=search[0]["naam"], shares=amount, price=(search[0]["prijs"]), \
                        total=(amount * search[0]["prijs"]), \
                        id=session["user_id"])

        # Else increment the shares count.
        else:
            shares_total = user_shares[0]["shares"] + amount
            db.execute("UPDATE portfolio SET shares=:shares \
                        WHERE id=:id AND symbol=:symbol", \
                        shares=shares_total, id=session["user_id"], \
                        symbol=search[0]["naam"])

        # Return to index.
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
    # Forget any user_id.
    session.clear()

    # If user reached route via POST (as by submitting a form via POST).
    if request.method == "POST":

        # Ensure username was submitted.
        if not request.form.get("username"):
            flash("You forgot to enter your username!")
            return redirect(url_for("login"))

        # Ensure password was submitted.
        elif not request.form.get("password"):
            flash("You forgot to enter your password!")
            return redirect(url_for("login"))

        # Query database for username.
        rows = db.execute("SELECT * FROM users \
                           WHERE username = :username", \
                           username=request.form.get("username"))

        # Ensure username exists and password is correct.
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            flash("This username/password combination is invalid!")
            return redirect(url_for("login"))


        # Remember which user has logged in.
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["cash"] = rows[0]["cash"]


        # Redirect user to home page.
        return redirect(url_for("index2"))

    # Else if user reached route via GET (as by clicking a link or via redirect).
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""
    # Forget any user_id.
    session.clear()

    # Redirect user to login form.
    return redirect(url_for("index"))

@app.route("/quote", methods=["GET", "POST"])
def quote():
    """Get coin information."""
    if request.method == "POST":
        api(100)

        # Lookup the (lowered) input symbol in database.
        naam = request.form.get("symbol").lower()

        search = db.execute("SELECT * from coins WHERE naam = :naam", naam = naam)

        # In case of failed search return flash error message.
        if not search:
            flash("The coin you entered does not exist!")

        return render_template("quoted.html", coins=search)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        # Ensure username was submitted.
        if not request.form.get("username"):
            flash("You forgot to enter a username!")
            return redirect(url_for("register"))

        # Ensure password was submitted.
        elif not request.form.get("password"):
            flash("You forgot to enter a password!")
            return redirect(url_for("register"))

        # Ensure password and verified password is the same.
        elif request.form.get("password") != request.form.get("passwordagain"):
            flash("The passwords you provided do not match!")
            return redirect(url_for("register"))

        # Insert the new user into users, storing the hash of the user's password.
        result = db.execute("INSERT INTO users (username, hash) \
                             VALUES(:username, :hash)", \
                             username=request.form.get("username"), \
                             hash=pwd_context.hash(request.form.get("password")))

        if not result:
            flash("The username you provided does already exist!")
            return redirect(url_for("register"))

        # Remember which user has logged in.
        session["user_id"] = result

        # Redirect user to home page.
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
        naam = request.form.get("symbol").lower()

        if request.method == "POST":
            search = db.execute("SELECT * from coins WHERE naam = :naam", naam = naam)

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

        # Select the symbol shares of that user.
        user_shares = db.execute("SELECT shares FROM portfolio \
                                 WHERE id = :id AND name=:name", \
                                 id=session["user_id"], name=search[0]["naam"])

        # Check if enough shares to sell.
        if not user_shares or int(user_shares[0]["shares"]) < amount:
            flash("You don't have that amount of coins!")
            return redirect(url_for("sell"))

        # Update history of a sell.
        db.execute("INSERT INTO histories (symbol, shares, price, id) \
                    VALUES(:symbol, :shares, :price, :id)", \
                    symbol=search[0]["naam"], shares=-amount, \
                    price=(search[0]["prijs"]), id=session["user_id"])

        # Update user cash (increase).
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=search[0]["prijs"] * float(amount))

        # Decrement the shares count.
        shares_total = user_shares[0]["shares"] - amount

        # If after decrement is zero, delete shares from portfolio.
        if shares_total == 0:
            db.execute("DELETE FROM portfolio \
                        WHERE id=:id AND symbol=:symbol", \
                        id=session["user_id"], \
                        symbol=search[0]["naam"])

        # Otherwise, update portfolio shares count.
        else:
            db.execute("UPDATE portfolio SET shares=:shares \
                    WHERE id=:id AND symbol=:symbol", \
                    shares=shares_total, id=session["user_id"], \
                    symbol=search[0]["naam"])
        # Return to index.
        return redirect(url_for("index2"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    api(100)

    # Delete coin from favorites when delete button is pressed.
    if request.method == "POST":
        coin = request.form.get("coin")
        remove = db.execute("DELETE FROM favorites WHERE id = :id and naam = :coin",\
                            id = session["user_id"], coin = coin)

    # Retrive favorites and portfolio from database.
    favorites = db.execute("SELECT DISTINCT naam from favorites WHERE id = :id",\
                            id = session["user_id"])
    portfolio = db.execute("SELECT DISTINCT name FROM portfolio WHERE id = :id",\
                            id=session["user_id"])
    amount = db.execute("SELECT name, shares FROM portfolio WHERE id = :id",\
                            id=session["user_id"])
    all_votes = Counter(votes)


    favorites_length = len(favorites)
    portfolio_length = len(portfolio)
    votes_length = len(votes)

    all_favorite_coins = [db.execute("SELECT * from coins WHERE naam = :naam",\
                            naam = favorites[i]["naam"]) for i in range (favorites_length)]
    all_portfolio_coins = [db.execute("SELECT * from coins WHERE naam = :naam",\
                            naam = portfolio[i]["name"]) for i in range (portfolio_length)]
    all_votes_coins = [db.execute("SELECT * from coins WHERE naam = :naam",\
                            naam = i) for i in all_votes]


    favorites_list = ([i for coin in all_favorite_coins for i in coin])
    portfolio_list = ([i for coin in all_portfolio_coins for i in coin])
    votes_list = ([i for coin in all_votes_coins for i in coin])

    possess_amount = defaultdict(int)

    for d in amount:
        possess_amount[d['name']] += int(d['shares'])

    return render_template("profile.html", favorite_coins = favorites_list,\
                            portfolio_coins = portfolio_list, vote_coins = votes_list, \
                            username = session["username"], money = str(round(session["cash"], 2)),\
                            vote_amount = all_votes, possessed = possess_amount)


@app.route("/password", methods=["GET", "POST"])
def password():
    '''Change password if user is logged in'''

    if request.method == "POST":
        # Checkt of er iets ingevuld is.
        if not request.form.get("old_pwd"):
            flash("You forgot to enter your old password!")
            return redirect(url_for("password"))

        elif not request.form.get("new_pwd"):
            flash("You forgot to enter a new password!")
            return redirect(url_for("password"))

        elif not request.form.get("confirm_pwd"):
            flash("You forgot to confirm your new password!")
            return redirect(url_for("password"))

        # Checkt of nieuwe password en conformation password hetzelfde zijn.
        if request.form.get("confirm_pwd") != request.form.get("new_pwd"):
            flash("The passwords you provided do not match!")
            return redirect(url_for("password"))

        # checkt of het oude Password correct is
        code = db.execute("SELECT hash FROM users WHERE id= :id", id=session["user_id"])

        # http://passlib.readthedocs.io
        if not pwd_context.verify(request.form.get("old_pwd"), code[0]["hash"]):
            flash("The old password you provided is incorrect!")
            return redirect(url_for("password"))

        # Update de user tabel in de
        db.execute("UPDATE users SET hash= :hash WHERE id= :id",\
                    hash=pwd_context.hash(request.form.get("new_pwd")), id=session["user_id"])

        flash("You've succesfully changed your password!")
        return redirect(url_for("index"))

    else:
        return render_template("password.html")

@app.route("/loan", methods=["GET", "POST"])
@login_required
def loan():
    """Get a loan."""

    if request.method == "POST":

        # Ensure must be integers.
        try:
            amount = request.form.get("loan").lower()
            loan = int(amount)

            if loan < 0:
                return apology("Loan must be positive amount")
            elif loan > 1000:
                flash("Cannot loan more than $1,000 at once")
                return redirect(url_for("loan"))
        except:
            flash("Loan must be positive integer")
            return redirect(url_for("loan"))

        # Update user cash (increase).
        db.execute("UPDATE users SET cash = cash + :loan WHERE id = :id", \
                    loan=loan, id=session["user_id"])

        # Return to index.
        flash("Loan is successful", "No need to pay me back")
        return redirect(url_for("loan"))
    else:
        return render_template("loan.html")
