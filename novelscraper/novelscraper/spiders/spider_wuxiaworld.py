import scrapy

from ..items import BookItem


class SpiderWuxiaWorld(scrapy.Spider):
    name = 'wuxia'

    def __init__(self, *args, **kwargs):
        super(SpiderWuxiaWorld, self).__init__(*args, **kwargs)

        # set url
        self.start_urls = [kwargs.get('link')]

        # set name
        if kwargs.get('name'):
            self.book_name = kwargs.get('name')
        else:
            self.book_name = 'unknown'

        # set file type attribute
        self.file_type = kwargs.get('file_type')

        print("Spider created")

    def parse(self, response):
        # get title of the chapter
        chapter_title = response.xpath('//div[@class="caption clearfix"]').css('h4::text').get()

        # get the content of the chapter and save it as a list of lines
        content = response.xpath('//div[@class="caption clearfix"]/following::div[@class="fr-view"]')
        list_of_lines = content.css('p::text').getall()

        # save the title and content as a scrapy item
        item = BookItem()
        item['chapter_title'] = chapter_title
        item['chapter_content'] = list_of_lines
        yield item

        # follow next page
        next_page = response.xpath('//li[@class="next"]/a/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
