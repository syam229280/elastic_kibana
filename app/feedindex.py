import feedparser
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk

config = [{'host': 'elasticsearch', 'port': '9200'}]
es = Elasticsearch(config)
es.indices.create(index='news', ignore=400)
  
def getFeeds():
    feeds = [
        'https://timesofindia.indiatimes.com/rssfeeds/1221656.cms',
        'https://timesofindia.indiatimes.com/rssfeeds/5880659.cms',
        'https://timesofindia.indiatimes.com/rssfeeds/2647163.cms',
        'http://www.espn.com/espn/rss/news',
        'https://www.thehindu.com/news/feeder/default.rss',
        'https://zeenews.india.com/rss/india-national-news.xml',
        'https://www.indiatvnews.com/rssnews/topstory-india.xml'
    ]
    return feeds  
   
def generateNews(): 
    feeds = getFeeds()   
    for feed in feeds:
        data = feedparser.parse(feed)
        for post in data.entries:
            yield {
                "_index": "news",
                "_type": "news",
                "_source": {
                    'title' : post.title,
                    'summary' : post.summary
                }
            }
        

bulk(es, generateNews())  
