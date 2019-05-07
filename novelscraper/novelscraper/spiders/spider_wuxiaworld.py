import scrapy

from ..data.file_types import FileTypes
from ..items import BookItem


class SpiderWuxiaWorld(scrapy.Spider):
    name = 'wuxia'
    custom_settings = {}

    def __init__(self, category=None, *args, **kwargs):
        super(SpiderWuxiaWorld, self).__init__(*args, **kwargs)
        # set url
        self.start_urls = [kwargs.get('link')]
        # set name
        if kwargs.get('name'):
            self.book_name = kwargs.get('name')
        else:
            self.book_name = 'unknown'
        # set custom settings
        self.setPipeline(kwargs.get('file_type'))

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

    def setPipeline(self, file_type):
        if file_type == FileTypes.DOXC:
            self.custom_settings = {
                'ITEM_PIPELINES': {
                    'novelscraper.pipelines.docx_pipeline.DocxPipeline': 100
                }
            }
        elif file_type == FileTypes.EPUB:
            self.custom_settings = {
                'ITEM_PIPELINES': {
                    'novelscraper.pipelines.epub_pipeline.EpubPipeline': 100
                }
            }
        elif file_type == FileTypes.PDF:
            self.custom_settings = {
                'ITEM_PIPELINES': {
                    'novelscraper.pipelines.pdf_pipeline.PDFPipeline': 100
                }
            }
        elif file_type == FileTypes.TXT:
            self.custom_settings = {
                'ITEM_PIPELINES': {
                    'novelscraper.pipelines.txt_pipeline.TxtPipeline': 100
                }
            }
        else:
            self.custom_settings = {
                'ITEM_PIPELINES': {
                }
            }
