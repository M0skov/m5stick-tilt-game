######Lab 4 - tilt-controlled ball-balancing game
##Jan Gomez
from bleak import BleakClient, BleakScanner
import threading
import asyncio
import struct
import pygame
import random

global score
score = 0

pygame.init()
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
img_a = pygame.image.load('background_seal.png')
img_background = pygame.transform.scale(img_a, (800,800))
img_b = pygame.image.load('ball_size_trial_1-removebg.png')
image_ball = pygame.transform.scale(img_b, (60,60))
img_c = pygame.image.load('angry_bird_trial_2.png')
image_bird = pygame.transform.scale(img_c, (70,70))
img_d = pygame.image.load('final_candidate_after_corrections_num16.png')
image_seal = pygame.transform.scale(img_d, (100,40))

global seal_dx, seal_dy, seal_tilt
seal_dx = 0
seal_dy = 0
seal_tilt  = 0
clock = pygame.time.Clock()
game_over = False

def run_controller():
    def callback(sender, data: bytearray):
        global seal_dx, seal_dy, seal_tilt
        number = struct.unpack("<fffh", data)
        x, y, b, c = number
        seal_dx = int(x * 10)
        seal_dy = int(y * 10)
        seal_tilt = x * 5
        print(f"accx: {x:.2f}, accy: {y:.2f}, tilt: {seal_tilt:.2f}")

    async def run():
        while True:
            devices = await BleakScanner.discover(1)
            for d in devices:
                if d.name == "M5StickCPlus-JanG":
                    async with BleakClient(d) as client:
                        await client.start_notify("82a7e967-7504-4f75-a68e-57c2803d8f41", callback)
                        while True:
                            await asyncio.sleep(.01)
    asyncio.run(run())

t = threading.Thread(target=run_controller)
t.daemon = True
t.start()

def stay_in(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class Seal_player:
    def __init__(self, x, y):
        self.original_image = pygame.transform.scale(image_seal, (300,80))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center =(x,y))
        self.angle = 0
    def move(self):
        if abs(seal_dx) < 4:
            self.rect.x += seal_dx
        self.rect.x = stay_in(self.rect.x, 0, width - self.rect.width)
        self.rect.y = stay_in(self.rect.y, 0, height - self.rect.height)
        self.angle = seal_tilt * 10
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=center)
    def draw(self):
        screen.blit(self.image, self.rect)

class angry_bird:
    def __init__(self, x, y, speed, image_bird):
        self.image = pygame.transform.scale(image_bird, (70,70))
        self.hit = self.image.get_rect(topleft =(x,y))
        self.speed = speed
    def move(self):
        self.hit.y += self.speed
    def reset(self):
        self.hit.x = random.randint(0, width-self.hit.width)
        self.hit.y = 0
    def draw(self, surface):
        surface.blit(self.image, self.hit)

class Ball_movement:
    def __init__(self):
        self.image = pygame.transform.scale(image_ball, (60,60))
        self.rect = self.image.get_rect(center=(random.randint(0,width -60),0))
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.5
        self.on_seal = False
        self.mov_side_to_side = -15.0

    def move(self, seal):
        global score
        if not self.on_seal:
            self.speed_y += self.gravity
            self.pos_y += self.speed_y
            if self.rect.colliderect(seal.rect) and self.speed_y > 0:
                self.on_seal = True
                self.speed_y = 0
                self.pos_y = seal.rect.top - self.rect.height/2
                score += 1
        else:
            if not self.rect.colliderect(seal.rect):
                self.on_seal = False
            else:
                tilt_force = seal_tilt * self.mov_side_to_side
                self.speed_x += tilt_force * 1.1
                self.speed_x *= .80
                self.pos_x += self.speed_x
                self.pos_y = seal.rect.top - self.rect.height/2
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
        if self.rect.top >= height:
            self.__init__()
    def draw(self):
        screen.blit(self.image, self.rect)

seal = Seal_player(400,700)
ball = Ball_movement()
birds = []
for i in range(2):
    x = random.randint(0, width -70)
    y = random.randint(-500,0)
    speed = random.randint(2,6)
    birds.append(angry_bird(x,y,speed,image_bird))

while not game_over:
    clock.tick(60)
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            game_over = True
    screen.blit(img_background, (0,0))
    seal.move()
    ball.move(seal)
    for bird in birds:
        bird.move()
        if bird.hit.top > height:
            bird.reset()
        bird.draw(screen)
    seal.draw()
    ball.draw()
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text,(50,50))
    pygame.display.update()
pygame.quit()
