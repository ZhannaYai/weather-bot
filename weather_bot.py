import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
OPENWEATHERMAP_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to the Weather Bot!')


def get_weather(update, context):
    location = context.args

    if location:
        try:
            weather = retrieve_weather(location)
            context.bot.send_message(chat_id=update.effective_chat.id, text=weather)
        except Exception as e:
            print(str(e))
            context.bot.send_message(chat_id=update.effective_chat.id, text='Failed to retrieve weather information.')


def retrieve_weather(location):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}'

    response = requests.get(url)
    json_data = response.json()

    if response.status_code == 200:
        city_name = json_data['name']
        temperature = json_data['main']['temp']
        weather_description = json_data['weather'][0]['description']

        weather_info = f'Weather in {city_name}:\nTemperature: {temperature}°C\nDescription: {weather_description}'
        return weather_info
    else:
        error_message = json_data['message']
        raise Exception(f'Failed to retrieve weather information. Error: {error_message}')


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    get_weather_handler = CommandHandler('getweather', get_weather)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(get_weather_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
