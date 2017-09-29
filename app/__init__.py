from flask import Flask
from flask_babel import Babel


app = Flask(__name__)
app.config.from_object('config')
babel = Babel(app)

from app import views

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)