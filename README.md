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

#### I like it, but it's annoying having to go to a special directory just to check the weather.

If you'd like to be able to run the script from anywhere, put the following line in your `.bashrc`, `.bash_profile`, or whichever file is appropriate for the shell you use. Don't forget to make the appropriate substitutions for the terms in all caps. 

	alias NAME_YOU_WANT_TO_TYPE='PYTHON3_COMMAND PATH/TO/simpleWeather.py'

You may optionally include flags in the above alias to make them run by default, or you can simply add them as you want them. Restart your shell after saving the file and your alias should be active.

As an example, mine looks like this:

	alias weather='python3 ~/repositories/simpleWeather/simpleWeather.py -t'

I can type `weather` from anywhere on my system and I get the current conditions and hourly forecast. Had I left off the -t flag I could type `weather -t` to get the same result.
