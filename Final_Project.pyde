"""ERRORS:
    1. (wall issue) Doesn't block wall if your y velocity is 0 (only moving horizontally on the ground), this is due to our condition to self.wall=0 only when self.vy==0 (so can walk through walls)

    Suggestions:
        1. Want to implement a time delay between touching the obstacle and restarting
        2. Some bonus for certain amount of coins collected (like fireball in class)
        
    To-Do:
        1. Coin counter (bar at top)
        2. Animation of dying (vanishing)
        3. Animation of coins dropping when you die
        4. TIME DELAY BETWEEN SAME OBSTACLE
    
As of now, we have 2 players (usual) and we have stars (which are supposed to be GPA +0.4) and 1 pikachu (which is the FAIL = restart and -0.5 GPA), and a counter of GPA.


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

        if isinstance (self, rGPA):
            self.f = (self.f+0.3)%self.F
        elif isinstance (self, rCM):
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
        self.money=0 #Total CM of player
        self.grade=0 #Total GPA of player
        self.ox=x
        self.oy=y
        
    def update(self):
        self.gravity()
        if self.vy==0:
            self.wall=0
            
        if self.x-self.r<0: #Left Boundary wall condition
            self.x=self.r
            
        if self.x+self.r>1440: #Right Boundary wall condition
            self.x=1440-self.r
            
        if self.y<0: #Roof condition
            self.y=self.r
            self.vy=5
            self.gravity()
        
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
        
        for t in game.oTrip:
            if self.cdistance(t) <= self.r + t.r:
                self.money=0
                self.x=self.ox
                self.y=self.oy
                    
        for f in game.oFail:
            if self.cdistance(f) <= self.r + f.r:
                self.grade-=0.5
                self.x=self.ox
                self.y=self.oy
                    
        for q in game.oQuiz:
            if self.cdistance(q) <= self.r + q.r and q.flag==0:
                self.grade-=0.2
                q.flag==1
                
        for s in game.oStarbucks:
            if self.cdistance(s) <= self.r + s.r and s.flag==0:
                self.money-=150
                s.flag==1
                
                    
                """ KILLING OBSTACLES
                if self.vy > 0 and self.y < t.y:
                    game.otrip.remove(t)
                    del t
                    self.kill.rewind()
                    self.kill.play()
                    self.vy = -8
                else:
                    self.money=0
                    self.x=self.ox
                    self.y=self.oy"""
        
        
        for m in game.CM:
            if self.cdistance(m) <= self.r + m.r:
                self.money+=50
                game.CM.remove(m)
                del m
                self.star.rewind()
                self.star.play()
                
        for g in game.GPA:
            if self.cdistance(g) <= self.r + g.r:
                self.grade+=0.4
                game.GPA.remove(g)
                del g
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
        self.money=0 #Total CM of player
        self.grade=0 #Total GPA of player
        self.ox=x
        self.oy=y
    def update(self):
        self.gravity()
        if self.vy==0:
            self.wall=0
            
        if self.x-self.r<0: #Left Boundary wall condition
            self.x=self.r
            
        if self.x+self.r>1440: #Right Boundary wall condition
            self.x=1440-self.r
        
        if self.y<0: #Roof condition
            self.y=self.r
            self.vy=5
            self.gravity()
        
        
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
            if  self.x>=(p.x-20) and self.x<=(p.x+p.w+20) and self.y>=(p.y-10) and self.y<=(p.y+p.h+40):
            #if  self.x+self.w>=(p.x) and self.x<=(p.x+p.w) and self.y+self.h>=(p.y) and self.y<=(p.y+p.h):
                self.vy=7
                self.vx=0
                self.wall=1
        
        for t in game.oTrip:
            if self.cdistance(t) <= self.r + t.r:
                self.money=0
                self.x=self.ox
                self.y=self.oy
                    
        for f in game.oFail:
            if self.cdistance(f) <= self.r + f.r:
                self.grade-=0.5
                self.x=self.ox
                self.y=self.oy
                    
        for q in game.oQuiz:
            if self.cdistance(q) <= self.r + q.r and q.flag==0:
                self.grade-=0.2
                q.flag==1
                
        for s in game.oStarbucks:
            if self.cdistance(s) <= self.r + s.r and s.flag==0:
                self.money-=150
                s.flag==1
                
                    
                """ KILLING OBSTACLES
                if self.vy > 0 and self.y < t.y:
                    game.otrip.remove(t)
                    del t
                    self.kill.rewind()
                    self.kill.play()
                    self.vy = -8
                else:
                    self.money=0
                    self.x=self.ox
                    self.y=self.oy"""
        
        
        for m in game.CM:
            if self.cdistance(m) <= self.r + m.r:
                self.money+=50
                game.CM.remove(m)
                del m
                self.star.rewind()
                self.star.play()
                
        for g in game.GPA:
            if self.cdistance(g) <= self.r + g.r:
                self.grade+=0.4
                game.GPA.remove(g)
                del g
                self.star.rewind()
                self.star.play()
        
        """for o in game.obstacles:
            if self.cdistance(o) <= self.r + o.r:
                # there is a collision
                if self.vy > 0 and self.y < o.y:
                    game.obstacles.remove(o)
                    del o
                    self.kill.rewind()
                    self.kill.play()
                    self.vy = -8
                else:
                    self.GPA=0
                    self.x=self.ox
                    self.y=self.oy
        
        for s in game.CM:
            if self.cdistance(s) <= self.r + s.r:
                self.coins+=1
                game.CM.remove(s)
                del s
                self.star.rewind()
                self.star.play()"""
            
        
    def cdistance(self,e): #COLLISION DETECTION
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 
    
"""class rCM(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.cx = x
        self.cy = y
        
    def gravity(self):
        return"""
    
class rGPA(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.cx = x
        self.cy = y #NO MOVEMENT
        
    def gravity(self):
        return
    
class rCM(Creature): #Creature unaffected by gravity (FLYING)
    def __init__(self,x,y,r,g,img,w,h,F,y1,y2): #y1 and y2 are the vertical endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.y1=y1
        self.y2=y2
        self.dir = -1
        
    def update(self): #Giving endpoints for the creature to move between (VERTICAL MOVEMENT)
        
        if self.y < self.y1:
            self.vy = 3
        elif self.y > self.y2:
            self.vy = -3
            
        self.y += self.vy
        
class Fail(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2): #x1 and x2 are the horizontal endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = 2
        #self.jump = player.loadFile(path+"/sounds/Pikachu.mp3")
        
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
        
class Trip(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2): #x1 and x2 are the horizontal endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = 2
        #self.jump = player.loadFile(path+"/sounds/Pikachu.mp3")
        
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
        
class Quiz(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2): #x1 and x2 are the horizontal endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = 2
        self.quiz=0
        #self.jump = player.loadFile(path+"/sounds/Pikachu.mp3")
        
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
        
class Coffee(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2): #x1 and x2 are the horizontal endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = 2
        self.coffee=0
        #self.jump = player.loadFile(path+"/sounds/Pikachu.mp3")
        
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
        
        self.CMImg=loadImage(path+"/images/star.png")
        self.GPAImg=loadImage(path+"/images/star.png")
        
        self.pause = False
        #self.pauseSound = player.loadFile(path+"/sounds/pause.mp3")
        
        #self.music = player.loadFile(path+"/sounds/music.mp3")
        #self.music.play()
        
        """self.bgImgs=[] BACKGROUND IMAGES
        for i in range(5,0,-1):
            self.bgImgs.append(loadImage(path+"/images/layer_0"+str(i)+".png"))"""
        
        self.p1 = Player1(50,668,35,self.g,"mario.png",100,70,11) #Player-1
        self.p2 = Player2(100,668,35,self.g,"mario.png",100,70,11) #Player-2
        
        self.oFail = [] #Fail that makes you restart position as well as reduces GPA by 0.5
        self.oTrip = [] #Trip that makes you restart position as well as reduces CM to 0
        self.oStarbucks = [] #Coffee cup that reduces your CM by 150
        self.oQuiz = [] #Quiz paper that makes you lose your GPA by 0.4
        
        #for i in range(5):
            #self.oFail.append(Fail(250+i*100,50,42,self.g,"fail.png",120,85,4,100,1000))
        #self.oFail.append(Koopa(150,50,35,self.g,"koopa.png",70,70,8,200,500))
        
        self.oFail.append(Fail(50,100,42,self.g,"pikatshu.png",120,85,4,50,450))
        
        self.platforms=[]
        #for i in range(3):
        self.platforms.append(Platform(0,150,1216,50)) #Platform-3
        self.platforms.append(Platform(400,350,1100,50)) #Platform-2
        self.platforms.append(Platform(0,550,1216,50)) #Platform-1
        
        self.platforms.append(Platform(-299,0,300,768)) #WALLS
        self.platforms.append(Platform(1439,0,300,768))
        
        self.platforms.append(Platform(0,718,1440,50)) #Ground
        
        self.CM = [] #Campus Money 
        self.GPA = [] #GPA
        
        for i in range(5):
            self.GPA.append(rGPA(50+i*50,120,20,self.g,"star.png",40,40,6)) #GPA hat objects (NO MOVEMENT)
        for i in range(5):
            self.GPA.append(rGPA(250+i*50,270,20,self.g,"star.png",40,40,6))
        
        self.CM.append(rCM(300,275,20,self.g,"star.png",40,40,6,300,500)) #Campus money objects (y1=top height limit, y2=bottom height limit)
        
    def display(self):
        stroke(255)
        #line(0,self.g,self.w,self.g)
        
        """cnt = 5 BACKGROUND IMAGES
        for img in self.bgImgs:
            x = (game.x//cnt)%game.w
            image(img,0-x,0)
            image(img,self.w-x-1,0)
            cnt-=1"""
            
        for p in self.platforms: #Displaying Platforms
            p.display()
            
        for f in self.oFail: #Displaying Fail restarts
            f.display()
            
        for t in self.oTrip: #Displaying Holiday Trip restarts
            t.display()
            
        for s in self.oStarbucks: #Displaying Starbucks cups
            s.display()
            
        for q in self.oQuiz: #Displaying Quiz papers
            q.display()
        
        for g in self.GPA: #Displaying GPA hats
            g.display() 
            
        for m in self.CM: #Displaying Campus Money
            m.display()
               
        self.p1.display()
        self.p2.display()
        
        """textSize(20) #Campus Money Counter
        fill(255) 
        text("P1 -"+str(self.p1.money),game.w-100,40)
        text("P2 -"+str(self.p2.money),game.w-100,75)
        image(self.CMImg,game.w-35,23, 20,20, 0,0, 40,40)
        image(self.CMImg,game.w-35,57, 20,20, 0,0, 40,40)"""
        
        textSize(20) #GPA Counter
        fill(255) 
        text("P1 -"+str(self.p1.grade),game.w-100,40)
        text("P2 -"+str(self.p2.grade),game.w-100,75)
        image(self.GPAImg,game.w-35,23, 20,20, 0,0, 40,40)
        image(self.GPAImg,game.w-35,57, 20,20, 0,0, 40,40)
        
        
        #rect(30,30,100,20)
        #fill(255,255,0)
        #rect(30,30,min(100,self.mario.CMCnt*10),20)
        
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
