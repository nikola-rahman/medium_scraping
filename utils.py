import requests


def download_page(url):
    response = requests.get(url, allow_redirects=True)
    assert response.ok
    html = response.content

    return html


def get_ymd(date):
    year = date.year
    month = date.month
    day = date.day

    return year, month, day