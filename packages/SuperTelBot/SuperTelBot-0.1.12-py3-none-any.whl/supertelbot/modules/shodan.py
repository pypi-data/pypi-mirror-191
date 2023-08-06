import requests


class Shodan:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://api.shodan.io"
        self.data = dict(key=self.api_key)

    def __do_get__(self, function: str, params: dict = None):
        search_params = self.data
        if params:
            search_params.update(**params)
        return requests.get(f"{self.endpoint}{function}", params=self.data).json()

    def host(self, ip: str):
        return self.__do_get__(f"/shodan/host/{ip}")

    def count(self, query: str, facets: str = None):
        total_query = dict(query=query)
        if facets:
            total_query.update(**dict(facets=facets))
        return self.__do_get__("/shodan/host/count", params=total_query)
