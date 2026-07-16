import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1100,700))
pygame.display.set_caption("Scene 1")
clock = pygame.time.Clock()

scene = 1

text_font = pygame.font.Font(None, 36)
text_surface = text_font.render("Loading...", True, (0, 0, 0))
text_rect = text_surface.get_rect(center=(550, 350))


background_rect = pygame.Rect(0,0,1100,700)
background_image = pygame.image.load("Assets/scene1background.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (1100, 700))

cookbutton_rect = pygame.Rect(620,300,200,200)
cookbutton_image = pygame.image.load("Assets/cookbutton.png").convert_alpha()

customer_rect = pygame.Rect(180,100,200,350)
customer_image = pygame.image.load("Assets/cat_customer.png").convert_alpha()

table_rect = pygame.Rect(0,150,100,100)
table_image = pygame.image.load("Assets/table.png").convert_alpha()
table_image = pygame.transform.scale(table_image, (1100, 600))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if scene == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if cookbutton_rect.collidepoint(event.pos):
                        scene = 2
        
            screen.blit(background_image, background_rect)
            screen.blit(customer_image, customer_rect)
            screen.blit(table_image, table_rect)
            screen.blit(cookbutton_image, cookbutton_rect)
            
        if scene ==2:
            screen.fill((255,210,138))
            screen.blit(text_surface, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()