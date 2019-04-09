from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk

config = [{'host': 'elasticsearch', 'port': '9200'}]
index_body = {
  "mapping": {
    "news_likes": {
      "properties": {
        "news": {
          "type": "text",
        },
        "user": {
          "type": "long"
        }
      }
    }
  }
}
es = Elasticsearch(config)
es.indices.create(index='news_likes', body=index_body, ignore=400)

user_ids = range(1,1000)

def getRandomNews(user_id):
    body = {
        "size": 20,
        "_source": "_id", 
        "query": {
            "function_score": {
                "functions": [
                    {
                        "random_score": {
                            "seed": user_id
                        }
                    }
                ]
            }
        }
    }
    data = es.search(index='news', body=body, filter_path=['hits.hits._id'])
    news = data['hits']['hits']
    news_ids = [d['_id'] for d in news]
    return news_ids


def generateLikes():
    for user in user_ids:
        news = getRandomNews(user)
        yield {
                "_index": "news_likes",
                "_type": "likes",
                "_source": {
                    'user' : user,
                    'news' : news
                }
            }

bulk(es, generateLikes())            
