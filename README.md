simpleWeather
=============

A simple command-line weather app using Python 3.

#### Setup

Make a file called "private.json" and include the following data, replacing it with your information:

	{
		"api_key": "MY_API_KEY",
		"latitude": "MY_LATITUDE",
		"longitude": "MY_LONGITUDE"
	}

simpleWeather will use the latitude and longitude specified here if it
is unable to identify your location automatically.

You can register for an API key here: https://developer.forecast.io/register.

Once that's done you'll need to make sure you have the Python modules and
other utilities required. The list is as follows:

- Python modules
	1. PrettyTable (availble via pip or at https://pypi.python.org/pypi/PrettyTable)
	2. requests (also available via pip/pypi or at http://www.python-requests.org/en/latest/)
- gnuplot (available at http://www.gnuplot.info/)


#### Okay, so how do I use it?

Once you've got the simply run the script using whatever method you prefer.
By default it just displays the current basic weather conditions. Several
additional options are available; to see them run the script with the `-h`
or `--help` flag.