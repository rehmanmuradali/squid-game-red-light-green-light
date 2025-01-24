import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Full-screen mode
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Red Light, Green Light Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load assets
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 74)

# Sounds
pygame.mixer.init()
red_light_mp3 = "red_light.mp3"
green_light_mp3 = "green_light.mp3"
pygame.mixer.music.load("background_music.mp3")

# Game state
is_red_light = False
background_music_playing = False
green_light_sound_playing = False
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)


# Helper functions
def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def play_mp3(sound_file):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()


def toggle_light():
    global is_red_light, green_light_sound_playing
    is_red_light = not is_red_light

    if is_red_light:
        pygame.mixer.music.stop()
        play_mp3(red_light_mp3)
        green_light_sound_playing = False
    else:
        pygame.mixer.music.stop()
        play_mp3(green_light_mp3)

        green_light_sound = pygame.mixer.Sound(green_light_mp3)
        green_light_sound.play()
        green_light_sound_playing = True


# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    button_text = "Green Light" if not is_red_light else "Red Light"
    text_surface = font.render(button_text, True, BLACK)

    padding = 20
    button_width = text_surface.get_width() + padding * 2
    button_height = text_surface.get_height() + padding * 2
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT - 100, button_width, button_height)

    pygame.draw.rect(screen, GREEN if not is_red_light else RED, button_rect)
    screen.blit(text_surface, (button_rect.x + padding, button_rect.y + padding))

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        elif event.type == MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
            toggle_light()

    if green_light_sound_playing and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
