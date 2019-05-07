# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os.path

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer


class PDFPipeline(object):

    def __init__(self):
        self.story = []
        self.content_style = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=12,
        )
        self.heading_style = ParagraphStyle(
            name='Heading',
            fontName='Helvetica-Bold',
            fontSize=16,
        )

    def process_item(self, item, spider):
        """Write the chapter to the story, which was created in the constructor"""

        # print chapter title
        self.story.append(Paragraph(item['chapter_title'], self.heading_style))

        # add space between title and content
        self.story.append(Spacer(1, 1 * cm))

        # add linebreak to the lines and join them to a string
        list_of_lines = item['chapter_content']
        list_of_lines = map(lambda x: x + '<br />\n', list_of_lines)
        chapter_content = ''.join(list_of_lines)

        # print chapter content
        self.story.append(Paragraph(chapter_content, self.content_style))
        self.story.append(PageBreak())

        return item

    def close_spider(self, spider):
        # create empty pdf doc
        path = spider.book_name.strip() + '.pdf'
        path = os.path.join('Output', 'Pdf', path)
        self.doc = SimpleDocTemplate(path)
        # wirte story to pdf
        self.doc.build(self.story)
