from bs4 import BeautifulSoup

from utils import download_page, get_ymd


class MediumArchiveCrawler:
    def __init__(self, date_):
        self.base_url = 'https://towardsdatascience.com/archive'
        self.date_ = date_
        self.make_url()
        self.page = None
        self.article_urls = []

    def get_article_url(self, article):
        url = article.find_all(recursive=False)[1].find('a')['href']
        url = url.split('?')[0]
        return url

    def make_url(self):
        year, month, day = get_ymd(self.date_)
        self.url = f'{self.base_url}/{year}/{month:02d}/{day:02d}'

    def get_article_urls(self):
        self.page = download_page(self.url)
        soup = BeautifulSoup(self.page, 'html.parser')
        articles = soup.find_all('div', class_='postArticle postArticle--short js-postArticle js-trackPostPresentation js-trackPostScrolls')
        self.article_urls = [self.get_article_url(a) for a in articles]