import sys, pygame
import random
import math
from abc import ABC, abstractmethod

WIDTH = 1000
HEIGHT = 1000
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)
#RED = (255,0,0)
BLUE = (0,0,255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aros")
clock = pygame.time.Clock()

big_center = (WIDTH/2, HEIGHT/2)
big_radio = WIDTH/3
arc_center = screen.get_rect().move(0,-HEIGHT/2)
arc_radio = big_radio
arc_start = 30*math.pi/180 #30°
arc_stop = 120*math.pi/180 #120°
line_start = (2/3*WIDTH, 2/3*HEIGHT)
line_stop = (WIDTH/3, 4/5*HEIGHT)

def direction(a,b):
	#x,y vector from a to b
	if hasattr(a,'rect'):
		xa = a.rect.centerx
		ya = a.rect.centery
	else:
		xa, ya = a
	if hasattr(b,'rect'):
		xb = b.rect.centerx
		yb = b.rect.centery
	else:
		xb, yb = b
	dx = xb -xa
	dy = yb - ya
	return dx, dy

def distance(a,b):
	#pitagoras distance between a and b
	dx, dy = direction(a,b)
	return (dx**2 + dy**2)**(1/2)

def reflection(normal, i_vector):
	'i_vector reflection with normal vector.'
	alpha = complex(*normal) / abs(complex(*i_vector))
	rotated = -complex(*i_vector) * (alpha/incidence)**2
	return rotated.real, rotated.imag

# Wall abstract base class, not intended tu instantiate.
# use the specific wall classes below
# CircunWall,
class Wall(ABC):

	@abstractmethod
	def draw(self, surface):
		pass

	@abstractmethod
	def collide(self, o):
		pass

	@abstractmethod
	def bounce(self, o):
		pass

	@abstractmethod
	def move_to_safe(self, o):
		while self.collide(o):
			o.rect.x += o.speedx
			o.rect.y += o.speedy

class CircunWall(Wall):
	def __init__(self, center, radio, color=WHITE):
		self.center = center
		self.radio = radio
		self.color = color

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.center, self.radio)

	def collide(self, o):
		centers_distance = distance(o.rect.center, self.center)
		distance_to_circunf = self.radio - centers_distance
		return -o.radio < distance_to_circunf < o.radio

	def bounce(self, o):
		normal = direction(self.center, o.rect.center)
		i_vector = o.speedx , o.speedy
		o.speedx, o.speedy = reflection(normal, i_vector)

	def move_to_safe(self, o):
		while self.collide(o):
			o.rect.x += o.speedx
			o.rect.y += o.speedy
		
class ArcWall(Wall):
	def __init__(self, center, radio, start, stop, color=WHITE):
		self.center = center
		self.radio = radio
		diam = 2*radio
		self.rect = pygame.Rect(center, (diam, diam)).move(-radio, -radio)
		self.start = start
		self.stop = stop
		self.color = color

	def draw(self, surface):
		pygame.draw.arc(surface, self.color, self.rect, -self.start)

	def collide(self, o):
		colliding = False
		o_rel_x, o_rel_y = direction(self.center, o)
		o_angle = math.atan2(o_rel_y, o_rel_x)
		if o_angle < 0:
			o_angle += math.tau
		if self.start <= o_angle <= self.stop:
			centers_distance = distance(o.rect.center, arc_center)
			distance_to_circunf = self.radio - centers_distance
			colliding = -o.radio < distance_to_circunf < o.radio
		return colliding

	def bounce(self, o):
		normal = direction(self.center, o.rect.center)
		i_vector = o.speedx, o.speedy
		o.speedx, o.speedy = reflection(normal, i_vector)

	def move_to_safe(self, o):
		while self.collide(o):
			o.rect.x += o.speedx
			o.rect.y += o.speedy

class LineWall(Wall):
	def __init__(self, start, stop, color=WHITE):
		self.start = start
		self.stop = stop
		self.color = color

	def draw(self, surface):
		pygame.draw.line(surface, self.color, self.start, self.stop)

	def collide(self, o):
		p = complex(*direction(self.start, o.rect.center))
		ba = complex(*direction(self.start, self.stop))
		pba = p/ba
		if 0 <= pba.real <= 1:
			line_distance = abs(pba.imag*abs(ba))
		else:
			line_distance = min(
				distance(self.start, o.rect.center), 
				distance(self.stop, o.rect.center))
		return line_distance < o.radio

	def bounce(self, o):
		normal = direction(self.start, self.stop)
		i_vector = -o.speedx, -o.speedy
		o.speedx, o.speedy = reflection(normal, i_vector)

	def move_to_safe(self, o):
		while self.collide(o):
			o.rect.x += o.speedx
			o.rect.y += o.speedy

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/Ball1.png"),(25,25)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.center = screen.get_rect().center
		self.rect.move_ip(random.randint(-20,20), random.randint(-20,20))
		self.radio = self.rect.w/2
		self.speedy = random.randint(-8,8)
		self.speedx = random.randint(-8,8)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy

start = True
running=True
circle = CircunWall(big_center, big_radio)
arc = ArcWall(arc_center, arc_radio, arc_start, arc_stop, BLUE)
line = LineWall(line_start, line_stop, GREEN)
walls = [circle, arc, line]

while running:
	screen.fill(BLACK)
	if start:
		start = False
			
		all_sprites = pygame.sprite.Group()
		ball = Ball()
		all_sprites.add(ball)

	for w in walls:
		w.draw(screen)	

	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()

	all_sprites.update()
	
	all_sprites.draw(screen)
	
	pygame.display.flip()