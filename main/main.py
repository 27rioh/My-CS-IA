import pygame
import sys

pygame.init()

#GLOBAL VARIABLES

#Screen size and caption
screen = pygame.display.set_mode((1100,700))
pygame.display.set_caption("Pygame Test")
#For FPS
clock = pygame.time.Clock()

#varaiables for dragging
item_being_dragged = None
Scene = 0

Active_bowl_list = []
Active_bowl_rect = pygame.Rect(350,380, 400, 300)

class Ingredients:
    def __init__(self, name, type, pos_x, pos_y, width, height): #add image later!!
        self.name = name
        self.type = type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.offset_x = 0
        self.offset_y = 0
        self.image = pygame.transform.scale(pygame.image.load("Assets/Wavy Noodles.png"), (150, 150))


ingredients_list = {
                    "Wavy Noodles":{"Name":"Wavy Noodles","Type":"Noodle","pos_x":100,"pos_y":100, "width": 150, "height": 150},
                    "Straight Noodles":{"Name":"Straight Noodles","Type":"Noodle","pos_x":250,"pos_y":100, "width": 150, "height": 150},
                    
                    "Shoyu Broth":{"Name":"Shoyu Broth","Type":"Broth","pos_x":400,"pos_y":100, "width": 150, "height": 150},
                    "Tonkotsu Broth":{"Name":"Tonkotsu Broth","Type":"Broth","pos_x":550,"pos_y":100, "width": 150, "height": 150},
                    "Miso Broth":{"Name":"Miso Broth","Type":"Broth","pos_x":400,"pos_y":250, "width": 150, "height": 150},
                    
                    "Chashu":{"Name":"Chashu","Type":"Topping","pos_x":700,"pos_y":100, "width": 150, "height": 150},
                    "Egg":{"Name":"Egg","Type":"Topping","pos_x":850,"pos_y":100, "width": 150, "height": 150},
                    "Green Onions":{"Name":"Green Onions","Type":"Topping","pos_x":700,"pos_y":250, "width": 150, "height": 150},
                    "Seaweed":{"Name":"Seaweed","Type":"Topping","pos_x":850,"pos_y":250, "width": 150, "height": 150}
                    }

for i in ingredients_list:
    ingredient = ingredients_list[i]
    ingredients_list[i] = Ingredients(ingredient["Name"], ingredient["Type"], ingredient["pos_x"], ingredient["pos_y"], ingredient["width"], ingredient["height"])


# anything that keeps going during the game should be inside this loopp!
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for key in ingredients_list:
                    item = ingredients_list[key]
                    if item.rect.collidepoint(event.pos):
                        item_being_dragged = item
                        mouse_x, mouse_y = event.pos # extracts the coordination of mouse only when clicked using (event.pos)
                        item_being_dragged.offset_x = item_being_dragged.rect.x - mouse_x
                        item_being_dragged.offset_y = item_being_dragged.rect.y - mouse_y  
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if item_being_dragged is not None:
                    if Active_bowl_rect.collidepoint(event.pos):
                        Active_bowl_list.append(item_being_dragged.name)
                        print(f"{item_being_dragged.name} added to the bowl!")
                    item_being_dragged.rect.x = item_being_dragged.pos_x
                    item_being_dragged.rect.y = item_being_dragged.pos_y
                    item_being_dragged = None
                    
                else:
                    item_being_dragged = None
                
                
        elif event.type == pygame.MOUSEMOTION:
            if item_being_dragged is not None:
                mouse_x, mouse_y = event.pos
                item_being_dragged.rect.x = mouse_x + item_being_dragged.offset_x
                item_being_dragged.rect.y = mouse_y + item_being_dragged.offset_y 


     #current_image = (250,100,100) if is_dragging else button_color
    
    screen.fill((255,210,138))
    screen.blit(pygame.transform.scale(pygame.image.load("Assets/Ramenbackground.png"),(1100,700)), (0,0))
    screen.blit(pygame.transform.scale(pygame.image.load("Assets/Ramen_bowl.png"),(400,300)), Active_bowl_rect)
    for key in ingredients_list:
        item = ingredients_list[key]
        current_image = item.image  #current_image = (250,100,100) if is_dragging else button_color
        screen.blit(current_image, item.rect)
    pygame.display.flip() #display.flip updates entirely while update only changes the parts changed
    clock.tick(60) #60 FPS

# Game logics

#Images, Rerndering

pygame.quit()
sys.exit()
