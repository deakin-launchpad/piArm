import pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
vel = 5

run = True

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        print('left')
        x -= vel

    if keys[pygame.K_RIGHT]:
        print('right')
        x += vel

    if keys[pygame.K_UP]:
        print('up')
        y -= vel

    if keys[pygame.K_DOWN]:
        print('down')
        y += vel

    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    pygame.display.update() 
    
pygame.quit()