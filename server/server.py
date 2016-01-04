import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data

class BoxesServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel
 
    def Connected(self, channel, addr):
        print 'new connection:', channel

#membuat server
host, port="localhost", 8000
boxesServe=BoxesServer(localaddr=(host, int(port)))
if (boxesServe):
	print "Server on: ", host, ":", port
	
while True:
	boxesServe.Pump()
	sleep(0.01)