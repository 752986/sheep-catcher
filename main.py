from enum import Enum
import pygame
import random


class Direction(Enum):
	LEFT = 0
	RIGHT = 1
	UP = 2
	DOWN = 3
	STOP = 4

	def get_vector(self) -> tuple[int, int]:
		match self:
			case Direction.LEFT:
				return (-1, 0)
			case Direction.RIGHT:
				return (1, 0)
			case Direction.UP:
				return (0, -1)
			case Direction.DOWN:
				return (0, 1)
			case Direction.STOP:
				return (0, 0)

	def flipped(self) -> "Direction":
		match self:
			case Direction.LEFT:
				return Direction.RIGHT
			case Direction.RIGHT:
				return Direction.LEFT
			case Direction.UP:
				return Direction.DOWN
			case Direction.DOWN:
				return Direction.UP
			case Direction.STOP:
				return Direction.STOP


class Sheep:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y
		self.dir: Direction = random.choice(list(Direction))
		self.timer: int = random.randint(0, 50)
		self.caught: bool = False

	def update(self):
		self.timer -= 1

		if self.timer % 50 == 0: # only change direction every 50 game loops
			self.dir = random.choice(list(Direction)) # set random direction
		
		direction = self.dir.get_vector()

		if self.x < 0:
			self.dir = Direction.RIGHT
		if self.x > 800 - 60:
			self.dir = Direction.LEFT
		if self.y < 0:
			self.dir = Direction.DOWN
		if self.y > 800 - 40:
			self.dir = Direction.UP

		self.x += direction[0]
		self.y += direction[1]

# set up pygame stuff
pygame.init()  
pygame.display.set_caption("top down game")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() # set up clock
gameover = False

# game variables
timer = 0 # used for sheep movement
score = 0

# images and fonts
SheepPic = pygame.image.load("res/sheep.jpg").convert()
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Score:', True, (200, 200, 0))
text2 = font.render(str(score), True, (200, 200, 0))
text3 = font.render('YOU WIN!', True, (200, 200, 0))

# function defintions
# can you tell me what the parameters are for these functions, and what they return (if anything)?
def collision(player_pos: tuple[int, int], sheep: Sheep):
	x = player_pos[0]
	y = player_pos[1]

	if (
		x + 40 > sheep.x
		and x < sheep.x + 40
		and y + 40 > sheep.y
		and y < sheep.y + 40
		and not sheep.caught # only catch uncaught sheeps!
	):
		sheep.caught = True # catch da sheepies!
		global score # make it so this function can change this value
		score +=1

# create sheep!
# numbers in list represent xpos, ypos, direction moving, and whether it's been caught or not!
# make more sheeps here!
sheeps = [Sheep(random.randint(0, 700), random.randint(0, 700)) for _ in range(10000)]


# player variables
xpos = 500 # xpos of player
ypos = 200 # ypos of player
vx = 0 # x velocity (left/right speed) of player
vy = 0 # y velocity (up/down speed) of player
keys = [False, False, False, False] # this list holds whether each key has been pressed

while not gameover: # GAME LOOP
	screen.fill((0,0,0)) # wipe screen so it doesn't smear

	clock.tick(60) # FPS	
	
	# Input Section
	for event in pygame.event.get(): # quit game if x is pressed in top corner
		if event.type == pygame.QUIT:
			gameover = True
		  
	# physics section
	
	keys = pygame.key.get_pressed()

	# player movement!
	if keys[pygame.K_LEFT]:
		vx = -3
	elif keys[pygame.K_RIGHT]:
		vx = 3
	else:
		vx = 0

	if keys[pygame.K_UP]:
		vy = -3
	elif keys[pygame.K_DOWN]:
		vy = 3
	else:
		vy = 0

	for sheep in sheeps:
		# player/sheep collision!
		collision((xpos, ypos), sheep)

		# update sheep position
		sheep.update()

		# draw sheep
		if sheep.caught: # don't draw them if they're already caught!
			sheeps.remove(sheep)

		screen.blit(SheepPic, (sheep.x, sheep.y))


	# update player position
	xpos+=vx 
	ypos+=vy
	  
	# Render Section  
	# draw player
	pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos, 40, 40))
	
	# display score
	screen.blit(text, (20, 20))
	text2 = font.render(str(score), True, (200, 200, 0))# update score number
	screen.blit(text2, (140, 20))

	pygame.display.flip()# this actually puts the pixel on the screen
	
# end game loop

# end screen
screen.fill((0,0,0)) 
screen.blit(text3, (400,400))
pygame.display.flip()
pygame.time.wait(2000)# pause for a bit before ending

pygame.quit()