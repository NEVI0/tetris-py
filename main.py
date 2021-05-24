# Imports
import pygame, sys

from pygame.locals import *
from tetris import Tetris

pygame.init() # Initialize Pygame
pygame.display.set_caption('Tetris Py') # Game Title
pygame.display.set_icon(pygame.image.load('assets/game_logo.png')) # Game Icon

# Game Music
# pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.load('assets/soundtrack.mp3')
# pygame.mixer.music.play(-1)

# Color Contants
BLACK: tuple = (0, 0, 0)
GRAY: tuple = (219, 219, 219)
COLORS: tuple = ((0, 0, 0), (120, 37, 179), (100, 179, 179), (80, 34, 22), (80, 134, 22), (180, 34, 22), (180, 34, 122))

# Game Config Contants
WINDOW_SIZE: tuple = (400, 500)
GAME_SCREEN: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)
GAME_FONT = pygame.font.SysFont('Trebuchet MS', 24, True, True)
TIMER = pygame.time.Clock()
FPS = 60

# Game Config Variables
pressing_down = False
done = False
counter = 0

game_obj: Tetris = Tetris(20, 10) # Initialize Tetris Object

# Game Over Screen
def game_over() -> None:

    GAME_SCREEN.fill((255, 255, 255))  # Deixa a tela branca

    # Game Over Message
    end_message = GAME_FONT.render(f'Game Over! You got {game_obj.score} points. Press ESC to restart!', True, (0, 0, 0)) 
    end_message_rect = end_message.get_rect()
    end_message_rect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2) # Centers message at the middle of screen

    # Game Events
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                # restart() Restart Game
                game_obj.__init__(20, 10) # Restart Game

    GAME_SCREEN.blit(end_message, end_message_rect) # Renders Game Over Message
    pygame.display.update() # Update Game Screen

# Game Loop
while not done:

    if game_obj.state == 'gameover':
        game_over()

    points_text = GAME_FONT.render(f'Pontos: {game_obj.score}', True, (0, 0, 0)) # Points Text
    points_text_rect = points_text.get_rect()
    points_text_rect.center = (0, 0)

    GAME_SCREEN.fill((255, 255, 255))  # White Background Color

    # Renders a new block if none
    if game_obj.block is None:
        game_obj.new_figure()
    
    counter += 1 # Increase Counter

    # Reset counter if bigger than 10000000
    if counter > 10000000:
        counter = 0

    if counter % (FPS // game_obj.level // 2) == 0 or pressing_down:
        if game_obj.state == 'start':
            game_obj.go_down()

    # Game Events
    for ev in pygame.event.get():
        # Quit Event
        if ev.type == QUIT:
            done = True

        # Keyboard Events
        if ev.type == KEYDOWN:
            if ev.key == K_UP:
                game_obj.rotate()

            if ev.key == K_DOWN:
                pressing_down = True

            if ev.key == K_LEFT:
                game_obj.go_side(-1)

            if ev.key == K_RIGHT:
                game_obj.go_side(1)

            if ev.key == K_SPACE:
                game_obj.go_space()

            if ev.key == K_ESCAPE:
                game_obj.__init__(20, 10)

        # Checks if the user is typing KEYUP
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_DOWN:
                pressing_down = False # Then, just move

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

    pygame.display.flip()
    TIMER.tick(FPS) # Runs Game in 60 FPS

pygame.quit()
