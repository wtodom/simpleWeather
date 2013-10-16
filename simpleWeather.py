import json
import requests
from optparse import OptionParser
# http://docs.python.org/3.3/library/optparse.html
# http://www.python-requests.org/en/latest/
# https://developer.forecast.io/

with open("data.json") as f:
	private = json.loads(f.read())
	api_key = private["api_key"]
	location = private["full_location"]

url = "https://api.forecast.io/forecast/{0}/{1}".format(api_key, location)

parser = OptionParser()
parser.set_defaults(location=location)
parser.add_option("-l", "--location")

(options, args) = parser.parse_args()

response = requests.get(url).json()

current_temp = response["currently"]["temperature"]
current_wind = response["currently"]["windSpeed"]
chance_of_rain = response["currently"]["precipProbability"]
precip_intensity = response["currently"]["precipIntensity"]

print()
print("Current temperature: {0} degrees F".format(current_temp))
print("Winds: {0}mph".format(current_wind))
print("Chance of rain: {0}%".format(chance_of_rain))
print("Intensity: {0}".format(precip_intensity))
print()