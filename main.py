from flask import Flask
from flask import render_template

from database import db


app = Flask(__name__)


def get_context(view):
    return {
        "quote": db.quotes.find_one(),
        "latest_articles": db.articles.find().limit(5).sort("date"),
        "has_more_articles": db.articles.find().count() > 5,
        "view": view
    }


@app.route('/<article_name>')
def article_by_name(article_name):
    return render_template("index.html", context=get_context("article"), article=db.articles.find_one())


@app.route('/')
def index():
    return render_template("index.html", context=get_context("main"))


@app.route('/list')
def articles_list():
    return render_template("index.html", context=get_context("article_list"), articles=db.articles.find())


@app.route('/tags/<tag_list>')
def articles_by_dags(tag_list):
    html_result = ""
    query_result = db.articles.find({"tags": {"$in": tag_list.split(",")}})
    for result in query_result:
        html_result += str(result) + "</br>"

    return html_result


if __name__ == '__main__':
    app.debug = True
    app.run()