import boto3
import os
from bs4 import BeautifulSoup
import re
from sqlalchemy.orm import sessionmaker

from housing.HousingModule import HousingModule
from housing.models import db_connect, create_tables
from housing.models.Ad import Ad
from housing.models.Record import WebSites


class ParserPAP(HousingModule):

    def __init__(self, file_name):
        """

        :param file_name: file name on S3 bucket
        """
        super(ParserPAP, self).__init__()

        self.file_name = file_name
        self.s3 = boto3.resource('s3')

        # setup db
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)


    def open(self, file_name):
        """
        Opens the file from S3 and returns the html content in a string format
        :return:
        """
        self.logger.debug(f'Opening file {file_name} from S3 bucket {os.getenv("AWS_BUCKET_NAME")}')

        try:
            obj = self.s3.Object(
                os.getenv("AWS_BUCKET_NAME"),
                self.file_name
            )

            content = obj.get()['Body'].read().decode('utf-8')
        except Exception as err:
            self.logger.error(err)

        return content



    def parse_item(self, item):
        """
        Parses a single item on the page
        :param item: bs4 item
        :return: parsed document
        """

        try:

            if (item.select_one(".item-price") is not None):

                id = "PAP_" + item.select_one('.item-title').get('name')
                price = int(item.select_one(".item-price").text[:-2].replace('.', ''))

                for li in item.select("ul.item-tags > li"):
                    if "m2" in str(li.text):
                        area = str(li.text)[:2]

                description = str(item.select_one('.item-description').text)
                localisation = description.split('.')[0].strip()

                postal_code = re.findall("\(\w+\)", localisation)[0][1:-1]
                url = "https://www.pap.fr" + item.select_one(".item-description a").get('href')

                ad = Ad(**{
                    'id'         : id,
                    'web_site'   : WebSites.PAP,
                    'source_file': self.file_name,

                    'price'      : price,
                    'area'       : area,
                    'postal_code': postal_code,
                    'url'        : url,
                })

                return ad

        except Exception as err:
            self.logger.error(err)


    def parse_doc(self, content):
        """
        parses the html content of the document and creates a "X" object
        :return:
        """
        soup = BeautifulSoup(content, 'lxml')
        items = soup.select('.search-list-item')

        parsed_items = [ self.parse_item(item) for item in items ]

        # keep only relevant items
        parsed_items = [item for item in parsed_items if item]

        if (len(parsed_items) < 2):
            raise Exception(f"Somehting went wrong on the parsing of the file {self.file_name}")

        self.logger.info(f'parsed {len(parsed_items)} items from {self.file_name}')

        return parsed_items

    def save_to_db(self, parsed_data):
        """
        Saves the  data to the database
        :param parsed_data: list of Ad elements
        :return:
        """
        self.logger.debug(f'saving {len(parsed_data)} items to the database')
        session = self.Session()


        try:

            # get already existing items
            already_existing = session \
                .query(Ad) \
                .filter(
                Ad.id.in_([item.id for item in parsed_data])
            ) \
                .all()

            existing_ids = [item.id for item in already_existing]
            self.logger.debug(f'..{len(existing_ids)} items already exist on the database')
            print('****')
            print(existing_ids)
            print([item.id for item in parsed_data])

            items_to_save = [item for item in parsed_data if item.id not in existing_ids]
            self.logger.info(f'..saving only {len(items_to_save)} items from file {self.file_name}')

            session.add_all(items_to_save)
            session.commit()
        except Exception:
            session.rollback()
            self.logger.error(Exception)
            raise
        finally:
            session.close()


    def run(self):

        # 1. open file from S3
        html_content = self.open(self.file_name)

        # 2. parse
        parsed_data = self.parse_doc(content=html_content)

        # 3. save to db
        self.save_to_db(parsed_data)



if __name__ == '__main__':
    file_name = 'ac1b8e__20181216_165518__PAP'
    ParserPAP(
        file_name=file_name
    ).run()