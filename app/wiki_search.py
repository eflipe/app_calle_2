import requests
from bs4 import BeautifulSoup


class CalleClass:
    def __init__(self, calle_url: str):
        self.calle_url = f'https://es.wikipedia.org/wiki/{calle_url}'
        self.tag_name = 'p'
        self.string_calle = None

    def load_calle(self) -> str:
        response = requests.get(self.calle_url)
        content = response.content.decode('utf-8')
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name)
        self.string_calle = element.text.strip()
        print(self.string_calle)
        return self.string_calle

    def wiki_calle(self) -> str:
        return self.calle_url
