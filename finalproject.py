#ICS3U
#Kevin Zhu & Neel Tandel
#Undead Rising is a single zombie survival game, where the user uses WASD and mouse to move and move cursor respectively.
#The purpose of the game is to survive the 3 waves of zombies, spawning at intervals of time.
#The user is placed in a map with openings, allowing for zombies to spawn then follow the user.
#The game features a point system, which you start off with no points and collect points by killing zombies.
#With points, the user may access the shop by pressing TAB, to purchase equipment and new weapons to help them survive the waves.

from pygame import *
from random import *
from math import *
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '120,110' # screen allignment

screen = display.set_mode((1024,768))
#pointcounter
font.init()
arialblackFont=font.SysFont("Arial Black",15)   #font type & size
smallFont=font.SysFont("Arial Black",10)
points=0
#menu, game buttons, etc. (buttons, images, and shapes used throughout)
startingscreen=image.load("images/startingscreen.png")
startingscreen=transform.scale(startingscreen,(1024,768))
starttitle=image.load("images/starttitle.png")
starttitle=transform.scale(starttitle,(670,150))
startbutton=image.load("images/startbutton.png")
startbuttonborder=Rect(420,260,200,100)
controls =image.load("images/controls.png")
controls = transform.scale(controls,(300,100))
controlimage = image.load("images/controlsimage.png")
controlimage = transform.scale(controlimage,(1024,768))
controlborder = Rect(380,400,320,100)
goback = Rect(10,10,75,75)
#gamefinishedbuttons
gameover = image.load("images/gameover.png")
gameover = transform.scale(gameover,(1024,768))
youwin = image.load("images/youwin.png")
youwin = transform.scale(youwin,(1024,768))
returntomenu = image.load("images/return.png")
menubutton=Rect(300,600,400,80)


# SHOP IMAGES & SHAPES
shopRect = (300,300,500,500)
arbox = image.load("images/arbox.png")
arbox = transform.scale(arbox,(80,80))
ammobox = image.load("images/ammobox.png")
ammobox = transform.scale(ammobox,(80,80))
firstaidkit = image.load("images/firstaidkit.png")
firstaidkit = transform.scale(firstaidkit,(80,80))
closeshop = image.load("images/closeshop.png")
closeshop = transform.scale(closeshop,(22,20))
pistolbox = image.load("images/pistolbox.png")
pistolbox = transform.scale(pistolbox,(80,80))
screen.blit(startingscreen,(0,0))
draw.rect(screen,(255,255,255),startbuttonborder)
draw.rect(screen,(255,255,255),controlborder)
screen.blit(starttitle,(165,50))
screen.blit(startbutton,(440,280))
screen.blit(controls,(380,400))

