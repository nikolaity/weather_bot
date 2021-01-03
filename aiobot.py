
import config
import logging
import sys

from aiogram import Bot, Dispatcher, executor, types
from pyowm import OWM
from pyowm.utils.config import get_default_config



config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('87213374dd7637798e63c138633d2da0', config_dict)


logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# Команда start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	await bot.send_message(message.from_user.id, "Хочешь узнать погоду? \n Напиши мне свой город")

	# Команда help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
	await bot.send_message(message.from_user.id, "Здесь ты можешь узнать погодую\n Напиши свой город")

# Эхо
@dp.message_handler(content_types=['text'])
async def echo(message):
	try:
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place( message.text )
		w = observation.weather
		temp = w.temperature('celsius')["temp"]

		answer = "В городе " + message.text + " сейчас: " + w.detailed_status + "\n"
		answer += "Температура сейчас в районе: " + str(temp) + "\n\n"

		if temp < 10:
			answer += "Сейчас холодно одевевай подштаники!" 

		elif temp < 20:
			answer += "Сейчас холодно одевайся теплее!" 

		else:
			answer += "Температура нормальная одевевай что хочешь!"

		await bot.send_message(message.from_user.id, answer)

	except:
		await bot.send_message(message.from_user.id, "Не верно указаный город!")

# запускаем лонг поллинг
if __name__ == '__main__':
	 executor.start_polling(dp, skip_updates=True)