
import requests
import bs4
from collections import namedtuple
from django.core.management.base import BaseCommand

from habr_parser.models import Article

InnerBlock = namedtuple('Block', 'author, title, url')


class Block(InnerBlock):
    def __str__(self):
        return f'{self.author}\t{self.title}\t{self.url}'


class HabrParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/99.0.4844.51 Safari/537.36 ',
            'Accept-Language': 'ru',
            }

    def get_page(self):
        url = 'https://habr.com/ru/all/'
        r = self.session.get(url)
        return r.text

    def parse_block(self, item):
        # получение блока author
        author_block = item.select_one('a.tm-user-info__username')
        author = author_block.string.strip()

        # получение блока title
        title_block = item.select_one('h2.tm-article-snippet__title.tm-article-snippet__title_h2 span')
        title = title_block.string.strip()

        # получение блока text
        # text_block = item.select_one('div.article-formatted-body.article-formatted-body_version-2')
        # text = text_block.string.strip()


        # получение блока url
        url_block = item.select_one('a.tm-article-snippet__title-link')
        href = url_block.get('href')
        if href:
            url = 'https://habr.com' + href
        else:
            url = None

        try:
            a = Article.objects.get(url=url)
            a.author = author
            a.title = title
            a.url = url
            a.save()
        except Article.DoesNotExist:
            a = Article(
                author=author,
                title=title,
                url=url,
                ).save()
            print(f'article {a}')

        return Block(
            author=author,
            title=title,
            url=url,
        )

    def get_blocks(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('div.tm-article-snippet')
        for item in container:
            block = self.parse_block(item=item)
            print(block)


class Command(BaseCommand):
    help = 'Парсинг Habr'

    def handle(self, *args, **options):
        a = HabrParser()
        a.get_blocks()

