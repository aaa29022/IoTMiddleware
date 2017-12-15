import SocketServer
import json
class MyUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
	d = json.loads(data)
        socket = self.request[1]
        print "from gateway {} :".format(self.client_address[0])
        print "Location:"+str(d['Location'])
        print "Total #:"+str(d['Lots'])
        print "Empty #:"+str(d['Empty'])
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "10.5.0.89", 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
