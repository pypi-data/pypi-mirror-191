from requests import get, post
from requests.models import Response


def exception_evade(default: object = None):
    def wrapp_func(f):
        def wrapper(*args, **kwargs):
            try:
                res = f(*args, **kwargs)
            except Exception as e:
                res = dict(code=200, data=default, warning=str(e))
            return res
        return wrapper
    return wrapp_func


class ApiManager:

    def __init__(self, endpoint: str, timeout: int = 3):
        self.endpoint = endpoint
        self.timeout = timeout

    @exception_evade(default=list())
    def __do_get__(self, function: str):
        return self.__parse_result__(get(f"{self.endpoint}{function}", timeout=self.timeout))

    @exception_evade(default=list())
    def __do_post__(self, function: str, data: dict = None):
        return self.__parse_result__(post(f"{self.endpoint}{function}", json=data, timeout=self.timeout))

    @staticmethod
    def __parse_result__(response: Response):
        if response.status_code != 200:
            return dict(code=response.status_code)
        if response.json().get("code") != 200:
            return response.json()
        return response.json().get("data")

    def get_allowed_users(self):
        try:
            return self.__do_get__("/permissions")
        except Exception as e:
            print(f"API Error - {str(e)}")
            return []

    def save_scan(self, data):
        print(data)
        return self.__do_post__("/scans/new", data=data)

    def save_auth(self, chat_id: str, module_name: str, function_name: str):
        print(f"[API] - Auth saving::POST::Chat_id:{chat_id}|Module_name:{module_name}|Function_name:{function_name}")
        return self.__do_post__("/auth/add", data=dict(
            chat_id=chat_id,
            module_name=module_name,
            function_name=function_name
        ))

    def show_auth(self, chat_id: str, module_name: str, function_name: str):
        print(f"[API] - Showing auth::POST::Chat_id:{chat_id}|Module_name:{module_name}|Function_name:{function_name}")
        return self.__do_post__("/auth/check", data=dict(
            chat_id=chat_id,
            module_name=module_name,
            function_name=function_name
        ))
