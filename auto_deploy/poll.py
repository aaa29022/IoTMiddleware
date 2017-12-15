import requests
import time
id = "f92ea1839dc16d7396db358365da7066"
while 1:
	r = requests.post('http://10.5.0.89:5000/applications/' + id + '/poll')
	print r.text
	time.sleep(2)
