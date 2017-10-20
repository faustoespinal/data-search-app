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

idCounter = 101
contentPath = sys.argv[1]
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
            drName = 'Unknown'
            for wIdx in range(0,len(words)):
                w = words[wIdx]
                if w.lower().startswith('dr.'):
                    drName = w + ' ' + words[wIdx+1]
                    print('DrName=',drName)

            doc = {
                'author': drName,
                'text': data,
                'timestamp': datetime.now(),
            }
            res = es.index(index="clinical-data-index", doc_type='radiology-report', id=idCounter, body=doc)
            # res = {
            #     'created' : False
            # }
            print('Created radiology report:', res['created'])
            idCounter = idCounter + 1
            #print(data)
            print('=======================================')


es.indices.refresh(index="clinical-data-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

