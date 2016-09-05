import os
import redis
import datetime

from flask import Flask, render_template, request

app = Flask(__name__)
db = redis.from_url(os.environ['REDISCLOUD_URL'])


@app.route('/')
def index_form():
    return render_template("index.html")

@app.route('/setname', methods=['GET','POST'])
def setname():
	if request.method == 'GET':
		return redirect(url_for('my_form'))
	name = request.form['name'].lstrip()
	time = datetime.datetime.now()
	
	db.set('name', name)
	db.set('time', time)

	db_name = db.get('name')
	db_time = db.get('time')

	return render_template("setname.html", name=db_name, time=db_time)


if __name__ == '__main__':
	app.run()

