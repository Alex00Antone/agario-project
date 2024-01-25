'''
Tutorial demonstrates how to create a game window with Python Pygame.

Any pygame program that you create will have this basic code
'''

import math
import random
import pygame
import sys

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Tutorial")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create clock to later control frame rate
clock = pygame.time.Clock()

class Food(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Food, self).__init__()
        self.index = 0
        self.radius = 5
        self.x = random.randint(75,725)
        self.y = random.randint(75,525)
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect_center = (self.x, self.y)
        self.speed = math.log(self.radius)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.x = random.randint(75, 725)
        self.y = random.randint(75, 525)
        self.radius = random.randint(10, 25)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32) 
        self.image = self.image.convert_alpha()
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 128)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.rect_center = (self.x, self.y)
        self.deltax = 0
        self.deltay = 0
        

    def move(self, count):
        if count %60 == 0:
            self.deltax =random.randint(-100, 100)/(20*math.log(self.radius))
            self.deltay =random.randint(-100, 100)/(20*math.log(self.radius))
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.deltax *= -1
        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.deltay *= -1

        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay
        self.rect_center = (self.rect.centerx, self.rect.centery)

    def collisionDetector(self, enemyrect_center, enemyradius):
        if math.dist(self.rect_center, enemyrect_center) < (self.radius+enemyradius)*.7:
            print(math.dist(self.rect_center, enemyrect_center))
            return True
        else:
            return False

    def consume(self, collision, enemyradius):
        self.radius += enemyradius
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = self.rect_center)
                





class Player(Ball):
    def __init__(self):
        super().__init__()
        self.color = (0, 0, 0, 255)
        self.radius = 25
        self.speed = math.log(self.radius)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (100, 100))
        self.speed = math.log(self.radius**2)
    
    def move(self):
        mx, my = pygame.mouse.get_pos()

        distx = mx-self.x
        disty = my-self.y

        distx2 = distx/self.speed
        disty2 = disty/self.speed

        disthype = math.sqrt((distx**2)+(disty**2))

        

        if disthype == 0:
            disthype = .1
        
        self.deltax = 10*(distx2)/((disthype))
        self.deltay = 10*(disty2)/((disthype))

        
        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay
        self.rect_center = (self.rect.centerx, self.rect.centery)

        
font = pygame.font.Font(None,100)
text_surface1 = font.render("You Won", False,"Green")
text_surface2 = font.render("You Lost", False,"Red")




# Main game loop
feast = pygame.sprite.Group()
for num in range(35):
    feast.add(Food('Green'))

enemies = pygame.sprite.Group()
for num in range(5):
    enemies.add(Ball())

players = pygame.sprite.Group()
for num in range(1):
    players.add(Player())



objects = pygame.sprite.Group()
objects.add(feast)
objects.add(enemies)
objects.add(players)


count = 0

running = True
while running:
    count +=1
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()

        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill(WHITE)

    for enemy in enemies:
        enemy.move(count)
        for bite in objects:
            if enemy != bite:
                var = enemy.collisionDetector(bite.rect_center, bite.radius)
                if var == True:
                    if enemy.radius > bite.radius:
                        enemy.consume(var, bite.radius)
                        if type(bite)== Food:
                            bite.rect_center = (random.randint(75, 525), random.randint(75, 725))
                            bite.rect = bite.image.get_rect(center = bite.rect_center)
                        else:
                            bite.kill()
    for player in players:
        player.move()
        for object in objects:
            if player != object:
                var = player.collisionDetector(object.rect_center, object.radius)
                if var == True:
                    if player.radius >object.radius:
                        player.consume(var, object.radius)
                        if type(object)== Food:
                            object.rect_center = (random.randint(75, 525), random.randint(75, 725))
                            object.rect = object.image.get_rect(center = object.rect_center)
                        else:
                            object.kill()

    
        
    objects.draw(screen)

    if len(enemies) == 0:
        screen.blit(text_surface1,(50,400))
    elif len(players) ==0:
        screen.blit(text_surface2,(50,400))

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()
