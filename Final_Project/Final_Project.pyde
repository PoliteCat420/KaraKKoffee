"""ERRORS:
    1. [DONE] (wall issue) Doesn't block wall if your y velocity is 0 (only moving horizontally on the ground), this is due to our condition to self.wall=0 only when self.vy==0 (so can walk through walls)
    2. [SORTA DONE] Door doesn't detect players (in player class, it says that it does'nt exist in self.players)
    3. 1 of the GPA objects still remains!!!
    
    
    Suggestions:
        1. Want to implement a time delay between touching the obstacle and restarting
        2. Some bonus for certain amount of coins collected (like fireball in class)
        
    To-Do:
        1. [DONE] CM counter (bar at top)
        2. [DONE] Animation of coins dropping when you die
        3. [DONE] TIME DELAY BETWEEN SAME OBSTACLE
        4. Animation of dying (vanishing)
        5. [DONE] Add doors at end
        6. Design 2 levels
        7. [SORTA DONE] Add background images
        8. Add feature (unity) for final level
        9. [SORTA DONE] Design Menu (Play game + Instructions)
        
    Doubts:
        1. Is it fine if we use Mario code
    
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

#Write these with "in [...]" ?
        if isinstance (self, rGPA):
            self.f = 1
        elif isinstance (self, rCM):
            self.f = 1
        elif isinstance (self, Fail):
            self.f = 1
        elif isinstance (self, Trip):
            self.f = 1
        elif self.vx != 0: #If the character is moving, then we cycle through the frames
            self.f = (self.f+0.3)%self.F
        else:
            self.f = 3 #Else we keep the same (stationary) frame (ONLY WORKS FOR MARIO TEMPLATE SINCE f=3 IS STATIONARY THERE)
            
        #if self.dir >0 and isinstance (self, Trip):
        
        if self.dir >0 and self.F>1:
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #int(self.f)*self.w, means to choose the x,y coords of the entire image (all frames) corresponding to which frame we need
        elif self.dir < 0 and self.F>1:
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #switching x1 with x2 and y1 with y2, to flip the image horizontally
        elif self.dir >0 and self.F==1:
            image(self.img,self.x-self.w//2,self.y-self.h//2, self.w,self.h)#, 0,0, self.w,self.h) FLIPPING IMAGES!!!
        elif self.dir < 0 and self.F==1:
            image(self.img,self.x-self.w//2,self.y-self.h//2, self.w,self.h)#, self.w,0, 0,self.h)
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
        self.fail=0 #Flag for fail object of P1
        self.trip=0 #Flag of trip object of P1
        self.quiz=0 #Flag of quiz object of P1
        self.GPA=0 #Flag of gpa object of P1
        self.coffee=0 #Flag of coffee object of P1
        self.CM=0 #Flag of money object of P1
        self.ox=x
        self.oy=y
        self.dead = False
        
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
            if self.cdistance(t) <= self.r + t.r and self.trip==0:
                bags=self.money #Amount of money player had before touching 
                grav=self.g
                self.money=0
                num=(bags//50) #Calculating the number of money objects corresponding to money lost
                for i in range (num-(num//2)): #Making half of money objects fall on right
                    game.CM.append(rCM(self.x+(70*(i+1)),self.y+20,20,grav,"Money.png",40,40,1,self.y,self.y,0)) #Appending money objects to display at point of character
                for i in range (num//2): #Making half of money objects fall on left
                    game.CM.append(rCM(self.x-(70*i),self.y+20,20,grav,"Money.png",40,40,1,self.y,self.y,0)) #Appending money objects to display at point of character
                self.x=self.ox
                self.y=self.oy
                #self.trip=1
                    
        for f in game.oFail:
            if self.cdistance(f) <= self.r + f.r and self.fail==0:
                self.grade-=0.5
                self.x=self.ox
                self.y=self.oy
                #self.fail=1
                    
        for q in game.oQuiz:
            if self.cdistance(q) <= self.r + q.r and self.quiz==0:
                self.grade-=0.2
                self.quiz=1
            if self.cdistance(q) > self.r + q.r:
                self.quiz=0
                
        for s in game.oStarbucks:
            if self.cdistance(s) <= self.r + s.r and self.coffee==0:
                self.money-=150
                self.coffee=1
            if self.cdistance(s) > self.r + s.r:
                self.coffee=0
                
                    
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
            
        if self.x>=(game.door.x-20) and self.x<=(game.door.x+game.door.w+20) and self.y>=(game.door.y-10) and self.y<=(game.door.y+game.door.h+40):
            self.dead = True
            game.alive_players-=1
        

        
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
        self.fail=0 #Flag of fail object of P2
        self.trip=0 #Flag of trip object of P2
        self.quiz=0 #Flag of quiz object of P2
        self.GPA=0 #Flag of gpa object of P2
        self.coffee=0 #Flag of coffee object of P2
        self.CM=0 #Flag of money object of P2
        self.ox=x
        self.oy=y
        self.dead = False
        
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
            if self.cdistance(t) <= self.r + t.r and self.trip==0:
                bags=self.money #Amount of money player had before touching 
                grav=self.g
                self.money=0
                num=(bags//50) #Calculating the number of money objects corresponding to money lost
                for i in range (num-(num//2)): #Making half of money objects fall on right
                    game.CM.append(rCM(self.x+(70*(i+1)),self.y+20,20,grav,"Money.png",40,40,1,self.y,self.y,0)) #Appending money objects to display at point of character
                for i in range (num//2): #Making half of money objects fall on left
                    game.CM.append(rCM(self.x-(70*i),self.y+20,20,grav,"Money.png",40,40,1,self.y,self.y,0)) #Appending money objects to display at point of character
                self.x=self.ox
                self.y=self.oy
                #self.trip=1
                    
        for f in game.oFail:
            if self.cdistance(f) <= self.r + f.r and f.fail==0:
                self.grade-=0.5
                self.x=self.ox
                self.y=self.oy
                #self.fail=1
                    
        for q in game.oQuiz:
            if self.cdistance(q) <= self.r + q.r and self.quiz==0:
                self.grade-=0.2
                self.quiz=1
            if self.cdistance(q) > self.r + q.r:
                self.quiz=0
                
        for s in game.oStarbucks:
            if self.cdistance(s) <= self.r + s.r and self.coffee==0:
                self.money-=150
                self.coffee=1
            if self.cdistance(s) > self.r + s.r:
                self.coffee=0
                
                    
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
        
        if self.x>=(game.door.x-20) and self.x<=(game.door.x+game.door.w+20) and self.y>=(game.door.y-10) and self.y<=(game.door.y+game.door.h+40):
            self.dead = True
            game.alive_players-=1
        
        """if self.x>=(game.door.x-20) and self.x<=(game.door.x+game.door.w+20) and self.y>=(game.door.y-10) and self.y<=(game.door.y+game.door.h+40):
            game.players.remove(self)"""
        
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
        #self.gpa=0
        
    def gravity(self):
        return
    
class rCM(Creature): #Creature unaffected by gravity (FLYING)
    def __init__(self,x,y,r,g,img,w,h,F,y1,y2,move): #y1 and y2 are the vertical endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.y1=y1
        self.y2=y2
        self.dir = -1
        self.move=move
        #self.money=0
        
    def update(self): #Giving endpoints for the creature to move between (VERTICAL MOVEMENT)
        
        if self.move==1:
            if self.y < self.y1:
                self.vy = 3
            elif self.y > self.y2:
                self.vy = -3
            
        elif self.move==0:
            self.vy=0
            
        self.y += self.vy
        
class Fail(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2): #x1 and x2 are the horizontal endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = 2
        #self.fail=0
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
        #self.trip=0
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
        #self.quiz=0
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
        #self.coffee=0
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
        
class Door:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img = loadImage(path+"/images/Door.png")
        self.d=1
        
    def display(self):
        rect(self.x,self.y,self.w,self.h)
        #image(self.img,self.x,self.y,self.w,self.h)
        
            
class Game:
    def __init__ (self,w,h,g): #width, height and ground of the game board
        self.w=w
        self.h=h
        self.g=g
        
        self.CMImg=loadImage(path+"/images/Money.png")
        self.GPAImg=loadImage(path+"/images/GPA.png")
        self.instImg=loadImage(path+"/images/Inst.png") #INSERT THE SCREENSHOT HERE
        
        self.state = "menu"
        self.level=1
        self.pause = False
        self.pauseSound = player.loadFile(path+"/sounds/pause.mp3")
        
        self.music = player.loadFile(path+"/sounds/music.mp3")
        self.music.play()
        
        self.BGImg=loadImage(path+"/images/BG"+str(self.level)+".jpg")
        
        
        self.oFail = [] #Fail that makes you restart position as well as reduces GPA by 0.5
        self.oTrip = [] #Trip that makes you restart position as well as reduces CM to 0
        self.oStarbucks = [] #Coffee cup that reduces your CM by 150
        self.oQuiz = [] #Quiz paper that makes you lose your GPA by 0.4
        self.CM = [] #Campus Money 
        self.GPA = [] #GPA
        self.platforms=[]
        self.door=[]
        self.players=[]
        self.alive_players = 2
        #for i in range(3):
            
        if self.level==1:
            self.lvl1()
            # if self.alive_players==0:
            #     self.level=2
        elif self.level==2:
            self.DelObject()
            self.lvl2()
            # if self.alive_players==0:
            #     self.level=3
        elif self.level==3:
            self.DelObject()
            self.lvl3()
     
    def lvl1(self):
        self.p1 = Player1(50,668,35,self.g,"mario.png",100,70,11) #Player-1
        self.p2 = Player2(100,668,35,self.g,"mario.png",100,70,11) #Player-2
        
        self.players.append(self.p1)
        self.players.append(self.p2)
        #print(len(self.players))
        
                
        self.platforms.append(Platform(0,150,1216,50)) #Platform-3
        self.platforms.append(Platform(400,350,1100,50)) #Platform-2
        self.platforms.append(Platform(0,550,1216,50)) #Platform-1
                
        self.platforms.append(Platform(-299,0,300,768)) #WALLS
        self.platforms.append(Platform(1439,0,300,768))
                
        self.platforms.append(Platform(0,718,1440,50)) #Ground
        
        self.door=Door(400,50,50,80) #Door
    
        for i in range(5):
            self.GPA.append(rGPA(50+i*60,120,20,self.g,"GPA.png",50,50,1)) #GPA hat objects (NO MOVEMENT)
        for i in range(5):
            self.GPA.append(rGPA(250+i*60,270,20,self.g,"GPA.png",50,50,1))
                
        self.CM.append(rCM(300,275,20,self.g,"Money.png",40,40,1,300,500,1)) #Campus money objects (y1=top height limit, y2=bottom height limit, last argument is move: =1 for vertical movement, =0 for no vertical movement)
        self.CM.append(rCM(300,250,20,self.g,"Money.png",40,40,1,300,500,1))
        self.CM.append(rCM(300,225,20,self.g,"Money.png",40,40,1,300,500,1))
        
        self.oStarbucks.append(Quiz(100,100,20,self.g,"Coffee.png",30,40,1,100,500))
        
        #self.oQuiz.append(Quiz(200,80,20,self.g,"Quiz.png",50,50,1,100,300)) #Creating quiz objects
                
        self.oTrip.append(Trip(50,100,42,self.g,"Trip.png",75,75,1,50,450)) #Creating Trip objects
        #self.oFail.append(Fail(50,100,42,self.g,"Fail.png",50,50,1,50,450)) #Creating Fail objects  
        
    
    def DelObject(self):
        for i in self.oFail:
            self.oFail.remove(i)
        for i in self.oTrip:
            self.oTrip.remove(i)
        for i in self.oStarbucks:
            self.oStarbucks.remove(i)
        for i in self.oQuiz:
            self.oQuiz.remove(i)
        for i in self.CM:
            self.CM.remove(i)
        for i in self.GPA:
            self.GPA.remove(i)
        for i in self.platforms:
            self.platforms.remove(i)
        self.door.d=0
        
        
    def instDisp(self):
        background(255)
        image(self.instImg,-75,-50,1400,700) #INSERT THE SCREENSHOT
        
    def update(self):
        if self.level==1 and self.alive_players==0:
            self.level=2
            self.DelObject()
            pass #UNSURE
            #self.lvl2()
        elif self.level==2 and self.alive_players==0:
            self.level=3
            self.DelObject()
            pass #UNSURE
            #self.lvl3()
        
    def display(self):
        
        self.update()
        
        stroke(255)
        #line(0,self.g,self.w,self.g)
        
        #BACKGROUND IMAGES
        image(self.BGImg,0,0,self.w,self.h)
        
        
        # BIT OF A HACK
        # 1 player alive: set self.alive_players = 1
        # two players alive: set it to 2
        # use this instead of the list len
        
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
               
        if self.door.d==1:
            self.door.display()
        
        if self.p1.dead == False:
            self.p1.display()
        if self.p2.dead == False:
            self.p2.display()
        
        """textSize(20) #Campus Money Counter
        fill(255) 
        text("P1:"+str(self.p1.money),game.w-150,40)
        text("P2:"+str(self.p2.money),game.w-150,110)
        image(self.CMImg,game.w-35,23, 20,20)
        image(self.CMImg,game.w-35,57, 20,20)
        
        textSize(20) #GPA Counter
        fill(255) 
        text(str(self.p1.grade),game.w-145,75)
        text(str(self.p2.grade),game.w-145,145)
        image(self.GPAImg,game.w-35,23, 20,20)
        image(self.GPAImg,game.w-35,57, 20,20)"""
        
        
        textSize(20) #Counters
        fill(255)
        image(self.CMImg,game.w-35,23, 20,20) #Player-1 Money counter
        text("P1:"+str(self.p1.money),game.w-150,40)
        image(self.GPAImg,game.w-35,55, 20,20) #Player-1 GPA counter
        text(str(self.p1.grade),game.w-120,75)
        image(self.CMImg,game.w-35,93, 20,20) #Player-2 Money counter
        text("P2:"+str(self.p2.money),game.w-150,110)
        image(self.GPAImg,game.w-35,127, 20,20) #Player-2 GPA counter
        text(str(self.p2.grade),game.w-120,145)
        """image(self.CMImg,game.w-35,23, 20,20)
        image(self.CMImg,game.w-35,57, 20,20)"""
        
        #rect(30,30,100,20)
        #fill(255,255,0)
        #rect(30,30,min(100,self.mario.CMCnt*10),20)
        
game = Game(1440,768,718) #Window dimensions and the ground value

def setup():
    size(game.w, game.h)
    background(0)
    
    
def draw():
    
    if game.state == "menu":
        background(0)
        textSize(34)
        # fill(255)
        # rect(game.w//2.5, game.h//3, 200, 50)
        # fill(255)
        # rect(game.w//2.5, game.h//3+100, 200, 50)
        
        if game.w//2.5 < mouseX < game.w//2.5 + 200 and game.h//3 < mouseY < game.h//3 + 50:
            fill(255,0,0)
        else:
            fill(255)
        text("Play Game", game.w//2.5, game.h//3+40)
        if game.w//2.5 < mouseX < game.w//2.5 + 200 and game.h//3+100 < mouseY < game.h//3 + 150:
            fill(255,0,0)
        else:
            fill(255)
        text("Instructions", game.w//2.5, game.h//3+140)
        
    elif game.state == "play":
        if game.pause == True:
            textSize(70)
            fill(255)
            rect(game.w//3,100,50,50)
            fill(0,255,255)
            text("Paused",game.w//3,100)
        
        else:
            background(0)
            game.display()
            
    elif game.state == "inst":
        if not game.pause:
            game.instDisp()
            if game.w//2.5-20 < mouseX < game.w//2.5 + 180 and game.h-135 < mouseY < game.h-85: #Use same ratios, but diff positions according to image used
                fill(255,0,0)
            else:
                fill(0)
            text("Play Game!", game.w//2.5, game.h-100)
            
    """elif game.pause == False:
        background(0)
        game.display()
    elif game.pause == True:
        textSize(70)
        fill(0)
        text("Paused",game.w//2,game.h//2)"""
        
def mouseClicked():
    if game.state=="menu" and game.w//2.5 < mouseX < game.w//2.5 + 200 and game.h//3 < mouseY < game.h//3 + 50:
        game.state="play"
        game.music.play()
    elif game.state=="menu" and game.w//2.5 < mouseX < game.w//2.5 + 200 and game.h//3+100 < mouseY < game.h//3 + 150:
        game.state="inst"
    elif game.state=="inst" and game.w//2.5-20 < mouseX < game.w//2.5 + 180 and game.h-135 < mouseY < game.h-85:
        game.state="play"
        game.music.play()
    
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
        game.pauseSound.rewind()
        game.pauseSound.play()
        
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
