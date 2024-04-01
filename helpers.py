import csv
import os
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"), ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(symbol):
    # Reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None
    
    # Reject symbol if it contains comma
    if "," in symbol:
        return None
    
    # Query Alpha Vantage for quote
    # https://www.alphavantage.co/documentation/
    try:
        
        # GET CSV
        url = f"https://www.alphavantage.co/query?apikey={os.getenv('API_KEY')}&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol={symbol}"
        webpage = urllib.request.urlopen(url)
        
        # Parse CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())
        
        # Ignore first row
        next(datareader)
        
        # Parse second row
        row = next(datareader)
        
        # Ensure stock exists
        try:
            price = float(row[4])
        except:
            return None
        
        # Return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {"price": price, "symbol": symbol.upper()}
        
    except:
        return None

def usd(value):
    return f"${value:,.2f}"
