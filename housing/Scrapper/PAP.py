from bs4 import BeautifulSoup
import requests
import time

from housing.Scrapper import Scrapper



class PAP(Scrapper):

    def __init__(self):
        super(PAP, self).__init__()
        self.base_url = "https://www.pap.fr/annonce/vente-appartements-paris-75-g439g39154g43265g43294g43298g43301-3-pieces-jusqu-a-550000-euros-a-partir-de-45-m2"
        self.web_site = "PAP"

    def generate_urls(self, number_pages):
        """
        Generates PAP urls for each page
        :param number_pages:
        :return:
        """
        self.logger.debug(f'generating urls for PAP')
        urls = [(
            self.base_url if page == 1 else self.base_url + f'-{page}'
         )
            for page in range(1, int(number_pages)+1)
        ]

        return urls

    def get_number_pages(self):
        """
        Gets the number of pages to fetch
        :return:
        """
        self.logger.info("Getting the number of pages")

        # initialize
        response = requests.get(self.base_url)
        if response.status_code != 200:
            raise ConnectionRefusedError('Refused connection to {}'.format(self.base_url))
        html_content = response.text
        soup = BeautifulSoup(html_content, 'lxml')
        page = 1

        stop_criteria = False
        while not stop_criteria:

            # get the last url number in the pagination
            uls = soup.select('.pagination > ul')
            if len(uls) == 3:
                pagination_ul = uls[1]
            elif len(uls) == 2:
                pagination_ul = uls[0] if page == 1 else uls[1]
            else:
                raise ValueError('inhandled number of uls')
            lis = pagination_ul.select('li')
            last_li  = lis[-1].select_one('a')
            page     = last_li.text
            next_url = last_li.get('href')
            self.logger.info(f'next page : {page} on {next_url}')

            # request this page
            time.sleep(10)
            response = requests.get('https://www.pap.fr' + next_url)
            html_content = response.text

            # update stop_criteria

            soup = BeautifulSoup(html_content, 'lxml')
            uls = soup.select('.pagination > ul')
            if len(uls) == 3:
                pagination_ul = uls[1]
            elif len(uls) == 2:
                pagination_ul = uls[0] if page == 1 else uls[1]
            else:
                raise ValueError('inhandled number of uls')
            lis = pagination_ul.select('li')
            last_li  = lis[-1].select_one('a')
            if last_li is None:
                last_li = lis[-1].select_one('span')
            next_page     = last_li.text
            print(next_page, page)
            stop_criteria = (next_page == page)

            # le dernier n'est pas un a mais un span !

        self.logger.info(f'{page} pages to scrap')
        return page



if __name__ == "__main__":
    scrapper = PAP()
    scrapper.run()
