from flask import render_template
from app import app
import requests
import demjson
from .forms import SearchForm
import json


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
def index():
    form = SearchForm()
    r = requests.get('http://daten.buergernetz.bz.it/services/WaitLists_Data/jsorereern')
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
                            form = form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404