from flask import Flask
from flask import render_template
from flask import g

import sqlite3

DATABASE = "elegant-pixel.db"

def db_get():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def db_query(query, args=(), one=False):
    cur = db_get().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_daily_quote():
    quote = db_query("select * from quotes where id = 1", one=True)
    return {'text' : quote[1], 'author': quote[2]}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html", quote=get_daily_quote())

if __name__ == '__main__':
    app.debug = True
    app.run()