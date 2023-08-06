import requests


class ImageGeneratorModel:

    def __init__(self, api_key: str = None):
        pass

    def new_image(self, context: str = None):
        return "", True


class DallE(ImageGeneratorModel):

    def __init__(self, api_key: str):
        super().__init__(api_key)
        import openai
        self.openai = openai
        self.openai.api_key = api_key

    def new_image(self, context: str = None):
        try:
            response = self.openai.Image.create(
                prompt=context,
                n=1,
                size="1024x1024"
            )
            return response['data'][0]['url'], True
        except Exception as e:
            return str(e), False


class ThisPersonDoesNotExist(ImageGeneratorModel):

    def __init__(self):
        super().__init__()
        self.url = "https://thispersondoesnotexist.com/image"
        self.headers = {'User-Agent': 'Mozilla Firefox'}

    def new_image(self, context: str = None):
        return requests.get(self.url, headers=self.headers).content, True


class Generator:

    def __init__(self, api_key: str = None):
        self.apis = {
            # "dalle": (DallE(api_key), True),
            "thispersondoesnotexist": (ThisPersonDoesNotExist(), False)
        }

    def generators(self):
        return self.apis

    def new_image(self, app, context: str = None):
        assert app in self.apis, f"'{app}' is not registerd in Image Generator module"
        mod_instance, needs_context = self.apis.get(app)
        return mod_instance.new_image(context if needs_context else None)
