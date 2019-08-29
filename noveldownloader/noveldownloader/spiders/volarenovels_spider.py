import scrapy

from data.hosts import Hosts
from ..items import Chapter


class VolareNovelsSpider(scrapy.Spider):
    name = Hosts.VOLARENOVELS.value
    website = 'www.volarenovels.com'

    def __init__(self, *args, **kwargs):
        super(VolareNovelsSpider, self).__init__(*args, **kwargs)

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
        title = response.xpath('//h4[@class=""]//text()').getall()
        title = ''.join(title)
        title = title.strip()

        # get the content of the chapter
        content = response.xpath('//div[@class="jfontsize_content fr-view"]').get()

        # save the title and content as a scrapy item
        item = Chapter()
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item

        # follow next page
        next_page = response.xpath('//div[@class="jfontsize_content fr-view"]/a/@href ').getall()
        next_page = next_page[-1]
        parts = next_page.split('/')
        next_page = parts[-1]

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
