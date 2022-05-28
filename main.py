from pygame import transform, image, display
from pygame.math import Vector2 as vec2
import pygame
import numpy as np
from random import choice

pygame.init()
screen = pygame.display.set_mode((800,800))
running = True
clock = pygame.time.Clock()

tile_size = (64,64)
def load_sc(path, sc):
	return transform.scale(image.load(path), sc)
def load_t(path):
	global tile_size
	return load_sc(path, tile_size)

texture_for_grid_value = {
	1: load_t("mini/tree.png"),
	2: load_t("mini/bigtree.png"),
	3: load_t("mini/pointytree.png"),

	4: load_t("mini/wheat1.png"),
	5: load_t("mini/wheat2.png"),
	6: load_t("mini/wheat3.png"),
	7: load_t("mini/wheat4.png"),

	8: load_t("mini/wkshop.png"),
	9: load_t("mini/house.png")
}
neighbors_for_value = {
	1: [1,1,2,4,5,9], 2: [1,2,2,2,3,9], 3: [2,3,3,9,9],
	4: [1,4,5], 5: [1,2,4,5,6], 6: [5,6,7], 7: [6,7],

	9: [8,8,1,2,3,7,7],
	8: [9,1,2,3,7,7]
}

pos = vec2(0.0, 0.0)
grid = np.zeros((16,16), dtype=np.int16)

import time
def fill_grid(p = (0,0)):
	global grid

	#print(f"Doing {p}")
	if grid[p[0], p[1]] == 0:
		grid[p] = choice([1,2,3,4,5,6,7])

	to_fill = []
	for tile in (
		[p[0]+1, p[1]], [p[0], p[1]+1],
		[p[0]-1, p[1]], [p[0], p[1]-1]
	):
		if tile[0] >= 0 and tile[0] < 16 and tile[1] <= 0 and tile[1] < 16:
			if grid[tile[0],tile[1]] == 0:
				grid[tile[0], tile[1]] = choice(neighbors_for_value[grid[p[0], p[1]]])
				#print(f"Set {tile} to {grid[tile[0], tile[1]]}")
				to_fill.append(tile)

	for tile_to_fill in to_fill:
		fill_grid(p=tile_to_fill)

fill_grid(p=(0,0))

grid_changed = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	down = pygame.key.get_pressed()
	move_keys = {
		pygame.K_a: vec2(-1.,0.),
		pygame.K_w: vec2(0.,-1.),
		pygame.K_d: vec2(1.,0.),
		pygame.K_s: vec2(0.,1.)
	}

	for move_key in move_keys.keys():
		if down[move_key]:
			pos += move_keys[move_key] * 4.

	if down[pygame.K_q]:
		grid = np.zeros((16,16), dtype=np.int16)
		fill_grid(p=[0,0])
		grid_changed = True

	if grid_changed:
		screen.fill((195,214,87))

		for x in range(0,16):
			for y in range(0,16):
				screen.blit(texture_for_grid_value[grid[x,y]], vec2(x,y) * tile_size[0] / 1.25)
		grid_changed = False

		display.flip()
