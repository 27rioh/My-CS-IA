import pygame
import sys

pygame.init()

#Screen size and caption
screen = pygame.display.set_mode((1100,700))
pygame.display.set_caption("Pygame Test")
#For FPS
clock = pygame.time.Clock()

button_rect = pygame.Rect(350,250,100,50)
button_color = (250,200,100)

#varaiables for dragging
is_dragging = False
offset_x = 0
offset_y = 0

Scene = 0

# anything that keeps going during the game should be inside this loopp!
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_rect.collidepoint(event.pos):
                    is_dragging = True
                    mouse_x, mouse_y = event.pos # extracts the coordination of mouse only when clicked using (event.pos)
                    #calculates how far the mouse is from the button
                    offset_x = button_rect.x - mouse_x
                    offset_y = button_rect.y - mouse_y  

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                mouse_x, mouse_y = event.pos
                button_rect.x = mouse_x + offset_x
                button_rect.y = mouse_y + offset_y
    screen.fill((240, 240, 240))    
    current_color = (250,100,100) if is_dragging else button_color
    pygame.draw.rect(screen, current_color, button_rect)
    pygame.display.flip() #display.flip updates entirely while update only changes the parts changed
    clock.tick(60) #60 FPS

# Game logics

#Images, Rerndering

pygame.quit()
sys.exit()