from urllib.parse import urlparse

from app import check_url_exists, find_id_by_url, insert_url_in_urls
from flask import flash, redirect, render_template, request, url_for
from validators import url as validate_url


INDEX_TEMPLATE = 'index.html'


def urls_post():
    actual_url = request.form.get("url", "").strip()
    if len(actual_url) > 255:
        flash("URL слишком длинный (максимум 255 символов)", "danger")
        return render_template(INDEX_TEMPLATE), 422
    if not validate_url(actual_url):
        flash("Некорректный URL", "danger")
        return render_template(INDEX_TEMPLATE), 422
    try:
        parsed = urlparse(actual_url)
        if not parsed.scheme:
            actual_url = f"https://{actual_url}"
            parsed = urlparse(actual_url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}"
    except Exception as e:
        flash(f"Ошибка обработки URL: {str(e)}", "danger")
        return render_template(INDEX_TEMPLATE), 422

    if check_url_exists(normalized_url):
        flash("Страница уже существует", "info")
        url_id = find_id_by_url(normalized_url)
    else:
        url_id = insert_url_in_urls(normalized_url)
        flash("Страница успешно добавлена", "success")
    return redirect(url_for("url_page", id=url_id))
