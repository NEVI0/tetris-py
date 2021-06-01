# Imports
import pygame, sys

from pygame.locals import *
from tetris import Tetris

pygame.init() # Initialize Pygame
pygame.display.set_caption('Tetris Py') # Game title
pygame.display.set_icon(pygame.image.load('assets/game_logo.png')) # Game icon

# Game music
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.load('assets/soundtrack.mp3')
pygame.mixer.music.play(-1)

# Color contants
BLACK: tuple = (0, 0, 0)
GRAY: tuple = (219, 219, 219)
COLORS: tuple = ((0, 0, 0), (120, 37, 179), (100, 179, 179), (80, 34, 22), (80, 134, 22), (180, 34, 22), (180, 34, 122))

# Game config contants
WINDOW_SIZE: tuple = (400, 500)
GAME_SCREEN: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)
GAME_FONT = pygame.font.SysFont('Trebuchet MS', 24, True, True)
TIMER = pygame.time.Clock()
FPS = 60

# Game config variables
pressing_down = False
done = False
counter = 0

game_obj: Tetris = Tetris(20, 10) # Initialize tetris object

# Game Over Screen
def game_over() -> None:

    GAME_SCREEN.fill((255, 255, 255)) # Set a blank screen

    game_over_text = GAME_FONT.render(f'Game Over!', True, (0, 0, 0)) # Game over text
    points_text = GAME_FONT.render(f'You have got {game_obj.score} points', True, (0, 0, 0)) # Points text
    restart_text = GAME_FONT.render(f'Press ESC to restart', True, (0, 0, 0)) # Restart text

    # Centers game over text at the middle of screen
    game_over_rect = game_over_text.get_rect();
    game_over_rect.center = (WINDOW_SIZE[0] // 2, 180)

    # Centers points text at the middle and bellow of game over text
    points_rect = points_text.get_rect();
    points_rect.center = (WINDOW_SIZE[0] // 2, 220)

    # Centers points restart text at the middle and bellow of points text
    restart_rect = restart_text.get_rect();
    restart_rect.center = (WINDOW_SIZE[0] // 2, 260)

    GAME_SCREEN.blit(game_over_text, game_over_rect)
    GAME_SCREEN.blit(points_text, points_rect)
    GAME_SCREEN.blit(restart_text, restart_rect)

    # Game events
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit() # Quit game

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game_obj.__init__(20, 10) # Restart Game

    pygame.display.update() # Update Game Screen

# Game Loop
while not done:

    points_text = GAME_FONT.render(f'Points: {game_obj.score}', True, (0, 0, 0)) # Points text

    GAME_SCREEN.fill((255, 255, 255))  # White background color
    GAME_SCREEN.blit(points_text, (10, 10)); # Renders points text at the top

    # Renders a new block if none
    if game_obj.block is None:
        game_obj.new_figure()
    
    counter += 1 # Increase Counter

    # Reset counter if bigger than 10000000
    if counter > 10000000:
        counter = 0

    # Makes block fall down
    if counter % (FPS // game_obj.level // 2) == 0 or pressing_down:
        if game_obj.state == 'start':
            game_obj.go_down() # Falls down if is not game over state

    # Game events
    for ev in pygame.event.get():
        if ev.type == QUIT: # Quit event
            done = True

        if ev.type == KEYDOWN: # Keyboard events
            if ev.key == K_UP:
                game_obj.rotate() # Rotate block
            if ev.key == K_DOWN:
                pressing_down = True # Increase block speed
            if ev.key == K_LEFT:
                game_obj.go_side(-1) # Goes left
            if ev.key == K_RIGHT:
                game_obj.go_side(1) # Goes right
            if ev.key == K_SPACE:
                game_obj.go_space() # Goes down
            if ev.key == K_ESCAPE:
                game_obj.__init__(20, 10) # Restart game

        if ev.type == pygame.KEYUP: # Keyup event
            if ev.key == pygame.K_DOWN:
                pressing_down = False # Reset block speed

    for i in range(game_obj.height):
        for j in range(game_obj.width):
            pygame.draw.rect(GAME_SCREEN, GRAY, [game_obj.x + game_obj.zoom * j, game_obj.y + game_obj.zoom * i, game_obj.zoom, game_obj.zoom], 1)
            if game_obj.field[i][j] > 0:
                pygame.draw.rect(GAME_SCREEN, COLORS[game_obj.field[i][j]],
                                 [game_obj.x + game_obj.zoom * j + 1, game_obj.y + game_obj.zoom * i + 1, game_obj.zoom - 2, game_obj.zoom - 1])

    if game_obj.block is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game_obj.block.image():
                    pygame.draw.rect(GAME_SCREEN, COLORS[game_obj.block.color],
                                     [game_obj.x + game_obj.zoom * (j + game_obj.block.x) + 1,
                                      game_obj.y + game_obj.zoom * (i + game_obj.block.y) + 1,
                                      game_obj.zoom - 2, game_obj.zoom - 2])

    if game_obj.state == 'gameover':
        game_over() # Renders game over screen

    pygame.display.flip() # Update the full display surface to the screen
    TIMER.tick(FPS) # Runs the game in 60 FPS

pygame.quit()
