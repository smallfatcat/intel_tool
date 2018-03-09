# Import a library of functions called 'pygame'
import pygame
import os
from math import pi
from pygame import gfxdraw

from ctypes import windll
SetWindowPos = windll.user32.SetWindowPos

_cached_fonts = {}
_cached_text = {}

# font helpers
def make_font(fonts, size):
	available = pygame.font.get_fonts()
	# get_fonts() returns a list of lowercase spaceless font names 
	choices = map(lambda x:x.lower().replace(' ', ''), fonts)
	for choice in choices:
		if choice in available:
			return pygame.font.SysFont(choice, size)
	return pygame.font.Font(None, size)

def get_font(font_preferences, size):
	global _cached_fonts
	key = str(font_preferences) + '|' + str(size)
	font = _cached_fonts.get(key, None)
	if font == None:
		font = make_font(font_preferences, size)
		_cached_fonts[key] = font
	return font

def create_text(text, fonts, size, color):
	global _cached_text
	key = '|'.join(map(str, (fonts, size, color, text)))
	image = _cached_text.get(key, None)
	if image == None:
		font = get_font(fonts, size)
		image = font.render(text, True, color)
		_cached_text[key] = image
	return image

NOSIZE = 1
NOMOVE = 2
TOPMOST = -1
NOT_TOPMOST = -2

def alwaysOnTop(yesOrNo):
	zorder = (NOT_TOPMOST, TOPMOST)[yesOrNo] # choose a flag according to bool
	hwnd = pygame.display.get_wm_info()['window'] # handle to the window
	SetWindowPos(hwnd, zorder, 0, 0, 0, 0, NOMOVE|NOSIZE)

# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
GREY = (128, 128, 128)
DARKBLUE = (0,0,50)
 
# Set the height and width of the screen
size = [800, 600]
# pygame.RESIZABLE
# pygame.NOFRAME
screen = pygame.display.set_mode(size)
asurf = pygame.image.load(os.path.join('17738_32.png'))
asurf.convert()

font_preferences = [
	"Tahoma"]
textArray = []
for i in range(10):
	text = create_text(str(i+1), font_preferences, 12, (0, 128, 0))
	textArray.append(text)

pygame.display.set_caption("Example code for the draw module")
 
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
myframe = 0
 
while not done:
 
	# This limits the while loop to a max of 10 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(100)
	myframe += 1

	pygame.display.set_caption(str(pygame.mouse.get_pos()) +str(pygame.mouse.get_pressed()))
	 
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop
 
	# All drawing code happens after the for loop and but
	# inside the main while done==False loop.
	 
	# Clear the screen and set the screen background
	screen.fill(DARKBLUE)

	# Draw on the screen a GREEN line from (0,0) to (50.75) 
	# 5 pixels wide.
	#pygame.draw.aaline(screen, GREEN, [0, 50],[50, 80], True)
	newX = 200
	newY = (0 + (myframe))
	if (newY > 600):
		myframe = 0 
	pygame.gfxdraw.aacircle(screen, newX+50, newY , 5, GREY)
	#pygame.gfxdraw.filled_circle(screen, 200, newY, 5, BLUE)
	screen.blit(asurf, (newX,newY))

	for i in range(10):
		screen.blit( textArray[i], (10 - textArray[i].get_width() // 2, (50*i)+textArray[i].get_height() ) )
	
	# Go ahead and update the screen with what we've drawn.
	# This MUST happen after all the other drawing commands.
	pygame.display.flip()
	alwaysOnTop(False)
	#print(myframe)
 
# Be IDLE friendly
pygame.quit()

