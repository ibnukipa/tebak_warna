import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data

class BoxesServer(PodSixNet.Server.Server):
 	def __init__(self, *args, **kwargs):
		PodSixNet.Server.Server.__init__(self, *args, **kwargs)
		self.games = []
		self.queue = None
		self.currentIndex=0
	
	channelClass = ClientChannel
 
	def Connected(self, channel, addr):
		print 'new connection:', channel
		if self.queue==None:
			self.currentIndex+=1
			channel.gameid=self.currentIndex
			self.queue=Game(channel, self.currentIndex)
		else:
			channel.gameid=self.currentIndex
			self.queue.player1=channel

			self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
			self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
			self.games.append(self.queue)
			self.queue=None

#membuat server
host, port="localhost", 8000
boxesServe=BoxesServer(localaddr=(host, int(port)))
if (boxesServe):
	print "Server on: ", host, ":", port
	
while True:
	boxesServe.Pump()
	sleep(0.01)