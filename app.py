from flask import Flask, render_template, request, session, redirect, url_for
import json, urllib2, os

app_id = "930378527100120"
app_secret = "a29be126bfe8062cb7a9ade82f790526"


app = Flask(__name__)
app.secret_key = os.urandom(128)


def callApi(apiKey):
	'''
	For the nasa portion of the assignment
	'''
	u = urllib2.urlopen("https://api.nasa.gov/planetary/apod?api_key=%s"%(apiKey))
	data = json.loads(u.read())
	#data = u.read()
	return data

#&response_type=token
def getLoginLink(redirect_url):
	return """
https://www.facebook.com/
v2.11/dialog/oauth?client_id=%s&redirect_uri=%s"""%(
	app_id, redirect_url)

def codeToToken(redirect_url, code):
	'''
	Converts a code received after user logs in to an access token.
	
	We can't grab the access token directly as the facebook graph api
	stores it in a url fragment, so flask won't be able to access it.
	'''
	
	url = """
https://graph.facebook.com/v2.11/oauth/access_token?
client_id=%s
&redirect_uri=%s
&client_secret=%s
&code=%s
"""%(app_id, redirect_url, app_secret, code)
	
	#urllib2 can't handle \n apparently
	url = str.join("", url.split("\n"))
	
	u = urllib2.urlopen(url)
	
	return json.loads(u.read())

def getProfilePic():
	u = urllib2.urlopen("https://graph.facebook.com/me?access_token=%s&fields=profile_pic"%(session["access_token"]) )
	
	return json.dumps(u.read())

@app.route("/nasa")
def nasa():
	data = callApi("kLf6LgwimzxpO917Kpurrjpcsp1DkgThHaeayMsW")
	
	return render_template("stars.html", date=data["date"], title=data["title"],
		image_url=data["url"], copyright=data["copyright"],
		explanation=data["explanation"])


@app.route("/")
def root():
	if "access_token" in session:
		return redirect(url_for("profile"))

	if "code" in request.args:
		token = codeToToken("http://localhost:5000/", request.args["code"])
		
		print token
		session["access_token"] = token["access_token"]
		
		return redirect(url_for("profile"))
	else:
		link = getLoginLink("http://localhost:5000/")
		return render_template("fb.html", login_link=link)

@app.route("/profile")
def profile():
	if not "access_token" in session:
		return redirect(url_for("root"))
	profile_pic = getProfilePic()
	return render_template("profile.html", pic=profile_pic)

if __name__ == "__main__":
	app.debug = True
	app.run()

