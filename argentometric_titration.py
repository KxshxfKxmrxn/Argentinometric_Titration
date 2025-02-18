import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Interactive Argentometric Method with Apparatus Animation')

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 128)

font = pygame.font.SysFont("Arial", 24)

volume_sample = 0.5  
concentration_agno3 = 0.01  
volume_agnitrate_used = 0  
titration_completed = False

chloride_concentration = 0
chloride_concentration_ppm = 0

score = 0  
level = 1  

def calculate_chloride_concentration():
    global chloride_concentration, chloride_concentration_ppm
    moles_agnitrate = concentration_agno3 * volume_agnitrate_used
    chloride_concentration = round(moles_agnitrate / volume_sample, 10)  
    chloride_concentration_ppm = round(chloride_concentration * 35.45 * 1e6, 2)


def calculate_beaker_color():
    max_color = min(int(chloride_concentration_ppm / 1000), 255)  
    return (max(255 - max_color, 0), min(max_color, 255), 0)


def draw_screen():
    global titration_completed, score, level

    screen.fill(WHITE)

    beaker_color = calculate_beaker_color()
    pygame.draw.rect(screen, BLUE, (100, 250, 200, 200)) 
    pygame.draw.rect(screen, beaker_color, (100, 250 + max(200 - volume_agnitrate_used * 400, 0), 200, min(volume_agnitrate_used * 400, 200)))


    pygame.draw.rect(screen, DARK_BLUE, (600, 100, 40, 400))
    pygame.draw.rect(screen, BLUE, (600, 100 + (400 - volume_agnitrate_used * 400), 40, volume_agnitrate_used * 400))

    pygame.draw.rect(screen, LIGHT_BLUE, (540, 100, 50, 50)) 


    pygame.draw.line(screen, BLACK, (250, 350), (250, 350 + 150), 5)


    text = font.render("Click to add AgNO3 to the water sample", True, BLACK)
    screen.blit(text, (250, 50))


    volume_text = font.render(f"Volume of AgNO3 used: {volume_agnitrate_used:.3f} L", True, BLACK)
    screen.blit(volume_text, (250, 120))


    concentration_text = font.render(f"Chloride Concentration: {chloride_concentration:.6f} mol/L", True, BLACK)
    screen.blit(concentration_text, (250, 180))
    ppm_text = font.render(f"Chloride Concentration: {chloride_concentration_ppm:.2f} ppm", True, BLACK)
    screen.blit(ppm_text, (250, 210))


    if titration_completed:
        completed_text = font.render("Titration Complete! Chloride concentration calculated.", True, RED)
        screen.blit(completed_text, (250, 250))

    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (600, 50))

    level_text = font.render(f"Level: {level}", True, GREEN)
    screen.blit(level_text, (600, 80))


    reset_button = pygame.Rect(650, 550, 120, 40)
    pygame.draw.rect(screen, RED, reset_button)
    reset_text = font.render("Reset Experiment", True, WHITE)
    screen.blit(reset_text, (670, 560))

    pygame.display.flip()


def add_agnitrate_animation():
    global volume_agnitrate_used, titration_completed, score
    if volume_agnitrate_used < 0.025:
        volume_agnitrate_used += 0.001  
        score += 10 
        calculate_chloride_concentration()
    else:
        titration_completed = True
        score += 50 


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()


            if not titration_completed and 600 <= x <= 640 and 100 <= y <= 500:
                add_agnitrate_animation()


            if 650 <= x <= 770 and 550 <= y <= 590:
                volume_agnitrate_used = 0
                titration_completed = False
                score = 0
                level = 1
                chloride_concentration = 0
                chloride_concentration_ppm = 0



    draw_screen()

pygame.quit()
sys.exit()
