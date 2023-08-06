from bs4 import BeautifulSoup as bs
import requests
from requests.exceptions import ConnectionError, ConnectTimeout


class Spider:

    def __init__(self, url: str, max_depth: int = 5):
        self.url = url
        self.max_depth = int(max_depth)
        self.results = {}
        self.total_links = []

    def extract_links(self, actual_url="", actual_depth: int = None):
        url = self.url if not actual_url else actual_url
        if not actual_depth:
            actual_depth = self.max_depth
        result = self.get(url)
        if result:
            soup = bs(result, "html.parser")
            links = soup.find_all("a", href=True)
            clean_url = url.replace("https://", "").replace("http://", "")
            for link in links:
                if clean_url not in link["href"]:
                    continue
                if link["href"] not in self.total_links and link["href"].startswith("http"):
                    self.total_links.append(link["href"])
                    if actual_depth > 0:
                        self.extract_links(link["href"], actual_depth=actual_depth - 1)

    def tree(self, thread_id):
        self.extract_links()
        for link in self.total_links:
            print(link)
            tmp_result = self.results
            clean_url = link.replace("https://", "").replace("http://", "")
            url_dir = clean_url.split('/')
            for i_space, space in enumerate(url_dir):
                if space:
                    if i_space < len(url_dir):
                        if space not in tmp_result and i_space + 1 < len(url_dir) and not space.startswith('?'):
                            tmp_result[space] = dict()
                    else:
                        if space not in tmp_result:
                            tmp_result[space] = []
                        if url_dir[-1] not in tmp_result[space]:
                            tmp_result[space].append(url_dir[-1])
                    if space in tmp_result:
                        tmp_result = tmp_result[space]
        return thread_id, self.results

    @staticmethod
    def get(url: str):
        tmp_http = tmp_https = url
        if 'http' not in url:
            tmp_http = f'http://{url}'
            tmp_https = f'https://{url}'
        try:
            response = requests.get(tmp_https, timeout=3)
        except (ConnectionError, ConnectTimeout):
            try:
                response = requests.get(tmp_http, timeout=3)
            except (ConnectionError, ConnectTimeout):
                return None
        if response.status_code != 200:
            return None
        return response.content
