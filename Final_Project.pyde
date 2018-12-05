"""ERRORS:
    1. (wall issue) Doesn't block wall if your y velocity is 0 (only moving horizontally on the ground), this is due to our condition to self.wall=0 only when self.vy==0 (so can walk through walls)

    Suggestions:
        1. Want to implement a time delay between touching the obstacle and restarting
        2. Some bonus for certain amount of coins collected (like fireball in class)
        
    To-Do:
        1. Coin counter (bar at top)
        2. Animation of dying (vanishing)
        3. Animation of coins dropping when you die
    

"""
add_library('minim')
import os
import time
path=os.getcwd()
player = Minim(this)

class Creature:
    def __init__(self,x,y,r,g,img,w,h,F):
        self.x=x
        self.y=y
        self.r=r #Radius of creature
        self.g=g #Gravity
        self.vx=0
        self.vy=0
        self.w=w #Width of image
        self.h=h #Height of image
        self.F=F #Total no of frames
        self.f=0 #Which frame exactly
        self.img = loadImage(path+"/images/"+img)
        self.dir = 1
        self.wall=0
    
    def gravity(self):
        if self.y+self.r < self.g: #If character is above ground
            self.vy += 0.25 #Give character velocity in positive y-axis (falling down)
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r) #To ensure character stops at ground EXACTLY (and not below)
        else:
            self.vy = 0 #-10 (else we keep velocity in y as 0)
            
        for p in game.platforms:
            if self.x in range(p.x, p.x+p.w) and self.y+self.r <= p.y: #(if character is above the platform AND within the width of platform)
                self.g = p.y #Turn the ground 
                break
            else:
                self.g = game.g #Else we stick to original ground
    
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()

        if isinstance (self, Koopa):
            self.f = (self.f+0.3)%self.F
        elif isinstance (self, Star):
            self.f = (self.f+0.3)%self.F
        elif self.vx != 0: #If the character is moving, then we cycle through the frames
            self.f = (self.f+0.3)%self.F
        else:
            self.f = 3 #Else we keep the same (stationary) frame
            
        if self.dir > 0:
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #int(self.f)*self.w, means to choose the x,y coords of the entire image (all frames) corresponding to which frame we need
        elif self.dir < 0:
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #switching x1 with x2 and y1 with y2, to flip the image horizontally
            
        # stroke(255)
        # noFill()
        # ellipse(self.x,self.y,2*self.r,2*self.r)
    
class Player1(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False}
        self.kill = player.loadFile(path+"/sounds/kill.mp3")
        self.gameover = player.loadFile(path+"/sounds/gameover.wav")
        self.star = player.loadFile(path+"/sounds/coin.mp3")
        self.ox=x
        self.oy=y
        
    def update(self):
        self.gravity()
        if self.vy==0:
            self.wall=0
        
        if self.keyHandler[LEFT] and self.wall==0:
            self.vx = -5
            self.dir = -1
            
        elif self.keyHandler[RIGHT] and self.wall==0:
            self.vx = 5
            self.dir = 1
        else:
            self.vx = 0
        
        if self.keyHandler[UP] and self.y+self.r == self.g: #AND statement ensures that we cannot double jump
            self.vy = -10
    
        self.x += self.vx
        self.y += self.vy
        
        for p in game.platforms:
            if  self.x>=(p.x-20) and self.x<=(p.x+p.w+20) and self.y>=(p.y-10) and self.y<=(p.y+p.h+40):
                self.vy=7
                self.vx=0
                self.wall=1
                #self.wall=0
                #self.vx=0
        
        for e in game.enemies:
            if self.cdistance(e) <= self.r + e.r:
                # there is a collision
                if self.vy > 0 and self.y < e.y:
                    game.enemies.remove(e)
                    del e
                    self.kill.rewind()
                    self.kill.play()
                    self.vy = -8
                else:
                    self.x=self.ox
                    self.y=self.oy
        
        
        for s in game.stars:
            if self.cdistance(s) <= self.r + s.r:
                game.stars.remove(s)
                del s
                self.star.rewind()
                self.star.play()
            
        
    def cdistance(self,e): #COLLISION DETECTION
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5
    
