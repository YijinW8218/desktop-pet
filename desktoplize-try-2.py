import pygame
import math
import os
import random
import time
pygame.init()

# set up the display
Info = pygame.display.Info()
screen_width = int(Info.current_w) # get 2/3 of the current screen width
screen_height = 130

# Set window attributes for Mac OS
if os.name == 'posix':
    info = pygame.display.Info()
    os.environ['SDL_WINDOW_POSITIONED'] = '1'
    # position window above dock(typically dock is 70px)
    dock_height = 70
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"0,{info.current_h - screen_height - dock_height}"

# set up window with no frame and with transparency support
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("Desktop Pet")
clock = pygame.time.Clock()





class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
    
        # Character attributes
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)  # create a surface with alpha
        self.image.fill(color=(67, 137, 87))
        # Character init position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Character physics properties
        self.velocity_y = 0  # initial vertical speed
        self.G_acceleration = 0.98 # gravity acceleration
        self.velocity_x = 2  # initial horizontal speed
        self.velocity_boost = 10  # boosting speed
        # Animation variables
        self.squash_timer = 0
        self.squash_duration = 15 # frames
        self.width = 50  # used to the shapes' change
        self.height =50
        self.stretch_timer = 0
        self.stretch_duration = 10
        # Interaction status
        self.is_jumping = False  # jump state
        self.is_squashing = False  # squashing state
        self.is_stretching = False  # stretching state
        self.is_in_air = False  # in-air state
        self.is_boosting = False  # boosting state


    def jump(self):
        if not self.is_jumping:  # only jump if not already jumping
            self.velocity_y = -11 # negative velocity to move up
            self.is_jumping = True
            # stretch animation: caused by jumping
            if not self.is_stretching: # only start stretching if not already stretching
                self.is_stretching = True
                self.stretch_timer = 0

    def boost(self, is_boosting):
        if is_boosting:
            self.velocity_x = self.velocity_boost if self.velocity_x > 0 else -self.velocity_boost
        else:
            self.velocity_x = 2 if self.velocity_x > 0 else -2
    
    def update(self):
        # update vertical position with gravity
        self.velocity_y += self.G_acceleration
        self.rect.y += self.velocity_y

        # handle stretch animation
        self.stretch_animation()

        ## Vertical Movement

        # check for collision with screen boundaries
        # control velocity_y to avoid collision with the top
        # Check for ground collision and handle squash animation

        # track if character is in air
        if self.rect.bottom < screen_height:
            self.is_in_air = True

        # ground collision detection
        if self.rect.bottom >= screen_height:
            # if it hits the bottom, stop falling
            self.rect.bottom = screen_height
            self.velocity_y = 0
            self.is_jumping = False
            
            # only squash only on landling (character was in air and not already squashing)
            if self.is_in_air and not self.is_squashing:
                self.is_squashing = True
                self.squash_timer = 0
                self.is_in_air = False  # reset in-air state

        # handle squashing animation
        self.squash_animation()
            

        ## Horizontal Movement
        self.rect.x += self.velocity_x
        # check for collision with screen boundaries
        if self.rect.right >= screen_width:
            # if it hits the right side, turn around
            self.rect.right = screen_width
            self.velocity_x = -self.velocity_x
        elif self.rect.left <= 0:
            # if it hits the left side, turn around
            self.rect.left = 0
            self.velocity_x = -self.velocity_x

    def squash_animation(self):
        if self.is_squashing:  # timer
            self.squash_timer += 1
            progress = self.squash_timer / self.squash_duration
            if progress <= 1:
                # Squash phase
                smooth_progress = math.sin(progress * math.pi / 2)
                self.width = 50 + (10 * smooth_progress) # 50 to 60
                self.height = 50 - (10 * smooth_progress) # 50 to 40
                # update image with new dimensions
                self.image = pygame.Surface((int(self.width), int(self.height)))
                self.image.fill(color=(67, 137, 87))
                # keep bottom position constant while updating rect
                bottom = self.rect.bottom
                x = self.rect.x
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.x = x
            elif progress <= 2:
                # recovery phase
                smooth_progress = math.sin((2 - progress) * math.pi / 2)
                self.width = 50 + (10 * smooth_progress)  # 60 back to 50
                self.height = 50 - (10 * smooth_progress)  # 40 back to 50
                # update image with new dimensions
                self.image = pygame.Surface((int(self.width), int(self.height)))
                self.image.fill(color=(67, 137, 87))
                # keep bottom position constant while updating rect
                bottom = self.rect.bottom
                x = self.rect.x
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.x = x
            else:
                # reset animation
                self.is_squashing = False
                self.width = 50
                self.height = 50
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill(color=(67, 137, 87))

    
    def stretch_animation(self):
        if self.is_stretching:
            self.stretch_timer += 1
            progress = self.stretch_timer / self.stretch_duration
            if progress <= 1:
                # stretch phase
                smooth_progress = math.sin(progress * math.pi / 2)
                self.width = 50 - (10 * smooth_progress) # 50 to 40
                self.height = 50 + (10 * smooth_progress) # 50 to 60
                # update image with new dimensions
                self.image = pygame.Surface((int(self.width), int(self.height)))
                self.image.fill(color=(67, 137, 87))
                # keep bottom position constant while updating rect
                bottom = self.rect.bottom
                x = self.rect.x
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.x = x
            elif progress <= 2:
                # recovery phase
                smooth_progress = math.sin((2 - progress) * math.pi / 2)
                self.width = 50 - (10 * smooth_progress) # 40 back to 50
                self.height = 50 + (10 * smooth_progress) # 60 back to 50
                # update image with new dimensions
                self.image = pygame.Surface((int(self.width), int(self.height)))
                self.image.fill(color=(67, 137, 87))
                # keep bottom position constant while updating rect
                bottom = self.rect.bottom
                x = self.rect.x
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.x = x
            else:
                # reset animation
                self.is_stretching = False
                self.width = 50
                self.height = 50
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill(color=(67, 137, 87))
            
        

    def draw(self, screen):
        # draw the character on the screen
        screen.blit(self.image, self.rect)



