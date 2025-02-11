from flask import (
    Flask,
    render_template,
    flash,
    request,
    redirect
)
import psycorg2


from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycorg2.connect(DATABASE_URL)


def get_db_connection():
    return psycorg2.connect(DATABASE_URL)


@app.route("/")
def index():
    return render_template(
        'index.html',
        title='Анализатор страниц'
    )


if __name__ == '__main__':
    app.run()
