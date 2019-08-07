import scrapy

from data.hosts import Hosts
from ..items import Chapter


class WuxiaWorldSpider(scrapy.Spider):
    name = Hosts.WUXIAWORLD.value

    def __init__(self, *args, **kwargs):
        super(WuxiaWorldSpider, self).__init__(*args, **kwargs)

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
        title = response.xpath('//div[@class="caption clearfix"]').css('h4::text').get()

        # get the content of the chapter
        content = response.xpath('//div[@class="caption clearfix"]/following::div[@class="fr-view"]').get()

        # only modify contents if so wished
        if self.beautify:
            # get the title of the content
            tmp_title = response.xpath(
                '// *[ @ id = "content-container"] / div[4] / div / div[2] / div[1] / div[3] / p[1] / span/text()').get()

            # compare the titles and select the longer one
            try:
                if len(title) < len(tmp_title):
                    title = tmp_title
            except TypeError as e:
                print(e)

            # remove link to previous/next chapter
            element_end = content.rfind('</p>')
            content = content[:element_end + 4]

        # save the title and content as a scrapy item
        item = Chapter()
        item['title'] = title
        item['content'] = content
        yield item

        # follow next page
        next_page = response.xpath('//li[@class="next"]/a/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
