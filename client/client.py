import pygame
from random  import *

class BoxesGame():
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
		self.acak = [[x for x in range(6)] for y in range(6)]
		shuffle(self.acak)
		map(shuffle, self.acak)

		#inialisasi untuk koordinat kotak pertama yang diklik client(pemain) 
		self.xpos = -1
		self.ypos = -1

		#inialisasi dari objek2 yang akan dipakai
		self.initGraphics()
		
	def update(self):
		
		#Membuat game menjadi 60 fps
		self.clock.tick(60)
		
		#Clear layar window
		self.screen.fill(0)
		
		#Membuat garis-garis untuk board
		self.drawBoard()

		#membuat kotak-kotak yang akan menjadi objek yang ditebak
		self.drawMap()
		
		#Untuk mengecek event quit window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		mouse = pygame.mouse.get_pos()
		
		xpos = int(mouse[0]/64.0)
		ypos = int(mouse[1]/64.0)
		
		if pygame.mouse.get_pressed()[0]:
			self.kotak[xpos][ypos]=True
			
			if self.xpos <0 and self.ypos <0:
				self.xpos = xpos
				self.ypos = ypos
		
		#Update screen
		pygame.display.flip()
	
	def initGraphics(self):
		self.normallinev=pygame.image.load("normalline.png").convert_alpha()
		self.normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90).convert_alpha()
		self.separators=pygame.image.load("separators.png").convert_alpha()
		self.satu=pygame.image.load("warna/1.png").convert_alpha()
		self.dua=pygame.image.load("warna/2.png").convert_alpha()
		self.tiga=pygame.image.load("warna/3.png").convert_alpha()
		self.empat=pygame.image.load("warna/4.png").convert_alpha()
		self.lima=pygame.image.load("warna/5.png").convert_alpha()
		self.enam=pygame.image.load("warna/6.png").convert_alpha()
	
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
		
bg=BoxesGame()
while 1:
	bg.update()