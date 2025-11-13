
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from urllib.parse import urlparse
#from hyprnews.auth import login_required
from .models import Article

bp = Blueprint('news', __name__)

@bp.route('/')
def index():

    articles = (
        Article.query
        .order_by(Article.created.desc())
        .limit(10)
        .all()
    )

    # articles = Article.query.order_by(Article.created.desc()).limit(10).all()

    return render_template('news/index.html', articles=articles)


@bp.route('/article/<id>')
def article(id):
    article = Article.query.get(id)

    if article is None:
        abort(404, f"Article id {id} doesn't exist.")

    parsed = urlparse(article.url)

    return render_template(
        "news/article.html",
        title  = article.title,
        body   = article.body,
        url    = article.url,
        domain = parsed.hostname,
    )


@bp.route("/new", methods=["GET", "POST"])
def new_article():
    if request.method == "POST":
        title   = request.form.get("title")
        content = request.form.get("content")
        url     = request.form.get("url")

        if title and content:
            article = Article(title=title, body=content, url=url)
            article.save()
            return redirect(url_for("news.article", id=article.id))

    return render_template("news/form.html")
