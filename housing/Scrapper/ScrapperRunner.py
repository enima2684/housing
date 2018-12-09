from housing.HousingModule import HousingModule
from housing.Scrapper.PAP import PAP
from housing.Scrapper.SeLoger import SeLoger
import os


class ScrapperRunner(HousingModule):

    def __init__(self):
        self.scrappers = [
            PAP(),
            SeLoger(),
        ]

    def run(self):
        for scrapper in self.scrappers:
            scrapper.run()

if __name__ == '__main__':
    ScrapperRunner().run()