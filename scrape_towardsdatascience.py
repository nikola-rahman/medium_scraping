from joblib import Parallel, delayed

import pandas as pd

from medium_crawler import MediumArchiveCrawler
from medium_article_scraper import MediumArticleScraper
# from medium_article_dataset import MediumArticleDataset

if __name__ == '__main__':
    df = pd.DataFrame()
    loop = Parallel(n_jobs=16)
    for date_ in pd.date_range(start='2022-01-01', end='2022-01-01'):
        crawler = MediumArchiveCrawler(date_)
        crawler.get_article_urls()
        # articles = []
        # for article_url in crawler.article_urls:
        #     article = MediumArticleScraper(article_url)
        #     article.get_data()
        #     articles.append(article.data)
        scrapers = [MediumArticleScraper(url) for url in crawler.article_urls]
        articles = loop(delayed(scraper.get_data)() for scraper in scrapers)
        df = df.append(pd.concat(articles, ignore_index=True), ignore_index=True)

    print(df)