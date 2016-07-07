from flask import Flask
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings                         #this function automatically loads the setting in settings.py function
import json
from celery import Celery

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)



#In settings.py, the JsonWriterPipeline has been activated by commenting out the required lines in settings.py
    

def getConfigData():                     #reads the data from the configuration file config.json                    
    with open('config.json') as dataFile:
        data = json.load(dataFile)
    return data

@celery.task()
def crawlWebsiteForItem(item,siteName):
    data = getConfigData()
    siteInfo = None
    for site in data["sites"]:
        if site["site_name"] == siteName:
            siteInfo = site
            break
    process = CrawlerProcess(get_project_settings())                              #creating a process to call a spider with needed setting
    process.crawl('shopper', item,siteInfo)                                     #schedulespider named shopper and search for the item
    process.start()

@app.route('/test')
def tester_function():                                   # function to test various new added features during development phase. To be removed in final product
    #data = getConfigData()
    #siteInfo = data["sites"][0]
    #process.crawl('shopper', item = 'stereo', siteInfo = siteInfo)       #schedulespider named shopper and search for the item
    #siteInfo = data["sites"][1]
    #process.crawl('shopper', item = 'bread', siteInfo = siteInfo)
    #process.start()                                                     #start the process. Once the process is done the item searched for and the prices from foodplus.co.ke are stored in items.jl as defined in the item pipeline file called pipelines.py
    crawlWebsiteForItem.apply_async(args = ["stereo","kilimall"])
    crawlWebsiteForItem.apply_async(args = ["bread","foodplus"])
    #return "Value = %s" % a.wait()
    return "wow"

@app.route('/shop')                                  #rule to test if spider is working
def hello_world():
    data = getConfigData()
    siteInfo = data["sites"][0]
    process.crawl('shopper', item = 'bread', siteInfo = siteInfo)       #schedulespider named foosplus and search for the item bread
    process.start()                                                     #start the process. Once the process is done the item searched for and the prices from foodplus.co.ke are stored in items.jl as defined in the item pipeline file called pipelines.py
    return "wow"


if __name__ == '__main__':
   app.run(debug = True)
