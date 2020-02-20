from flask import Flask, render_template, request, json
import os
import urllib.request
from datetime import datetime
from jinja2 import ext


app=Flask(__name__)

#ná í petrol a apis.is
with urllib.request.urlopen('https://apis.is/petrol') as url:
    data = json.loads(url.read().decode())

app.jinja_env.add_extension(ext.do)

def format_time(data):
    return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y. KL.%H:%M ')
app.jinja_env.filters['format_time'] = format_time

#def returntime():
 #   lst=data['results']
  #  timestampPriceCheck = ['timestampPriceCheck']
   # return [timestampPriceCheck]
    #Nope sorry nothing        
        #var returntime i data


def minPetrol():#LÆGSTA VERÐ yhman
    minPetrolPrice = 1000
    company = None
    address = None
    lst = data['results']
    for i in lst:#looop
        if i['bensin95'] is not None:     
            if i['bensin95'] < minPetrolPrice:
                minPetrolPrice = i['bensin95']
                company = i['company']
                address = i['name']
    return [minPetrolPrice, company, address]#LÆGSTA VERD

def minDiesel():#LÆGSTA VERÐ yhman
    minDieselPrice = 1000
    company = None
    address = None
    lst1 = data['results']
    for i in lst1:#looop
        if i['diesel'] is not None:     
            if i['diesel'] < minDieselPrice:
                minDieselPrice = i['diesel']
                company = i['company']
                address = i['name']
    return [minDieselPrice, company, address]#LÆGSTA VERD


@app.route('/')#Öll fyrirtæki einusinni
def home():
    return render_template('index.html', data=data, MinP=minPetrol(), MinD=minDiesel())

#Eitt fyrirtæki allar stodvar
@app.route('/company/<company>')
def comp(company):
    return render_template('company.html',data=data,com=company)

#bensínstod fyrirtækis
@app.route('/moreinfo/<key>')
def info(key):
    return render_template('moreinfo.html',data=data,key=key)


@app.errorhandler(404)
def YOUWERETHECHOSENONE(error):
    return render_template('NOOYOUWERETHECHOSENONE.html'),404

if __name__ == "__main__":
    app.run(debug=True)


