"""
A simple command-line weather app using Python 3 and following modules:

http://docs.python.org/3.3/library/optparse.html
http://docs.python.org/3.3/library/json.html
http://www.python-requests.org/en/latest/
https://pypi.python.org/pypi/PrettyTable

Major thanks to the creators of the following APIs:

https://developer.forecast.io/
http://freegeoip.net/
http://ip.42.pl

And also to the people over at gnuplot:
http://www.gnuplot.info/
"""

import json
import requests
import subprocess
import time
from optparse import OptionParser
from prettytable import PrettyTable


NUM_HOURLY_RECORDS = 16

speed = ["mph", "m/s"]
degrees = ["F", "C"]
length = ["in", "cm"]

parser = OptionParser()


with open("private.json") as f:
	private = json.loads(f.read())
	api_key = private["api_key"]
	loc = private["latitude"] + "," + private["longitude"]

	try:
		ip = requests.get("http://ip.42.pl/raw").text
		geo_url = "http://freegeoip.net/{0}/{1}".format("json", ip)
		location_info = requests.get(geo_url).json()
		longitude = str(location_info["longitude"])
		latitude = str(location_info["latitude"])
		loc = latitude + "," + longitude

	except Exception as e:
		print("Failed to detect location. Using default value from private.json")

parser.set_defaults(debug=False, graphics=False, location=loc, metric=False, today=False, week=False)
parser.add_option("-d", "--debug", action="store_true", help="show debug messages")
parser.add_option("-g", "--graphics", action="store_true", help="display visuals for weekly forecasts")
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

def plot_weekly():
	highs = []
	lows = []
	rain = []
	days = []
	for day in response["daily"]["data"]:
		highs.append(str(day["temperatureMax"]))
		lows.append(str(day["temperatureMin"]))
		rain.append(str(day["precipProbability"]))
		days.append(str(time.ctime(day["time"]).split()[2]))

	start_day = time.ctime(response["daily"]["data"][0]["time"]).split(" ")
	start_day_pretty = start_day[0] + ' ' + start_day[1] + ' ' + start_day[2]

	end_day = time.ctime(response["daily"]["data"][-1]["time"]).split(" ")
	end_day_pretty = end_day[0] + ' ' + end_day[1] + ' ' + end_day[2]

	period = start_day_pretty + " - " + end_day_pretty


	plot_data = []
	for day, low, high in zip(days, lows, highs):
		plot_data.append(day + "\t" + low + "\t" + high + "\n")

	gnuplot = subprocess.Popen(['gnuplot','-persist'], stdin=subprocess.PIPE).stdin
	gnuplot.write("set terminal dumb\n".encode())
	gnuplot.write("set title 'High and Low Temperatures, {0}'\n".format(period).encode())
	gnuplot.write("set nokey\n".encode())
	gnuplot.write("set xrange [{0}:{1}]\n".format(days[0], days[-1]).encode())
	gnuplot.write("set yrange [0:100]\n".encode())
	gnuplot.write("set ytics 0,5\n".encode())
	gnuplot.write("set tic scale 0\n".format(days[0], days[-1]).encode())

	gnuplot.write("plot '-' u 1:2 w l, '-' u 1:3 w l\n".encode())
	for line in plot_data: # iterate through once for the lows 
		gnuplot.write(line.encode())
	gnuplot.write("e\n".encode())
	for line in plot_data: # then again for the highs (per gnuplot docs)
		gnuplot.write(line.encode())
	gnuplot.write("e\n".encode())
	gnuplot.flush()


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
	print("Chance of precipitation: {0}%".format(chance_of_rain))
	print("Intensity: {0}".format(intensity))
	print()

def display_hourly_forecast():
	day_summary = response["hourly"]["summary"]

	print()
	print("Hourly forecast: {0}".format(day_summary))

	table = PrettyTable([
		"Time",
		"Summary",
		"Precipitation",
		"Intensity",
		"Temperature",
		"Wind",
		"Humidity"
	])

	for hour in response["hourly"]["data"][0:NUM_HOURLY_RECORDS]:
		dt = time.ctime(hour["time"]).split()
		short_dt = dt[0] + " " + dt[3][0:5]
		table.add_row([
			short_dt,
			hour["summary"],
			str(int(hour["precipProbability"]*100)) + "%",
			hour["precipIntensity"],
			str(hour["temperature"]) + " (" + degrees[options.metric] + ")",
			str(hour["windSpeed"]) + " " + speed[options.metric],
			str(int(hour["humidity"]*100)) + "%"
		])

	print(table)

def display_weekly_forecast():
	week_summary = response["daily"]["summary"]

	print()
	print("Forecast for the coming week: {0}".format(week_summary))

	table = PrettyTable([
		"Day",
		"Summary",
		"Precipitation",
		"Intensity",
		"High",
		"Low",
		"Wind",
		"Humidity"
	])

	for day in response["daily"]["data"]:
		dt = time.ctime(day["time"]).split()
		short_dt = dt[0] + " " + dt[1] + " " + dt[2]
		table.add_row([
			short_dt,
			day["summary"],
			str(int(day["precipProbability"]*100)) + "%",
			day["precipIntensity"],
			str(day["temperatureMax"]) + " (" + degrees[options.metric] + ")",
			str(day["temperatureMin"]) + " (" + degrees[options.metric] + ")",
			str(day["windSpeed"]) + " " + speed[options.metric],
			str(int(day["humidity"]*100)) + "%"
		])
	print(table)

if __name__ == "__main__":
	display_current_weather()
	if options.graphics:
		plot_weekly()
	if options.today:
		display_hourly_forecast()
	if options.week:
		display_weekly_forecast()
