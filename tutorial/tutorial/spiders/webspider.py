import scrapy

from tutorial.items import ShoppingItem

class ShoppingSpider(scrapy.Spider):
    name = "shopper"

    def __init__(self,item = 'eggs',siteInfo = None,*args, **kwargs):              #initialize spider with item to be searched
        super(ShoppingSpider,self).__init__(*args,**kwargs)
        self.allowed_domains = [siteInfo["domain"]]
        self.start_urls = [siteInfo["start_url"] % item]
        self.siteInfo = siteInfo
        
    def parse(self, response):
        for sel in response.xpath(self.siteInfo["parent_selector"]):
            item = ShoppingItem()
            item['productName'] = sel.xpath(self.siteInfo["product_name_selector"])[0].extract()                   #get product name
            item['price']       = sel.xpath(self.siteInfo["price_selector"])[0].extract()            #get price of product
            yield item

        next_page = response.xpath(self.siteInfo["next_page_selector"])                           #find the link to the next page if available
        if next_page:
            url = response.urljoin(next_page[int(self.siteInfo["next_page_index"])].extract())
            yield scrapy.Request(url,self.parse)                                                            #redirect to the next page if more products are there
