#map.py
import requests,sys
id = sys.argv[1]
r = requests.post('http://10.5.0.89:5000/applications/' + id + '/deploy/map')
print r.text
