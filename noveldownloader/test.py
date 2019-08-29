from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from data.hosts import Hosts

process = CrawlerProcess(get_project_settings())

process.crawl(Hosts.VOLARENOVELS.value,
              link='https://www.volarenovels.com/novel/transmigrator-meets-reincarnator/tmr-chapter-1',
              name="Transmigrator Meets Reincarnator")
process.crawl(Hosts.VOLARENOVELS.value, link='https://www.volarenovels.com/novel/great-demon-king/gdk-chapter-0',
              name="Great Demon King")
# process.crawl(Hosts.WUXIAWORLD.value, link='https://www.wuxiaworld.com/novel/desolate-era/de-book-1-chapter-1', name="Desolate Era")
# process.crawl(Hosts.WUXIAWORLD.value, link='https://www.wuxiaworld.com/novel/heavenly-jewel-change/hjc-book-1-chapter-1-01', name="Heavenly Jewel Change")
# process.crawl(Hosts.WUXIAWORLD.value, link='https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens/issth-book-1-chapter-1', name="I Shall Seal the Heavens")
# process.crawl(Hosts.WUXIAWORLD.value, link='https://www.wuxiaworld.com/novel/martial-world/mw-chapter-0', name="Martial World")
# process.crawl(Hosts.WUXIAWORLD.value, link='https://www.wuxiaworld.com/novel/skyfire-avenue/sfl-chapter-1', name="Skyfire Avenue")
# process.crawl(Hosts.WUXIAWORLD.value, link='https://www.wuxiaworld.com/novel/terror-infinity/ti-vol-1-chapter-1-1', name="Terror Infinity")
# process.crawl(Hosts.WUXIAWORLD.value, link='https://www.wuxiaworld.com/novel/warlock-of-the-magus-world/wmw-chapter-1', name="Warlock of the Magus World")
# process.crawl(Hosts.WUXIAWORLD.value, link='https://www.wuxiaworld.com/novel/wu-dong-qian-kun/wdqk-chapter-1', name="Wu Dong Qian Kun")
process.start()  # the script will block here until the crawling is finished
