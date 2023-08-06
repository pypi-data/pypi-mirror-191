from ..modules.weather import Weather, WeatherResult
from ..core.models import BotModel
from ..core.manager import Bot


class WeatherBot(BotModel):

    def __init__(self, name: str, bot: Bot, api_key: str, **kwargs):
        super().__init__(name, bot, api_key, **kwargs)

        @bot.add_command(commands=["weather"], app_name=self.name)
        def weather(chat_id: int, command: str, message: str):
            """
            This function returns the weather from the place you indicate
            """
            if not message:
                bot.send_message(chat_id, "No city given")
                return
            weather_module = Weather(api_key)
            result: WeatherResult = weather_module.get(message)
            if result.errors:
                bot.send_message(chat_id, f"Unable to find this city: {message}")
                return
            msg = f"*Weather in*: {result.city}"
            msg += f"\n*Country*: {result.country}"
            msg += f"\n*Time*: {result.time_stamp}"
            msg += f"\n*Temp*: {result.temperature} ºC"
            msg += f"\n*Humidity*: {result.humidity} %"
            bot.send_message(chat_id, msg, parse_mode="markdown")
