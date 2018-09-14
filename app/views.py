from flask import render_template, request, abort, g, Blueprint
from app import app, babel
import requests
from .forms import SearchForm
import datetime
from config import SUPPORTED_LANGUAGES, BABEL_DEFAULT_LOCALE
import json
import time

bp = Blueprint('frontend', __name__, url_prefix='/<lang_code>')


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(SUPPORTED_LANGUAGES.keys())
    return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])


@app.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or not g.lang_code:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code


@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code', None)


@app.before_request
def ensure_lang_support():
    lang_code = g.get('lang_code', None)
    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
        return abort(404)


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
@app.route('/<lang_code>', methods=('GET', 'POST'))
@app.route('/<lang_code>/index', methods=('GET', 'POST'))
def index():
    form = SearchForm()
    now = time.ctime(int(time.time()))
    r = requests.get('http://daten.buergernetz.bz.it/services/WaitLists_Data/json')
    print("Time: {0} / Used Cache: {1}".format(now, r.from_cache))
    if r.status_code != requests.codes.ok:
        return render_template("index.html",
                               title='Home',
                               resultServices="",
                               services="",
                               check=False,
                               form=form)

    # to use a local copy of the data
    # with open('../waitListsDataExample.json') as data_file:
    #   data = json.load(data_file)

    data = r.json()
    # aggiungere gestione errore

    resultServices = []
    services = set([])
    for i in data:
            services = _addToListServices(services, i)
            if form.validate_on_submit() and _isServiceDescription(form.name.data, i):
                resultServices.append(i)

    resultServices = data if not form.validate_on_submit() else resultServices

    max_ = _findMaxWaiting(resultServices)

    for i in resultServices:
        i['waitingDaysPer'] = _valueProgressBar(i, max_)
        i['waitingDays'] = i['waitingDays'] if i['waitingDaysPer'] != -1 else 0
        i['SurveyDate'] = datetime.datetime.strptime(i['SurveyDate'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%y')

    return render_template("index.html",
                           title='Home',
                           resultServices=resultServices,
                           services=services,
                           check=True,
                           locale=g.lang_code,
                           form=form)


def _addToListServices(services, i):
    if g.lang_code == 'de':
        services.add(i['activityDescriptionDe'])  # list of services for the search form
    else:
        services.add(i['activityDescriptionIt'])
    return services


def _isServiceDescription(text, service):
    return text.lower() in service['activityDescriptionIt'].lower() or text.lower() in service['activityDescriptionDe'].lower()


def _valueProgressBar(elem, max_):
    if elem['waitingDays'] is not None:
        value = round(elem['waitingDays'] * 100 / max_, 2)  # value for the progress bar
        return value if value > 10 else -1
    else:
        return -1


def _findMaxWaiting(data):
    return max([i['waitingDays'] for i in data], key=lambda i: i if i is not None else 0)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500


@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return render_template('500.html'), 500
