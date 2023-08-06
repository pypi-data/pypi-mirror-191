import inspect
from inspect import currentframe, getmembers
from datetime import datetime
from telebot import TeleBot
from telebot.types import ForceReply
import json
import os

from .utils import History, get_sender
from .api import ApiManager

from .keyboards import Button, KeyBoard, NavBar


class Bot:

    def __init__(self, api_key: str, history_file: str = "history.json", home_button_function: callable = None):
        assert history_file.endswith('.json'), "History file have to be a json extension file"
        self.name = 'Script'
        self.main_path = os.path.split(inspect.stack()[1][1])[0]
        self.bot = TeleBot(api_key)
        self.conf = {
            "telegram_api": "http://192.168.1.190:8519",
            "user_agent": "Connor Lil Homer was here"
        }
        assert self.conf.get("telegram_api"), "'telegram_api' key missing in config.json file"
        self.api = ApiManager(self.conf.get("telegram_api"))
        self.bot_whitelist = self.api.get_allowed_users()
        self.functions_doc = dict()
        self.modules = dict()
        self.modules_obj = dict()
        self.modules_callbacks = dict()
        self.history: History = History(history_file)
        self.reply_callbacks = dict()
        self.father_bot = self.add_module("Father Bot", FatherBot, home_button_function=home_button_function)

    def __notify_admins__(self, function_name: str, chat_id: int):
        for admin in self.bot_whitelist:
            self.bot.send_message(
                admin,
                f"A user with ID {chat_id} tried to talk the bot to {function_name}\
                function without permissions"
            )

    def __multi_handler__(self, message):
        chat_id, msg_command, msg_text = self.__prepare_args_from_received_msg__(message)
        if message.reply_to_message:
            for callback, callback_content in self.reply_callbacks.items():
                if message.reply_to_message.id == callback:
                    reply_callback, reply_append_command = self.reply_callbacks.pop(message.reply_to_message.id)
                    self.history.save_message(self.name, chat_id, message.message_id)
                    reply_callback(chat_id,
                                   reply_append_command or msg_command,
                                   msg_command if reply_append_command else msg_text)
                    return
        self.bot.delete_message(chat_id, message.message_id)
        for module_name, commands in self.modules_obj.items():
            if msg_command in commands:
                self.history.save_message(module_name, chat_id, message.message_id)
                print(f"[START] - [{module_name}] - [{msg_command}] - {datetime.now()}")
                if commands[msg_command][1] and not self.__auth_check__(message, module_name):
                    return
                commands[msg_command][0](chat_id, msg_command, msg_text)
                print(f"[ END ] - [{module_name}] - [{msg_command}] - {datetime.now()}")
                return
        for module_name, commands in self.modules_callbacks.items():
            msg = message.text.removeprefix('/').strip()
            comm = msg.split(' ')[0]
            if command_func := commands.get(msg, commands.get(comm, None)):
                self.history.save_message(module_name, chat_id, message.message_id)
                print(f"[START] - [{module_name}] - [{msg_command}] - {datetime.now()}")
                command_func(chat_id, message.text, message.text)
                print(f"[ END ] - [{module_name}] - [{msg_command}] - {datetime.now()}")
                return

        self.history.save_message(self.name, chat_id, message.message_id)
        if msg_command:
            sent_id = self.bot.send_message(chat_id, f"Command '{msg_command}' not implemented").message_id
        else:
            sent_id = self.bot.send_message(chat_id, "I'm not prepared for that").message_id
        self.history.save_message(self.name, chat_id, sent_id)

    def __multi_callback_handler__(self, call):
        for module_name, command in self.modules_callbacks.items():
            if call.data in command:
                print(f"[START] - [{module_name}] - [{call.data}] - {datetime.now()}")
                command[call.data](call.from_user.id, call.data, call.data)
                print(f"[ END ] - [{module_name}] - [{call.data}] - {datetime.now()}")
                return

    @staticmethod
    def __extract_command__(request):
        return request.text.strip().split(' ')[0].removeprefix('/') if request.text else str()

    @staticmethod
    def __extract_message__(request):
        if tmp := request.text.strip().split(' ') if request.text else None:
            tmp.pop(0)
            return ' '.join(tmp)
        return ''

    def __auth_check__(self, request, app_name: str):
        chat_id = request.chat.id if hasattr(request, 'chat') else request.from_user.id
        res = self.api.show_auth(chat_id, app_name,
                                 '-'.join([app_name, self.__extract_command__(request)]))
        if res.get('code') == 200:
            return True
        self.__notify_admins__(self.__extract_command__(request), request.chat.id)
        return False

    def __has_permissions__(self, request, app_name: str = None,
                            require_permission: bool = False, server_whitelisted: bool = False):
        if require_permission and request.chat.id not in self.bot_whitelist:
            self.__notify_admins__(self.__extract_command__(request), request.chat.id)
            return False
        if server_whitelisted:
            if not self.__auth_check__(request, app_name):
                return False
        return True

    def __get_mod_name_command__(self, request, f, app_name: str = None):
        for module, module_commands in self.modules_obj.items():
            for func_command, func_obj in module_commands.items():
                if func_obj[0] == f:
                    if func_obj[1]:
                        if not self.__auth_check__(request, app_name):
                            return None, None
                    return module, func_command
        return None, None

    def __prepare_args_from_received_msg__(self, request):
        chat_id = request.chat.id if hasattr(request, 'chat') else request.from_user.id
        msg_command = self.__extract_command__(request)
        message = self.__extract_message__(request)
        return chat_id, msg_command, message

    def __register_command__(self, wrapper, f, commands: list, app_name: str = None,
                             server_whitelisted: bool = False, ignore_listing: bool = False,
                             content_types=None, regexp=None, func=None, chat_types=None, callback: str = None):
        if not hasattr(f, '__name__'):
            return
        for command in commands:
            self.functions_doc[command] = f.__doc__ if not ignore_listing else None, app_name
            if not app_name:
                f_class_reference = [m[1] for m in getmembers(f) if m[0] == '__qualname__'][0]
                f_class = f_class_reference.split('.')[0]
            else:
                f_class = app_name
            if not callback and f_class not in self.modules_obj:
                self.modules_obj[f_class] = dict()
            elif callback and (app_name not in self.modules_callbacks):
                self.modules_callbacks[app_name] = dict()
            if not callback:
                self.modules_obj[f_class][command] = (f, server_whitelisted, )
            else:
                self.modules_callbacks[app_name][callback] = f
        if callback:
            return
        self.bot.register_message_handler(wrapper, commands=commands,
                                          content_types=content_types, regexp=regexp,
                                          func=func, chat_types=chat_types)

    def __execute_function__(self, request, f, mod_name: str, mod_command: str):
        print(f"[START] - [{mod_name}] - [{mod_command}] - {datetime.now()}")
        chat_id, msg_command, message = self.__prepare_args_from_received_msg__(request)
        f(chat_id, msg_command, message)
        print(f"[ END ] - [{mod_name}] - [{mod_command}] - {datetime.now()}")

    def __register_reply_callback__(self, chat_id: int, reply_callback: callable = None,
                                    reply_append_command: str = None):
        if not reply_callback:
            return
        self.reply_callbacks[chat_id] = (reply_callback, reply_append_command)

    def start(self):
        self.bot.register_callback_query_handler(self.__multi_callback_handler__, func=lambda message: True)
        self.bot.register_message_handler(self.__multi_handler__, func=lambda message: True)
        print("[BOT] - Functions Loaded:")
        for function_name in self.functions_doc:
            print(f"\t[COMMAND] - /{function_name}")
        print("[BOT] - Started successfully")
        self.bot.infinity_polling()

    def create_module(self, name: str):
        from .models import BotModel
        self.add_module(name, BotModel)

    def add_module(self, name: str, module, api_key: str = None, **kwargs):
        from .models import BotModel
        assert issubclass(module, BotModel) or module == BotModel, "Module have to inherit core.models.BotModel"
        self.modules[name] = module(name, self, api_key, **kwargs)
        return self.modules.get(name)

    def send_message(self, chat_id: int, message: str, parse_mode: str = None,
                     reply_markup: object = None, reply_callback: callable = None,
                     reply_append_command: str = None):
        sender = get_sender(currentframe(), self.modules, self.modules_obj)
        if reply_callback:
            reply_markup = ForceReply(selective=False)
        sent_msg = self.bot.send_message(chat_id, message, parse_mode=parse_mode, reply_markup=reply_markup)
        self.__register_reply_callback__(sent_msg.message_id, reply_callback, reply_append_command)
        self.history.save_message(sender, chat_id, sent_msg.message_id)

    def send_photo(self, chat_id: int, photo: str, reply_markup: object = None):
        sender = get_sender(currentframe(), self.modules, self.modules_obj)
        sent_msg = self.bot.send_photo(chat_id, photo, reply_markup=reply_markup)
        self.history.save_message(sender, chat_id, sent_msg.message_id)

    def register_handler(self, module, func: object, commands: list,
                         whitelisted: bool = False, is_callback: bool = False,
                         content_types=None, regexp=None, chat_types=None):
        from .models import BotModel
        assert issubclass(module.__class__, BotModel), \
            "Only models that inherit from core.models.BotModel can register handlers"
        if not is_callback and module.name not in self.modules_obj:
            self.modules_obj[module.name] = dict()
        elif is_callback and module.name not in self.modules_callbacks:
            self.modules_callbacks[module.name] = dict()
        for command in commands:
            if not is_callback:
                self.modules_obj[module.name][command] = (func, whitelisted)
            else:
                self.modules_callbacks[module.name][command] = func
            self.functions_doc[command] = func.__doc__, module.name
        self.bot.register_message_handler(func, commands=commands,
                                          content_types=content_types, regexp=regexp,
                                          func=func, chat_types=chat_types)

    def register_callback(self, model: callable, f: callable, callback: str):
        self.__register_command__(None, f, commands=[callback],
                                  app_name=model.name, callback=callback)

    def add_command(self, commands: list, app_name: str = None, require_permission: bool = False,
                    server_whitelisted: bool = False, ignore_listing: bool = False,
                    content_types=None, regexp=None, func=None, chat_types=None):
        def wrapp_function(f):
            def wrapper(request):
                self.history.save_message(self.name, request.chat.id, request.message_id)
                if not self.__has_permissions__(request, app_name, require_permission, server_whitelisted):
                    return
                mod_name, mod_command = self.__get_mod_name_command__(request, f, app_name)
                if not mod_name or not mod_command:
                    return
                self.__execute_function__(request, f, mod_name, mod_command)

            self.__register_command__(wrapper, f, commands, app_name, server_whitelisted, ignore_listing,
                                      content_types, regexp, func, chat_types)
            return wrapper
        return wrapp_function


