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
BLUE = (0, 0, 255)
RED = (255, 0, 0)
TIMER_COLOR = (255, 255, 255)  # White for the timer text
BACKGROUND_COLOR = (255, 0, 0)  # Red background for the timer

# Load assets
background_front = pygame.image.load("background-front.jpg")
background_back = pygame.image.load("backgreound_back.png")
background = pygame.transform.scale(background_front, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 74)

# Timer font
timer_font = pygame.font.Font(None, 150)

# Sounds
pygame.mixer.init()
red_light_mp3 = "red_light.mp3"
green_light_mp3 = "green_light.mp3"
alarm_mp3 = "alarm.mp3"
pygame.mixer.music.load("background_music.mp3")

# Game state
is_red_light = True
is_game_started = False
is_game_ended = False
alarm_played = False
background_music_playing = False
green_light_sound_playing = False
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

# Timer state
start_time = None # Record the start time
time_limit = 5 * 60 * 1000  # 10 minutes in milliseconds (5 * 60 * 1000)
remaining_time = time_limit  # Set the remaining time to 5 minutes initially

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
        background = pygame.transform.scale(background_front, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
    else:
        pygame.mixer.music.stop()
        play_mp3(green_light_mp3)
        background = pygame.transform.scale(background_back, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        green_light_sound = pygame.mixer.Sound(green_light_mp3)
        green_light_sound.play()
        green_light_sound_playing = True


# Function to convert milliseconds to MM:SS format
def format_time(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

# Main game loop
clock = pygame.time.Clock()
running = True
background = pygame.transform.scale(background_front, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
screen.blit(background, (0, 0))

while running:
    #screen.fill(WHITE)
   # screen.blit(background, (0, 0))

    # Calculate the remaining time
    if is_game_started == True:
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = time_limit - elapsed_time  # Decrease the remaining time

    if remaining_time <= 0:
        is_game_ended = True
        remaining_time = 0
        if alarm_played == False:
            pygame.mixer.music.stop()
            play_mp3(alarm_mp3)
            alarm_played = True
            green_light_sound_playing = False

    # Format and display the countdown timer
    timer_text = format_time(remaining_time)

    # Padding and position for the timer
    padding = 10
    text_surface = timer_font.render(timer_text, True, TIMER_COLOR)

    # Timer width and height with padding
    timer_width = text_surface.get_width() + padding * 2
    timer_height = text_surface.get_height() + padding * 2

    # Position of the timer (top-right corner)
    timer_rect = pygame.Rect(SCREEN_WIDTH * 0.7 , 120, timer_width, timer_height)

    # Draw the red background rectangle behind the timer text
    pygame.draw.rect(screen, BACKGROUND_COLOR, timer_rect)

    # Draw the timer text
    screen.blit(text_surface, (timer_rect.x + padding, timer_rect.y + padding))

    # Button text
    button_text = "Green Light" if not is_red_light else "Red Light"
    if is_game_started == False:
        button_text = "START" 
    if is_game_ended == True:
        button_text = "GAME ENDS" 
    text_surface = font.render(button_text, True, BLACK)

    padding = 20
    button_width = text_surface.get_width() + padding * 2
    button_height = text_surface.get_height() + padding * 2
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT - 100, button_width, button_height)

    color = GREEN if not is_red_light else RED
    if is_game_started == False:
        color = WHITE
    if is_game_ended == True:
        color = WHITE

    pygame.draw.rect(screen, color, button_rect)
    screen.blit(text_surface, (button_rect.x + padding, button_rect.y + padding))

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        if (event.type == KEYDOWN and event.key == K_SPACE) or (event.type == MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos)):
            is_game_started = True
            if start_time == None:
                start_time = pygame.time.get_ticks()
            if is_game_ended == False:
                toggle_light()

    # Handle sound playback for green light
    if green_light_sound_playing and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)

    pygame.display.flip()

    # Update the clock
    clock.tick(30)  # Cap the frame rate at 30 FPS

pygame.quit()
sys.exit()