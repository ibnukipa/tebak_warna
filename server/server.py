import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
class ClientChannel(PodSixNet.Channel.Channel):
	def Network(self, data):
		print data
	def Network_place(self, data):
		x = data["x"]
		y = data["y"]
		x2 = data["x2"]
		y2 = data["y2"]
		num = data["num"]
		self.gameid = data["gameid"]

		#cek jika client berhasil menyamakan kotak
		if x >=0:
			self._server.placeKotak(x, y, x2, y2, data, self.gameid, num)
		else:
			self._server.gantiTurn(self.gameid, num)

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

	def placeKotak(self, x, y, x2, y2, data, gameid, num):
		game = [a for a in self.games if a.gameid==gameid]
		if len(game)==1:
			game[0].placeKotak(x, y, x2, y2, data, num)

	def gantiTurn(self, gameid, num):
		game = [a for a in self.games if a.gameid==gameid]
		
		if len(game)==1:
			game[0].gantiTurn(num)
			
class Game:
	def __init__(self, player0, currentIndex):
		self.turn = 0
		self.kotak=[[False for x in range(6)] for y in range(6)]
		self.player0=player0
		self.player1=None
		self.gameid=currentIndex
#membuat server
host, port="localhost", 8000
boxesServe=BoxesServer(localaddr=(host, int(port)))
if (boxesServe):
	print "Server on: ", host, ":", port
	
while True:
	boxesServe.Pump()
	sleep(0.01)