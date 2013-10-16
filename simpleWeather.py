"""
A simple command-line weather app using the following Python modules:

http://docs.python.org/3.3/library/optparse.html
http://docs.python.org/3.3/library/json.html
http://www.python-requests.org/en/latest/


Made possible by the forecast.io API:

https://developer.forecast.io/
"""

import json
import requests
from optparse import OptionParser


parser = OptionParser()


with open("private.json") as f:
	private = json.loads(f.read())
	api_key = private["api_key"]
	loc = private["full_location"]


parser.set_defaults(location=loc)
parser.add_option("-l", "--location")

(options, args) = parser.parse_args()


url = "https://api.forecast.io/forecast/{0}/{1}".format(api_key, loc)

response = requests.get(url).json()

summary = response["currently"]["summary"]
current_temp = response["currently"]["temperature"]
current_wind = response["currently"]["windSpeed"]
chance_of_rain = response["currently"]["precipProbability"]
precip_intensity = response["currently"]["precipIntensity"]

print()
print("Current conditions: {0}".format(summary))
print("Current temperature: {0} degrees F".format(current_temp))
print("Winds: {0}mph".format(current_wind))
print("Chance of rain: {0}%".format(chance_of_rain))
print("Intensity: {0}".format(precip_intensity))
print()
