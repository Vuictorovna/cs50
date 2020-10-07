import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, add_history

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    summa = 0
    stocks = db.execute("SELECT symbol, name, SUM(shares) as shares FROM history WHERE user_id = :user_id GROUP BY name",
                        user_id=user_id)

    for stock in stocks:
        symbol = stock["symbol"]
        shares = stock["shares"]
        price = lookup(symbol)["price"]
        total = shares * price
        stock["total"] = usd(total)
        stock["price"] = usd(price)
        summa += total

    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=user_id)
    balance = cash[0]["cash"]
    super_total = summa + balance
    balance = usd(balance)
    super_total = usd(super_total)

    return render_template("index.html", stocks=stocks, balance=balance, super_total=super_total )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        shares = int(request.form.get("shares"))
        if shares <= 0:
            return apology("must provide positive number", 403)

        symbol = request.form.get("symbol")
        symbol_info = lookup(symbol)
        if not symbol_info:
             return apology(f"symbol '{symbol}' does not exist", 403)

        symbol = symbol_info["symbol"]
        price = symbol_info["price"]
        name = symbol_info["name"]

        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=user_id)
        if len(rows) != 1:
            return apology("user not found", 500)

        if rows[0]["cash"] < price * shares:
            return apology("you do not have enough money", 403)

        balance = rows[0]["cash"] - price * shares
        db.execute("UPDATE users SET cash = :balance WHERE id = :user_id", user_id=user_id, balance=balance)

        add_history(db=db, user_id=user_id, symbol=symbol, company_name=name,  shares_amount=shares, price=price)

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    histories = db.execute("SELECT symbol, shares, price, transacted FROM history WHERE user_id = :user_id",
                            user_id=user_id)
    for history in histories:
        symbol = history["symbol"]
        shares = history["shares"]
        price = history["price"]
        history["price"] = usd(price)
        transacted = history["transacted"]

    return render_template("history.html", histories = histories)


@app.route("/add_cash", methods=["GET", "POST"])
def add_cash():

    if request.method == "GET":
        return render_template("add_cash.html")

    if request.method == "POST":
        user_id = session["user_id"]
        amount = int(request.form.get("amount"))
        row_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        if len(row_cash) != 1:
            return apology("user not found", 500)

        balance = amount + row_cash[0]["cash"]
        db.execute("UPDATE users SET cash = :balance WHERE id = :user_id", user_id=user_id, balance=balance)

        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        symbol = request.form.get("symbol")
        symbol_info = lookup(symbol)
        if not symbol_info:
             return apology(f"symbol '{symbol}' does not exist", 403)
        name = symbol_info.get("name")
        symbol = symbol_info.get("symbol")
        price = symbol_info.get("price")

        return render_template("quoted.html", name=name, symbol=symbol, price=price)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :hahaha",
                          hahaha=username)
        if len(rows) != 0:
            return apology("this username already exist", 403)

        password = request.form.get("password")
        if not password:
            return apology("must provide password", 403)
        if password != request.form.get("confirmation"):
            return apology("the passwords must match", 403)

        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:username,:password_hash )", username=username, password_hash=password_hash)

        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "GET":
        rows = db.execute("SELECT symbol, shares FROM history WHERE user_id = :user_id GROUP BY name", user_id=user_id)
        symbol_list = []
        for row in rows:
            shares = row["shares"]
            if shares > 0:
                symbol = row["symbol"]
                symbol_list.append(symbol)
        return render_template("sell.html", symbol_list=symbol_list)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
           return apology("missing symbol", 403)

        symbol_info = lookup(symbol)
        price = symbol_info["price"]
        name = symbol_info["name"]

        try:
            sell_shares = int(request.form.get("shares"))
        except ValueError:
            return apology("must provide number", 403)

        if sell_shares <= 0:
            return apology("must provide positive number", 403)

        total_shares = db.execute("SELECT SUM(shares) as shares FROM history WHERE symbol = :symbol and user_id = :user_id",
                                  user_id=user_id, symbol = symbol)
        if len(total_shares) != 1:
            return apology("something went wrong", 500)

        if sell_shares > total_shares[0]["shares"]:
            return apology("you do not have enough shares", 403)

        row_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        if len(row_cash) != 1:
            return apology("user not found", 500)

        balance = row_cash[0]["cash"] + price * sell_shares
        db.execute("UPDATE users SET cash = :balance WHERE id = :user_id", user_id=user_id, balance=balance)

        add_history(db=db, user_id=user_id, symbol=symbol, company_name=name,  shares_amount=-sell_shares, price=price)

        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
