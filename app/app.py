from flask import Flask
from elasticsearch import Elasticsearch
from flask import jsonify
import logging
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    config = [{'host': 'elasticsearch', 'port': '9200'}]
    es = Elasticsearch(config)
    if not es.ping():
        print('Elastic not available')
        raise Exception('Cannot initialize elastic search')

    try:
        query_type  = request.args.get('q')
        if query_type=='all':
            fields =[]
        else:
            fields = ['hits.hits._id', 'hits.hits._source.log_type', 'hits.hits._source.message']
      
        data = es.search(index='logs*', filter_path=fields)
    except Exception as e:
        return str(e)
    
   
    
    if data:
        return jsonify(data)

    return 'No results'

if __name__ == '__main__':
    logging.basicConfig(filename='logs/error_log',level=logging.DEBUG)
    app.run(debug=True,host='0.0.0.0')
