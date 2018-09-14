from flask import Flask
from flask_babel import Babel
import requests_cache


app = Flask(__name__)
app.config.from_object('config')
babel = Babel(app)

requests_cache.install_cache('opendata_cache', expire_after=7200)

from app import views

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)