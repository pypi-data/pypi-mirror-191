from ..core.workers import worker
from ..core.utils import AppData
from ..core.keyboards import KeyBoard, Button
from ..core.exceptions import KeyBoardLayoutException
from .manager import Bot
import json
import os


class BotModel:
    """
        For registering a new function as a handler when something is said
        in the Telegram Bot conversation, you could use something like this:

            self.bot.register_handler(self, self.YOUR_FUNCTION, commands=["COMMAND_GOES_HERE"])

        Then you have to create a class method with that function name:

            def YOUR_FUNCTION(self, chat_id: int, command: str, message: str):
                # Here goes your code

        You can use keyboards that you previously added into passwords.json file

        This config file should looks something like this:

            # YOUR_MODEL_IN_BOTS_FOLDER.json
            {
                "buttons": {
                    "COMMAND_GOES_HERE": "LABEL TEXT",
                    ...
                },
                "keyboards": [...]
            }

        Buttons also could be defined like a link this way:

            # YOUR_MODEL_IN_BOTS_FOLDER.json
            {
                "buttons": {
                    "COMMAND_GOES_HERE": {
                        "label": "LABEL TEXT",
                        "url": "https://example.com"
                    },
                    ...
                },
                "keyboards": [...]
            }

        Keyboard definition example:

            # YOUR_MODEL_IN_BOTS_FOLDER.json
            {
                "buttons": {...},
                "keyboards": {
                    "KEYBOARD_NAME": {
                        "inline": false (true/false),
                        "buttons": [
                            ["COMMAND_GOES_HERE", "COMMAND_GOES_HERE"],
                            ["COMMAND_GOES_HERE"],
                        ]
                    }
                }
            }

        Then, for using all of this, you have to load keyboards with this method:

            # YOUR_MODEL_IN_BOTS_FOLDER.py -> __init__
            self.load_keyboards(self, __file__)

        Finally, integrate it in your code like this:

            # YOUR_MODEL_IN_BOTS_FOLDER.py -> Any function
            def YOUR_FUNCTION(self, chat_id: int, command: str, message: str):
                keyboard = self.keyboards.get('KEYBOARD_NAME', [])
                self.bot.send_message(chat_id, "YOUR MESSAGE", reply_markup=keyboard.markup)

    """

    name = None

    def __init__(self, name: str, bot: Bot, api_key: str = None, **kwargs):
        assert bot is not None, "TeleBot instance needed with Bot Manager"
        self.name = name
        self.api = api_key
        self.bot = bot
        self.keyboards = dict()
        self.keyboards_buttons = dict()
        self.vault = AppData(name=self.name)
        self.threads = dict()
        self.config = dict()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __load_config__(self, executor_filter):
        config_file_name = f"{executor_filter.split('.')[0]}.json"
        if os.path.isfile(config_file_name):
            with open(config_file_name, 'r') as f:
                self.config = json.loads(f.read())

    def create_keyboard(self, buttons: list = None, name: str = None, is_inline: bool = False):
        if not buttons:
            buttons = list()
        buttons += self.keyboards_buttons.get(name, [])
        buttons += [
            self.bot.father_bot.NAVBAR.get(Home=True, Help=True, Clean=True)
        ]
        return KeyBoard(self, buttons, is_inline=self.config.get('keyboards', {})
                        .get(name, {})
                        .get('inline', is_inline)
                        ).get()

    def load_keyboards(self, module, executor_file: str):
        self.__load_config__(executor_file)
        assert issubclass(module.__class__, BotModel), "Loading keyboards only work inside BotModel inherited modules"
        assert self.config, "[CONFIG] Config file not loaded"
        assert self.config.get('keyboards'), "[CONFIG] 'keyboards' does not exist inside config file"
        assert self.config.get('buttons'), "[CONFIG] 'buttons' does not exist inside config file"
        _keyboards = self.config.get('keyboards')
        _buttons = self.config.get('buttons')
        assert isinstance(_keyboards, dict), \
            "[CONFIG] 'keyboards' config have to be a dict"
        assert isinstance(_buttons, dict), \
            "[CONFIG] 'buttons' config have to be a dict with your button commands as keys and labels as values"
        for _command, _command_buttons in _keyboards.items():
            assert 'inline' in _command_buttons, \
                f"[CONFIG] Missing 'inline' (bool field) inside 'keyboards[\"{_command}\"]' config"
            assert 'buttons' in _command_buttons, \
                f"[CONFIG] Missing 'buttons' (list field) inside 'keyboards[\"{_command}\"]' config"
            _command_keyboard = list()
            for _row in _command_buttons.get('buttons', []):
                _buttons_row = list()
                for _btn_row in _row:
                    if isinstance(_btn_row, str):
                        _label = _buttons.get(_btn_row, _btn_row)
                        _url = None
                        if isinstance(_label, dict) and 'label' in _label:
                            _url = _label.get('url', None)
                            _label = _label.get('variable', _label.get('label'))
                        _buttons_row.append(Button(_label, _btn_row, _command, _url))
                        assert hasattr(module, _btn_row), f"[CONFIG] Module '{module.name}' has no function '{_btn_row}'"
                        self.bot.register_callback(module, getattr(module, _btn_row), _label)
                    else:
                        raise KeyBoardLayoutException(
                            f"{_btn_row} has invalid format (should be function name as string)"
                        )
                _command_keyboard.append(_buttons_row)
            self.keyboards[_command] = KeyBoard(self, _command_keyboard, is_inline=_command_buttons.get('inline', False)).get()
            self.keyboards_buttons[_command] = _command_keyboard

    # Para Spider Bot
    def execute_background(self, name: str, chat_id: int,
                           class_obj: object, class_method: str,
                           callback: object = None):
        thread_id = f"{self.name} - {name}"
        self.threads[thread_id] = chat_id
        worker(thread_id, class_obj, class_method, args=(thread_id,), callback=callback,
               loop=False, run_until_end=True, log=True)
