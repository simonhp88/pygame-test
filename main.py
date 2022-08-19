# Import the pygame module
import pygame
# Import time,sys module
import time, sys
# Import random for random numbers
import random
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define variables for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a Player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Use jet.png for Player and convert the altha channel for transparancy
        self.surf = pygame.image.load("jet.png").convert_alpha()
        # Resize the player sprite
        self.surf = pygame.transform.scale(self.surf, (50, 40))
        # Set Spawn to center screen on the most left
        self.rect = self.surf.get_rect(center=(0,(SCREEN_HEIGHT/2)-40,))
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            # Move sprite up 5 pixels
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            # Move sprite down 5 pixels
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            # Move sprite left 5 pixels
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            # Move sprite right 5 pixels
            self.rect.move_ip(5, 0)

        # if sprite x y coords are = < 0 then set them to boundry values to keep on scren
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # Use missile.png for Enemy and convert the altha channel for transparancy
        self.surf = pygame.image.load("missile.png").convert_alpha()
        # Resize the missle image
        self.surf = pygame.transform.scale(self.surf, (60, 30)) 
        # Set random spawn location just off screen
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        #Set random speed for instance of enemy
        self.speed = random.randint(5, 10)

    # Move the sprite based on speed
    def update(self):
        global score
        self.rect.move_ip(-self.speed, 0)
        # Remove the sprite when it passes the left edge of the screen
        if self.rect.right < 0:
            # Add to the Score value if the sprite leaves the screen
            score += 1
            self.kill()

# Define the cloud object
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        # Use cloud.png for cloud and convert the altha channel for transparancy
        self.surf = pygame.image.load("cloud.png").convert_alpha()
        # Resize the cloud image
        self.surf = pygame.transform.scale(self.surf, (80, 40)) 
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                #Set the height of clouds at least half way up the screen so there not ground level
                random.randint(0, SCREEN_HEIGHT/2),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Define the background object
class Background():
    def __init__(self):
        # use BG.png for the background
        self.bgimage = pygame.image.load('BG.png')
        self.rectBGimg = self.bgimage.get_rect()
        #Set XY coords for first image
        self.bgY1 = 0
        self.bgX1 = 0
        #Set XY for trailing image
        self.bgY2 = 0
        #Set X of trailing image to end of the first image
        self.bgX2 = self.rectBGimg.width
        #Set the moving speed
        self.moving_speed = 2
    # On update calculate new XY Coords to slowly move both images
    def update(self):
        self.bgX1 -= self.moving_speed
        self.bgX2 -= self.moving_speed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width
    #Once new XY coords are set render both images
    def render(self):
        screen.blit(self.bgimage, (self.bgX1, self.bgY1))
        screen.blit(self.bgimage, (self.bgX2, self.bgY2))

# Initialize pygame
pygame.init()
# Setup for sounds.
pygame.mixer.init()
# Setup for fonts.
pygame.font.init()
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Set the Score value
score = 0
#Set the font and size from system font
my_font = pygame.font.SysFont('Arial', 30)
# Load and play background music
pygame.mixer.music.load("background music.mp3")
#Set the volume so ears don't hurt
pygame.mixer.music.set_volume(0.1)
#Make it loop
pygame.mixer.music.play(loops=-1)
# Set the Collision sound
collision_sound = pygame.mixer.Sound("Collision.flac")
#Set the volue
collision_sound.set_volume(0.3)
# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
#Create timer to randomly spawn enemy
pygame.time.set_timer(ADDENEMY, 250)
#Create custom event for clouds to spawn
ADDCLOUD = pygame.USEREVENT + 2
#Create timer for clouds
pygame.time.set_timer(ADDCLOUD, 1000)
#Spawn the background
back_ground = Background()
# Instantiate player.
player = Player()
# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True
# Setup the clock for a decent framerate
clock = pygame.time.Clock()
# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
                # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
                # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    # Update object positions
    back_ground.update()
    back_ground.render()
    enemies.update()
    clouds.update()

    # Fill the screen with black
    #Set the Score value
    scoretext = my_font.render("Score {0}".format(score), 1, (0,0,0))
    #Send new score value on screen
    screen.blit(scoretext, (5, 10))
    # Draw all sprites in groups
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    #Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, play collision sound, pause to allow the sound to actually play
        collision_sound.play()
        time.sleep(1)
        # Kill the player
        player.kill()
        #Stop the music
        pygame.mixer.music.stop()
        #Safely quit the mixer properly
        pygame.mixer.quit()
        #Exit :(
        running = False
    #Update the display
    pygame.display.flip()
    # Ensure program maintains a rate of 60 frames per second
    clock.tick(60) / 1000
    # All done! Stop and quit the mixer.