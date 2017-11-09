from flask import Flask
import json, urllib2

app = Flask(__name__)

def callApi(apiKey):
	u = urllib2.open("key=%s"%(apiKey))

@app.route("/")
def root():
	return "fef"

if __name__ == "__main__":
	app.debug = True
	app.run()
