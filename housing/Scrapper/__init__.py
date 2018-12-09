import requests

from housing.HousingModule import HousingModule


class Scrapper(HousingModule):

    def __init__(self):
        super(Scrapper, self).__init__()
        self.url = None

    def run(self):

        if self.url is None:
            raise ValueError('a url for parsing must be provided')

        # 1. Scrap the website
        self.logger.info("Scrapping the website {}".format(self.url))

        # 2. save the data
        self.logger.info("Saving the data")

        # 3. update the metadata
        self.logger.info("Updating the metadata")


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.run()
