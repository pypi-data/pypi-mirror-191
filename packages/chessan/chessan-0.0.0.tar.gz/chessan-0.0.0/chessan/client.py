import time
import requests
from rich.progress import track


class Client:
    def __init__(self, parse: bool, sleep: float = 0.1, verbose: bool = False) -> None:
        self.parse = parse
        self.sleep = sleep
        self.verbose = verbose
        self.endpoint = "https://api.chess.com/pub"

    def profile(self, user: str) -> dict:
        data = requests.get(f"{self.endpoint}/player/{user}").json()
        if self.parse:
            return self.parse_profile(data)
        else:
            return data

    def games(self, user: str) -> dict:
        urls = requests.get(f"{self.endpoint}/player/{user}/games/archives").json()[
            "archives"
        ]
        archive = list()
        for url in track(urls, disable=not self.verbose, description=user):
            games_month = requests.get(url).json()["games"]
            archive.extend(games_month)
            time.sleep(self.sleep)
        return archive

    def download(self, user: str) -> dict:
        data = self.profile(user)
        data["games"] = self.games(user)
        return data


class RecursiveClient:
    pass
