from medium_crawler import MediumArchiveCrawler
from medium__article_scraper import MediumArticleScraper
from medium_article_dataset import MediumArticleDataset

if __name__ == '__main__':
    data = MediumArticleDataset()
    for date_ in date_range:
        crawler = MediumArchiveCrawler(date_)
        crawler.get_article_urls()
        for article_url in crawler.article_urls:
            article = MediumArticleScraper(article_url)
            article.get_data()
            # article.download_page()
            # article.parse()
            data.append(article.data)