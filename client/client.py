import pygame
import time
from threading import Thread
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


class BoxesGame(ConnectionListener):
	def Network_startgame(self, data):
		self.running=True
		self.num=data["player"]
		self.gameid=data["gameid"]
		self.acak = data["acak"]

	def Network_place(self, data):
		x = data["x"]
		y = data["y"]
		x2 = data["x2"]
		y2 = data["y2"]
		self.kotak[x][y] = True
		self.kotak[x2][y2] = True
		self.hasil.append([x,y])
		self.hasil.append([x2,y2])
		
	def Network_yourturn(self, data):
		self.turn = data["torf"]

	def Network_win(self, data):
		self.me+=1
		
	def Network_lose(self, data):
		self.otherplayer+=1

	def Network_close(self, data):
		exit()

	def __init__(self):
		pass
		#Membuat kotak window dengan pygame
		pygame.init()
		width, height = 390, 490
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Tebak warna")
		self.clock = pygame.time.Clock()
		
		#inisialisasi untuk membuat objek pada board
		#board adalah window yang akan dipakai untuk client(pemain) bermain
		#self.boardh dan self.boardv adalah objek garis pada board
		self.boardh = [[False for x in range(6)] for y in range(7)]
		self.boardv = [[False for x in range(7)] for y in range(6)]
		
		#self.kotak adalah sebgai objek yang akan ditebak.
		self.kotak = [[False for x in range(6)] for y in range(6)]
		#self.hasil adalah array untuk menampung koordinat kotak yang berhasil disamakan oleh client(pemain)
		self.hasil = []	

		#inialisasi untuk koordinat kotak pertama yang diklik client(pemain) 
		self.xpos = -1
		self.ypos = -1

		#inialisasi untuk koordinat kotak kedua yang diklik client(pemain) 
		self.xpos2 = -1
		self.ypos2 = -1
		#inialisasi dari objek2 yang akan dipakai
		self.initGraphics()

		#inialisasi untuk bermain multiplier
		self.turn = True
		self.me=0
		self.otherplayer=0
		self.didiwin=False

		#konek ke server
		host, port="localhost", 8000
		print "Connect to: ", host, ":", port
		self.Connect((host, int(port)))

		#inialisasi untuk status permainan (koordinasi dengan server)
		self.gameid = None
		self.num = None
		self.running = False

		#Membuat layar menunggu untuk client yang pertama konek ke server
		if not self.running:
			thread = Thread(target = self.tunggu())
			thread.start()
		
		#untuk mengecek sudahkah ada musuh yang masuk
		while not self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			connection.Pump()
			self.Pump()
			sleep(0.01)

		if self.num==0:
			self.turn=True
		else:
			self.turn=False
		
	def tunggu(self):
		self.screen.fill(0)
		myfont = pygame.font.SysFont(None, 40)
		
		label = myfont.render("Menunggu musuh..", 1, (255,255,255))

		self.screen.blit(label, (10, 225))
	
		pygame.display.flip()

	def update(self):
		#pengecekan jumlah poin untuk kemenangan
		if self.me+self.otherplayer==18:
			self.didiwin=True if self.me>self.otherplayer else False
			return 1

		connection.Pump()
		self.Pump()
			
		#Membuat game menjadi 60 fps
		self.clock.tick(60)
		
		#Clear layar window
		self.screen.fill(0)
		
		#Membuat garis-garis untuk board
		self.drawBoard()

		#membuat kotak-kotak yang akan menjadi objek yang ditebak
		self.drawMap()

		#membuat bar status pada client
		self.drawHUD()
		
		#Untuk mengecek event quit window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		mouse = pygame.mouse.get_pos()
		
		xpos = int(mouse[0]/64.0)
		ypos = int(mouse[1]/64.0)

		board=self.kotak
		isoutofbounds=False
		try: 
			if not board[ypos][xpos]:
				pass
		except:
			isoutofbounds=True
			pass
		
		if pygame.mouse.get_pressed()[0] and ([xpos, ypos] not in self.hasil) and not isoutofbounds and self.turn==True:
                        
			self.kotak[xpos][ypos]=True
			#cek untuk klik kotak pertama
			if self.xpos <0 and self.ypos <0:
				self.xpos = xpos
				self.ypos = ypos

			#cek untuk klik kotak kedua
			if self.xpos != xpos or self.ypos != ypos:
				if self.xpos2 < 0 and self.ypos2 < 0:
					self.xpos2 = xpos
					self.ypos2 = ypos

		#untuk cek kalo kotak yang udah diklik 2
		if self.xpos >=0 and self.xpos2 >= 0:
			self.kotak[self.xpos][self.ypos]=True
			self.kotak[self.xpos2][self.ypos2]=True
			self.drawMap()
			pygame.display.flip()
			time.sleep(0.3)
			thread = Thread(target = self.cek())
			thread.start()

		#Update screen
		pygame.display.flip()

	def cek(self):
		if not self.acak[self.xpos][self.ypos] == self.acak[self.xpos2][self.ypos2] :
			self.Send({"action": "place", "x":-1, "y":-1, "x2":-1, "y2":-1, "gameid": self.gameid, "num": self.num})
			self.kotak[self.xpos][self.ypos]=False
			self.kotak[self.xpos2][self.ypos2]=False
			self.drawMap()
			self.reset()
		else:
			self.Send({"action": "place", "x":self.xpos, "y":self.ypos, "x2":self.xpos2, "y2":self.ypos2, "gameid": self.gameid, "num": self.num})
			self.hasil.append([self.xpos,self.ypos])
			self.hasil.append([self.xpos2,self.ypos2])
			self.reset()

	def reset(self):
		self.xpos =-1
		self.ypos = -1
		self.xpos2 = -1
		self.ypos2 = -1

	def initGraphics(self):

		self.myfont40 = pygame.font.SysFont(None, 40)
		self.myfont85 = pygame.font.SysFont(None, 85)
		self.myfont20 = pygame.font.SysFont(None, 20)
		
		self.normallinev=pygame.image.load("normalline.png").convert_alpha()
		self.normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90).convert_alpha()
		self.separators=pygame.image.load("separators.png").convert_alpha()
		self.satu=pygame.image.load("warna/1.png").convert_alpha()
		self.dua=pygame.image.load("warna/2.png").convert_alpha()
		self.tiga=pygame.image.load("warna/3.png").convert_alpha()
		self.empat=pygame.image.load("warna/4.png").convert_alpha()
		self.lima=pygame.image.load("warna/5.png").convert_alpha()
		self.enam=pygame.image.load("warna/6.png").convert_alpha()
		self.winningscreen=pygame.image.load("youwin.png").convert_alpha()
		self.gameover=pygame.image.load("gameover.png").convert_alpha()
		self.score_panel=pygame.image.load("score_panel.png").convert_alpha()
		self.redindicator=pygame.image.load("redindicator.png").convert_alpha()
		self.greenindicator=pygame.image.load("greenindicator.png").convert_alpha()

	def drawBoard(self):
		for x in range(6):
			for y in range(7):
				if not self.boardh[y][x]:
					self.screen.blit(self.normallineh, [(x)*64+5, (y)*64])
		for x in range(7):
			for y in range(6):
				if not self.boardv[y][x]:
					self.screen.blit(self.normallinev, [(x)*64, (y)*64+5])
		for x in range(7):
			for y in range(7):
				self.screen.blit(self.separators, [x*64, y*64])

	def drawMap(self):
		for x in range(6):
			for y in range(6):
				if self.kotak[x][y] :
					if self.acak[x][y] == 0:
						self.screen.blit(self.satu, (x*64+5, y*64+5))
					if self.acak[x][y] == 1:
						self.screen.blit(self.dua, (x*64+5, y*64+5))
					if self.acak[x][y] == 2:
						self.screen.blit(self.tiga, (x*64+5, y*64+5))
					if self.acak[x][y] == 3:
						self.screen.blit(self.empat, (x*64+5, y*64+5))
					if self.acak[x][y] == 4:
						self.screen.blit(self.lima, (x*64+5, y*64+5))
					if self.acak[x][y] == 5:
						self.screen.blit(self.enam, (x*64+5, y*64+5))
	def drawHUD(self):
		self.screen.blit(self.score_panel, [0, 389])
		self.screen.blit(self.greenindicator if self.turn else self.redindicator, (155, 400))

		scoreme = self.myfont85.render(str(self.me), 1, (255,255,255))
		scoreother = self.myfont85.render(str(self.otherplayer), 1, (255,255,255))
		scoretextme = self.myfont20.render("Poin Anda", 1, (255,255,255))
		scoretextother = self.myfont20.render("Poin Musuh", 1, (255,255,255))
		text_width_te, text_height_te = self.myfont20.size("Poin Musuh")
		text_width, text_height = self.myfont85.size(str(self.otherplayer))
		
		self.screen.blit(scoretextme, (10, 400))
		self.screen.blit(scoreme, (10, 415))
		self.screen.blit(scoretextother, (389-text_width_te-10, 400))
		self.screen.blit(scoreother, (389-text_width-10, 415))

	def finished(self):
		self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0,0))
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			pygame.display.flip()

bg=BoxesGame()
while 1:
	if bg.update() == 1:
		break
bg.finished()
