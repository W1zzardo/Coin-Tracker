from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

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

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

    profile = db.execute("SELECT * FROM portfolios WHERE id=:id", id=session["user_id"])
    return render_template("index.html", profile=profile)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":

        # valid name submitted
        if not request.form.get("symbol"):
            return apology("No Symbol")
        elif not request.form.get("shares"):
            return apology("No shares")

        # Symbols worden hoofdletters
        symbol = request.form.get("symbol").upper()

        # Gebruik lookup functie van helpers.py voor het ophalen van YAHOO DB
        quote = lookup(symbol)

        # check of het ophalen van de data niet gelukt is
        if quote == None:
            return apology("Invalid Symbol")

        # vul shares in
        shares = int(request.form.get("shares"))

        # checkt of iets wordt in gevuld
        if shares < 0:
            return apology("Positive integer needed!")

        # select user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = int(cash[0]["cash"])
        cash_new = cash - quote["price"] * shares

        # check if you can afford the shares
        if  cash_new < 0:
            return apology("Not enough cash!")

        db.execute("UPDATE users SET cash = :cash_new WHERE id = :id ", cash_new=cash_new, id=session['user_id'])
        # koop shares en update cash
        rows = db.execute("SELECT * FROM portfolios WHERE id = :id AND symbol=:symbol", id=session['user_id'], symbol=symbol)

        # Als hij de shares nog niet heeft maak nieuwe rij in de portfolio
        if len(rows) == 0:
            db.execute("INSERT INTO portfolios (id, symbol, shares) VALUES (:id, :symbol, :shares)", id=session["user_id"], symbol=symbol, shares=shares)
        # Anders update de shares
        else:
            db.execute("UPDATE portfolios SET shares= shares + :shares WHERE id=:id", shares=shares, id=session["user_id"])

        # Update history
        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES (:id, :symbol, :shares, :price)", id=session["user_id"], symbol=symbol, shares=shares, price=quote["price"])

        # redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("buy.html")




@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    geschiedenis = db.execute("SELECT * FROM history WHERE id=:id", id=session["user_id"])

    return render_template("history.html", geschiedenis=geschiedenis)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    # forget any user_id
    session.clear()
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        row = request.form.get("symbol")
        # valid name submitted
        if not row:
            return apology("No Symbol")

        # Symbols worden hoofdletters
        symbol = request.form.get("symbol").upper()

        # Gebruik lookup functie van helpers.py voor het ophalen van YAHOO DB
        quote = lookup(symbol)
        # check of het ophalen van de data niet gelukt is
        if quote == None:
            return apology("Invalid Symbol")

        return render_template("quoted.html", name=quote["name"], symbol=symbol, price=quote["price"])

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # forget any user_id
    session.clear()

     # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password_check was submitted
        elif not request.form.get("password_check"):
            return apology("must provide password")
        # ensure passwords are equal
        elif request.form.get("password") != request.form.get("password_check"):
            return apology("password did not match")

        # add user into database
        result = db.execute("INSERT  INTO users(username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

        # if the username already exists -> messege
        if not result:
            return apology("Username already taken")

        # vraag username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":

        # valid name submitted
        if not request.form.get("symbol"):
            return apology("No Symbol")

        # Symbols worden hoofdletters
        symbol = request.form.get("symbol").upper()

        # Gebruik lookup functie van helpers.py voor het ophalen van YAHOO DB
        quote = lookup(symbol)

        # check of het ophalen van de data niet gelukt is
        if quote == None:
            return apology("Invalid Symbol")

        # vul shares in
        shares = int(request.form.get("shares"))

         # kijkt of de user de shares heeft die hij wilt verkopen
        owned_shares = db.execute("SELECT shares FROM portfolios WHERE id= :id AND symbol= :symbol", id=session["user_id"], symbol=symbol)
        if (len(owned_shares)) == 0:
            return apology("symbol niet in bezit")

        own_shares = owned_shares[0]["shares"]
        updated_shares = own_shares - shares
        if (updated_shares) < 0:
            return apology("U don't have these shares")

        # cash neemt toe met het bedrag van cash_sell
        price = quote["price"]
        cash_sell = price * shares;

        # update de user tabel in de D.B
        db.execute("UPDATE users SET cash = cash + :cash_sell WHERE id = :id", cash_sell=cash_sell, id=session['user_id'])

        # update portfolios tabel in de D.B, maar als shares 0 is, delete hele rij
        if updated_shares == 0:
            db.execute("DELETE FROM portfolios WHERE id = :id AND symbol=:symbol", id=session['user_id'], symbol=symbol)
        # anders
        elif updated_shares > 0:
            db.execute("UPDATE portfolios SET shares= :updated_shares WHERE id = :id", updated_shares=updated_shares, id=session["user_id"])

        # update history tabel in de D.B (negatieve shares)
        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES (:id, :symbol, :shares, :price)", id=session["user_id"], symbol=symbol, shares=-(shares), price=price)

        # redirect user to home page
        return redirect(url_for("index"))
    else:
        return render_template("sell.html")


@app.route("/password", methods=["GET", "POST"])
def password():
    '''Change password if user is logged in'''
    if request.method == "POST":
        # checkt of er iets ingevuld is
        if not request.form.get("old_pwd"):
            return apology("Please enter old password")
        elif not request.form.get("new_pwd"):
            return apology("Please enter new password")
        elif not request.form.get("confirm_pwd"):
            return apology("Please enter new password again")

        # checkt of nieuwe password en conformation password hetzelfde zijn
        if request.form.get("confirm_pwd") != request.form.get("new_pwd"):
            return apology("Password do not match")

        # checkt of het oude Password correct is
        code = db.execute("SELECT hash FROM users WHERE id= :id", id=session["user_id"])

        # http://passlib.readthedocs.io
        if not pwd_context.verify(request.form.get("old_pwd"), code[0]["hash"]):
            return apology("old password is incorrect...")

        # update de user tabel in de D.B ZIE REGISTER!
        db.execute("UPDATE users SET hash= :hash WHERE id= :id", hash=pwd_context.hash(request.form.get("new_pwd")), id=session["user_id"])
        flash("password changed!")
        return redirect(url_for("index"))

    else:
        return render_template("password.html")



