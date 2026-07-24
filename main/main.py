import pygame
import sys
import random
import os
from collections import Counter

pygame.init()

#GLOBAL VARIABLES

#Screen size and caption
screen = pygame.display.set_mode((1100,700))
pygame.display.set_caption("Pygame Test")
#For FPS
clock = pygame.time.Clock()

duration = 30
start_ticks = pygame.time.get_ticks() 

scene = 1
#Scene 1
text_path = os.path.join("Assets","Fonts","Teko-Variable.ttf")
text_font = pygame.font.Font(text_path,36)

text_surface = text_font.render("Loading...", True, (0, 0, 0))
text_rect = text_surface.get_rect(center=(550, 350))

current_customer = None
current_customer_name = None
current_order = None
current_customer_image = None
customer_rect = pygame.Rect(180,100,200,350)
customer_is_talking = False
customer_is_grading = False

background_rect = pygame.Rect(0,0,1100,700)
background_image = pygame.image.load("Assets/scene1background.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (1100, 700))

cookbutton_rect = pygame.Rect(620,300,300,200)
cookbutton_image = pygame.image.load("Assets/cookbutton.png").convert_alpha()
cookbutton_hitbox = pygame.Rect(650,450,450,150)


speech_bubble_image = pygame.transform.scale(pygame.image.load("Assets/speechbubble.png").convert_alpha(),(450,300))
speech_bubble_image_rect = pygame.Rect(600,100,450,300)


table_rect = pygame.Rect(0,150,100,100)
table_image = pygame.image.load("Assets/table.png").convert_alpha()
table_image = pygame.transform.scale(table_image, (1100, 600))

dialogue_index = 0

current_score = 0
total_score = 0


#Scene 2
#varaiables for dragging
item_being_dragged = None

Active_bowl_list = {"Broth":None,
                    "Noodle":None,
                    "Toppings":[]
                    }
Active_bowl_rect = pygame.Rect(350,380, 400, 300)

nextbutton_rect = pygame.Rect(740,400,200,200)
nextbutton_image = pygame.image.load("Assets/cookbutton.png").convert_alpha()
nextbutton_hitbox = pygame.Rect(750,550,450,150)

#Scene 3
finishbutton_image = pygame.image.load("Assets/cookbutton.png").convert_alpha()
finishbutton_rect = pygame.Rect(620,300,300,200)
finishbutton_hitbox = pygame.Rect(650,450,450,150)
finished_serving = False

#Scene 4
restartbutton_image = pygame.image.load("Assets/cookbutton.png").convert_alpha()
restartbutton_rect = pygame.Rect(400,300,450,150)
restartbutton_hitbox = pygame.Rect(550,400,450,150)

Ramen_menu = {"Classic":{
                "Broth": "Shoyu Broth",
                "Noodles":"Wavy Noodles",
                "Toppings": ["Chashu","Egg","Green Onions","Seaweed"],
                "Price": 800},

                "Tonkotsu":{
                "Name": "Tonkotsu Ramen",
                "Broth": "Tonkotsu Broth",
                "Noodles" : "Straight Noodles",
                "Toppings": ["Chashu","Chashu","Egg","Seaweed"],
                "Price":900},

                "Miso":{
                "Name": "Miso Ramen",
                "Broth": "Miso Broth",
                "Noodles" : "Wavy Noodles",
                "Toppings": ["Chashu","Egg","Egg","Green Onions"],
                "Price": 850}
                }
class Customer:
    def __init__(self,name,patience):
        self.name = name
        self.state = 1 # 1=waiting, 2=angry, 3=leaves
        self.patience = patience
        self.order = None
        self.order_broth = None
        self.order_noodle = None
        self.order_toppings = None
        self.order_price = None
        self.image = pygame.image.load("Assets/"+name+".png").convert_alpha()
    
    def Make_order(self):
        self.order = random.choice(list(Ramen_menu))
        menu_details = Ramen_menu[self.order]
        self.order_broth = menu_details["Broth"]
        self.order_noodle = menu_details["Noodles"]
        self.order_toppings = menu_details["Toppings"]
        self.order_price = menu_details["Price"]

    def check_order(self):
        global current_score
        global total_score
        print (current_customer.order_broth,current_customer.order_noodle, current_customer.order_toppings)
        print (Active_bowl_list["Broth"],Active_bowl_list["Noodle"],Active_bowl_list["Toppings"])
        right_broth = False
        right_noodle = False
        if Active_bowl_list["Broth"] == current_customer.order_broth:
            print("right broth")
            right_broth = True
            current_score += 500
        if Active_bowl_list["Noodle"] == current_customer.order_noodle:
            print("right noodle")
            right_noodle = True
            current_score += 500
        if all(i in Active_bowl_list["Toppings"] for i in current_customer.order_toppings):
            print("all required topping is in here")
            if Counter(Active_bowl_list["Toppings"]) == Counter(current_customer.order_toppings) and right_broth and right_noodle:
                current_score += 1000
                print("All are right")

            else:
                extra = Counter(Active_bowl_list["Toppings"]) - Counter(current_customer.order_toppings)
                missing = Counter(current_customer.order_toppings) - Counter(Active_bowl_list["Toppings"])
                print(f"Missing: {missing} \n Extra: {extra})")
                for i in extra:
                    current_score -= 50
                for i in missing:
                    current_score -= 50
        total_score += current_score



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

    customer_rect.x = -300      


def Scene1_customer_talking():
    greeting_text = text_font.render(customer_dialogue[current_customer_name][dialogue_index].format(order=current_customer.order), True, (255,255,255))
    greeting_text_rect = greeting_text.get_rect(center = (810,220))
    screen.blit(speech_bubble_image, speech_bubble_image_rect)
    screen.blit(greeting_text,greeting_text_rect)
    screen.blit(cookbutton_image, cookbutton_rect)

def Scene3_customer_talking():
    score_text = text_font.render("Score: "+ str(current_score), True, (255,255,255))
    score_text_rect = score_text.get_rect(center = (810,220))
    feedback_text = text_font.render("Good job", True, (255,255,255))
    feedback_text_rect = feedback_text.get_rect(center = (810,270))
    screen.blit(speech_bubble_image, speech_bubble_image_rect)
    screen.blit(score_text,score_text_rect)
    screen.blit(feedback_text,feedback_text_rect)
    screen.blit(finishbutton_image, finishbutton_rect)

def reset_bowl(bowl):
    bowl["Broth"] = None
    bowl["Noodle"] = None
    bowl["Toppings"] = []



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
        self.image = pygame.transform.scale(pygame.image.load("Assets/"+self.name+".png"), (150, 150))


ingredients_list = {
                    "Wavy Noodles":{"Name":"Wavy Noodles","Type":"Noodle","pos_x":100,"pos_y":100, "width": 150, "height": 150},
                    "Straight Noodles":{"Name":"Straight Noodles","Type":"Noodle","pos_x":250,"pos_y":100, "width": 150, "height": 150},
                    
                    "Shoyu Broth":{"Name":"Shoyu Broth","Type":"Broth","pos_x":400,"pos_y":100, "width": 150, "height": 150},
                    "Tonkotsu Broth":{"Name":"Tonkotsu Broth","Type":"Broth","pos_x":550,"pos_y":100, "width": 150, "height": 150},
                    "Miso Broth":{"Name":"Miso Broth","Type":"Broth","pos_x":400,"pos_y":250, "width": 150, "height": 150},
                    
                    "Chashu":{"Name":"Chashu","Type":"Toppings","pos_x":700,"pos_y":100, "width": 150, "height": 150},
                    "Egg":{"Name":"Egg","Type":"Toppings","pos_x":850,"pos_y":100, "width": 150, "height": 150},
                    "Green Onions":{"Name":"Green Onions","Type":"Toppings","pos_x":700,"pos_y":250, "width": 150, "height": 150},
                    "Seaweed":{"Name":"Seaweed","Type":"Toppings","pos_x":850,"pos_y":250, "width": 150, "height": 150}
                    }

for i in ingredients_list:
    ingredient = ingredients_list[i]
    ingredients_list[i] = Ingredients(ingredient["Name"], ingredient["Type"], ingredient["pos_x"], ingredient["pos_y"], ingredient["width"], ingredient["height"])


# anything that keeps going during the game should be inside this loopp!
running = True
while running:
    if scene != 4:
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = duration - seconds_passed
        timer_text = text_font.render(f"Time: {time_left:.0f}", True, (255, 255, 255))
    if time_left <= 0:
        scene = 4
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if scene == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if background_rect.collidepoint(event.pos) and customer_is_talking:
                        if dialogue_index < len(customer_dialogue[current_customer_name])-1:
                            dialogue_index += 1              
                        else:
                            customer_is_talking = False

                    if cookbutton_hitbox.collidepoint(event.pos) and customer_is_talking is not True:
                        scene = 2
                        dialogue_index = 0         
                        print ("now it's scene 2")
        elif scene == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for key in ingredients_list:
                        item = ingredients_list[key]
                        if item.rect.collidepoint(event.pos):
                            item_being_dragged = item
                            mouse_x, mouse_y = event.pos # extracts the coordination of mouse only when clicked using (event.pos)
                            item_being_dragged.offset_x = item_being_dragged.rect.x - mouse_x
                            item_being_dragged.offset_y = item_being_dragged.rect.y - mouse_y  
                            break
                        if nextbutton_hitbox.collidepoint(event.pos):
                            if scene == 2:
                                scene = 3
                                print("scene is now 3")
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if item_being_dragged is not None:
                        if Active_bowl_rect.collidepoint(event.pos): 
                            try:
                                Active_bowl_list[item_being_dragged.type].append(item_being_dragged.name)
                            except:
                                Active_bowl_list[item_being_dragged.type] = item_being_dragged.name
                            print(Active_bowl_list)
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

        elif scene == 3:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if finishbutton_hitbox.collidepoint(event.pos):
                        finished_serving = True
        elif scene == 4:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if restartbutton_hitbox.collidepoint(event.pos):
                        start_ticks = pygame.time.get_ticks() 
                        reset_bowl(Active_bowl_list)
                        current_score = 0
                        customer_is_grading = False
                        finished_serving = False
                        current_customer = None
                        dialogue_index = 0
                        scene = 1

                       
    #めんだこ…takotako

    if scene == 1:
        if current_customer is None:
            Spawn_customer()

        if current_customer is not None:       
            target_x = 180
            speed = 10
            if customer_rect.x < target_x:
                customer_rect.x += speed
        
        screen.blit(background_image, background_rect)
        screen.blit(current_customer_image, customer_rect)
        screen.blit(table_image, table_rect)
        screen.blit(timer_text, (80, 100))

        if customer_rect.x==target_x:
            customer_is_talking = True
        if customer_is_talking == True:
            Scene1_customer_talking() 
        if customer_is_talking == False:
            cookbutton_rect = pygame.Rect(620,300,300,200)

           
    
    if scene == 2:
        screen.fill((255,210,138))
        screen.blit(pygame.transform.scale(pygame.image.load("Assets/Ramenbackground.png"),(1100,700)), (0,0))
        screen.blit(pygame.transform.scale(pygame.image.load("Assets/Ramen_bowl.png"),(400,300)), Active_bowl_rect)
        for key in ingredients_list:
            item = ingredients_list[key]
            current_image = item.image  #current_image = (250,100,100) if is_dragging else button_color
            screen.blit(current_image, item.rect)
        screen.blit(nextbutton_image,nextbutton_rect)
        screen.blit(timer_text, (100, 50))

    if scene == 3:
        if customer_is_grading is False:
            current_customer.check_order()
            customer_is_grading = True
        screen.blit(background_image, background_rect)
        screen.blit(current_customer_image, customer_rect)
        screen.blit(table_image, table_rect)
        screen.blit(timer_text, (80, 100))
        Scene3_customer_talking() 

        if finished_serving is True:       
            target_x = -700
            speed = 10
            if customer_rect.x > target_x:
                customer_rect.x -= speed
            if customer_rect.x == target_x:
                reset_bowl(Active_bowl_list)
                current_score = 0
                customer_is_grading = False
                finished_serving = False
                current_customer = None
                scene = 1
    if scene == 4:
        total_score_text = text_font.render(str(total_score),True, (0,0,0))
        screen.blit(background_image, background_rect)
        pygame.draw.rect(screen,(255,255,255), (400, 250, 350, 150))
        screen.blit(total_score_text, (555, 300))
        screen.blit(restartbutton_image, restartbutton_rect)



    
    
    pygame.display.flip() #display.flip updates entirely while update only changes the parts changed
    clock.tick(60) #60 FPS



pygame.quit()
sys.exit()