class Player2(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler={'a':False, 'd':False, 'w':False}
        self.kill = player.loadFile(path+"/sounds/kill.mp3")
        self.gameover = player.loadFile(path+"/sounds/gameover.wav")
        self.star = player.loadFile(path+"/sounds/coin.mp3")
        self.ox=x
        self.oy=y
    def update(self):
        self.gravity()
        if self.vy==0:
            self.wall=0
        
        if self.keyHandler['a'] and self.wall==0:
            self.vx = -5
            self.dir = -1
        elif self.keyHandler['d'] and self.wall==0:
            self.vx = 5
            self.dir = 1
        else:
            self.vx = 0
        
        if self.keyHandler['w'] and self.y+self.r == self.g:
            self.vy = -10
        
        self.x += self.vx
        self.y += self.vy   
        
        for p in game.platforms:
            if  self.x>=(p.x-20) and self.x<=(p.x+p.w+20) and self.y>=(p.y-10) and self.y<=(p.y+p.h+10):
                self.vy=7
                self.vx=0
                self.wall=1
        
        for e in game.enemies:
            if self.cdistance(e) <= self.r + e.r:
                # there is a collision
                if self.vy > 0 and self.y < e.y:
                    game.enemies.remove(e)
                    del e
                    self.kill.rewind()
                    self.kill.play()
                    self.vy = -8
                else:
                    self.x=self.ox
                    self.y=self.oy
        
        for s in game.stars:
            if self.cdistance(s) <= self.r + s.r:
                game.stars.remove(s)
                del s
                self.star.rewind()
                self.star.play()
            
        
    def cdistance(self,e): #COLLISION DETECTION
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 
    
class Star(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.cx = x
        self.cy = y
        
    def gravity(self):
        return
    
class Koopa(Creature): #Creature unaffected by gravity
    def __init__(self,x,y,r,g,img,w,h,F,y1,y2): #y1 and y2 are the vertical endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.y1=y1
        self.y2=y2
        self.dir = -1
        
    def update(self): #Giving endpoints for the creature to move between
        
        if self.y < self.y1:
            self.vy = 3
        elif self.y > self.y2:
            self.vy = -3
            
        self.y += self.vy
        
class Pikatshu(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2): #x1 and x2 are the horizontal endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = 2
        self.jump = player.loadFile(path+"/sounds/Pikachu.mp3")
        
    def update(self):
        self.gravity()
        
        if self.x > self.x2:
            self.vx = -2
            self.dir = -1
        elif self.x < self.x1:
            self.vx = 2
            self.dir = 1
        
        #Jumping functionality
        """if int(random(100)) == 1 and self.y+self.r == self.g: #To randomly make some jump (will fall back down tho cuz gravity)
            self.vy = -10
            # self.jump.rewind()
            # self.jump.play()"""
        
        self.x += self.vx
        self.y += self.vy

class Platform:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img = loadImage(path+"/images/platform.png")
        
    def display(self):
        rect(self.x,self.y,self.w,self.h)
        #image(self.img,self.x,self.y,self.w,self.h)
        
            
class Game:
    def __init__ (self,w,h,g): #width, height and ground of the game board
        self.w=w
        self.h=h
        self.g=g
        
        self.pause = False
        #self.pauseSound = player.loadFile(path+"/sounds/pause.mp3")
        
        #self.music = player.loadFile(path+"/sounds/music.mp3")
        #self.music.play()
        
        """self.bgImgs=[] BACKGROUND IMAGES
        for i in range(5,0,-1):
            self.bgImgs.append(loadImage(path+"/images/layer_0"+str(i)+".png"))"""
        
        self.p1 = Player1(50,668,35,self.g,"mario.png",100,70,11) #Player-1
        self.p2 = Player2(100,668,35,self.g,"mario.png",100,70,11) #Player-2
        self.enemies = []
        #for i in range(5):
            #self.enemies.append(Pikatshu(250+i*100,50,42,self.g,"pikatshu.png",120,85,4,100,1000))
        #self.enemies.append(Koopa(150,50,35,self.g,"koopa.png",70,70,8,200,500))
        
        self.enemies.append(Pikatshu(50,100,42,self.g,"pikatshu.png",120,85,4,50,450))
        
        self.platforms=[]
        #for i in range(3):
        self.platforms.append(Platform(0,150,1216,50)) #Platform-3
        self.platforms.append(Platform(400,350,1016,50)) #Platform-2
        self.platforms.append(Platform(0,550,1216,50)) #Platform-1
        
        self.platforms.append(Platform(-299,0,300,768)) #WALLS
        self.platforms.append(Platform(1439,0,300,768))
        
        self.platforms.append(Platform(0,718,1440,50)) #Ground
        
        self.stars = [] #STARS
        for i in range(5):
            self.stars.append(Star(50+i*50,120,20,self.g,"star.png",40,40,6))
        for i in range(5):
            self.stars.append(Star(250+i*50,270,20,self.g,"star.png",40,40,6))
        
        
    def display(self):
        stroke(255)
        #line(0,self.g,self.w,self.g)
        
        """cnt = 5 BACKGROUND IMAGES
        for img in self.bgImgs:
            x = (game.x//cnt)%game.w
            image(img,0-x,0)
            image(img,self.w-x-1,0)
            cnt-=1"""
            
        for p in self.platforms:
            p.display()
        
        for e in self.enemies:
            e.display() 
            
        for s in self.stars: #STAR DISPLAY
            s.display()
               
        self.p1.display()
        self.p2.display()
        
        """fill(255,0,0) STAR COUNTER
        rect(30,30,100,20)
        fill(255,255,0)
        rect(30,30,min(100,self.mario.starsCnt*10),20)"""
        
game = Game(1440,768,718) #Window dimensions and the ground value

def setup():
    size(game.w, game.h)
    background(0)
    
def draw():
    if game.pause == False:
        background(0)
        game.display()
    else:
        textSize(70)
        fill(0,255,255)
        text("Paused",game.w//2,game.h//2)
    
def keyPressed():
    if keyCode == LEFT:
        game.p1.keyHandler[LEFT]=True
    elif keyCode == RIGHT:
        game.p1.keyHandler[RIGHT]=True
    elif keyCode == UP:
        game.p1.keyHandler[UP]=True
    elif key in ['a','A']:
        game.p2.keyHandler['a']=True
    elif key in ['d','D']:
        game.p2.keyHandler['d']=True
    elif key in ['w','W']:
        game.p2.keyHandler['w']=True
    elif key in ['p','P']: #Pause functions
        game.pause = not game.pause
        #game.pauseSound.rewind()
        #game.pauseSound.play()
        
        if game.pause == True:
            game.music.pause()
        else:
            game.music.play()
        
def keyReleased():
    if keyCode == LEFT:
        game.p1.keyHandler[LEFT]=False
    elif keyCode == RIGHT:
        game.p1.keyHandler[RIGHT]=False   
    elif keyCode == UP:
        game.p1.keyHandler[UP]=False
    elif key in ['a','A']:
        game.p2.keyHandler['a']=False
    elif key in ['d','D']:
        game.p2.keyHandler['d']=False
    elif key in ['w','W']:
        game.p2.keyHandler['w']=False
