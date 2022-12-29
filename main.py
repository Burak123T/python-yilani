# Import and initialize the pygame library
import pygame, random

# Simple dificulty system
numEnemiesLimit = 3
score = 0
user_score = 0
speedMul= 3
scoreMul = 1
killedNum = 0
ticks = 0

# Run or not?
end = False
exit = False
exit_direct = False

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 750

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# List of all non-player sprites
bullet_list = pygame.sprite.Group()
enemies_list = pygame.sprite.Group();

# Set up the drawing window and name
screen = pygame.display.set_caption('Acebattle 2D v0.2')
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGTH])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("placeholder plane.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (115,90))
        self.image = self.surf
        self.mask = pygame.mask.from_surface( self.surf )
        self.rect = self.surf.get_rect()
        self.rect.x = (SCREEN_WIDTH/2) - 50
        self.rect.y = (SCREEN_HEIGTH/2) + 250

    # Going up/down is disabled
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-9, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(9, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGTH:
            self.rect.bottom = SCREEN_HEIGTH
    
    def reset(self):
        self.rect.x = (SCREEN_WIDTH/2) - 50
        self.rect.y = (SCREEN_HEIGTH/2) + 250

class Fire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("fire example 2.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (72, 72))
        self.image = self.surf
        self.mask = pygame.mask.from_surface( self.surf )
        self.rect = self.surf.get_rect()
        self.rect.x = player.rect.x + 20
        self.rect.y = player.rect.y - 40
        
    def update(self):
        self.rect.y -= 30

class EnemyBoat(pygame.sprite.Sprite):

    def __init__(self):  
        super().__init__()
        self.surf = pygame.image.load("placeholder enemy plane.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (80,60))
        self.image = self.surf
        self.mask = pygame.mask.from_surface( self.surf )
        self.image = self.surf
        self.rect = self.surf.get_rect()
        self.rect.y = -40
        self.speedMultiplier = speedMul
    
    def random_x(self, next_x):
        self.rect.x = next_x

    def update(self):
        self.speedMultiplier = speedMul
        self.rect.y += self.speedMultiplier

    def explode(self):
        self.surf = pygame.image.load("Fire4_1.png").convert_alpha()
    
    # Another difficulty increasing function
    def incrSpeed(self):
        global speedMul
        speedMul += 1

    def reset(self):
        global speedMul, scoreMul
        self.surf = pygame.image.load("placeholder enemy plane.png").convert_alpha()
        speedMul = 3
        scoreMul = 1
 
(numOfPass, numOfFail) = pygame.init()
pygame.mixer.init()

print("\n")

# Audio stuff
kill_sound = pygame.mixer.Sound("example explosion sound.wav")
bullet_sound = pygame.mixer.Sound("example bullet sound.wav")
level_incr_sound = pygame.mixer.Sound("example level increase sound.wav")
game_over_sound = pygame.mixer.Sound("example game over sound.wav")

print(" - Number of succesfully initialized imports:", numOfPass)

if numOfFail > 0:
    print("     - Number of failed imports:", numOfFail)
else:
    print("     - No failed imports")

# Create player object
player = Player()

# load the images/sprites
gameIcon = pygame.image.load("acebattle 2d game icon example 1.png")
background_one = pygame.image.load("sky wallpaper.jpg").convert()
#background_one = pygame.image.load("sea background.png").convert()
 
# set icon
pygame.display.set_icon(gameIcon)

###
# main loop
###

def main_loop():

    global end, exit, exit_direct, numEnemiesLimit, score, screen, speedMul, scoreMul, user_score, killedNum

    clock = pygame.time.Clock()

    while end == False:

        # Game speed
        clock.tick(100)

        CUSTOM_EVENT = pygame.USEREVENT+1
        my_event = pygame.event.Event(CUSTOM_EVENT, message="event added")
        pygame.event.post(my_event)
    
        # If user clicked the window close button
        for event in pygame.event.get(): 

            numOfBullets = len(bullet_list)
            numOfEnemies = len(enemies_list)
            x_pos = random.randint(20, 730)

            if event.type == QUIT:
                exit = True
                exit_direct = True
                end = True
            # Spawn enemies when needed
            if numOfEnemies < numEnemiesLimit:  
                boat = EnemyBoat()

                if (score > 0) and (score % 10 == 0):
                    pygame.mixer.Sound.play(level_incr_sound)
                    speedMul += 1
                    numEnemiesLimit += 2
                    score += 1
                    scoreMul += 2
                    print("     - Difficulty increased to:", str(numEnemiesLimit))
                    print("         - score modulo of", score-1)
                    print("         - SpeedMul:", str(speedMul))

                boat.random_x(x_pos)
                enemies_list.add(boat)
                numOfBullets = len(bullet_list)
                numOfEnemies = len(enemies_list)
            # Did the user hit a key ?
            if event.type == KEYDOWN:
                # Was it the Escape key, so stop the loop
                if event.key == K_ESCAPE:
                    end = True
                if event.key == K_SPACE:
                    if numOfBullets < 50:
                        # Bullet logic
                        pygame.mixer.Sound.play(bullet_sound)
                        bullet = Fire()
                        bullet_list.add(bullet)
  
        ### Game logic
        # If player collides with enemy
        if (pygame.sprite.spritecollide( player, enemies_list, False, collided=pygame.sprite.collide_mask )):
                pygame.mixer.Sound.play(game_over_sound)
                end = True
        else:
            if numOfEnemies > 0:
                for enemy in enemies_list:
                        # If bullet hits enemy
                        if (pygame.sprite.spritecollide( enemy, bullet_list, True, collided=pygame.sprite.collide_mask )):
                            enemy.explode()
                            killedNum += 1
                            score += 1
                            user_score += scoreMul
                            pygame.mixer.Sound.play(kill_sound)
                            #bullet_list.remove(bullet)
                            enemies_list.remove(enemy)
                            break
                        else:
                            for bullet in bullet_list:
                                if bullet.rect.y <= -20:
                                    bullet_list.remove(bullet)
                            if enemy.rect.y >= 800:
                                enemies_list.remove(enemy)
                                break
            else:
                boat = EnemyBoat()
                
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        # Update sprites
        player.update(pressed_keys)
        bullet_list.update() 
        enemies_list.update()

        # Blit and flip the display, objects
        screen.blit(background_one, (0,0))
        screen.blit(player.surf, player.rect)
        bullet_list.draw(screen)
        enemies_list.draw(screen)

        pygame.display.flip()


def restart():
    global enemies_list, bullet_list, player, score, screen, numEnemiesLimit, speedMul, user_score

    enemies_list.empty()
    bullet_list.empty()
    
    for enemy in enemies_list:
        enemy.reset()
    
    speedMul = 3

    score = 0
    user_score = 0
    screen = pygame.display.set_caption("Acebattle 2D v0.2")
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGTH])
    numEnemiesLimit = 3

while (exit == False) and (exit_direct == False):
    print(" - main loop start")
    main_loop()
    print("     - Score:", str(user_score))
    print("     - SpeedMul:", str(speedMul))
    screen = pygame.display.set_caption("Acebattle 2D v0.2        END SCORE: " + str(user_score))
    while (exit_direct == False) and (end == True):
     for event in pygame.event.get():
        if event.type == QUIT:
            exit_direct = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit_direct = True
            if event.key == K_UP:
                end = False
                exit = False
                exit_direct = False
                restart()

while exit_direct == False:
     for event in pygame.event.get():
        if event.type == QUIT:
            exit_direct = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit_direct = True

pygame.mixer.quit()

# Done! Time to quit.
print(" - Quit called")
pygame.quit()
print("     - Killed enemies in total:", str(killedNum))
print("         - End enemies length:", len(enemies_list))
print("         - End bullet length:", len(bullet_list))
print("\n")