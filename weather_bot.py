from telegram.ext import Updater, CommandHandler
import logging
import requests
import json

# Enble logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)


# Gets the current weather data in Tampere from OpenWeatherMap API
# and returns the weather report as a sring
def all_wether_data():
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"q": "Tampere,fi", "lat": "0", "lon": "0", "callback": "weather","id": "2172797",
                   "lang": "null","units": "\"metric\" or \"imperial\"", "mode": "xml, html"}

    headers = {
        'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # personal key
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).text

    text = response[8:-1]
    return text

# Takes the wanted information from the weather report and
# returns it in str
def weather_to_bot():
    text = all_wether_data()
    dict = json.loads(text)

    weather = dict["weather"][0]["description"]
    temp = int(dict["main"]["temp"] - 273.15)
    feels = int(dict["main"]["feels_like"] - 273.15)
    press = dict["main"]["pressure"]
    humid = dict["main"]["humidity"]
    visib = int(dict["visibility"] / 1000)
    wind = dict["wind"]["speed"]
    clouds = dict["clouds"]["all"]

    weather_info = ("Weather in Tampere: " + str(weather) + ", temperature: " + str(temp) +"C feels like: "+ str(feels) +
                     "C, pressure: " + str(press) +", humidity: " + str(humid) + "%" +", wisibility: "+
                     str(visib) + "km, wind: " + str(wind) + "m/s, clouds: " + str(clouds) + "%.")

    return weather_info


def start(update, context):
    # Send start message when command /start is issued.
    update.message.reply_text("Hi! Use /weather command to see current "
                              "weather in Tampere.")

def weather(update, context):
    # Send weather report when command /weather is issued.
    weathertext = weather_to_bot()
    update.message.reply_text(weathertext)

def error(update, context):
    # Log Errors caused by Updates.
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Creates Updater and pass bot's token to it
    updater = Updater("TOKEN")

    # Get the dispatcer to register handlers
    dp = updater.dispatcher

    # Different Telegram commands
    dp.add_handler(CommandHandler('weather', weather))
    dp.add_handler(CommandHandler('start', start))

    # Log all errors
    dp.add_error_handler(error)

    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
