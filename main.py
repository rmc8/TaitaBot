from time import sleep
from datetime import datetime

import yaml
import requests as r


class TaitaBot:
    def __init__(self, interval, name, url, tar_min=55):
        self.tar_min = tar_min
        self.interval = interval
        self.name = name
        self.url = url
        self.done = False

    def taita(self):
        r.post(self.url, data={"content": "炊いた？"})

    def jiho(self):
        dt = datetime.now()
        if not self.done and dt.minute == self.tar_min:
            msg = f"{self.name}が{dt.hour}時{dt.minute}分をお知らせいたします。"
            r.post(self.url, data={"content": msg})
            self.done = True

    def run(self):
        while True:
            self.taita()
            self.done = False
            for _ in range(60 * self.interval):
                sleep(1)
                self.jiho()

def main():
    with open("config.yaml") as f:
        obj = yaml.safe_load(f)
    settings = obj["base"]
    jb = TaitaBot(**settings, tar_min=55)
    jb.run()


if __name__ == "__main__":
    main()