class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # white

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True  # button clicked


class Fish:
    def __init__(self):
        # Fish attributes
        self.size = 20
        self.image = pygame.Surface((self.size, self.size))
        # Random color (R,G,B)
        self.color = (random.randint(0,255),
                       random.randint(0,255),
                       random.randint(0,255))
        self.image.fill(self.color)

        # Random position (avoid screen edges)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(self.size, screen_width - self.size)
        self.rect.y = random.randint(self.size, screen_height - self.size)

        # Time management
        self.spawn_time = time.time()  # record the time when the fish is spawned
        # Random disappear time between 60s and 120s
        self.lifetime = random.uniform(60,120)
        self.alive = True

        # Movement properties
        self.velocity = 0
        self.movement_timer = time.time()  # record the last time the fish moved
        self.movement_interval = random.uniform(1, 5)  # change direction every 1-5s
        self.possible_speeds = [-2, 0, 2]  # possible speeds for movement

    def update(self):
        # check lifetime
        current_time = time.time()  # get current time
        if current_time - self.spawn_time >= self.lifetime:
            self.alive = False
            return

        # update movement
        if current_time - self.movement_timer >= self.movement_interval:
            # get a random speed
            self.velocity = random.choice(self.possible_speeds)
            # update the movement timer
            self.movement_timer = current_time
            self.movement_interval = random.uniform(1, 5)  # reset the interval
        self.rect.x += self.velocity  # move the fish horizontally

        # screen boundary collision
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
            self.velocity = -abs(self.velocity)  # makesure to move backwards(left)
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.velocity = abs(self.velocity)  # makesure to move right

    def draw(self, screen):
        screen.blit(self.image, self.rect)



# create a object of Character
character = Character(x=100, y=screen_height-25)  # initial position

# create a object of Button
button_size = 30
button_margin = 10
button_setting = Button(
    x=screen_width - button_size - button_margin,
    y=screen_height - button_size - button_margin,
    width=button_size,
    height=button_size)

# fish management
fish_list = []
last_fish_spawn_time = time.time() # record the last time a fish was spawned
fish_spawn_interval = random.uniform(10, 60)  # spawn a new fish every 10-80 s



# event loop
running = True
while running:
    # control game speed (60 FPS)
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if button_setting.handle_event(event):  # click button_setting to call setting window
            print("Button clicked!")
        
        elif event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_SPACE:  # if [space] is pressed
                character.jump()
            elif event.key == pygame.K_ESCAPE:  # Add ESC key to quit
                running = False
        elif event.type == pygame.KEYUP:  # release SHIFT to stop boosting
            if event.key == pygame.K_LSHIFT:
                character.boost(is_boosting=False)
                character.is_boosting = False #
    # knowledge: KEYDOWN/KEYUP/get_pressed

    # pressing left SHIFT remains boosting status
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        character.boost(is_boosting=True)
        character.is_boosting = True

    character.update() # update character position

    # Fish spawing and management
    current_time = time.time()
    if current_time - last_fish_spawn_time >= fish_spawn_interval:  # check if it's time to spawn a new fish
        fish_list.append(Fish())  # create a new fish and add it to the list
        last_fish_spawn_time = current_time  # update the last spawn time
        fish_spawn_interval = random.uniform(10,60)  # reset the spawn interval to a new random value
        
    for fish in fish_list[:]:
        fish.update() 
        if not fish.alive:
            fish_list.remove(fish)  # remove dead fish
    if len(fish_list) > 10:  # limit the number of fish to 10
        fish_list.remove(fish_list[0])
    

    # fill and draw
    screen.fill((60, 90, 120))  # background color
    character.draw(screen)  # draw the character
    for fish in fish_list:
        fish.draw(screen)  # draw living fish
    button_setting.draw(screen)  # draw the button
    pygame.display.flip() # update the display

#quit pygame
pygame.quit()
