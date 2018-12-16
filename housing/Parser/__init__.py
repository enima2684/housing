from sqlalchemy.orm import sessionmaker

from housing.HousingModule import HousingModule
from housing.models import db_connect, create_tables
from housing.models.Record import Record, WebSites
from housing.Parser.ParserPAP import ParserPAP

class Parser(HousingModule):

    def __init__(self):
        super(Parser, self).__init__()

        # setup db
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)


    def run(self):

        # 1. get non processed files
        session = self.Session()
        try:
            records = session.query(Record).filter(Record.processed == False).all()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

        # 2. run the correct parser for each record

        for record in records:
            if record.web_site is WebSites.PAP:
                ParserPAP(file_name=record.file_name).run()
                record.processed = True


            if record.web_site is WebSites.SeLoger:
                print('SE LOGER PARSER PLACEHOLDER')


        # 3. resave the status of the files
        session = self.Session()
        try:
            session.add_all(records)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


if __name__ == '__main__':
    parser = Parser()
    parser.run()
