# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class StackspiderPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        return item

class MongoDBPipeline:
    def __init__(self):
        connection = MongoClient(
            host=settings['MONGODB_SERVER'],
            port=settings['MONGODB_PORT']
        )

        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        return item
