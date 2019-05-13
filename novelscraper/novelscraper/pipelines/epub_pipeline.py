# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os.path
import sys

sys.path.append('..')

from ebooklib import epub

from data.file_types import FileTypes


class EpubPipeline():

    def __init__(self):
        # create book
        self.book = epub.EpubBook()
        self.create_book = True


    def process_item(self, item, spider):
        """Write the chapter to the Epub, which was created from the constructor"""

        if not self.create_book:
            return item

        # if the file type is not doxc skip this pipeline
        if spider.file_type != FileTypes.EPUB.value:
            self.create_book = False
            return item

        # add linebreak to the lines and join them to a string
        list_of_lines = item['chapter_content']
        list_of_lines = map(lambda x: '<p>' + x + '</p>', list_of_lines)
        chapter_content = ''.join(list_of_lines)

        # prepare stuff for chapter
        title = item['chapter_title']
        f_name = title.lower().strip()

        # create chapter
        chapter = epub.EpubHtml(title=title, file_name=f_name, lang='en')
        title_html = '<h1>' + title + '</h1>'
        chapter.set_content(title + chapter_content)

        # add chapter to book
        self.book.add_item(chapter)
        self.book.spine.append(chapter)
        self.book.toc.append(chapter)
        return item


    def close_spider(self, spider):
        # do not create the book if it should not be created
        if not self.create_book:
            return

        # set metadata
        self.book.set_identifier(spider.book_name)
        self.book.set_title(spider.book_name)
        self.book.set_language('en')
        try:
            self.book.add_author(spider.author)
        except AttributeError:
            self.book.add_author("Unknown")

        self.book.spine.append('nav')

        # add navigation elements
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        # create ebook
        path = spider.book_name.strip() + '.epub'
        path = os.path.join('Output', 'Epub', path)
        epub.write_epub(path, self.book)
