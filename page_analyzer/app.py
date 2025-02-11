from flask import (
    Flask,
    render_template,
    url_for,
    flash,
    request,
    redirect
)
import psycorg2


from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
