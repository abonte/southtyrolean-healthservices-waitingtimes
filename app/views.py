from flask import render_template
from app import app
import requests
import demjson
from .forms import SearchForm
import json


@app.route('/', methods=('GET', 'POST'))
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = SearchForm()
    r = requests.get('http://daten.buergernetz.bz.it/services/WaitLists_Data/json')
    #with open('../WaitLists_Data.json') as data_file:    
     #   data = json.load(data_file)
    
    #v=data
    v = demjson.decode(r.text)
    services=set([])
    for i in v:
        services.add(i['activityDescriptionIt'])
        if i['waitingDays'] is not None:
            i['waitingDaysPer']= round(i['waitingDays']*100/365, 2)
        else:
            i['waitingDaysPer']= -1
            i['waitingDays'] = "Non disponibile"   

    # aggiungere gestione errore
    result=[]
    if form.validate_on_submit():
        for i in v:
            if form.name.data.lower() in i['activityDescriptionIt'].lower():
                result.append(i)         
    else:       
        result=v 
    return render_template("index.html",
                            title='Home',
                            posts=result,
                            services=services,
                            form = form)