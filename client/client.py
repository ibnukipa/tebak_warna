import pygame

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
		
		#inialisasi dari objek2 yang akan dipakai
		self.initGraphics()
		
	def update(self):
		
		#Membuat game menjadi 60 fps
		self.clock.tick(60)
		
		#Clear layar window
		self.screen.fill(0)
		
		#Membuat garis-garis untuk board
		self.drawBoard()
		
		#Untuk mengecek event quit window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		
		#Update screen
		pygame.display.flip()
	
	def initGraphics(self):
		self.normallinev=pygame.image.load("normalline.png").convert_alpha()
		self.normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90).convert_alpha()
		self.separators=pygame.image.load("separators.png").convert_alpha()
	
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
		
bg=BoxesGame()
while 1:
	bg.update()