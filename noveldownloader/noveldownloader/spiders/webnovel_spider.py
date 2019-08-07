import scrapy

from data.hosts import Hosts
from ..items import Chapter


class WebnovelSpider(scrapy.Spider):
    name = Hosts.WEBNOVEL.value

    def __init__(self, *args, **kwargs):
        super(WebnovelSpider, self).__init__(*args, **kwargs)

        # set url
        if kwargs.get('link'):
            self.start_urls = [kwargs.get('link')]
        else:
            self.start_urls = []

        # set name
        if kwargs.get('name'):
            self.book_name = kwargs.get('name')
        else:
            self.book_name = 'unknown'
        # set beautify
        if kwargs.get('beautify'):
            self.beautify = kwargs.get('beautify')
        else:
            self.beautify = False

    def parse(self, response):
        # get title of the chapter
        title = response.xpath('//h3/text()').get()

        # get the content of the chapter
        content = response.css('div.cha-words').get()

        # save the title and content as a scrapy item
        item = Chapter()
        item['title'] = title
        item['content'] = content
        yield item
        #
        # # follow next page
        # next_page = response.xpath('//li[@class="next"]/a/@href').get()
        #
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
