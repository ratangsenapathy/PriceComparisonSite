from flask import Flask
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings          #this function automatically loads the setting in settings.py function
import json

app = Flask(__name__)
process = CrawlerProcess(get_project_settings())          #creating a process to call a spider with needed setting
#In settings.py, the JsonWriterPipeline has been activated by commenting out the required lines in settings.py


def getConfigData():                     #reads the data from the configuration file config.json                    
    with open('config.json') as dataFile:
        data = json.load(dataFile)
    return data

@app.route('/test')
def tester_function():                                   # function to test various new added features during development phase. To be removed in final product
    data = getConfigData()
    siteInfo = data["sites"][0]
    process.crawl('shopper', item = 'stereo', siteInfo = siteInfo)       #schedulespider named shopper and search for the item
    #siteInfo = data["sites"][1]
    #process.crawl('shopper', item = 'bread', siteInfo = siteInfo)
    process.start()                                                     #start the process. Once the process is done the item searched for and the prices from foodplus.co.ke are stored in items.jl as defined in the item pipeline file called pipelines.py
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
