from flask import Flask, render_template
import json, urllib2

app_id = 930378527100120


app = Flask(__name__)

def callApi(apiKey):
	u = urllib2.urlopen("https://api.nasa.gov/planetary/apod?api_key=%s"%(apiKey))
	data = json.loads(u.read())
	#data = u.read()
	return data
	
def getLoginLink(redirect_url):
	return """
https://www.facebook.com/
v2.11/dialog/oauth?client_id=%s&redirect_uri=%s&
response_type=token"""%(
	str(app_id), redirect_url)

@app.route("/nasa")
def nasa():
	data = callApi("kLf6LgwimzxpO917Kpurrjpcsp1DkgThHaeayMsW")
	#print data.keys()
	#return data
	
	return render_template("stars.html", date=data["date"], title=data["title"],
		image_url=data["url"], copyright=data["copyright"],
		explanation=data["explanation"])


@app.route("/")
def root():
	link = getLoginLink("https://localhost:5000")
	
	return render_template("fb.html", login_link=link)

if __name__ == "__main__":
	app.debug = True
	app.run()

