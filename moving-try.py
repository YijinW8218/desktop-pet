import pygame
pygame.init()
import math

# set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Object Example")
clock = pygame.time.Clock()

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
    
        # Character attributes
        self.image = pygame.Surface((50, 50))  # create a square surface
        self.image.fill(color=(0, 255, 0, 255)) # fill it with green color
        # Character init position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Character init speed
        self.velocity_y = 0
        self.G_acceleration = 0.98 # reduced gravity acceleration
        self.is_jumping = False  # jump state
        self.velocity_x = 2
        # Animation variables
        self.is_in_air = False  # in-air state
        self.is_squashing = False  # squashing state
        self.squash_timer = 0
        self.squash_duration = 15 # frames
        self.width = 50
        self.height =50
        self.is_stretching = False  # stretching state
        self.stretch_timer = 0
        self.stretch_duration = 10


    def jump(self):
        if not self.is_jumping:  # only jump if not is jumping
            self.velocity_y = -12 # negative velocity to move up
            self.is_jumping = True
            # stretch animation
            if not self.is_stretching: # only start stretching if not already stretching
                self.is_stretching = True
                self.stretch_timer = 0
    
    def update(self):
        # update position
        self.velocity_y += self.G_acceleration
        self.rect.y += self.velocity_y

        # stretch animation
        self.stretch_animation()

        ## Vertical Movement

        # check for collision with screen boundaries
        # control velocity_y to avoid collision with the top
        # Check for ground collision and handle squash animation

        # set is_in_air flag when character leaves ground
        if self.rect.bottom < screen_height:
            self.is_in_air = True

        # check for ground collision
        if self.rect.bottom >= screen_height:
            # if it hits the bottom, stop falling
            self.rect.bottom = screen_height
            self.velocity_y = 0
            self.is_jumping = False
            
            # only squash if character was in air and not already squashing
            if self.is_in_air and not self.is_squashing:
                self.is_squashing = True
                self.squash_timer = 0
                self.is_in_air = False  # reset in-air state

        # handle squashing animation
        self.squash_animation()
            

        ## horizontal movement
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
                self.image.fill(color=(0, 255, 0, 255))
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
                self.image.fill(color=(0, 255, 0, 255))
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
                self.image.fill(color=(0, 255, 0, 255))

    
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
                self.image.fill(color=(0, 255, 0, 255))
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
                self.image.fill(color=(0, 255, 0, 255))
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
                self.image.fill(color=(0, 255, 0, 255))
            
        

    def draw(self, screen):
        # draw the character on the screen
        screen.blit(self.image, self.rect)

# create a object of Character
character = Character(x=screen_width//2, y=screen_height//2)  # initial position




# event loop
running = True
while running:
    # control game speed (60 FPS)
    clock.tick(60)
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_SPACE:  # if [space] is pressed
                character.jump()
    character.update() # update character position

    # fill the screen
    screen.fill((0, 0, 0))  # black background
    character.draw(screen)  # draw the character
    pygame.display.flip() # update the display

#quit pygame
pygame.quit()