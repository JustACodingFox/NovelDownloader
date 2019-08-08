from string import Template

import scrapy

from data.hosts import Hosts
from ..items import Chapter


def extract_ids(meta_data):
    book_id, next_chapter_id = None, None
    for line in meta_data.split('\n'):
        line = line.strip()
        if line.startswith(WebnovelSpider.attr_next_chapter_id):
            parts = line.split(' ')
            next_chapter_id = parts[2]
            next_chapter_id = next_chapter_id[1:-2]
        if line.startswith(WebnovelSpider.attr_book_id):
            parts = line.split(' ')
            book_id = parts[2]
            book_id = book_id[1:-2]
        if book_id and next_chapter_id:
            break
    return book_id, next_chapter_id


class WebnovelSpider(scrapy.Spider):
    name = Hosts.WEBNOVEL.value
    attr_book_id = 'g_data.bookId'
    attr_next_chapter_id = 'g_data.nextcId'

    def __init__(self, *args, **kwargs):
        super(WebnovelSpider, self).__init__(*args, **kwargs)

        # set url
        if kwargs.get('link'):
            self.start_urls = [kwargs.get('link')]
        else:
            self.start_urls = []

        # set template url
        self.url_template = Template('https://www.webnovel.com/book/$bookid/$chapterid')

        # set name
        if kwargs.get('name'):
            self.book_name = kwargs.get('name')
        else:
            self.book_name = 'unknown'

    def parse(self, response):
        meta_info = response.xpath('/html/body/script[7]/text()').get()
        book_id, next_chapter_id = extract_ids(meta_info)

        # get title of the chapter
        title = response.xpath('//h3/text()').get()

        # get the content of the chapter
        content = response.css('div.cha-words').get()

        # save the title and content as a scrapy item
        item = Chapter()
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item

        # follow next page
        next_page = self.url_template.substitute(bookid=book_id, chapterid=next_chapter_id)

        if int(book_id) and int(next_chapter_id) > -1:
            yield response.follow(next_page, callback=self.parse)
