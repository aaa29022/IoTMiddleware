#deploy.py
import requests
import time,sys
id = sys.argv[1]
r = requests.post('http://10.5.0.89:5000/applications/' + id + '/deploy')
while "Application has been deployed!" not in r.text:
        r = requests.post('http://10.5.0.89:5000/applications/' + id + '/poll')
        print r.text
        time.sleep(2)

