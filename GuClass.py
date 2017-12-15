from udpwkpf import WuClass, Device
import sys
import socket
from udpwkpf_io_interface import *
from twisted.internet import reactor
import json

if __name__ == "__main__":
    class GuClass(WuClass):
        def __init__(self):
            WuClass.__init__(self)
            self.loadClass('GuClass')
            self.numLots = 2
	    self.numEmpty = 2
            self.empty = "1 2 "
	    self.numOccupied = 0
	    self.lots = [0, 0]
	    self.tmp = 0

            self.light_actuator_gpio_R = pin_mode(11, PIN_TYPE_DIGITAL, PIN_MODE_OUTPUT)
            self.light_actuator_gpio_G = pin_mode(12, PIN_TYPE_DIGITAL, PIN_MODE_OUTPUT)
            self.light_actuator_gpio_B = pin_mode(13, PIN_TYPE_DIGITAL, PIN_MODE_OUTPUT)
            digital_write(self.light_actuator_gpio_R, 0)
            digital_write(self.light_actuator_gpio_G, 1)
            digital_write(self.light_actuator_gpio_B, 0)

            try:
                #create an AF_INET, STREAM socket (TCP)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except socket.error, msg:
                print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
                sys.exit();             
            print 'Socket Created'

            #Send some data to remote server
            HOST, PORT = "10.5.0.89", 9999
            send_data = {'Location':1, 'Lots':self.numLots, 'Empty':self.empty}
            send_data = json.dumps(send_data)
            (self.sock).sendto(send_data + "\n", (HOST, PORT))
            print "Sent:     {}".format(str(send_data))
            
            receive_data = (self.sock).recv(1024)
            print "Received: {}".format(receive_data)

        def update(self,obj,pID=None,val=None):
            try:
	        # location/Lot in/NUM_lot/NUM_empty/Num_occupied/refresh_rate
		# id=> parking lot id / (Empty = 0 Occupied = 1)
		self.numLots = obj.getProperty(2)
		self.tmp = obj.getProperty(1)

                is_occupied = self.tmp % 10
                parking_id = self.tmp / 10
		if is_occupied == 1 :
		    if self.lots[parking_id - 1] == 0 :
			self.lots[parking_id - 1] = 1
			self.numOccupied = self.numOccupied + 1
			print "%s occupied!" % parking_id
		elif is_occupied == 0 :
		    if(self.lots[parking_id - 1] == 1):
			self.lots[parking_id - 1] = 0
			self.numOccupied = self.numOccupied - 1
                        print "%s empty." % parking_id
		self.numEmpty = self.numLots - self.numOccupied
		#obj.setProperty(3,self.numEmpty)
		#obj.setProperty(4,self.numOccupied)
                if self.numEmpty==0:
                    digital_write(self.light_actuator_gpio_R, 1)
                    digital_write(self.light_actuator_gpio_G, 0)
                    digital_write(self.light_actuator_gpio_B, 0)
                else:
                    digital_write(self.light_actuator_gpio_R, 0)
                    digital_write(self.light_actuator_gpio_G, 1)
                    digital_write(self.light_actuator_gpio_B, 0)

                self.empty = ""
                for n in range(0, 2):
                    if self.lots[n] == 0:
                        self.empty += str(n + 1)
                        self.empty += " "

                if self.empty == "" :
                    self.empty = "none"

                #Send some data to remote server
                HOST, PORT = "10.5.0.89", 9999
                send_data = {'Location':1, 'Lots':self.numLots, 'Empty':self.empty}
                send_data = json.dumps(send_data)
                (self.sock).sendto(send_data + "\n", (HOST, PORT))
                print "Sent:     {}".format(str(send_data))
                
                receive_data = (self.sock).recv(1024)
                print "Received: {}".format(receive_data)
                 
            except IOError:
                print ("Error")

    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            cls = GuClass()
            self.addClass(cls,0)
            self.addObject(cls.ID)

    if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
