'''Game main module.

Last Day Game Entry, by Clint Herron
'''

import data
import pygame
from pygame.locals import *
from data import *
from math import sin

BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 12, 20
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 240, 400
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT = SCREEN_WIDTH / BOARD_WIDTH, SCREEN_HEIGHT / BOARD_HEIGHT

TILE_COLOR = (127, 127, 255)
TILE_COLOR_ALT = (255, 127, 127)
TILE_COLOR_LOSE = (64, 64, 128)
TILE_COLOR_ALT_LOSE = (127, 64, 64)

BLACK = (0,0,0)

LEVEL_SPEED = ( 80, 80, 75, 75, 70, 70, 65, 60, 55, 50,
				45, 40, 35, 30, 32 )
MAX_WIDTH = (3, 3, 3, 3, 2, 2, 2, 2, 1, 1,
				1, 1, 1, 1, 1)
				
COLOR_CHANGE_Y = 10 # The block below which are displayed in the alternate color
WIN_LEVEL = 15

current_speed = 50 # Current tile speed in milliseconds
board = []
lose_tiles = []
current_direction = 1
current_x, current_y, current_width = 0, BOARD_HEIGHT - 1, 3
current_level = 0

INTRO = 0
PLAYING = 1
LOSE = 2
WIN = 3

game_state = INTRO

bg_images = ( load_image("intro.png"), load_image("game.png"), load_image("lose.png"), load_image("win.png") )

bg_images[WIN].set_colorkey(BLACK)
bg_images[LOSE].set_colorkey(BLACK)

keep_running = True

def main():
	global game_state, current_x, current_y, current_speed, keep_running, current_width, current_level
	
	pygame.init()
	screen = pygame.display.set_mode( SCREEN_SIZE )	
	
	reset_game()

	while(keep_running):
		update_movement()
		update_board_info()
		update_screen(screen)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				keep_running = False
			elif event.type == KEYDOWN:				if event.key == K_SPACE:					key_hit()
				elif event.key == K_ESCAPE:
					if game_state == INTRO:
						keep_running = False
					else:
						reset_game()
				elif event.key == K_F1: # Yes, this is a cheat.
					current_x -= 1
					if (current_x < 0): current_x = 0
					current_width += 1
					if (current_width >= BOARD_WIDTH): current_width = BOARD_WIDTH - 1
					
	pygame.display.quit()

def reset_game():
	global game_state, current_x, current_y, current_speed, keep_running, current_width, current_level, lose_tiles

	clear_board()
	lose_tiles = []
	
	keep_running = True
	
	game_state = INTRO
	
	current_x = 0
	current_y = BOARD_HEIGHT - 1
	current_level = 0
	current_speed = LEVEL_SPEED[current_level]
	current_width = MAX_WIDTH[current_level]

def key_hit():
	global keep_running, game_state, current_x, current_y, current_width, current_speed, current_level, lose_tiles
	
	if game_state == PLAYING:
		if current_y < BOARD_HEIGHT - 1:
			for x in range(current_x, current_x + current_width):
				if board[x][current_y + 1] == 0: # If they're standing on a block that did not work
					current_width -= 1 # Then next time, give them one less block
					board[x][current_y] = 0 # Also, get rid of this block that isn't standing on solid ground.
					# Then, add a lose tile for that missed block
					# Lose tile format is (x, y, color, start time)
					lose_tiles.append( (x, current_y,
										pygame.time.get_ticks()) )

		current_level += 1
		check_win_lose()
		current_y -= 1
	elif game_state == INTRO:
		game_state = PLAYING
	elif (game_state == LOSE) or (game_state == WIN):
		reset_game()
		game_state = INTRO
	else:
		keep_running = False

def check_win_lose():
	global game_state, current_width, current_level, current_speed, keep_running, TILE_COLOR
	
	if current_width == 0:
		game_state = LOSE
	elif current_level == WIN_LEVEL:
		current_speed = 100
		game_state = WIN
	else:
		current_speed = LEVEL_SPEED[current_level]
		if current_width > MAX_WIDTH[current_level]:
			current_width = MAX_WIDTH[current_level]

last_time = 0
def update_movement():
	global game_state, last_time, current_x, current_y, current_width, current_speed, current_direction

	current_time = pygame.time.get_ticks()
	if (last_time + current_speed <= current_time):
		if game_state == PLAYING:
			new_x = current_x + current_direction

			if (new_x < 0) or (new_x + current_width > BOARD_WIDTH):
				current_direction = -current_direction

			current_x += current_direction

		last_time = current_time
		
def update_screen(screen):
	global game_state

	if game_state == PLAYING:
		draw_background(screen)
		draw_board(screen)
	elif game_state == INTRO:
		draw_background(screen)
		pass
	elif (game_state == LOSE) or (game_state == WIN):
		screen.fill(BLACK)
		draw_board(screen)	
		draw_background(screen)
		
	pygame.display.flip()
	
def draw_background(screen):
	global game_state
	screen.blit(bg_images[game_state], (0,0,SCREEN_WIDTH,SCREEN_HEIGHT),	(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
	
	
def update_board_info():
	global game_state
	
	if game_state == PLAYING:
		clear_row(current_y)
		fill_current_row()
	
def draw_board(screen):
	for x in range(BOARD_WIDTH):
		for y in range(BOARD_HEIGHT):
			if board[x][y] == 1:
				draw_tile(screen, x, y)
	
	draw_lose_tiles(screen)
	
def draw_tile(screen, x, y):
	xoffset = 0 # XOffset is used to draw some wiggle in the tower when you win
	col = TILE_COLOR
	if (y < COLOR_CHANGE_Y):
		col = TILE_COLOR_ALT
		
	if (game_state == LOSE):
		col = TILE_COLOR_LOSE
		if (y < COLOR_CHANGE_Y):
			col = TILE_COLOR_ALT_LOSE	

	if game_state == WIN:
		xoffset = sin(pygame.time.get_ticks() * 0.004 + y * 0.5) * (SCREEN_WIDTH / 4)

	pygame.draw.rect(screen, col, (x * TILE_WIDTH + xoffset, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
	pygame.draw.rect(screen, BLACK, (x * TILE_WIDTH + xoffset, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)

# Lose tiles are ones that fall off from the edge when you miss placing them on the proper stack
def draw_lose_tiles(screen):
	for lt in lose_tiles:
		deltaT = (pygame.time.get_ticks() - lt[2]) * 0.008 # How long it has been falling
		x = lt[0] * TILE_WIDTH
		y = lt[1] * TILE_HEIGHT + deltaT * deltaT
		
		col = TILE_COLOR_LOSE
		if (lt[1] < COLOR_CHANGE_Y):
			col = TILE_COLOR_ALT_LOSE
		
		if (y > SCREEN_HEIGHT):
			lose_tiles.remove(lt)
		else:
			pygame.draw.rect(screen, col, (x+2, y+2, TILE_WIDTH-3, TILE_HEIGHT-3))

def clear_board():
	global board
	
	board = []
	for x in range(BOARD_WIDTH):
		board.append([])
		for y in range (BOARD_HEIGHT):
			board[x].append(0)

def clear_row(y):
	for x in range(BOARD_WIDTH):
		board[x][y] = 0

def fill_current_row():
	global current_x, current_y, current_width
	for x in range(current_x, current_x + current_width):
		board[x][current_y] = 1