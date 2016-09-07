import os
import redis
import datetime
import pyowm

from flask import Flask, render_template, request

app = Flask(__name__)
#Redis
db = redis.from_url(os.environ['REDISCLOUD_URL'])
#Openweathermap API key
owm = pyowm.OWM(os.environ['OWM_KEY']) 

@app.route('/')
def index_form():
    return render_template("index.html")

@app.route('/setname', methods=['GET','POST'])
def setname():
	if request.method == 'GET':
		return redirect(url_for('index_form'))

	name = request.form['name'].lstrip()

	forecast = owm.daily_forecast(name)
	tomorrow = pyowm.timeutils.tomorrow()
	ans = ''

	if forecast.will_be_sunny_at(tomorrow) == True:
		ans = 'Yes!'
	else:
		ans = 'No'

	#Get temperatures
	w = owm.weather_at_place(name).get_weather()
	temp = w.get_temperature(unit='celsius')['temp']

	#Set values in DB
	db.set('name', name)
	db.set('sunny', ans)
	db.set('temp', temp)

	#Get values
	db_name = db.get('name')
	db_sunny = db.get('sunny')
	db_temp = db.get('temp')

	return render_template("setname.html", name=db_name, sunny=db_sunny, temp=db_temp)


if __name__ == '__main__':
	app.run()
