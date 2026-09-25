#lab 4 part 1
##Jan Gomez
##we import pygame
import pygame


#we set the size of the window
window_widht = 800
window_height = 800
##color for the bolck going up
Vc_color_block_red = (255,0,0)
##window coloe
window_color = (0,0,0)
##and the whiyte color for the letter Vc= random numbers
white_color = (255, 255, 255)
##next are the values for the voltage, resistance , the capacitance, and the time in seconds
Vs = 5
R = 2000
C = .001
dt = 0.01
Q =  0
##we start the game and the title of the window
pygame.init()
window = pygame.display.set_mode((window_widht, window_height))
pygame.display.set_caption("Simulator")
clock = pygame.time.Clock()
charge = False
simulator_running = True
##while the simulator is runing this would run perfectly
while simulator_running:
    window.fill(window_color)

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            simulator_running = False
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_c:
                charge = True
        elif evt.type == pygame.KEYUP:
            if evt.key == pygame.K_c:
                charge = False
    Vc = Q/C
    if charge:
        I = (Vs-Q/C)/R
    else:
        I = (-Q/C)/R
    Q = Q+I*dt
    Vc = Q /C
    voltage_height = int((Vc/Vs )*window_height)
    pygame.draw.rect(window, Vc_color_block_red,(150,window_height-voltage_height, 100, voltage_height))
    font = pygame.font.SysFont(None,24)
    text = font.render(f"Vc ={Vc:.2f}V", True, white_color)
    window.blit(text, (50,50))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
