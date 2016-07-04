from flask import Flask
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings          #this function automatically loads the setting in settings.py function


app = Flask(__name__)
process = CrawlerProcess(get_project_settings())          #creating a process to call a spider with needed setting
#In settings.py, the JsonWriterPipeline has been activated by commenting out the required lines in settings.py

@app.route('/hello')                                  #rule to test if spider is working
def hello_world():
    
    process.crawl('foodplus', item = 'bread')       #schedulespider named foosplus and search for the item bread
    process.start()                                 #start the process. Once the process is done the item searched for and the prices from foodplus.co.ke are stored in items.jl as defined in the item pipeline file called pipelines.py
    return "wow"



if __name__ == '__main__':
   app.run(debug = True)
