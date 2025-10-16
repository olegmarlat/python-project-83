import os
from urllib.parse import urlparse

import psycopg2
import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from psycopg2.extras import NamedTupleCursor
from validators import url as validate_url

from .parser import parse_page

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


@app.route('/urls')
def urls_get():
    urls = get_list_of_urls.all_urls()
    return render_template(
        'urls.html',
        urls=urls
    )


@app.get("/urls/<int:id>")
def url_page(id):
    page = get_data_from_urls(id)
    checks = get_data_from_url_checks(id)
    if page:
        id, name, created_at = page
        return render_template(
            "url_page.html",
            name=name,
            id=id,
            created_at=created_at,
            data=checks
        )
    else:
        return render_template("404.html")


@app.post("/urls/<int:id>/checks")
def url_check(id):
    url = get_data_from_urls(id)[1]
    try:
        response = requests.get(url, allow_redirects=True)
        if response is None or response.status_code != 200:
            flash("Произошла ошибка при проверке", category="danger")
            return redirect(url_for("url_page", id=id))
    except requests.exceptions.RequestException:
        flash("Произошла ошибка при проверке", category="danger")
        return redirect(url_for("url_page", id=id))
    status_code, header, title, description = parse_page(response)
    insert_data_into_url_checks(id, status_code, header, title, description)
    flash("Страница успешно проверена", category="success")
    return redirect(url_for("url_page", id=id))


def check_url_exists(url):
    sql = "select * from urls where name = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (url,))
            return cur.fetchone() is None


def insert_url_in_urls(url):
    sql = """insert into urls
            (name) values (%s)
            RETURNING id;"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (url,))
            url_id = cur.fetchone()[0]
            conn.commit()
            return url_id


def get_data_from_urls(id):
    sql = "select id, name, created_at::date from urls where id = %s;"
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(sql, (id,))
            return cur.fetchone()


def get_list_of_urls():
    sql = """select distinct on (urls.id)
                urls.id,
                urls.name,
                checks.created_at::date,
                checks.status_code
            from urls
            left join url_checks as checks on urls.id = checks.url_id
            order by urls.id, checks.created_at::date desc;
            """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()


def find_id_by_url(name):
    sql = "select id from urls where name = %s;"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name,))
            return cur.fetchone()[0]


def get_data_from_url_checks(id):
    sql = """
        select id, status_code, h1, title, description, created_at::date
        from url_checks
        where url_id = %s
        order by created_at desc;
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(sql, (id,))
            return cur.fetchall()


def insert_data_into_url_checks(id, status_code, h1, title, description):
    sql_urls = """
               insert into url_checks
               (url_id, status_code, h1, title, description)
               values (%s, %s, %s, %s, %s)
               """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_urls, (id, status_code, h1, title, description))
            conn.commit()
