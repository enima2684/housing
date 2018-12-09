from housing.Scrapper import Scrapper


class PAP(Scrapper):

    def __init__(self):
        super(PAP, self).__init__()

    def run(self):
        super(PAP, self).run()
        print("And the I am running PAP")

if __name__ == "__main__":
    scrapper = PAP()
    scrapper.run()
