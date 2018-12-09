import requests
import os
from datetime import datetime
import boto3
from sqlalchemy.orm import sessionmaker
import hashlib
import uuid

from housing.models import db_connect, create_tables
from housing.models.Scrap_Metadata import Scrap_Metadata
from housing.HousingModule import HousingModule


class Scrapper(HousingModule):

    def __init__(self):
        super(Scrapper, self).__init__()
        self.web_site = None
        self.url = None
        self.s3 = boto3.resource('s3')
        self.html_content = None

        # setup db
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

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

    def save_to_s3(self):
        """
        Saves the html content to S3
        :param html_content: parsed html content
        :return:
        """
        self.logger.info("Saving the data on S3")
        file_name = "__".join([
            uuid.uuid4().hex[:6],
            datetime.now().strftime("%Y%m%d_%H%M%S"),
            self.web_site,
            ])
        self.s3.Object(
            os.getenv("AWS_BUCKET_NAME"),
            file_name
        ).put(Body=self.html_content)

        self.logger.debug("html saved under {}".format(file_name))

        return file_name


    def getHash(self):
        hash_object = hashlib.sha256(self.html_content.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def update_metadata(self, file_name):
        self.logger.info(f"Saving metadata for {self.web_site}")
        session = self.Session()

        hash = self.getHash()

        meta = Scrap_Metadata(
            file_name=file_name,
            web_site =self.web_site,
            hash_doc = hash,
        )

        try:
            session.add(meta)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def run(self):

        if self.url is None:
            raise ValueError('a url for parsing must be provided')

        # 1. Scrap the website
        self.html_content = self.scrap()

        # 2. save the data
        file_name = self.save_to_s3()

        # 3. update the metadata
        self.update_metadata(file_name=file_name)


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.run()