ammopricetxt=smallFont.render("$200(20 Bullets)",True,(255,255,255))
firstaidpricetxt=smallFont.render("$200(37.5 HP)",True,(255,255,255))
pistolpricetxt=smallFont.render("$300",True,(255,255,255))
arpricetxt=smallFont.render("$600",True,(255,255,255))
#startingscreenmusic
init()
mixer.music.load("music/menumusic.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(-1)



#character (images of user holding different weapons)
pistol_wield = image.load("images/pistol_wield.png")
pistol_wield = transform.scale(pistol_wield,(60,60))
knife_wield = image.load("images/knife_wield.png")
knife_wield = transform.scale(knife_wield,(60,60))
rifle_wield = image.load("images/rifle_wield.png")
rifle_wield = transform.scale(rifle_wield,(60,60))

# enemies
zombie1 = image.load("images/zombie1.png")
zombie1 = transform.scale(zombie1,(70,70))



def drawScene(room,angle,rotPic,pts,bullets,wavenum): #when page=game, these things are drawn 
    screen.blit(room,(0,0))
    screen.blit(rotPic,(pos[X]-rotPic.get_width()//2,pos[Y]-rotPic.get_height()//2))
    crosshair(mx,my)

   # font related stuff
    point_countertxt=arialblackFont.render("POINTS = %d"%(pts),True,(255,255,255))
    screen.blit(point_countertxt,(180,10))
    ammo_countertxt=arialblackFont.render("%d"%(bullets),True,(255,255,0))

    if buy_pistol==True or buy_ar==True: #if the user had purchased a pistol or rifle, an ammo counter will display on the bottom right side of the screen.
        screen.blit(ammo_countertxt,(900,700))
    wave_countertxt=arialblackFont.render("WAVE %s"%(wavenum),True,(255,255,255))
    screen.blit(wave_countertxt,(900,5))
        



    

#making sure guy doesn't go thru walls    
def clear(x,y): 
    if x<0 or x >= mask.get_width() or y<0 or y >= mask.get_height(): #if x and y coords of the zombie or the guy are not in the map
        return False
    else:
        return mask.get_at((x,y)) != WALL

#same thing but for gun bullets
def clearshot(x,y):
    if x<0 or x >= mask.get_width() or y<0 or y >= mask.get_height():
        return False
    

#healthbar
def draw_healthbar(health,health_lost):
    if health_lost < 37.5:
        draw.rect(screen,(0,255,0),(10,10,health-health_lost,20))
    if health_lost > 37.5 and health_lost < 75:
        draw.rect(screen,(255,255,0),(10,10,health-health_lost,20))
    if health_lost > 75 and health_lost < 112.5:
        draw.rect(screen,(255,165,0),(10,10,health-health_lost,20))
    if health_lost > 112.5 and health_lost <= 150:
         draw.rect(screen,(255,0,0),(10,10,health-health_lost,20))
    if health_lost>=150:
        page = "gameover"


        
    
health = 150

health_lost = 0

#character movement

def movegunman(pos):
    keys = key.get_pressed()
    if keys[K_a] and pos[X] > 0  and clear(pos[X]-12,pos[Y]): # lEFT
        pos[X] -= 2
    if keys[K_d] and pos[X] < 1024 and clear(pos[X]+12,pos[Y]): # RIGHT
        pos[X] += 2
    if keys[K_s] and pos[Y] < 768 and clear(pos[X],pos[Y]+12): # DOWN
        pos[Y] += 2
    if keys[K_w] and pos[Y] > 0 and clear(pos[X],pos[Y]-12): # UP
        pos[Y] -= 2
#guypos
X=0
Y=1

wave1 = 400
wave2 = 300
wave3 = 200
def spawnZombie(wave):
    if frame%wave==0:
        zombies.append([randint(13,15),randint(595,600)])
        zombies.append([randint(640,650),randint(730,740)])
        zombies.append([randint(10,15),randint(40,50)])
        zombies.append([randint(490,500),randint(40,50)])



#for guns
shots = []
shot = []
gun_cooldown = 0
ammo=20

#startingpointonmap
pos = [400,400]

#weapons
weapons=[knife_wield,pistol_wield,rifle_wield]
weapondrawn=weapons[0]

#map
room=image.load("images/room1.png")
room=transform.scale(room,(1024,768))
mask = image.load("images/room1_mask.png")
mask = transform.scale(mask,(1024,768))



#weaponcrosshair
def crosshair(mx,my):
    draw.line(screen,(0,255,0),(mx,my+4),(mx,my+6),2)
    draw.line(screen,(0,255,0),(mx,my-4),(mx,my-6),2)
    draw.line(screen,(0,255,0),(mx+4,my),(mx+6,my),2)
    draw.line(screen,(0,255,0),(mx-4,my),(mx-6,my),2)

wave=1
buy_pistol = False
buy_ar = False
show_shop=False
angle=0
zombangle=0
WALL = (255,0,0,255)
myClock = time.Clock()
frame = 0
zombies = []
running=True
page = "menu" 
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False

    frame += 1
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()
    keys = key.get_pressed()


#switchingweapons
    if keys[K_1]:
        weapondrawn=weapons[0]
    if keys[K_2] and buy_pistol == True:
        weapondrawn=weapons[1]
    if keys[K_3] and buy_ar == True:
        weapondrawn=weapons[2]


    angle = degrees(atan2(mx-pos[X],my-pos[Y]))-80
    rotPic = transform.rotate(weapondrawn,angle)

    if page == "menu":
        screen.blit(startingscreen,(0,0))
        draw.rect(screen,(255,255,255),startbuttonborder)
        draw.rect(screen,(255,255,255),controlborder)
        screen.blit(starttitle,(165,50))
        screen.blit(startbutton,(440,280))
        screen.blit(controls,(380,400))

        if startbuttonborder.collidepoint(mx,my) and mb[0]==1:
            page = "game"
            if health_lost>=150:
                health_lost = 0
                wave = 1
                points = 0

        if controlborder.collidepoint(mx,my) and mb[0] ==1: # this has the controls, instructions and the story
            page = "controls"

    if page == "controls":
            screen.blit(controlimage,(0,0))
            draw.rect(screen,(255,255,255),goback)
            draw.polygon(screen,(255,0,0),[[60,10],[60,60],[20,35]])
            if goback.collidepoint(mx,my) and mb[0] ==1:
                page = "menu"
    if page == "gameover":
            mouse.set_visible(True)
            screen.blit(gameover,(0,0))
            screen.blit(returntomenu,(300,600))
            draw.rect(screen,(0),menubutton,1)
            if menubutton.collidepoint((mx,my)) and mb[0]==1:
                page = "menu"
    if page == "win": # PLAYER WINS 
            screen.blit(youwin,(0,0))
            screen.blit(returntomenu,(320,500))
            draw.rect(screen,(255,0,0),menubutton,1)
            if menubutton.collidepoint((mx,my)) and mb[0]==1:
                page="menu"

    if page == "game":
        mouse.set_visible(False)

        movegunman(pos)
        drawScene(room,angle,rotPic,points,ammo,wave)
        clear(pos[0],pos[1])
        spawnZombie(wave1)
        # waves change after x amount of frames
        if frame==4500:
            spawnZombie(wave2)
            wave=2
        if frame==6000:
            spawnZombie(wave3)
            wave=3
        if frame==8000:
            mouse.set_visible(True)
            page = "win"

        # SHOP STUFF
        if keys[K_TAB]:
            show_shop = True # OPEN SHOP WITH TAB BUTTON
            
        if show_shop == True: # PLAYER CAN BUY STUFF FROM SHOP WITH POINTS
            mouse.set_visible(True)
            shop_Rect=draw.rect(screen,(0),(650,25,300,120))
            ammoRect = draw.rect(screen,(255,0,0),(660,50,80,80))
            firstaidRect = draw.rect(screen,(255,255,0),(760,50,80,80))
            gunRect = draw.rect(screen,(255,255,255),(860,50,80,80))
            noshop_Rect = draw.rect(screen,(255,0,0),(920,25,22,20))
            # BOX IMAGES FOR SHOP
            screen.blit(ammobox,(660,50))
            screen.blit(firstaidkit,(760,50))
            screen.blit(closeshop,(920,25))
            screen.blit(pistolbox,(860,50))
            # TEXT FONT PRICE
            screen.blit(ammopricetxt,(655,40))
            screen.blit(firstaidpricetxt,(760,40))
            screen.blit(pistolpricetxt,(885,40))
            


            if show_shop==True and buy_pistol == True:
                shop_Rect=draw.rect(screen,(0),(650,25,300,120))
                ammoRect = draw.rect(screen,(255,0,0),(660,50,80,80))
                firstaidRect = draw.rect(screen,(255,255,0),(760,50,80,80))
                gunRect = draw.rect(screen,(255,255,255),(860,50,80,80))
                noshop_Rect = draw.rect(screen,(255,0,0),(920,25,22,20))

                screen.blit(ammobox,(660,50))
                screen.blit(firstaidkit,(760,50))
                screen.blit(closeshop,(920,25))
                screen.blit(arbox,(860,50))

                screen.blit(ammopricetxt,(655,40))
                screen.blit(firstaidpricetxt,(760,40))
                screen.blit(arpricetxt,(880,40))
                if gunRect.collidepoint(mx,my) and points>=600 and mb[0] == 1: 
                    points-=600
                    buy_ar = True
            
            if noshop_Rect.collidepoint(mx,my) and mb[0] == 1:  # CLOSE THE SHOP
                show_shop = False

            if ammoRect.collidepoint(mx,my) and mb[0] == 1:
                if points >= 200:
                    ammo+= 20
                    points-=100
                   
            if firstaidRect.collidepoint(mx,my) and points>=200 and health_lost>37.5 and mb[0] == 1:
                health_lost-=37.5
                points-=200
            if firstaidRect.collidepoint(mx,my) and points>=200 and health_lost<37.5 and mb[0] == 1:
                health_lost-=health_lost
                points-=200



            if gunRect.collidepoint(mx,my) and points>=300 and mb[0] == 1:
                points-=300
                buy_pistol = True
              


        #zombies movement and collision
        for zomb in zombies:
            if zomb[0]<pos[0]-20 and clear(int(zomb[0]+20),int(zomb[1])): #R
                zomb[0]+=1
            if zomb[0]>pos[0]-20 and clear(int(zomb[0]-20),int(zomb[1])): #L
                zomb[0]-=1
            if zomb[1]<pos[1]-20 and clear(int(zomb[0]),int(zomb[1]+20)): #D
                zomb[1] += 1
            if zomb[1]>pos[1]+20 and clear(int(zomb[0]),int(zomb[1]-20)): #U
                zomb[1]-=1
            
            zombangle = degrees(atan2(pos[X]-zomb[0],pos[Y]-zomb[1]))#zombies face guy
            rotZomb = transform.rotate(zombie1,zombangle)
            zomb_pos = screen.blit(rotZomb,(zomb[0]-rotZomb.get_width()//2,zomb[1]-rotZomb.get_height()//2))

            
            if zomb_pos.collidepoint((pos)): #character losing health
                health_lost+= .3
                if weapondrawn==weapons[0] and mb[0]==1: #for knife
                    zombies.remove(zomb)
                    points+=30
                    

            for shot in shots:
            
                if zomb_pos.collidepoint([int(shot[0]-20),int(shot[1]-20)]): #bullets collide with zombie
                    shots.remove(shot)
                    zombies.remove(zomb)
                    points+=20
           
     
        #clearshot #bullet collision with walls
        if len(shot)>=1:
            clearshot(shot[0],shot[1]) 


        # healthbar
        draw_healthbar(health,health_lost)



                
        #shootpistol
        if weapondrawn==weapons[1]:
            gun_cooldown -= 1
            for shot in shots:
                shot[0] += shot[2]
                shot[1] += shot[3]
                draw.circle(screen,(255,255,0),(int(shot[0]),int(shot[1])),3)

                
                if mask.get_at((int(shot[0]),int(shot[1])))==WALL:
                    shots.remove(shot)
                

            if mb[0]==1 and gun_cooldown <=0 and ammo>0:
                bigx = mx-pos[0]
                bigy = my-pos[1]
                dist = hypot(bigx,bigy)
                sx = 5 * bigx/dist 
                sy = 5 * bigy/dist
                shots.append([pos[0],pos[1],sx,sy])
                gun_cooldown = 40
                ammo-=1
                mixer.music.load("music/shot.mp3")
                mixer.music.set_volume(0.5)
                mixer.music.play(1)
                
            

             
        # assault rifle shoot
        if weapondrawn==weapons[2]:
            gun_cooldown -= 1
            
            for shot in shots:
                bulletpos=draw.circle(screen,(255,255,0),(int(shot[0]),int(shot[1])),3)
                shot[0] += shot[2]
                shot[1] += shot[3]
           
                
                if mask.get_at((int(shot[0]),int(shot[1])))==WALL: #if shot x and y coord hit, wall, it is removed from list
                    shots.remove(shot)
                
                    
            if mb[0]==1 and gun_cooldown <=0 and ammo>0: # player shoot
                bigx = mx-pos[0]
                bigy = my-pos[1]
                dist = hypot(bigx,bigy)
                sx = 5 * bigx/dist 
                sy = 5 * bigy/dist
                gun_cooldown = 20
                shots.append([pos[0],pos[1],sx,sy])
                ammo-=1
                
                mixer.music.load("music/shot.mp3")
                mixer.music.set_volume(0.5)
                mixer.music.play(1)

        if health_lost>=150: # PLAYER DIES
            page="gameover"


    
        


    display.flip()
    myClock.tick(100) 
quit()
