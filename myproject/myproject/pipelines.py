# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from collections import defaultdict
import json

jumpit_file_path = './data/jumpit.json'

class JumpitPipeline(object):
    """
    Pipeline used for jumpitbot
    """

    def open_spider(self, spider):
        self.json_response = defaultdict()
    
    def close_spider(self, spider):
        for k in self.json_response:
            self.json_response[k]['techStacks'] = list(set(self.json_response[k]['techStacks']))

        with open(jumpit_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.json_response, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        if str(item["id"]) in self.json_response:
            for tech in item["techStacks"]:
                self.json_response[str(item["id"])]["techStacks"].append(tech)
        else:
            self.json_response[str(item["id"])] = {
                "companyName": "",
                "techStacks": [],
                "logo": "",
                "locations": []
            }
            self.json_response[str(item["id"])]["companyName"] = item["companyName"]
            self.json_response[str(item["id"])]["techStacks"] += item["techStacks"]
            self.json_response[str(item["id"])]["logo"] = item["logo"]
            self.json_response[str(item["id"])]["locations"] += item["locations"]

        return item