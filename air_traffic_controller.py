#!/usr/bin/env python

import pygame, codeclub
from pygame.locals import *
import random

class Plane(codeclub.CodeClubFreeRotatingSprite):
	def __init__(self, screensize):
		codeclub.CodeClubFreeRotatingSprite.__init__(self)
		X_MAX = screensize[0]
		Y_MAX = screensize[1]
		x = int(random.random() * X_MAX)
		y = int(random.random() * Y_MAX)
		whichedge = int(random.random() * 4)
		if (whichedge == 0): # left
			x = 0
			direction = 90 
		elif (whichedge == 1): # top
			y = 0
			direction = 180
		elif (whichedge == 2): # right
			x = X_MAX
			direction = 270
		else:
			y = Y_MAX # bottom
			direction = 0
		direction += int(random.random() * 180)
		if (direction > 359):
			direction -= 360
		self.set_costume('plane_icon.png', 60)
		self.move_to((x, y))
		self.point_in_direction(direction)

def main():
	pygame.init()
	screensize = (800, 483)
	screen = pygame.display.set_mode(screensize)

	wallpaper = codeclub.load_image('stansted-map.png')
	wallpaper = pygame.transform.scale(wallpaper, (screensize))

	plane = Plane(screensize)
	allplanes = pygame.sprite.Group((plane))
	
	clock = pygame.time.Clock()
	
	while True:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return

		plane.move(1)

		screen.blit(wallpaper, (0, 0))
		allplanes.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()
pygame.quit ()

