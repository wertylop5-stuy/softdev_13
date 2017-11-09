from flask import Flask, render_template
import json, urllib2

app = Flask(__name__)

def callApi(apiKey):
	u = urllib2.urlopen("https://api.nasa.gov/planetary/apod?api_key=%s"%(apiKey))
	data = json.loads(u.read())
	#data = u.read()
	return data
	

@app.route("/")
def root():
	data = callApi("kLf6LgwimzxpO917Kpurrjpcsp1DkgThHaeayMsW")
	#print data.keys()
	#return data
	
	return render_template("stars.html", date=data["date"], title=data["title"],
		image_url=data["url"], copyright=data["copyright"],
		explanation=data["explanation"])
	

if __name__ == "__main__":
	app.debug = True
	app.run()

