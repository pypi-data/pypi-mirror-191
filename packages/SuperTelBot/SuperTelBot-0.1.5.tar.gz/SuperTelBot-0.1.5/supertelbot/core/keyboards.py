from telebot.types import InlineKeyboardMarkup as _Ikm
from telebot.types import InlineKeyboardButton as _Ikb
from telebot.types import ReplyKeyboardMarkup as _Rkm


class NavBar:

    def __init__(self, buttons: list):
        self.buttons = buttons

    def get(self, **kwargs):
        tmp_buttons = []
        for arg, value in kwargs.items():
            for button in self.buttons:
                if arg == button.command and value is True:
                    tmp_buttons.append(button)
        return tmp_buttons


class Button:

    def __init__(self, label: str, command: str, func: callable, url: str = None):
        self.label = label
        self.command = command
        self.func = func
        self.url = url


class KeyBoard:

    def __init__(self, module, buttons: list, is_inline: bool = False, navbar: list = None):
        self.markup = _Ikm() if is_inline else _Rkm()
        self.module = module
        self.buttons = buttons
        self.is_inline = is_inline
        self.navbar = navbar

    def get(self, navbar: bool = True):
        markup = _Ikm() if self.is_inline else _Rkm()
        for row in self.buttons:
            items_row = list()
            for button in row:
                assert isinstance(button, Button), "Button doesn't inherits from superbot.bots.keyboards.Button"
                btn = _label = button.label.get('variable', button.label.get('label')) if isinstance(button.label, dict) else button.label
                (self.module.bot if hasattr(self.module.bot, 'register_callback') else self.module)\
                    .register_callback(self.module, button.func, _label if not self.is_inline else button.command)
                if self.is_inline:
                    btn = _Ikb(
                        _label,
                        callback_data=button.command,
                        url=button.url
                    )
                items_row.append(btn)
            if self.is_inline:
                markup.add(*items_row, row_width=len(row))
            else:
                markup.row(*items_row)
        if navbar and self.navbar:
            if self.is_inline:
                markup.add(*self.navbar, row_width=len(self.navbar))
            else:
                markup.row(*self.navbar)
        return markup
