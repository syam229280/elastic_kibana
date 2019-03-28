from flask import Flask
from elasticsearch import Elasticsearch
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    es = Elasticsearch()
    #data = es.search(index='school'])
    #print(data)
    return 'Flask Docker'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
