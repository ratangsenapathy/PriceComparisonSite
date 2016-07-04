from flask import Flask
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


app = Flask(__name__)
process = CrawlerProcess(get_project_settings())

@app.route('/hello')
def hello_world():
    
    process.crawl('foodplus', item = 'bread')
    process.start()
    return "wow"


@app.route('/test')
def test_world():
    return "little"

if __name__ == '__main__':
   app.run(debug = True)
