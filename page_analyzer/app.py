from flask import Flask, render_template, url_for, flash, request, redirect
import psycopg2


from dotenv import load_dotenv
import os
from psycopg2.extras import NamedTupleCursor
from validators import url as validate_url
from urllib.parse import urlparse
import requests

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    return render_template("index.html", title="Анализатор страниц")


@app.post("/urls")
def urls_post():
    actual_url = request.form.get("url")
    if validate_url(actual_url):
        scheme = urlparse(actual_url).scheme
        hostname = urlparse(actual_url).hostname
        url = f"{scheme}://{hostname}"
        if check_url_exists(url):
            url_id = insert_url_in_urls(url)
            flash("Страница успешно добавлена", category="info")
            return redirect(url_for("url_page", id=url_id))
        else:
            flash("Страница уже существует", category="info")
            url_id = find_id_by_url(url)
            return redirect(url_for("url_page", id=url_id))
    elif not validate_url(actual_url) or len(actual_url) > 255:
        flash("Некорректный URL", category="danger")
        return render_template("index.html", 422)


# if __name__ == '__main__':
#       app.run()
