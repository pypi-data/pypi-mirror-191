from uuid import UUID
import json

from ..modules.passwords import Passwords
from ..core.models import BotModel
from ..core.manager import Bot
from ..core.keyboards import Button


class PasswordBot(BotModel):

    def __init__(self, name: str, bot: Bot, vault_path: str = None, **kwargs):
        super().__init__(name, bot, vault_path, **kwargs)
        self.load_keyboards(self, __file__)
        self.bot.register_handler(self, self.main, commands=["🔐", "passwords"])
        self.module = Passwords(vault=self.vault)
        self.cypher_key = self.config.get('vault', {}).get('fernet_key', None)
        self.keepass_extensions = ['kdbx', 'keyx']

        @bot.bot.message_handler(func=lambda m: any(m.document.file_name.endswith(ext)
                                                    for ext in self.keepass_extensions),
                                 content_types=['document'])
        def get_keepass_file(message):
            chat_id = message.chat.id
            file_name = message.document.file_name
            file_id = message.document.file_id
            chat_dir = self.vault.make_dir(str(chat_id))
            file_content_dir = self.vault.make_dir(file_name.split('.')[0], path=chat_dir)
            file_path = bot.bot.get_file(file_id).file_path
            file_content = bot.bot.download_file(file_path)
            if not self.vault.save_file(file_name, file_content, file_content_dir, binary=True):
                bot.send_message(chat_id, f"Something went wrong saving file {file_name}")
                return
            if file_name.endswith('kdbx'):
                bot.send_message(message.chat.id,
                                 f"File {file_name} saved into vault.\nIf your file "
                                 f"need's a password for been opened, reply it here:",
                                 reply_callback=self.save_password,
                                 reply_append_command=file_name)
                return
            bot.send_message(message.chat.id, f"File {file_name} saved into vault",
                             reply_markup=self.keyboards.get('main'))

    @staticmethod
    def __parse_callback__(callback_data: str):
        command = callback_data.split('|')
        is_vault = int(command[0]) == 1
        vault_name = command[1]
        is_group = int(command[2]) == 1
        entry_uuid = command[3]
        return is_vault, vault_name, is_group, entry_uuid

    def save_password(self, chat_id: int, command: str, message: str):
        message = self.vault.encrypt(message, self.cypher_key)
        self.vault.save_file("password.bot", message, self.vault.get_dir(str(chat_id), command.split('.')[0]))
        self.bot.send_message(chat_id, "Password saved encrypted in your vault",
                              reply_markup=self.create_home_keyboard(chat_id))

    def create_home_keyboard(self, chat_id: int):
        vaults_buttons = [
            [
                Button(
                    label=vault,
                    command=f"1|{vault}|0|",
                    func=self.vault_keyboard
                )
            ]
            for vault in self.vault.list_dir(str(chat_id))
        ]
        return self.create_keyboard(vaults_buttons, "home")

    def create_vault_keyboard(self, chat_id: int, vault_name: str):
        vault_buttons = []
        for group in self.module.load_file(chat_id, vault_name, self.cypher_key).groups:
            for subgroup in group.subgroups:
                vault_buttons.append([
                    Button(label=f"📦 {subgroup.name}",
                           command=f"0|{vault_name}|1|{str(subgroup.uuid)}",
                           func=self.vault_keyboard)
                ])
        for entry in self.module.load_file(chat_id, vault_name, self.cypher_key).entries:
            vault_buttons.append([
                Button(label=f"🔐{entry.title} - {entry.username}",
                       command=f"0|{vault_name}|0|{str(entry.uuid)}",
                       func=self.entry_keyboard)
            ])
        return self.create_keyboard(buttons=vault_buttons, name="vault")

    def home_keyboard(self, chat_id: int, command: str, message: str):
        """
        This function returns the home keyboard of the module
        """
        msg = """🗃 Vaults 🗃"""
        self.bot.send_message(chat_id, msg,
                              reply_markup=self.create_home_keyboard(chat_id))

    def vault_keyboard(self, chat_id: int, command: str, message: str):
        """
        This function returns the vault keyboard of the module
        """
        is_vault, vault_name, is_group, entry_uuid = self.__parse_callback__(command)
        kp_module = self.module.load_file(chat_id, vault_name, self.cypher_key)
        if is_vault:
            msg = """🗃 Groups and entries 🗃"""
            self.bot.send_message(chat_id, msg,
                                  reply_markup=self.create_vault_keyboard(chat_id, vault_name))
            return
        if is_group and entry_uuid:
            group_name = kp_module.find_groups(uuid=UUID(entry_uuid))[0].name
            msg = f"""🗃 Groups and entries for {group_name} 🗃"""
            self.bot.send_message(chat_id, msg,
                                  reply_markup=self.create_vault_keyboard(chat_id, vault_name))
            return
        if entry_uuid:
            entry_name = kp_module.find_entries(uuid=UUID(entry_uuid))[0].name
            msg = f"""🗃 Entry information for {entry_name} 🗃"""
            self.bot.send_message(chat_id, msg,
                                  reply_markup=self.create_vault_keyboard(chat_id, vault_name))
            return
        msg = f"""Something went wrong with entry/group UUID"""
        self.bot.send_message(chat_id, msg,
                              reply_markup=self.create_vault_keyboard(chat_id, vault_name))

    def entry_keyboard(self, chat_id: int, command: str, message: str):
        """
        This function returns the vault keyboard of the module
        """
        is_vault, vault_name, is_group, entry_uuid = self.__parse_callback__(command)
        kp_module = self.module.load_file(chat_id, vault_name, self.cypher_key)
        entry_data = kp_module.find_entries(uuid=UUID(entry_uuid))[0]
        msg = f"""🔐 Selected entry {entry_data.title} - {entry_data.username} 🔐"""
        self.bot.send_message(chat_id, msg,
                              reply_markup=self.create_keyboard(name="entry"))

    def main(self, chat_id: int, command: str, message: str):
        """
        This function returns the keyboard for managing passwords
        """
        keyboard = self.keyboards.get('home', [])
        self.bot.send_message(chat_id, "home", reply_markup=keyboard)

    def create_vault(self, chat_id: int, command: str, message: str):
        """
        This function returns the keyboard for managing passwords
        """
        msg = """Indica el nombre del vault que quieres crear:"""
        self.bot.send_message(chat_id, msg, reply_callback=self.create_vault_name)

    def create_vault_name(self, chat_id: int, command: str, message: str):
        keyboard = self.keyboards.get('home', [])
        vault_name = '_'.join(f"{command} {message}".strip().title().split(' '))
        self.bot.send_message(chat_id, f"Vault creado con el nombre {vault_name}", reply_markup=keyboard)

    def edit_vault(self, chat_id: int, command: str, message: str):
        """
        This function returns the keyboard for managing passwords
        """
        self.bot.send_message(chat_id, "Llegas a editar un vault")

    def delete_vault(self, chat_id: int, command: str, message: str):
        """
        This function returns the keyboard for managing passwords
        """
        self.bot.send_message(chat_id, "Llegas a borrar un vault")

    def create_group(self, chat_id: int, command: str, message: str):
        """
        This function allows to create a new group
        """
        self.bot.send_message(chat_id, "Llegas a creat un group")

    def edit_group(self, chat_id: int, command: str, message: str):
        """
        This function allows to edit a specified group
        """
        self.bot.send_message(chat_id, "Llegas a editar un group")

    def delete_group(self, chat_id: int, command: str, message: str):
        """
        This function allows to delete a specified group
        """
        self.bot.send_message(chat_id, "Llegas a borrar un group")

    def show_entry(self, chat_id: int, command: str, message: str):
        """
        This function allows to show the information of a specified entry
        """
        self.bot.send_message(chat_id, "Llegas a ver un entry")

    def create_entry(self, chat_id: int, command: str, message: str):
        """
        This function allows to create a new entry
        """
        self.bot.send_message(chat_id, "Llegas a crear un entry")

    def edit_entry(self, chat_id: int, command: str, message: str):
        """
        This function allows to edit a specified entry
        """
        self.bot.send_message(chat_id, "Llegas a editar un entry")

    def delete_entry(self, chat_id: int, command: str, message: str):
        """
        This function allows to delete a specified entry
        """
        self.bot.send_message(chat_id, "Llegas a borrar un entry")

    def show_password(self, chat_id: int, command: str, message: str):
        """
        This function allows to show just the password for a specified entry
        """
        pass

    def show_info(self, chat_id: int, command: str, message: str):
        """
        This function allows to show all the information of a specified entry
        """
        pass
