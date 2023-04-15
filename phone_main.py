import pygame, time, struct, socket
import pygame.event as pygevent
import pygame.draw as pygdraw
import pygame.font as pygfont

pygame.init()
windowSize = [1080, 1920]
#windowSize = [1920 ,1080]
display = pygame.display.set_mode(windowSize)
font = pygfont.SysFont("Arial",16)

addr = ["ip","port"]
#server = socket.create_connection(addr)

pressPos = [[.5,.5],[.5,.5],[],[],[],[],[]]
pressedFingers = [0] * 10
lmbClick = False

baseResolution = 3
resolution = (10 ** baseResolution)

workZone = pygame.Rect(windowSize[0]/3,windowSize[1]/3.5,500,800)
lmbClickZone = pygame.Rect(windowSize[0]/4*3,0,200,400)

sqColor = (56,56,56)
posX = .5 * resolution
posY = .5 * resolution

while True:
    for event in pygevent.get():
        if event.type == pygame.FINGERDOWN:
            if(event.finger_id == 1):
                lmbTouch = (int(event.x * windowSize[0]), int(event.y * windowSize[1]))
                if lmbClickZone.collidepoint(lmbTouch):
                    lmbClick = True
                else:
                    lmbClick = False
        if event.type == pygame.FINGERUP:
            if(event.finger_id == 1):
                lmbClick = False
        if event.type == pygame.FINGERMOTION:
            pressPos[event.finger_id] = [event.x,event.y]

    sqColor = (255,0,0)
    touchPos = [int(pressPos[0][0] * windowSize[0]), int(pressPos[0][1] * windowSize[1])]
    if(workZone.collidepoint(tuple(touchPos))):
        sqColor = (56,56,56)
        posX = int((touchPos[0] - workZone.x) / workZone.width * resolution)
        posY = int((touchPos[1] - workZone.y) / workZone.height * resolution)
        
    data = struct.pack("<bbII", baseResolution, lmbClick, posX, posY)
    #server.send(data)
    pygdraw.rect(display, sqColor, workZone)
    pygdraw.rect(display, (144,144,144), lmbClickZone)
    pygame.display.flip()
    time.sleep(0.01)
