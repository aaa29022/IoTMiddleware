#edit.py
import requests
import sys
import string
fd = open("log" , "r+", 0)
nodeid = fd.read()
#print nodeid.split(" ")[3]
loc = sys.argv[1]

r = requests.put("http://10.5.0.89:5000/nodes/"+str(nodeid),data={"location":loc})    

