import pygame
import sys
import random
import os

pygame.init()
screen = pygame.display.set_mode((1100,700))
pygame.display.set_caption("Scene 1")
clock = pygame.time.Clock()

scene = 1

text_path = os.path.join("Assets","Fonts","Teko-Variable.ttf")
text_font = pygame.font.Font(text_path,36)

text_surface = text_font.render("Loading...", True, (0, 0, 0))
text_rect = text_surface.get_rect(center=(550, 350))

greeting_text = text_font.render("Hello",True, (0,0,0))
greeting_rect = greeting_text.get_rect(center = (520,350))

current_customer = None
current_customer_name = None
current_order = None
current_customer_image = None
customer_rect = pygame.Rect(180,100,200,350)
customer_is_talking = False


background_image = pygame.image.load("Assets/scene1background.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (1100, 700))
background_rect = background_image.get_rect()

cookbutton_rect = pygame.Rect(620,300,200,200)
cookbutton_image = pygame.image.load("Assets/cookbutton.png").convert_alpha()

speech_bubble_image = pygame.transform.scale(pygame.image.load("Assets/speechbubble.png").convert_alpha(),(450,300))
speech_bubble_image_rect = pygame.Rect(600,100,450,300)


table_rect = pygame.Rect(0,150,100,100)
table_image = pygame.image.load("Assets/table.png").convert_alpha()
table_image = pygame.transform.scale(table_image, (1100, 600))

dialogue_index = 0

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
        self.order = None
        self.order_broth = None
        self.order_noodles = None
        self.order_toppings = None
        self.order_price = None
        self.current_score = 0
        self.image = pygame.image.load("Assets/"+name+".png").convert_alpha()
    
    def Make_order(self):
        self.order = random.choice(list(Ramen_menu))
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


customer_list = {"Sarah":{"Name":"Sarah","Patience":45},
                 "Nana":{"Name":"Nana", "Patience":50},
                 "Matt":{"Name":"Matt","Patience":40},
                 "Layne":{"Name":"Layne","Patience":35}}

customer_dialogue = {"Sarah":["Hello","It's such a good weather today, isn't it?","I would like to have {order}","Thanks"],
                     "Nana":["Meep (Hello human)","Meep","Meep (I would like to have {order})", "Meep (Don't make me disappointed)"],
                     "Matt":["Hi","Do you allow smoking here?","Jk, anyway I want {order}","Thanks man"],
                     "Layne": ["Hello...","...No sweets menu here...?","Okay...I would like to have {order}","Please...Thanks"]}

for i in customer_list:
    Customerr = customer_list[i]
    customer_list[i] = Customer(Customerr["Name"],Customerr["Patience"])


def Spawn_customer():
    global current_customer
    global current_customer_image 
    global customer_rect 
    global current_customer_name
    global current_order

    current_customer = random.choice(list(customer_list.values()))
    current_customer_name = current_customer.name
    order = current_customer.Make_order()
    current_customer_image = current_customer.image
    current_order = current_customer.order
    print (current_customer.order)

    customer_rect.x = -400      


def Customer_talking():
    greeting_text = text_font.render(customer_dialogue[current_customer_name][dialogue_index].format(order=current_customer.order), True, (255,255,255))
    greeting_text_rect = greeting_text.get_rect(center = (810,220))
    screen.blit(speech_bubble_image, speech_bubble_image_rect)
    screen.blit(greeting_text,greeting_text_rect)









running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if scene == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if background_rect.collidepoint(event.pos) and customer_is_talking is True:
                        if dialogue_index < len(customer_dialogue)-1:
                            dialogue_index += 1
                        


                    if cookbutton_rect.collidepoint(event.pos):
                        scene = 2
                    

    if current_customer is None:
        Spawn_customer()
                

    if current_customer is not None:       
        target_x = 180
        speed = 5
        if customer_rect.x < target_x:
            customer_rect.x += speed
        if customer_rect.x==target_x and customer_is_talking == False:
            customer_is_talking = True           
        

    if scene == 1:
        screen.blit(background_image, background_rect)
        screen.blit(current_customer_image, customer_rect)
        screen.blit(table_image, table_rect)
        screen.blit(cookbutton_image, cookbutton_rect)
    
    if customer_is_talking == True:
        Customer_talking()
            
    if scene ==2:
        screen.fill((255,210,138))
        screen.blit(text_surface, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
