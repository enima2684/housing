import requests
import os
from datetime import datetime
import boto3


from housing.HousingModule import HousingModule


class Scrapper(HousingModule):

    def __init__(self):
        super(Scrapper, self).__init__()
        self.website = None
        self.url = None
        self.s3 = boto3.resource('s3')

    def scrap(self):
        """
        Scraps the website and returns the html content
        :return:
        """
        self.logger.info("Scrapping the website {}".format(self.url))
        response = requests.get(self.url)
        if response.status_code != 200:
            raise ConnectionRefusedError('Refused connection to {}'.format(self.url))
        html_content = response.text
        return html_content

    def save_to_s3(self, html_content):
        """
        Saves the html content to S3
        :param html_content: parsed html content
        :return:
        """
        self.logger.info("Saving the data on S3")
        key_value = datetime.now().strftime("%Y%m%d_%H%M%S") + "__" + self.website

        self.s3.Object(
            os.getenv("AWS_BUCKET_NAME"),
            key_value
        ).put(Body=html_content)

        self.logger.debug("htlm saved under {}".format(key_value))

    def run(self):

        if self.url is None:
            raise ValueError('a url for parsing must be provided')

        # 1. Scrap the website
        html_content = self.scrap()

        # 2. save the data
        self.save_to_s3(html_content=html_content)

        # 3. update the metadata
        self.logger.info("Updating the metadata")


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.run()