from .models import BotModel


class FatherBot(BotModel):

    def __init__(self, name: str, bot: Bot, api_key: str = None, home_button_function: callable = None, **kwargs):
        super().__init__(name, bot, **kwargs)
        self.help_commands = ['help', 'Help']
        self.NAVBAR = None
        self.buttons = [
            (Button('Home', 'Home', home_button_function or self.home), ['start', 'home']),
            (Button('Help', 'Help', self.help_function), self.help_commands),
            (Button('Clean', 'Clean', self.clean_chat), ['clean'])
        ]
        self.__register_navbar__(self.buttons)

    def __register_navbar__(self, buttons):
        self.NAVBAR = NavBar([b[0] for b in buttons])
        for button in buttons:
            btn_instance, btn_commands = button
            self.bot.modules_obj[self.name] = dict()
            for command in btn_commands:
                self.bot.register_callback(self, btn_instance.func, callback=command)
                self.bot.modules_obj[self.name][command] = (btn_instance.func, True,)

    def home(self, chat_id: int, command: str, message: str):
        buttons = [
            [Button(label=mod_name, command=mod_name, func=mod_instance.home_keyboard)]
            for mod_name, mod_instance in self.bot.modules.items()
            if hasattr(mod_instance, 'home_keyboard')
        ]
        buttons += [self.NAVBAR.buttons]
        keyboard = KeyBoard(self, buttons).get()
        self.bot.send_message(chat_id, 'Selecciona una opción:', reply_markup=keyboard)

    def help_function(self, chat_id: int, command: str, message: str):
        """This function automatically returns the help docstring to each function"""
        help_msg = """
            This function returns the help docstring by each function defined in the Telegram Bot.

Actually, you could get help for this functions:
"""
        funcs = dict()
        for fun in self.bot.functions_doc:
            if fun_name := self.bot.functions_doc.get(fun, None):
                if fun_name[0] and fun_name[1]:
                    if fun_name[1] not in funcs:
                        funcs[fun_name[1]] = list()
                    funcs[fun_name[1]].append(fun)
        for mod_name, mod_funcs in funcs.items():
            help_msg += "\n" + "#" * 32
            help_msg += f"\n    [{mod_name}]"
            for fun in mod_funcs:
                help_msg += f"\n        {'/' if fun.isalpha() else ''}{fun}"
        function_name = message.strip()
        for help_command in self.help_commands:
            function_name = function_name.removeprefix(help_command).strip()
            function_name = function_name.removeprefix(f"/{help_command}").strip()
        if not function_name:
            self.bot.send_message(chat_id, help_msg)
            return
        if function_name not in self.bot.functions_doc.keys():
            self.bot.send_message(chat_id,
                                  f"Function {function_name} does not exist")
            return
        if doc := self.bot.functions_doc.get(function_name, None):
            self.bot.send_message(chat_id, doc[0])
            return
        self.bot.send_message(chat_id, f"Function {function_name} does not have documentation")

    def clean_chat(self, chat_id: int, command: str, message: str):
        self.bot.history.clean(chat_id, self.bot.bot)
