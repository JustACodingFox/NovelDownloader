import os.path

from ebooklib import epub


class EpubPipeline:

    def __init__(self):
        # create book
        self.book = epub.EpubBook()

    def process_item(self, item, spider):
        """Write the chapter to the Epub, which was created from the constructor"""
        # prepare stuff for chapter
        title = item['title']
        file_name = title.lower().replace(' ', '')

        # create chapter
        chapter = epub.EpubHtml(title=title, file_name=file_name, lang='en')
        title_html = '<h1>' + title + '</h1>'
        chapter.set_content(title_html + item['content'])

        # add chapter to book
        self.book.add_item(chapter)
        self.book.spine.append(chapter)
        self.book.toc.append(chapter)
        return item

    def close_spider(self, spider):
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
        path = spider.book_name.replace(' ', '') + '.epub'
        path = os.path.join('Output', path)
        epub.write_epub(path, self.book)
