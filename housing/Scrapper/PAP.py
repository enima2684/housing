from housing.Scrapper import Scrapper


class PAP(Scrapper):

    def __init__(self):
        super(PAP, self).__init__()
        self.url = "https://www.pap.fr/annonce/vente-appartements-paris-75-g439g39154g43265g43294g43298g43301-3-pieces-jusqu-a-450000-euros-a-partir-de-45-m2"
        self.web_site = "PAP"

if __name__ == "__main__":
    scrapper = PAP()
    scrapper.run()
