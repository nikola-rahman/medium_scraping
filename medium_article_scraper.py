import pandas as pd
from bs4 import BeautifulSoup

from utils import download_page


class MediumArticleScraper:
    def __init__(self, url):
        self.url = url
        self.data = None
        self.page = None

    def get_data(self):
        try:
            data = {}
            data['url'] = [self.url]
            self.page = download_page(self.url)

            self.article = BeautifulSoup(self.page, 'html.parser')
            data['image_cnt'] = len(self.get_all_images())
            data['claps'] = self.get_claps()
            data['author'] = [self.get_author()]
            data['date'] = [self.get_date()]
            data['length_mins'] = [self.get_length()]
            data['title'] = [self.get_title()]
        except Exception as e:
            raise Exception(self.url).with_traceback(e)

        self.data = pd.DataFrame(data)

    def get_all_images(self):
        return self.article.find_all('figure')

    def get_claps(self):
        claps = None
        svgs = self.article.find_all('svg')
        for svg in svgs:
            try:
                aria_label = svg['aria-label']
            except KeyError:
                aria_label = None
            if aria_label == 'clap':
                try:
                    claps = svg.parent.parent.parent.parent.parent.parent.find_all('button')[0].text
                    if 'K' in claps:
                        claps = int(float(claps.split('K')[0]) * 1000)
                    else:
                        claps = int(claps)
                    break
                except IndexError:
                    claps = None
                    break
        return claps

    def get_author(self):
        try:
            author = self.article.find_all('div', class_='db')[1].find('p').text
        except IndexError:
            author = None
        return author

    def get_date(self):
        try:
            date_and_length = self.article.find_all('div', class_='db')[1].find_all('p')[1].text
            date_str = date_and_length.split('·')[0]
            #TODO remove
            return date_str
            if date_str == '':
                date_ = None
            elif 'ago' in date_str: # 6 days ago
                days_ago = int(date_str.split(' ')[0])
                date_ = date.today() - timedelta(days=days_ago)
                date_ = pd.to_datetime(date_)
            elif ',' not in date_str: # Feb 6 -> Feb 6 of the current year
                year = date.today().year
                date_str = f'{date_str}, {year}'
                date_ = pd.to_datetime(date_str, format='%b %d, %Y')
            elif ',' in date_str:
                date_ = pd.to_datetime(date_str, format='%b %d, %Y')
        except IndexError:
            date_ = None

        return date_

    def get_length(self):
        try:
            date_and_length = self.article.find_all('div', class_='db')[1].find_all('p')[1].text
            length = date_and_length.split('·')[1]
            try:
                length = int(length.split(' ')[0])
            except ValueError:
                length = None
        except IndexError:
            length = None

        return length

    def get_title(self):
        try:
            title = self.article.find('h1').text
        except AttributeError:
            title = None

        return title