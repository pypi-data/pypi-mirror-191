from ..modules.nmap_scanner import Scanner
from ..core.models import BotModel
from ..core.manager import Bot


class NmapBot(BotModel):

    def __init__(self, name: str, bot: Bot, api_key: str = None,
                 user_agent: str = "Mozilla Firefox", **kwargs):
        super().__init__(name, bot, api_key, **kwargs)
        self.user_agent = user_agent

        @bot.add_command(commands=["ports"], app_name=self.name)
        def ports(chat_id: int, command: str, message: str):
            """
            This functions scan ports from a given address
            """
            content = message.split(" ")
            target = content[0]
            if not target:
                self.bot.send_message(chat_id, "You need to set your target")
                return
            port_range = content[-1]
            if target == port_range:
                port_range = "0-1024"
            self.bot.send_message(chat_id,
                                  f"*Starting scan against-->* {target} {port_range}",
                                  parse_mode="markdown")
            scanner = Scanner(target, port_range)
            result = scanner.scan()
            result_json, result_text = scanner.parse_result(result, port_range)
            self.bot.send_message(chat_id, result_text, parse_mode="markdown")
            self.bot.api.save_scan(result_json)
