import pygame

pygame.init()
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill("Purple")
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()