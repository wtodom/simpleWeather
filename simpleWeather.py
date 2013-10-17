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
import time
from optparse import OptionParser
from prettytable import PrettyTable


NUM_HOURLY_RECORDS = 16

speed = ["mph", "kph"]
degrees = ["F", "C"]
length = ["in", "cm"]
parser = OptionParser()


with open("private.json") as f:
	private = json.loads(f.read())
	api_key = private["api_key"]
	loc = private["full_location"]


parser.set_defaults(location=loc, metric=False, debug=False)
parser.add_option("-d", "--debug", action="store_true", help="show debug messages")
parser.add_option("-l", "--location", help="specify a location other than the default")
parser.add_option("-m", "--metric", action="store_true", help="use metric rather than imperial units")
parser.add_option("-t", "--today", action="store_true", help="display today's hourly forecast")
parser.add_option("-w", "--week", action="store_true", help="display the weekly forecast")

(options, args) = parser.parse_args()

if options.debug:
	print()
	print("Options: " + str(options))
	print("Args: " + str(args))

url = "https://api.forecast.io/forecast/{0}/{1}".format(api_key, loc)

if options.metric:
	url += "?units=si"

response = requests.get(url).json()

def display_current_weather():
	summary = response["currently"]["summary"]
	current_temp = response["currently"]["temperature"]
	current_wind = response["currently"]["windSpeed"]
	chance_of_rain = response["currently"]["precipProbability"]
	intensity = response["currently"]["precipIntensity"]

	print()
	print("Current conditions: {0}".format(summary))
	print("Current temperature: {0} degrees (".format(current_temp) + degrees[options.metric] + ")")
	print("Winds: {0} ".format(current_wind) + speed[options.metric])
	print("Chance of rain: {0}%".format(chance_of_rain))
	print("Intensity: {0}".format(intensity))
	print()

def display_hourly_forecast():
	current_time = time.time()
	day_summary = response["hourly"]["summary"]

	print()
	print("Hourly forecast: {0}".format(day_summary))

	table = PrettyTable(["Time", "Summary", "Rain", "Intensity", "Temperature", "Feels Like", "Wind", "Humidity"])

	for hour in response["hourly"]["data"][0:NUM_HOURLY_RECORDS]:
		dt = time.ctime(hour["time"]).split()
		short_dt = dt[0] + " " + dt[3][0:5]
		table.add_row([short_dt, hour["summary"], str(int(hour["precipProbability"]*100)) + "%", hour["precipIntensity"], hour["temperature"], hour["apparentTemperature"], hour["windSpeed"], hour["humidity"]])

	print(table)

display_current_weather()
if options.today:
	display_hourly_forecast()