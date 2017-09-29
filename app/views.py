from flask import render_template, request, abort, g, Blueprint
from app import app, babel
import requests
import demjson
from .forms import SearchForm
from config import SUPPORTED_LANGUAGES, BABEL_DEFAULT_LOCALE    
import json

bp = Blueprint('frontend', __name__, url_prefix='/<lang_code>')

@babel.localeselector
def get_locale():
    #return request.accept_languages.best_match(SUPPORTED_LANGUAGES.keys())
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
    r = requests.get('http://daten.buergernetz.bz.it/services/WaitLists_Data/json')
    if r.status_code != 200:
        return render_template("index.html",
                            title = 'Home',
                            resultServices = "",
                            services = "",
                            check = False,
                            form = form)
    
    #to use a local copy of the data
    #with open('../waitListsDataExample.json') as data_file:    
    #   data = json.load(data_file)

    data = demjson.decode(r.text)

    # aggiungere gestione errore
    
    resultServices=[]
    if form.validate_on_submit():
        # filter the services
        for i in data:
            if form.name.data.lower() in i['activityDescriptionIt'].lower():
                resultServices.append(i)         
    else: 
        # all the services      
        resultServices=data

    services=set([])
    for i in resultServices:
        services.add(i['activityDescriptionIt']) #list of services for the search form
        if i['waitingDays'] is not None:
            i['waitingDaysPer']= round(i['waitingDays']*100/365, 2) #value for the progress bar
        else:
            #if waitingDay is not available
            i['waitingDaysPer']= -1
            i['waitingDays'] = "Non disponibile"

    return render_template("index.html",
                            title='Home',
                            resultServices=resultServices,
                            services=services,
                            check = True,
                            locale = g.lang_code,
                            form = form)

''' @app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return render_template('500.html'), 500  '''