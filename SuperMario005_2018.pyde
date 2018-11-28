add_library('minim')
import os
path=os.getcwd()
player = Minim(this)

class Creature:
    def __init__(self,x,y,r,g,img,w,h,F):
        self.x=x
        self.y=y
        self.r=r
        self.g=g
        self.vx=0
        self.vy=0
        self.w=w
        self.h=h
        self.F=F
        self.f=0
        self.img = loadImage(path+"/images/"+img)
        self.dir = 1
    
    def gravity(self):
        if self.y+self.r < self.g:
            self.vy += 0.3
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0 #-10
            
        for p in game.platforms:
            if self.x in range(p.x, p.x+p.w) and self.y+self.r <= p.y:
                self.g = p.y
                break
            else:
                self.g = game.g
    
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()

        if isinstance (self, Koopa):
            self.f = (self.f+0.3)%self.F
        elif self.vx != 0:
            self.f = (self.f+0.3)%self.F
        else:
            self.f = 3
            
        if self.dir > 0:
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
            
        # stroke(255)
        # noFill()
        # ellipse(self.x,self.y,2*self.r,2*self.r)
    
class Mario(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler={LEFT:False, RIGHT:False, UP:False}
    def update(self):
        self.gravity()
        
        if self.keyHandler[LEFT]:
            self.vx = -5
            self.dir = -1
        elif self.keyHandler[RIGHT]:
            self.vx = 5
            self.dir = 1
        else:
            self.vx = 0
        
        if self.keyHandler[UP] and self.y+self.r == self.g:
            self.vy = -10
        
        self.x += self.vx
        self.y += self.vy
    
class Koopa(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,y1,y2):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.y1=y1
        self.y2=y2
        self.dir = -1
        
    def update(self):
        
        if self.y < self.y1:
            self.vy = 3
        elif self.y > self.y2:
            self.vy = -3
            
        self.y += self.vy
        
class Pikatshu(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
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
        
        if int(random(100)) == 1 and self.y+self.r == self.g:
            self.vy = -10
            # self.jump.rewind()
            # self.jump.play()
        
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
        image(self.img,self.x,self.y)
            
class Game:
    def __init__ (self,w,h,g):
        self.w=w
        self.h=h
        self.g=g
        self.mario = Mario(50,50,35,self.g,"mario.png",100,70,11)
        self.enemies = []
        for i in range(5):
            self.enemies.append(Pikatshu(250+i*100,50,42,self.g,"pikatshu.png",120,85,4,100,1000))
        self.enemies.append(Koopa(150,50,35,self.g,"koopa.png",70,70,8,200,500))
        
        self.platforms=[]
        for i in range(3):
            self.platforms.append(Platform(250+i*250,450-150*i,200,50))
        
    def display(self):
        stroke(255)
        line(0,self.g,self.w,self.g)
            
        for p in self.platforms:
            p.display()
        
        for e in self.enemies:
            e.display() 
               
        self.mario.display()
        
game = Game(1024,768,600)

def setup():
    size(game.w, game.h)
    background(0)
    
def draw():
    background(0)
    game.display()
    
def keyPressed():
    if keyCode == LEFT:
        game.mario.keyHandler[LEFT]=True
    elif keyCode == RIGHT:
        game.mario.keyHandler[RIGHT]=True
    elif keyCode == UP:
        game.mario.keyHandler[UP]=True
        
def keyReleased():
    if keyCode == LEFT:
        game.mario.keyHandler[LEFT]=False
    elif keyCode == RIGHT:
        game.mario.keyHandler[RIGHT]=False   
    elif keyCode == UP:
        game.mario.keyHandler[UP]=False
        
            
                    
