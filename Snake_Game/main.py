from classes import *

pygame.init()
screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER + 20 + 2 * FONT_SIZE))
clock = pygame.time.Clock()
text_font = pygame.font.SysFont("calibri", FONT_SIZE)

main = Main()

pygame.time.set_timer(SCREEN_UPDATE, CALC_TIME)

while True:
    # draws all elements
    for event in pygame.event.get():
        if event.type == pygame.QUIT or main.restart_count > 200:
            main.game_over()
        if event.type == SCREEN_UPDATE:
            main.update()

    screen.fill((30, 30, 30))
    main.draw_elem(screen)
    pygame.display.update()
    clock.tick(FRAMERATE)
