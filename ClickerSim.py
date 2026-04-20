import pygame
import sys
from DataStore import DataStore
from Bnum import Bnum

pygame.init()

# ---------------- DATA ----------------
data = DataStore()

clicks = data.get("Clicks", Bnum.fromNumber(0))
clickplus = data.get("ClicksPlus", Bnum.fromNumber(1))  # default +1 per click

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker Simulator")

clock = pygame.time.Clock()

# Fonts
big_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Button
button = pygame.Rect(150, 160, 200, 100)

# Colors
BG = (25, 25, 25)
BUTTON = (0, 200, 0)
BUTTON_HOVER = (0, 255, 0)
WHITE = (255, 255, 255)
PANEL = (40, 40, 40)

running = True

# ---------------- GAME LOOP ----------------
while running:
    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()
    hovered = button.collidepoint(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if hovered:
                clicks = Bnum.add(clicks, clickplus)

    # ---------------- DRAW ----------------
    screen.fill(BG)

    pygame.draw.rect(screen, PANEL, (10, 10, 480, 80), border_radius=10)

    clicks_text = big_font.render(
        f"Clicks: {Bnum.format(clicks)}",
        True,
        WHITE
    )
    screen.blit(clicks_text, (20, 20))

    color = BUTTON_HOVER if hovered else BUTTON
    pygame.draw.rect(screen, color, button, border_radius=12)

    btn_text = small_font.render(
        f"+{Bnum.format(clickplus)} Clicks",
        True,
        WHITE
    )
    screen.blit(btn_text, (button.x + 45, button.y + 35))

    pygame.display.flip()

# ---------------- SAVE ----------------
data.set("Clicks", clicks)
data.set("ClicksPlus", clickplus)

data.close()

pygame.quit()
sys.exit()