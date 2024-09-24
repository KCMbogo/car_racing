import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (100, 100, 100)

pygame.init()
pygame.font.init()

text_font = pygame.font.SysFont("Comic Sans MS", 40)

clock = pygame.time.Clock()
size = width, height = 700, 680
road_width = 512
screen = pygame.display.set_mode(size)

pygame.display.set_caption("MBOGO'S DODGE CAR)")

road_speed = 1
road = pygame.image.load("image/road1.jpg")
road = pygame.transform.scale(road, (road_width, height))

# Road background positioning for scrolling
road_y1 = 0
road_y2 = -height

# car sizes
car_width, car_height = 80, 60
truck_width, truck_height = 150, 100
van_width, van_height = 100, 80

# player's car
player_car = pygame.image.load("image/car.svg")
player_car = pygame.transform.scale(player_car, (car_width, car_height))
player_car = pygame.transform.rotate(player_car, 90)
car_x = (width / 2) - (car_width / 2)
car_y = height - car_height - 20
car_speed = 2

# opposing cars
opposing_car_images = [
    pygame.transform.rotate(pygame.transform.scale(pygame.image.load("image/car2.png"), (car_width, car_height)), 90),
    pygame.transform.rotate(pygame.transform.scale(pygame.image.load("image/truck.png"), (truck_width, truck_height)), -90),
    pygame.transform.rotate(pygame.transform.scale(pygame.image.load("image/car1.svg"), (van_width, van_height)), -90),
]
opposing_car_speed = 2 
num_opposing_cars = 5  

opposing_cars = []

# Lane positions calculated to align the cars in each lane
lane_positions = [24, 152, 280, 408]  # Pre-calculated x-positions for each lane
min_gap = 200  # Minimum gap between cars in the same lane 

def can_spawn_in_lane(lane_x, min_gap):
    for car in opposing_cars:
        if car[0] == lane_x and car[1] < min_gap:
            return False
    return True

crash_sound = pygame.mixer.Sound("sound/crush.flac")
game_sound = pygame.mixer.Sound("sound/game.ogg")
game_sound.play(-1)
crash_sound_played = False

# score
score = 0

running = True
game_over = False
start_time = pygame.time.get_ticks()
last_elapsed_time = 0

while running:
    if not game_over:
        elapsed_time = pygame.time.get_ticks() - start_time
        elapsed_time_to_sec = elapsed_time / 1000
        
        if elapsed_time_to_sec - last_elapsed_time >= 5:
            car_speed += 1
            opposing_car_speed += 1
            road_speed += .5
            score += 5
            last_elapsed_time = elapsed_time_to_sec
        
    pressed = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pressed[pygame.K_q] or pressed[pygame.K_ESCAPE]:
            running = False
        
    # Car movement
    if not game_over:
        if pressed[pygame.K_UP] and car_y > 0:
            car_y -= car_speed  
        if pressed[pygame.K_DOWN] and car_y < height - car_height - 20:
            car_y += car_speed 
        if pressed[pygame.K_RIGHT] and car_x < road_width - car_width:
            car_x += car_speed 
        if pressed[pygame.K_LEFT] and car_x > 20:
            car_x -= car_speed 

    # Check each lane if we can spawn a new car with proper spacing
    for lane_x in lane_positions:
        if can_spawn_in_lane(lane_x, min_gap):
            if random.random() < 0.01:  # Small chance to spawn a car in any given frame
                opposing_y = random.randint(-600, -100)  
                car_image = random.choice(opposing_car_images)
                opposing_cars.append([lane_x, opposing_y, car_image])
    
    # Move the opposing cars down and respawn them when off-screen
    for car in opposing_cars:
        car[1] += opposing_car_speed  
        # check for collision
        # opposing_rect = pygame.Rect(car[0], car[1], car_width, car_height)
        # player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        
        # if player_rect.colliderect(opposing_rect):
        #     game_sound.stop()
        #     game_over = True  
        player_car_mask = pygame.mask.from_surface(player_car)
        opposing_car_mask = pygame.mask.from_surface(car[2])
        
        offset = (car[0] - car_x, car[1] - car_y)   
        
        if player_car_mask.overlap(opposing_car_mask, offset):
            game_sound.stop()
            game_over = True 
            if not crash_sound_played:
                crash_sound.play()
                crash_sound_played = True
        
        # Remove and respawn the car once it goes off the bottom of the screen
        if car[1] > height:#WHITE
            opposing_cars.remove(car)   
            # Respawn in a new random lane with a gap
            new_lane = random.choice(lane_positions)
            if can_spawn_in_lane(new_lane, min_gap):
                if random.random() < 0.01:
                    new_opposing_y = random.randint(-600, -100)
                    new_car_image = random.choice(opposing_car_images)
                    opposing_cars.append([new_lane, new_opposing_y, new_car_image])
    
    # Move the road to create scrolling effectWHITE
    road_y1 += road_speed
    road_y2 += road_speed     
    
    # Reset the road position once it scrolls completely
    if road_y1 >= height:
        road_y1 = road_y2 - height 
    if road_y2 >= height:
        road_y2 = road_y1 - height
    
    score_value = text_font.render("Your score:" + "\n" + str(score), True, WHITE)
    score_text = text_font.render("Your Score:", True, WHITE)
    scored_value = text_font.render(str(score), True, WHITE)
    
    if game_over == False:
        screen.fill(GREY)
        
        screen.blit(road, (0, road_y1))
        screen.blit(road, (0, road_y2))
        screen.blit(player_car, (car_x, car_y))
        
        for car in opposing_cars:
            screen.blit(car[2], (car[0], car[1]))  
            
        screen.blit(score_text, (road_width + 2, 10)) 
        screen.blit(scored_value, (road_width + (width - road_width) / 2, 50)) 
           
    else:
        text_game_over = text_font.render("GAME OVER", True, BLACK)
        options = text_font.render("Press ENTER to play or ESC to quit", True, BLACK)
        
        text_game_over_rect = text_game_over.get_rect(center=(width / 2, height / 2 - 20))
        options_rect = options.get_rect(center=(width / 2, height / 2 + 20))
        score_rect = score_value.get_rect(center=(width / 2, height / 2 +60))
        screen.blit(text_game_over, text_game_over_rect)
        screen.blit(options, options_rect)
        screen.blit(score_value, score_rect)
        
        if pressed[pygame.K_RETURN]:
            crash_sound_played = False
            game_over = False
            car_x = (width / 2) - (car_width / 2)
            car_y = height - car_height - 20
            opposing_cars = []
            car_speed, opposing_car_speed = 2, 2
            road_speed = 1
            game_sound.play(-1)
        elif pressed[pygame.K_ESCAPE]:
            running = False
        
    pygame.display.flip()
    
 
    clock.tick(60)

pygame.quit()
