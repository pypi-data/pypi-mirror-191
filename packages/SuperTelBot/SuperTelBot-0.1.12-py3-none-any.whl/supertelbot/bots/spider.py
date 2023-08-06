from ..core.models import BotModel
from ..core.manager import Bot
from ..core.utils import thread_result
from ..modules.spider import Spider

import json


class SpiderBot(BotModel):

    def __init__(self, name: str, bot: Bot, api_key: str, **kwargs):
        super().__init__(name, bot, api_key, **kwargs)
        self.threads = dict()

        @bot.add_command(commands=["spider"], app_name=self.name)
        def spider(chat_id: int, command: str, message: str):
            """
            This function returns the weather from the place you indicate
            """
            url = message.split(" ")[0]
            depth = message.split(" ")[-1]
            if not url:
                bot.send_message(chat_id, "No url given")
                return
            try:
                depth = int(depth)
            except ValueError:
                depth = 1
            if not isinstance(depth, int) or depth < 1:
                depth = 1
            msg = "*Starting Spider*"
            msg += f"\n\t*URL*: {url}"
            msg += f"\n\t*Depth*: {depth}"
            bot.send_message(chat_id, msg, parse_mode="markdown")
            self.execute_background(url, chat_id, Spider(url, depth), "tree", __spider_results__)

        @thread_result(self)
        def __spider_results__(chat_id: int, result: object):
            bot.send_message(chat_id, json.dumps(result))
