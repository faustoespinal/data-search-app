import os
import sys
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['3.28.94.22'],
    http_auth=('elastic','changeme'),
    port=80,
    headers={
        'X-Host-Override' : 'elasticsearch.edison',
        'Host' : 'elasticsearch.edison'
    },
    use_ssl=False
)

institutions = ['Sports Institute', 'Research Institute', 'FC Institute', 'ABC Institute', 'XYZ Institute']
locations = ['40.7128, 74.0060', '34.0522, 118.2437', '41.8781, 87.6298', '48.8566, 2.3522', '39.9042, 116.4074']

indexDef = {
  'mappings': {
      'entry-type' : {
          'properties' : {
                'id' : {
                    'type' : 'integer'
                },
                'timestamp' : {
                    'type' : 'date'
                },
                'institution' : {
                    'type' : 'string',
                    'analyzer' : 'keyword'
                },
                'author' : {
                    'type' : 'string'
                },
                'tags' : {
                    'type' : 'string'
                },
                'content' : {
                    'type' : 'text'
                },
                'location' : {
                    'type' : 'geo_point'
                }
          }
      }
  }
}
index_name = 'rad-data-index'
es.indices.create(index=index_name,body=indexDef)

idCounter = 101
contentPath = sys.argv[1]
idx = 0
for root, directories, filenames in os.walk(contentPath):
    # for directory in directories:
    #     print(os.path.join(root, directory) )
    for filename in filenames: 
        if filename.endswith('.txt'):
            filePath = os.path.join(root,filename)
            print(filePath)
            with open(filePath, 'r') as myfile:
                data=myfile.read()  #.replace('\n', '')
                myfile.close()
            
            words = data.split(' ')
            author = 'Author unknown'

            doc = {
                'author': author,
                'content': data,
                'timestamp': datetime.now(),
                'institution': institutions[idx],
                'location' : locations[idx],
                'tags' : 'radiology, open-source'
            }
            idx = (idx+1) % len(locations)
            res = es.index(index=index_name, doc_type='rad-report', id=idCounter, body=doc)
            print('Created radiology report:', res['created'])
            idCounter = idCounter + 1
            #print(data)
            print('=======================================')


es.indices.refresh(index=index_name)

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

