from pykeepass import PyKeePass as Pk

from pykeepass.exceptions import CredentialsError

from ..core.exceptions import KdbxFileNotFound, KdbxFileCredentialsError
from ..core.utils import AppData


class Passwords:

    pykee: Pk

    def __init__(self, vault: AppData):
        self.vault = vault

    def save_file(self):
        self.pykee.save()

    def load_file(self, chat_id: int, vault_name: str, cypher_key: str = None):
        files = self.vault.list_dir(str(chat_id), vault_name)
        if not any([f.endswith(".kdbx") for f in files]):
            raise KdbxFileNotFound("Kdbx file doesn´t exists")
        name = f"{vault_name}.kdbx"
        key_name = f"{vault_name}.keyx"
        pass_name = "password.bot"
        file_path, _ = self.vault.get(name, str(chat_id), vault_name)
        keyfile_path, keyfile_exists = self.vault.get(key_name, str(chat_id), vault_name)
        keyfile_path = keyfile_path if keyfile_exists else None
        password_path, password_exists = self.vault.get(pass_name, str(chat_id), vault_name)
        password = self.vault.decrypt(open(password_path, "r").read(), cypher_key) if password_exists else None
        try:
            return Pk(file_path, password=password, keyfile=keyfile_path)
        except CredentialsError:
            raise KdbxFileCredentialsError("Authentication error, invalid password or keyfile")

    def edit_entry(self, **kwargs):
        pass

    def edit_password(self, **kwargs):
        pass

    def load_groups(self):
        pass

    def edit_group(self):
        pass

    def show_password(self, **kwargs):
        pass

    def show_info(self, **kwargs):
        pass
