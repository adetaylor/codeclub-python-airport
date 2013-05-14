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
		self.course = []

	def update(self):
		self.move(1)
		if not self.rect.colliderect(self.area):
			self.kill()

		if len(self.course) > 0: # only do this stuff if a course has been set
			nextfix = self.course[0]
			if pygame.sprite.collide_rect(self, nextfix):
				self.course.pop(0) # remove this item from the course...
				nextfix.kill() # ... and remove this fix from 'allfixes' so it is no longer drawn.
			else:
				self.point_towards(nextfix)

	def add_destination(self, position):
		self.course.append(position)

class Fix(codeclub.CodeClubSprite):
	def __init__(self, pos):
		codeclub.CodeClubSprite.__init__(self)
		self.set_costume('fix.png', 4)
		self.move_to(pos)

def main():
	pygame.init()
	screensize = (800, 483)
	screen = pygame.display.set_mode(screensize)

	wallpaper = codeclub.load_image('stansted-map.png')
	wallpaper = pygame.transform.scale(wallpaper, (screensize))

	allplanes = pygame.sprite.Group()
	allfixes = pygame.sprite.Group()
	chance_of_new_plane_in_next_tick = 1
	
	clock = pygame.time.Clock()

	draggingplane = None

	while True:
		clock.tick(60)
		if random.random() < chance_of_new_plane_in_next_tick:
			newplane = Plane(screensize)
			allplanes.add(newplane)
			chance_of_new_plane_in_next_tick = -0.003
		else:
			chance_of_new_plane_in_next_tick += 0.0001

		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			elif event.type == MOUSEBUTTONDOWN:
				for plane in allplanes:
					if plane.rect.collidepoint(pygame.mouse.get_pos()):
						draggingplane = plane
						break
			elif event.type == MOUSEBUTTONUP:
				draggingplane = None

		allplanes.update()
		for planea in allplanes:
			for planeb in allplanes:
				if not planea == planeb:
					if pygame.sprite.collide_mask(planea, planeb):
						return

		if not draggingplane == None:
			fix = Fix(pygame.mouse.get_pos())
			draggingplane.add_destination(fix)
			allfixes.add(fix)

		screen.blit(wallpaper, (0, 0))
		allplanes.draw(screen)
		allfixes.draw(screen)
		pygame.display.flip()

if __name__ == '__main__': main()
pygame.quit ()

