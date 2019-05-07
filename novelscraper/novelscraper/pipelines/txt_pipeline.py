# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os.path

class TxtPipeline():

    def __init__(self):
        # make the book title an argument
        self.chapter_list = []


    def process_item(self, item, spider):
        """Append the chapter to a list, which was created in the constructor"""

        # add linebreak to the lines and join them to a string
        list_of_lines = item['chapter_content']
        list_of_lines = map(lambda x: x + '\n', list_of_lines)
        chapter_content = ''.join(list_of_lines)

        # chapter sting
        chapter_string = item['chapter_title'] + '\n' + chapter_content + '\n \n \n \n'
        self.chapter_list.append(chapter_string)
        return item

    def close_spider(self, spider):
        # open txt file
        path = spider.book_name.strip() + '.txt'
        path = os.path.join('Output', 'Txt', path)
        self.file = open(path, 'w')

        # write to txt file
        book_string = "".join(self.chapter_list)
        self.file.write(book_string)

        # close file
        self.file.close()
