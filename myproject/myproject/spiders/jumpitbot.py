from scrapy import Request, Spider
import math, json
import requests
from urllib.parse import urljoin, urlparse

JUMPIT_DATA_NUM = 16

class ProgrammersSpider(Spider):
    name = 'jumpitbot'
    allowed_domains = ['jumpit.co.kr']
    start_urls = ['https://www.jumpit.co.kr']

    async def parse(self, response):
        page_num = 1
        data = requests.get('https://www.jumpit.co.kr/api/positions').json()

        total_page = math.ceil(data['result']['totalCount'] / 16)
        last_page_company_num = data['result']['totalCount'] % 16

        while page_num <= total_page:
            if page_num == total_page:
                content_num = last_page_company_num
            else:
                content_num = JUMPIT_DATA_NUM
            positions_api = urljoin(response.url, f"/api/positions?page={page_num}")
            page_num += 1
            yield Request(positions_api, callback=self.getStacksByComapny, meta={'content_num': content_num})


    async def getStacksByComapny(self, response):
        companies_data = requests.get(response.url).json()
        content_num = response.meta['content_num']
        for data in range(content_num):
            company = companies_data['result']['positions'][data]
            item = {
                'id': company['id'],
                'logo': company['logo'],
                'companyName': company['companyName'],
                'techStacks': company['techStacks'],
                'locations': company['locations']
            }
            yield item
        


