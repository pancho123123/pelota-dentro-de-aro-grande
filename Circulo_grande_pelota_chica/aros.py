import sys, pygame

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
#GREEN = (0, 255, 0)
#RED = (255,0,0)
#BLUE = (0,0,255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aros")
clock = pygame.time.Clock()


aro = pygame.draw.circle(screen,WHITE,(400,300),250)

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/Ball1.png"),(25,25)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH // 2
		self.rect.y = HEIGHT // 2
		self.speedy = 1
		self.speedx = 1

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
start = True
running=True
while running:
	screen.fill(BLACK)
	if start:
		start = False
			
		all_sprites = pygame.sprite.Group()
		ball = Ball()
		all_sprites.add(ball)
	pygame.draw.circle(screen,WHITE,(400,300),250)	

	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()

	all_sprites.update()
	
	all_sprites.draw(screen)
	
	pygame.display.flip()