from housing.Scrapper import Scrapper


class SeLoger(Scrapper):

    def __init__(self):
        super(SeLoger, self).__init__()
        self.url = "https://www.seloger.com/list.htm?types=1,2&projects=2&enterprise=0&natures=1,2,4&price=NaN/450000&surface=45/NaN&bedrooms=2&places=[{cp:75}|{ci:920050}|{ci:920026}|{ci:920062}|{ci:920063}|{ci:780146}]&qsVersion=1.0&abSLC=new"

    def run(self):
        super(SeLoger, self).run()
        print("And the I am running SeLoger")

if __name__ == "__main__":
    scrapper = SeLoger()
    scrapper.run()
