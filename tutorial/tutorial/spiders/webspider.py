import scrapy

from tutorial.items import FoodPlusItem

class FoodPlusSpider(scrapy.Spider):
    name = "foodplus"                                #spider to scrape foodplus.co.ke
    allowed_domains = ["foodplus.co.ke"]

def __init__(self,item = 'eggs', *args, **kwargs):              #initialize spider with item to be searched
        super(FoodPlusSpider,self).__init__(*args,**kwargs)
        self.start_urls = ['https://www.foodplus.co.ke/catalogsearch/result/?q=%s' % item]
        
    def parse(self, response):
        for sel in response.xpath('//div[@class="name-price"]'):
            item = FoodPlusItem()
            item['productName'] = sel.xpath('h2[@class="product-name"]/a/text()')[0].extract()                   #get product name
            item['price']       = sel.xpath('div[@class="price-box"]/span/span/text()')[0].extract()            #get price of product
            yield item

        next_page = response.xpath('//div[@class = "pages"]/ol/li/a/attribute::href')                           #find the link to the next page if available
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url,self.parse)                                                            #redirect to the next page if more products are there
