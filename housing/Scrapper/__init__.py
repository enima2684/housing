import requests
import os
from datetime import datetime
import boto3
from sqlalchemy.orm import sessionmaker
import hashlib
import uuid
import time

from housing.models import db_connect, create_tables
from housing.models.Record import Record
from housing.HousingModule import HousingModule


class Scrapper(HousingModule):

    def __init__(self):
        super(Scrapper, self).__init__()
        self.web_site = None
        self.base_url = None
        self.s3 = boto3.resource('s3')

        # setup db
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def scrap(self, url):
        """
        Scraps the website and returns the html content
        :return:
        """
        self.logger.info("Scrapping the website {}".format(url))
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionRefusedError('Refused connection to {}'.format(url))
        html_content = response.text
        return html_content

    def save_to_s3(self, html_content, page=1):
        """
        Saves the html content to S3
        :param html_content: parsed html content
        :return:
        """
        self.logger.info("Saving the data on S3")

        file_name = "__".join([
            uuid.uuid4().hex[:6],
            str(page),
            datetime.now().strftime("%Y%m%d_%H%M%S"),
            self.web_site,
            ])
        self.s3.Object(
            os.getenv("AWS_BUCKET_NAME"),
            file_name
        ).put(Body=html_content)

        self.logger.debug("html saved under {}".format(file_name))

        return file_name

    def update_metadata(self, file_name):
        self.logger.info(f"Saving metadata for {self.web_site}")
        session = self.Session()

        meta = Record(
            file_name=file_name,
            web_site=self.web_site
        )

        try:
            session.add(meta)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def generate_urls(self, number_pages):
        raise NotImplementedError("generate_urls not implemented")

    def get_number_pages(self):
        """
        Gets the number of pages for the search
        :return:
        """
        raise NotImplementedError("get_number_pages not implemented")

    def run(self):

        if self.base_url is None:
            raise ValueError('a base_url for parsing must be provided')

        # get number of pages
        number_pages = self.get_number_pages()

        # generate urls
        urls = self.generate_urls(number_pages)

        for page, url in enumerate(urls):

            # 1. Scrap the website
            html_content = self.scrap(url=url)

            # 2. save the data
            file_name = self.save_to_s3(html_content, page=page+1)

            # 3. update the metadata
            self.update_metadata(file_name=file_name)

            # 4. sleep a little bit
            time.sleep(30)


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.run()
