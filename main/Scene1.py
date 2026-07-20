import pygame
import sys
import random

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

Ramen_menu = {"Classic":{
                "Broth": "Shoyu",
                "Noodles":"wavy",
                "Toppings": ["Chashu","egg","Green Onions","Seaweed"],
                "Price": 800},

                "Tonkotsu":{
                "Name": "Tonkotsu Ramen",
                "Broth": "Tonkotsu",
                "Noodles" : "straight",
                "Toppings": ["Chashu","Chashu","egg","Seaweed"],
                "Price":900},

                "Miso":{
                "Name": "Miso Ramen",
                "Broth": "Miso",
                "Noodles" : "wavy",
                "Toppings": ["Chashu","egg","egg","Green Onions"],
                "Price": 850}
                }
class Customer:
    def __init__(self,name,patience):
        self.name = name
        self.state = 1 # 1=waiting, 2=angry, 3=leaves
        self.patience = patience
        self.order_broth = None
        self.order_noodles = None
        self.order_toppings = None
        self.order_price = None
        self.current_score = 0
    
    def Make_order(self):
        self.order = random.choice(Ramen_menu)
        menu_details = Ramen_menu[self.order]
        self.order_broth = menu_details["Broth"]
        self.order_noodles = menu_details["Noodles"]
        self.order_toppings = menu_details["Toppings"]
        self.order_price = menu_details["Price"]

    def check_order(self):
        pass

    def patince_timer(self):
        if self.state == 1:
            pass

    def score_calc(self):
        pass


Customer_list = {"Sarah":{"Name":"Sarah","Patience":45},
                 "Nana":{"Name":"Nana", "Patience":50},
                 "Matt":{"Name":"Matt","Patience":40},
                 "Layne":{"Name":"Layne","Patience":35}}

for i in Customer_list:
    Customerr = Customer_list[i]
    Customer_list[i] = Customer(Customerr["Name"],Customerr["Patience"])

def Spawn_customer():
    current_customer = random.choice(Customer_list)
    greetings_text = text_font.render("Hello",True, (0,0,0))
    current_order = current_customer.Make_order

    pass












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
