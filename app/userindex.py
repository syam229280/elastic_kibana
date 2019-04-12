from faker import Faker
from faker.providers import address
from faker.providers import job
from faker.providers import company
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk

index_body = '''{
    "mappings": {
        "users" : {
          "properties" : {
             "name": {
                "type": "keyword"
              },
              "company": {
                "type": "keyword"
              },
              "job": {
                "type": "keyword"
              },
              "address": {
                "type": "keyword"
              },
              "city": {
                "type": "completion"
              }
          }
        }
    }
}'''
config = [{'host': 'elasticsearch', 'port': '9200'}]
es = Elasticsearch(config)
es.indices.create(index='users', body=index_body, ignore=400)

fake = Faker()
fake.add_provider(address)
fake.add_provider(job)
fake.add_provider(company)

def generateUsers():   
    for _ in range(100000):
        yield {
            "_index": "users",
            "_type": "users",
            "_source": {
                'name' : fake.name(),
                'company' : fake.company(),
                'job' : fake.job(),
                'address' : fake.address(),
                'city' : fake.city()
            }
        }

bulk(es, generateUsers())      

# search query
# GET users/_search
# {
#     "suggest": {
#         "city-suggest" : {
#             "prefix" : "tama", 
#             "completion" : { 
#                 "field" : "city",
#                 "fuzzy" : {
#                     "fuzziness" : 1
#                 },
#                 "size" : 15,
#                 "skip_duplicates" : true
#             }
#         }
#     }
# }
        
