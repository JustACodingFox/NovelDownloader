import sys

from PySide2.QtWidgets import QDialog, QComboBox, QPushButton, QApplication, QFormLayout, QLineEdit
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from data.file_types import FileTypes
from data.hosts import Hosts

# define dialog dimensions
DIALOG_HEIGHT = 280
DIALOG_WIDTH = DIALOG_HEIGHT * 16 / 9


class CustomDialog(QDialog):

    def __init__(self):
        super(CustomDialog, self).__init__()
        self.setWindowTitle("Novel Downloader")
        self.resize(DIALOG_WIDTH, DIALOG_HEIGHT)

        # create widgets
        name_edit = QLineEdit()
        author_edit = QLineEdit()
        link_edit = QLineEdit()
        self.host_selector = QComboBox()
        self.file_selector = QComboBox()
        self.fill_selectors()
        self.download_button = QPushButton('Download Novel')
        self.download_button.clicked.connect(
            lambda: self.download(name_edit.text(), author_edit.text(), link_edit.text(),
                                                              self.host_selector.currentText(),
                                                              self.file_selector.currentText()))

        # set layout
        form_layout = QFormLayout()
        form_layout.addRow(self.tr('&Name'), name_edit)
        form_layout.addRow(self.tr('&Author'), author_edit)
        form_layout.addRow(self.tr('&Link(First Chapter)'), link_edit)
        form_layout.addRow(self.tr('&Host'), self.host_selector)
        form_layout.addRow(self.tr('&Output File'), self.file_selector)
        form_layout.addRow(self.download_button)
        form_layout.setVerticalSpacing(20)
        self.setLayout(form_layout)

    def fill_selectors(self):
        for type in FileTypes:
            self.file_selector.addItem(type.value)
        for host in Hosts:
            self.host_selector.addItem(host.value)

    def download(self, name, author, link, host, file):
        # block the button
        self.download_button.setText('Downloading')
        self.download_button.setCheckable(False)

        process = CrawlerProcess(get_project_settings())
        if host == Hosts.WUXIAWORLD.value:
            process.crawl('wuxia', name=name, author=author, link=link, file_type=file)

        process.start()

        # unblock button
        self.download_button.setText('Download Novel')
        self.download_button.setCheckable(True)


if __name__ == '__main__':
    app = QApplication()
    view = CustomDialog()
    view.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
