from ..core.workers import stop
from cryptography.fernet import Fernet
from contextlib import suppress
import json
import re
import os


MAX_LENGTH = 57


class History:

    """
    This class is used for saving all the commands sent to the bot
    and all the messages sent by the bot.

    With this class we can clean all the messages in a chat conversation.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def __save_history__(self, history: dict):
        """Save the log file"""
        with open(self.file_path, 'w') as convert_file:
            convert_file.write(json.dumps(history, indent=4))
        return True

    def __load_history__(self):
        """Returns the dictionary with the full history message of the file"""
        if not os.path.isfile(self.file_path):
            return dict()
        with open(self.file_path, 'r') as f:
            content = f.read()
            result = json.loads(content)
        return result

    def save_message(self, module_name: str, chat_id: int, message_id: int):
        """Save the message in the chat_id`s proper module_names' history"""
        history = self.__load_history__()
        history[str(chat_id)] = message_id
        self.__save_history__(history)

    def clean(self, chat_id: int, bot):
        history = self.__load_history__()
        if last_message_id := history.get(str(chat_id), 0):
            for message_id in range(last_message_id, 1, -1):
                try:
                    bot.delete_message(chat_id, message_id)
                except Exception:
                    pass
        del history[str(chat_id)]
        self.__save_history__(history)


def is_email_address(email_address: str):
    """Function that verifies if a text is an email address"""
    regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    return re.fullmatch(re.compile(regex), email_address)


def center_text(text: str):
    """Function that returns the same text divided into multiline text centered"""
    result = []
    for text_line in text.split("\n"):
        if len(text_line) <= MAX_LENGTH:
            result.append(text_line)
            continue
        words = text_line.split(" ")
        tmp_line = []
        tmp_phrase = []
        creating = True
        for word in words:
            if len(' '.join(tmp_phrase)) + len(word) + 1 <= MAX_LENGTH:
                tmp_phrase.append(word)
                creating = True
            else:
                tmp_line.append(' '.join(tmp_phrase))
                tmp_phrase = [word]
                creating = False
        if creating:
            tmp_line.append(' '.join(tmp_phrase))
        result.append('\n'.join(tmp_line))
    return '\n'.join(result)


def get_sender(current_frame, modules: dict, modules_obj: dict):
    caller_frame = current_frame.f_back
    if 'self' in caller_frame.f_locals:
        caller_instance = caller_frame.f_locals['self']
        from ..core.manager import Bot
        assert caller_instance.name in modules or isinstance(caller_instance, Bot), \
            "Module does not exist in modules list"
        return caller_instance.name
    elif 'f' in caller_frame.f_back.f_locals:
        caller_function = caller_frame.f_back.f_locals
        for module, module_commands in modules_obj.items():
            for func_command, func_obj in module_commands.items():
                if func_obj[0] == caller_function:
                    for loaded_mod, instance in modules.items():
                        if module == instance.__class__.__name__:
                            return loaded_mod
    return 'Script'


def thread_result(obj):
    def function(f):
        def wrapper(thread_id: str, result: object):
            chat_id = obj.threads.pop(thread_id)
            stop(thread_id)
            f(chat_id, result)
        return wrapper
    return function


class AppData:

    def __init__(self, name: str):
        self.project = "superbotlib"
        self.name = name
        self.path = os.path.join(os.getenv("APPDATA", os.path.expanduser("~")), f".{self.project}")
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.module_path = os.path.join(self.path, self.name)
        if not os.path.isdir(self.module_path):
            os.mkdir(self.module_path)
        self.extensions_map = {
            "kdbx": None,
            "json": self.__to_json__,
            "keyx": None,
            "ppk": None,
        }

    @staticmethod
    def __to_json__(file_path: str, content: object, encoding: str = 'utf-8'):
        with open(file_path, 'w', encoding=encoding) as convert_file:
            try:
                convert_file.write(json.dumps(content))
            except Exception as e:
                print(e)
                return False
        return True

    @staticmethod
    def __to_binary__(file_path: str, content: bytes):
        with open(file_path, 'wb') as convert_file:
            try:
                convert_file.write(content)
            except Exception as e:
                print(e)
                return False
        return True

    @staticmethod
    def __to_file__(file_path, content: str, encoding: str = 'utf-8'):
        with open(file_path, 'w', encoding=encoding) as convert_file:
            try:
                convert_file.write(content)
            except Exception as e:
                print(e)
                return False
        return True

    def __write_file__(self, file_path: str, content: any, extension: str,
                       binary: bool = False, encoding: str = 'utf-8'):
        if func := self.extensions_map.get(extension):
            return func(file_path, content)
        if binary:
            return self.__to_binary__(file_path, content)
        return self.__to_file__(file_path, content, encoding)

    def get(self, file_name: str, dir_name: str = None, sub_dir_name: str = None):
        tmp_file_path = self.module_path
        if dir_name:
            tmp_file_path = os.path.join(tmp_file_path, dir_name)
            if sub_dir_name:
                tmp_file_path = os.path.join(tmp_file_path, sub_dir_name)
        tmp_file_path = os.path.join(tmp_file_path, file_name)
        return tmp_file_path, os.path.isfile(tmp_file_path)

    def get_dir(self, dir_name: str, sub_dir_name: str = None):
        tmp_dir_path = self.make_dir(dir_name)
        if sub_dir_name:
            tmp_dir_path = self.make_dir(sub_dir_name, path=tmp_dir_path)
        return tmp_dir_path

    def exists_dir(self, dir_name: str, sub_dir_name: str = None, path: str = None):
        final_path = os.path.join(self.module_path if not path else path, dir_name)
        if sub_dir_name:
            final_path = os.path.join(final_path, sub_dir_name)
        return final_path if os.path.isdir(final_path) else None

    def list_dir(self, dir_name: str, sub_dir_name: str = None, path: str = None):
        final_path = os.path.join(self.module_path if not path else path, dir_name)
        if sub_dir_name:
            final_path = os.path.join(final_path, sub_dir_name)
        return os.listdir(final_path) if os.path.isdir(final_path) else list()

    def make_dir(self, name: str, path: str = None):
        new_path = os.path.join(path or self.module_path, name)
        with suppress(FileExistsError):
            os.mkdir(new_path)
        return new_path

    def save_file(self, name: str, content: object, path: str = None, encoding: str = 'utf-8', binary: bool = False):
        new_file_path = os.path.join(path or self.module_path, name)
        if not os.path.isdir(os.path.split(new_file_path)[0]):
            os.mkdir(os.path.split(new_file_path)[0])
        extension = name.split(".")[-1].lower()
        return self.__write_file__(new_file_path, content, extension, encoding=encoding, binary=binary)

    @staticmethod
    def encrypt(content: str, cypher_key: str = None):
        if not cypher_key:
            return content
        fernet = Fernet(cypher_key.encode())
        return fernet.encrypt(content.encode()).decode()

    @staticmethod
    def decrypt(content: str, cypher_key: str = None):
        if not cypher_key:
            return content
        fernet = Fernet(cypher_key.encode())
        return fernet.decrypt(content.encode()).decode()
