from ..modules.image_generation import Generator
from ..core.models import BotModel
from ..core.manager import Bot
from ..core.keyboards import Button


class ImageGenerationBot(BotModel):

    def __init__(self, name: str, bot: Bot, api_key: str = None, **kwargs):
        super().__init__(name, bot, api_key, **kwargs)
        self.generator = Generator(api_key)

        buttons_provider = [
            [Button(label=mod_name, command=mod_name, func=mod_instance[0].new_image)]
            for mod_name, mod_instance in self.generator.generators().items()
        ]
        self.keyboard_provider = self.create_keyboard(buttons_provider, "")
        self.bot.register_handler(self, self.new_image, commands=list(self.generator.generators().keys()))

    def new_image(self, chat_id: int, command: str, message: str):
        """This function creates an image depending on the app and the context given"""
        if command not in self.generator.apis:
            self.bot.send_message(chat_id,
                                  f"Command '{command}' does not exist in Image Generator module",
                                  reply_markup=self.keyboard_provider)
            return
        if self.generator.apis.get(command)[1]:
            self.bot.send_message(chat_id, "Please, describe your context: ",
                                  reply_callback=self.new_image_by_context,
                                  reply_append_command=command)
            return
        if img := self.generator.new_image(command, message):
            self.bot.send_photo(chat_id, img[0],
                                reply_markup=self.keyboard_provider)
            return
        self.bot.send_message(chat_id, "Something went wrong",
                              reply_markup=self.keyboard_provider)

    def home_keyboard(self, chat_id: int, command: str, message: str):
        msg = """Por favor elije un proveedor para la imagen:"""
        self.bot.send_message(chat_id, msg,
                              reply_markup=self.keyboard_provider)

    def new_image_by_context(self, chat_id: int, command: str, message: str):
        img, generated = self.generator.new_image(command, message)
        if generated:
            self.bot.send_photo(chat_id, img,
                                reply_markup=self.keyboard_provider)
            return
        self.bot.send_message(chat_id, f"Cant generate image ({img})",
                              reply_markup=self.keyboard_provider)
