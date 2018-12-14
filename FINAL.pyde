"""TO DO:
        1. Design level-3
        2. Populate level 1 and 3
        3. Change instructions page


"""

add_library('minim')
import os                     #libraries and importing os/time
import time
path=os.getcwd()
player = Minim(this)

class Creature:
    def __init__(self,x,y,r,g,img,w,h,F): #Creature Class with 
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
        self.grav=0
    
    def gravity(self):
        if self.grav==1:
            if self.y+self.r < self.g: #If character is above ground. used to be self.y + self.r
                self.vy += 0.25 #Give character velocity in positive y-axis (falling down) 
        
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r) #To ensure character stops at ground EXACTLY (and not below)
        
            
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
        
        if isinstance (self, rGPA or rCM or Fail or Trip):
            self.f = 1
            
        elif isinstance (self, Poof): 
            self.f = (self.f+0.1)%self.F
        elif self.vx != 0: #If the character is moving, then we cycle through the frames
            self.f = (self.f+0.3)%self.F
        else:
            self.f = 4 #Else we keep the same (stationary) frame 
            
        if self.dir >0 and self.F>1:
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h) #int(self.f)*self.w, means to choose the x,y coords of the entire image (all frames) corresponding to which frame we need
        elif self.dir < 0 and self.F>1:
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h) #switching x1 with x2 and y1 with y2, to flip the image horizontally
        elif self.dir >0 and self.F==1:
            image(self.img,self.x-self.w//2,self.y-self.h//2, self.w,self.h)#, 0,0, self.w,self.h) FLIPPING IMAGES!!!
        elif self.dir < 0 and self.F==1:
            image(self.img,self.x-self.w//2,self.y-self.h//2, self.w,self.h)#, self.w,0, 0,self.h)
        
        
class Player(Creature):
    def __init__(self,x,y,r,g,img,w,h,F, k):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler=k
        #print(self.keyHandler)
        self.coinSound = player.loadFile(path+"/sounds/coin.mp3")
        self.gpaSound = player.loadFile(path+"/sounds/gpa.mp3")
        self.coffeeSound = player.loadFile(path+"/sounds/coffee.mp3")
        self.failSound = player.loadFile(path+"/sounds/fail.mp3")
        self.quizSound = player.loadFile(path+"/sounds/quiz.mp3")
        self.tripSound = player.loadFile(path+"/sounds/restart.mp3")
        
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
        self.buttong0=0
        self.buttong1=0

        
    def update(self):

        for p in game.platforms:
              if self.isAbove(p) and self.buttong0==0 and self.buttong1==0:
                  self.g=p.y
                  self.grav=1
                  break
              elif not self.isAbove(p) and self.buttong0==0 and self.buttong1==0:
                  self.grav=1
                  self.g = game.g #Else we stick to original ground
                  
        for p in game.mplatforms:
            if self.isAbove(p): #(if character is above the platform AND within the width of platform) and not self.isInside(p) #and not self.keyHandler['UP']:
                self.g=p.y
                
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
        
        if game.l==1:
        
            if self.keyHandler['LEFT'] and self.wall==0:
                if game.buttons[0].pressed==0 and game.buttons[1].pressed==0 and game.gate.x-2+game.gate.w<=self.x-self.w//2<=game.gate.x+2+game.gate.w and game.gate.y<=self.y<=game.gate.y+game.gate.h:
                    return
                else:
                    self.vx = -5
                    self.dir = -1
                
            elif self.keyHandler['RIGHT'] and self.wall==0:
                if game.buttons[0].pressed==0 and game.buttons[1].pressed==0 and game.gate.x-2<=self.x+self.w//2<=game.gate.x+2 and game.gate.y<=self.y<=game.gate.y+game.gate.h:
                    return
                else:
                    self.vx = 5
                    self.dir = 1
            else:
                self.vx=0 
                
        if game.l in [2,3]:
            
            if self.keyHandler['LEFT'] and self.wall==0:
                self.vx = -5
                self.dir = -1
                
            elif self.keyHandler['RIGHT'] and self.wall==0:
                self.vx = 5
                self.dir = 1
            else:
                self.vx=0 
                
        if self.keyHandler['UP'] and self.g <= self.y+20: #and self.grav==0: #AND statement ensures that we cannot double jump
            self.vy = -10
    
        self.x += self.vx
        self.y += self.vy
        
        for p in game.platforms:
            if self.x in range(p.x, p.x+p.w) and self.y in range(p.y-10,p.y+p.h+40):
                self.vy=7
                self.vx=0
                self.wall=1

                    
        if self.isAbove(game.buttons[0]):
            self.buttong0=1
            self.g=game.buttons[0].y
            game.buttons[0].pressed=1
            #print ("button 0 pushed")
            #print(b.pressed)
        else:
            self.buttong0=0
            game.buttons[0].pressed=0 #NEED TO DISPLAY BARRIER ONCE BUTTON IS NOT PUSHED
            #print ("button 0 not pushed")
            
        if self.isAbove(game.buttons[1]):
            self.buttong1=1
            self.g=game.buttons[1].y
            game.buttons[1].pressed=1
            #print ("button 1 pushed")
            #print(b.pressed)
        else:
            self.buttong1=0
            game.buttons[1].pressed=0 #NEED TO DISPLAY BARRIER ONCE BUTTON IS NOT PUSHED
            #print ("button 1 not pushed")
    
               
                
        for t in game.oTrip:
            if self.cdistance(t) <= self.r + t.r and self.trip==0:
                game.poof.append(Poof(self.x,self.y,50,0,"Poof.png",128,128,10))
                bags=self.money #Amount of money player had before touching 
                grav=self.g
                self.money=0
                num=(bags//50) #Calculating the number of money objects corresponding to money lost
                for i in range (num-(num//2)): #Making half of money objects fall on right
                    game.CM.append(rCM(self.x+(70*(i+1)),self.y+20,20,grav,"Money.png",40,40,1,self.y,self.y,0)) #Appending money objects to display at point of character
                for i in range (num//2): #Making half of money objects fall on left
                    game.CM.append(rCM(self.x-(70*i),self.y+20,20,grav,"Money.png",40,40,1,self.y,self.y,0)) #Appending money objects to display at point of character
                self.tripSound.rewind()
                self.tripSound.play()
                self.x=self.ox
                self.y=self.oy
                
        for f in game.oFail:
            if self.cdistance(f) <= self.r + f.r and self.fail==0:
                game.poof.append(Poof(self.x,self.y,50,0,"Poof.png",128,128,10))
                if self.grade>=0.5:
                    self.grade-=0.5
                else:
                    self.grade=0
                self.failSound.rewind()
                self.failSound.play()
                self.x=self.ox
                self.y=self.oy
                #self.fail=1
                    
# for q in game.oQuiz:
#     if self.quiz==-1 and self.cdistance(q) < self.r + q.r:
#         self.quiz=0
#     if self.cdistance(q)==self.r+q.r and self.quiz==0:
#         self.quiz=1
#     if self.quiz==1:
#         self.grade-=0.2
#         # if self.grade>=0.2:
#         #     self.grade-=0.2
#         # else:
#         #     self.grade=0
            
        
# for s in game.oStarbucks:
#     if s.coffee==-1 and self.cdistance(s) < self.r + s.r:
#         s.coffee=0
#     if self.cdistance(s) >= self.r + s.r and s.coffee==0:
#         s.coffee=1
#     if s.coffee==1:
#         self.money-=150
#         s.coffee = -1
#         print (s.coffee)
#         # if self.money>=150:
#         #     self.money-=150
#         # else:
#         #     self.money=0
            
                    
        for q in game.oQuiz:
            if self.quiz==0 and self.cdistance(q) < self.r + q.r:
                self.quiz=1
                if self.grade>=0.2:
                    self.grade-=0.2
                else:
                    self.grade=0
                self.quizSound.rewind()
                self.quizSound.play()
                q.x=q.ox
                q.y=q.oy
                self.quiz=0
                    
                
        for s in game.oStarbucks:
            if self.coffee==0 and self.cdistance(s) < self.r + s.r:
                self.coffee=1
                if self.money>=150:
                    self.money-=150
                else:
                    self.money=0
                self.coffeeSound.rewind()
                self.coffeeSound.play()
                s.x=s.ox
                s.y=s.oy
                self.coffee=0          
                    
                
        for m in game.CM:
            if self.cdistance(m) <= self.r + m.r:
                self.money+=50
                game.CM.remove(m)
                del m
                self.coinSound.rewind()
                self.coinSound.play()
                
        for g in game.GPA:
            if self.cdistance(g) <= self.r + g.r:
                self.grade+=0.2
                game.GPA.remove(g)
                del g
                self.gpaSound.rewind()
                self.gpaSound.play()
            
        if self.isInside(game.door):
            self.dead = True
            game.alive_players-=1
            
    def cdistance(self,e): #COLLISION DETECTION
        return (((self.x+self.w//2)-(e.x+e.w//2))**2+((self.y+self.h//2)-(e.y+e.h//2))**2)**0.5

    def isAbove(self,platform):
        return self.x in range(platform.x, platform.x+platform.w) and self.y <= platform.y
    
    def isInside(self,platform):
        return self.x in range(platform.x, platform.x+platform.w) and self.y in range(platform.y,platform.y+platform.h)
    
    # def closestWall(self,platform):
    #     if abs(self.x-platform.x)<abs((self.x-(platform.x+platform.w))):
    #         x = platform.x
    #         xdist = abs(self.x-platform.x)
    #     else:
    #         x = platform.x+platform.w
    #         xdist = abs((self.x-(platform.x+platform.w)))
    #     if abs(self.y-platform.y)<abs((self.y-(platform.y+platform.h))):
    #         y = platform.y
    #         ydist = abs(self.y-platform.y)
    #     else:
    #         y = platform.y+platform.h
    #         ydist = abs((self.y-(platform.y+platform.h)))
            
    #     if xdist < ydist:
    #         return x, self.y
    #     else:
    #         return self.x, y
    
class rGPA(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.cx = x
        self.cy = y #NO MOVEMENT
        
    def gravity(self):
        return

class rCM(Creature): #Creature unaffected by gravity (FLYING)
    def __init__(self,x,y,r,g,img,w,h,F,y1,y2,move): #y1 and y2 are the vertical endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.y1=y1
        self.y2=y2
        self.vy=3
        self.dir = -1
        self.move=move
        
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
        self.vx = 3
                
    def update(self):
        self.gravity()
        
        if self.x > self.x2:
            self.vx = -3
            self.dir = -1
        elif self.x < self.x1:
            self.vx = 3
            self.dir = 1
        
        self.x += self.vx
        self.y += self.vy
        
class Trip(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,t,r1,move):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.cx = x
        self.cy = y
        self.t = t
        self.r1 = r1
        self.move=move
        
    def update(self):
        
        if self.move==1:
            self.t = self.t+1 #Circular movement
            
            self.x = self.cx + self.r1 * cos (self.t * PI/180)
            self.y = self.cy + self.r1 * sin (self.t * PI/180)
        
class Quiz(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2): #x1 and x2 are the horizontal endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = 2
        self.ox=x
        self.oy=y
    
    def update(self):
        self.gravity()
        
        if self.x > self.x2:
            self.vx = -2
            self.dir = -1
        elif self.x < self.x1:
            self.vx = 2
            self.dir = 1
        
        self.x += self.vx
        self.y += self.vy
        
class Coffee(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2): #x1 and x2 are the horizontal endpoints
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1=x1
        self.x2=x2
        self.vx = 3
        self.ox=x
        self.oy=y
        self.coffee=-1
        
    def update(self):
        self.gravity()
        
        if self.x > self.x2:
            self.vx = -3
            self.dir = -1
        elif self.x < self.x1:
            self.vx = 3
            self.dir = 1
            
        self.x += self.vx
        self.y += self.vy
        
class Poof(Creature): #The animation of characters restarting positions
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        
    def gravity(self):
        return    
    
    def update(self):
        if int(self.f) == 9:
            game.poof.remove(self)
            del self
            return
        
class Platform: #STATIONARY
    def __init__(self,x,y,w,h,c=0):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.c=c
        self.img1 = loadImage(path+"/images/platform1.png")
        self.img2 = loadImage(path+"/images/platform2.png")
        
    def display(self):
        #rect(self.x,self.y,self.w,self.h)
        if self.c==0:
            image(self.img1,self.x,self.y,self.w,self.h, 0,0, self.w,self.h)
        else:
            image(self.img2,self.x,self.y,self.w,self.h, 0,0, self.w,self.h)
        
class mPlatform: #Moving Platforms
    def __init__(self,x,y,w,h,m=0,y1=0,y2=0):
        self.x=x
        self.y=y
        self.y1=y1
        self.y2=y2
        self.vy=+4
        self.w=w
        self.h=h
        self.m=m #Flag to check whether it's a stationary platform (m=0) or a moving one (m=1)
        self.img = loadImage(path+"/images/platform1.png")
        
    def display(self):
        self.update()
        #rect(self.x,self.y,self.w,self.h)
        image(self.img,self.x,self.y,self.w,self.h, 0,0, self.w,self.h)
        
    def update(self): #Making the platform move between vertical points
        if self.m:
            if self.vy == 0:
                self.vy=-4
            if self.y <= self.y1:
                self.vy = 4
            if self.y >= self.y2:
                self.vy = -4     
        else:
            self.vy=0
            
        self.y += self.vy
        
class Door:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img = loadImage(path+"/images/door.png")
        #self.d=1 #WHY DID I NEED THIS? FOR GATE?
        
    def display(self):
        #rect(self.x,self.y,self.w,self.h)
        image(self.img,self.x,self.y,self.w,self.h)
        
class Gate(Door):
    def __init__(self,x,y,w,h):
        Door.__init__(self,x,y,w,h)
        self.opened=1
        self.img = loadImage(path+"/images/Wall.png")
        
    def display(self):
        print ("0: ", game.buttons[0].pressed)
        print ("1: ", game.buttons[1].pressed)

        if not (game.buttons[1].pressed or game.buttons[0].pressed):
            #rect(self.x,self.y,self.w,self.h)
            image(self.img,self.x,self.y,self.w,self.h)
        
class Button(Platform):
    def __init__(self,x,y,w,h):
        Platform.__init__(self,x,y,w,h)
        self.pressed=0
        

class Game:
    def __init__ (self,w,h,g,l): #width, height and ground of the game board
        self.w=w
        self.h=h
        self.g=g
        self.l=l
        
        self.CMImg=loadImage(path+"/images/Money.png")
        self.GPAImg=loadImage(path+"/images/GPA.png")
        self.instImg=loadImage(path+"/images/Inst.png") #INSERT THE SCREENSHOT HERE
        self.ENDImg=loadImage(path+"/images/Congratulations.jpg")
        
        self.state = "menu"
        self.pause = False
        self.pauseSound = player.loadFile(path+"/sounds/pause.mp3")
        self.winSound = player.loadFile(path+"/sounds/Congratulations!.mp3")
        
        self.music = player.loadFile(path+"/sounds/game.mp3")
        if self.l==1:
            self.music.play()
        
        self.BGImg=loadImage(path+"/images/BG"+str(self.l)+".jpg")
        
        
        self.oFail = [] #Fail that makes you restart position as well as reduces GPA by 0.5
        self.oTrip = [] #Trip that makes you restart position as well as reduces CM to 0
        self.oStarbucks = [] #Coffee cup that reduces your CM by 150
        self.oQuiz = [] #Quiz paper that makes you lose your GPA by 0.4
        self.CM = [] #Campus Money 
        self.GPA = [] #GPA
        self.platforms=[]
        self.mplatforms=[]
        # self.door=[]
        # self.gate=[]
        self.buttons=[]
        self.players=[]
        self.poof=[]
        self.alive_players = 2
        #for i in range(3):
            
        if self.l==1:
            self.lvl1()
        elif self.l==2:
            self.lvl2()
        elif self.l==3:
            self.lvl3()
        elif self.l==4:
            self.lvl4()
            
    def lvl1(self):
        self.p1 = Player(50,668,20,self.g,"Player1.png",52,70,8,{'LEFT':False, 'RIGHT':False, 'UP':False}) #Player-1
        self.p2 = Player(100,668,20,self.g,"Player1.png",52,70,8,{'LEFT':False, 'RIGHT':False, 'UP':False}) #Player-2
        
        self.players.append(self.p1)
        self.players.append(self.p2)
        #print(len(self.players))
        
                
        self.platforms.append(Platform(0,150,1216,50,1)) #Platform-3
        self.platforms.append(Platform(400,350,1216,50,1)) #Platform-2
        self.platforms.append(Platform(0,550,1216,50,1)) #Platform-1
                
        self.platforms.append(Platform(-299,0,300,768)) #WALLS
        self.platforms.append(Platform(1439,0,300,768))
        
        #BUTTON FOR BARRIER
        self.buttons.append(Button(0,540,50,10)) #Bottom left
        self.buttons.append(Button(900,340,50,10)) #Top right
                
        #self.platforms.append(Platform(0,718,1440,50)) #Ground
        
        self.door=Door(200,80,70,70) #Door
        self.gate=Gate(600,200,50,150) #Gate
    
        for i in range(5):
            self.GPA.append(rGPA(50+i*60,100,20,self.g,"GPA.png",50,50,1)) #GPA hat objects (NO MOVEMENT)
        for i in range(5):
            self.GPA.append(rGPA(250+i*60,270,20,self.g,"GPA.png",50,50,1))
                
        for i in range(5):
            self.CM.append(rCM(300,275+i*50,20,self.g,"Money.png",40,40,1,250,500,1))  #Campus money objects (y1=top height limit, y2=bottom height limit, last argument is move: =1 for vertical movement, =0 for no vertical movement)      
        
        # self.CM.append(rCM(300,275,20,self.g,"Money.png",40,40,1,300,500,1)) 
        # self.CM.append(rCM(300,250,20,self.g,"Money.png",40,40,1,300,500,1))
        # self.CM.append(rCM(300,225,20,self.g,"Money.png",40,40,1,300,500,1))
        
        self.oStarbucks.append(Coffee(100,105,20,self.g,"Coffee.png",30,40,1,100,500))
        
        #self.oQuiz.append(Quiz(200,80,20,self.g,"Quiz.png",50,50,1,100,300)) #Creating quiz objects
                
        #self.oTrip.append(Trip(50,100,42,self.g,"Trip.png",75,75,1,50,850,0)) #Creating Trip objects
        #self.oFail.append(Fail(50,100,42,self.g,"Fail.png",50,50,1,50,450)) #Creating Fail objects  
        
    def lvl2(self):
        self.p1 = Player(50,668,20,self.g,"Player1.png",52,70,8,{'LEFT':False, 'RIGHT':False, 'UP':False}) #Player-1
        self.p2 = Player(1350,668,20,self.g,"Player2.png",52,70,8,{'LEFT':False, 'RIGHT':False, 'UP':False}) #Player-2
        
        self.players.append(self.p1)
        self.players.append(self.p2)
        #print(len(self.players))
        
        self.buttons.append(Button(695,440,50,10)) #1st Middle button
        self.buttons.append(Button(350,140,50,10)) #Top left
        
        #Top platforms    
        
        #Left    
        self.platforms.append(Platform(0,150,400,50)) 
        self.oFail.append(Fail(50,125,20,self.g,"Fail.png",50,50,1,50,350))
        #self.oStarbucks.append(Coffee(40,130,10,self.g,"Coffee.png",30,40,1,40,470))
        
        for i in range(3):
            self.GPA.append(rGPA(50+i*60,125,20,self.g,"GPA.png",50,50,1)) #GPA hat objects (NO MOVEMENT)
        
        #Right
        self.platforms.append(Platform(1040,150,400,50))
        self.oStarbucks.append(Coffee(1410,130,10,self.g,"Coffee.png",30,40,1,1055,1410))
        
        for i in range(5):
            self.CM.append(rCM(1130+i*60,130,20,self.g,"Money.png",40,40,1,300,500,0))
        
        self.platforms.append(Platform(660,450,120,50)) #Middle tiny platform
        
        #Bonus platforms
        
        #Left
        self.platforms.append(Platform(75,300,270,50)) 
        
        self.oTrip.append(Trip(220,355,20,self.g,"Trip.png",75,75,1,180,130,1))
        
        self.CM.append(rCM(100,280,20,self.g,"Money.png",40,40,1,300,500,0))
        self.GPA.append(rGPA(150,275,20,self.g,"GPA.png",50,50,1))
        self.CM.append(rCM(210,280,20,self.g,"Money.png",40,40,1,300,500,0))
        self.GPA.append(rGPA(260,275,20,self.g,"GPA.png",50,50,1))
        self.CM.append(rCM(320,280,20,self.g,"Money.png",40,40,1,300,500,0))
            
        #Right
        self.platforms.append(Platform(1070,300,270,50)) 
        
        self.oTrip.append(Trip(1215,355,20,self.g,"Trip.png",75,75,1,0,130,1))
        
        self.CM.append(rCM(1095,280,20,self.g,"Money.png",40,40,1,300,500,0))
        self.GPA.append(rGPA(1145,275,20,self.g,"GPA.png",50,50,1))
        self.CM.append(rCM(1205,280,20,self.g,"Money.png",40,40,1,300,500,0))
        self.GPA.append(rGPA(1255,275,20,self.g,"GPA.png",50,50,1))
        self.CM.append(rCM(1305,280,20,self.g,"Money.png",40,40,1,300,500,0))
        
        #Moving Platforms
        self.mplatforms.append(mPlatform(500,600,150,50,0,200,600)) #Left
        self.mplatforms.append(mPlatform(790,600,150,50,0,200,600)) #Right
        
        for i in range(8):
            self.CM.append(rCM(720,100+i*60,20,self.g,"Money.png",40,40,1,100,700,1))
                
        self.platforms.append(Platform(-299,0,300,768)) #WALLS
        self.platforms.append(Platform(1439,0,300,768))
                
        #self.platforms.append(Platform(0,718,1440,50)) #Ground
        self.oStarbucks.append(Coffee(200,698,10,self.g,"Coffee.png",30,40,1,50,1350))
        self.oStarbucks.append(Coffee(650,698,10,self.g,"Coffee.png",30,40,1,50,1350))
        self.oStarbucks.append(Coffee(1150,698,10,self.g,"Coffee.png",30,40,1,50,1350))
        
        self.door=Door(200,80,70,70) #Door
    
    
    def lvl3(self):
        self.p1 = Player(50,668,20,self.g,"Player1.png",52,70,8,{'LEFT':False, 'RIGHT':False, 'UP':False}) #Player-1
        self.p2 = Player(100,668,20,self.g,"Player1.png",52,70,8,{'LEFT':False, 'RIGHT':False, 'UP':False}) #Player-2
        
        self.players.append(self.p1)
        self.players.append(self.p2)
        
        #TOP
        self.platforms.append(Platform(0,150,500,50))
        self.platforms.append(Platform(940,150,500,50))
        
        #BOTTOM
        self.platforms.append(Platform(0,550,500,50))
        self.platforms.append(Platform(940,550,500,50))
        
        self.platforms.append(Platform(0,300,200,50))
        self.platforms.append(Platform(1240,300,200,50))
        
        #MOVING PLATFORM
        self.mplatforms.append(mPlatform(630,600,150,50,0,200,600))
        self.buttons.append(Button(680,590,50,10))
        
        self.buttons.append(Button(1050,140,50,10))
        
        self.door=Door(1330,80,70,70)
    
    def instDisp(self):
        background(255)
        image(self.instImg,0,-20,1440,768) #INSERT THE SCREENSHOT
        
    def update(self): #LEVEL CHANGE CONDITIONS
        if self.l==1 and self.alive_players==0:
            game.__init__(1440,768,718,2)
            game.state="play"
            self.lvl2()
        elif self.l==2 and self.alive_players==0:
            game.__init__(1440,768,718,3)
            game.state="play"
        elif self.l==3 and self.alive_players==0:
            game.music.pause()
            time.sleep(0.3)
            game.state="win"
            
    def display(self):
        
        background(0)
        self.update()
        
        stroke(255)
        #line(0,self.g,self.w,self.g)
        
        #BACKGROUND IMAGES
        image(self.BGImg,0,0,self.w,self.h)
        
        for p in self.platforms: #Displaying Platforms
            p.display()
            
        for m in self.mplatforms: #Displaying Moving Platforms
            m.display()
            
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
            
        for p in self.poof: #Displaying smoke when player restarts
            p.display()
            
        for b in self.buttons:
            b.display()
               
        if self.l==1: #GATES ONLY IN LEVEL 1
            if not (self.p1.isAbove(self.buttons[0]) or self.p2.isAbove(self.buttons[0]) or self.p1.isAbove(self.buttons[1]) or self.p2.isAbove(self.buttons[1])):
                self.gate.display() 
        
        if self.l==2:
            if self.p1.isAbove(self.buttons[0]) or self.p2.isAbove(self.buttons[0]) or self.p1.isAbove(self.buttons[1]) or self.p2.isAbove(self.buttons[1]):
                self.mplatforms[0].m=1
                self.mplatforms[1].m=1
            else:
                self.mplatforms[0].m=0
                self.mplatforms[1].m=0
                
        if self.l==3:
            if self.p1.isAbove(self.buttons[0]) or self.p2.isAbove(self.buttons[0]) or self.p1.isAbove(self.buttons[1]) or self.p2.isAbove(self.buttons[1]):
                self.mplatforms[0].m=1
            else:
                self.mplatforms[0].m=0
                    
                #print (self.mplatforms[0].m,self.mplatforms[1].m)
    
        self.door.display()
        
        if self.p1.dead == False:
            self.p1.display()
        if self.p2.dead == False:
            self.p2.display()
        
        
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

        
game = Game(1440,768,718,3) #Window dimensions, ground value and the level of the game

def setup():
    size(game.w, game.h)
    background(0)
    

def draw():
    
    if game.state == "menu":
        background(0)
        textSize(20)
        
        if game.w//2.5 < mouseX < game.w//2.5 + 200 and game.h-170 < mouseY < game.h-150:
            fill(160,160,160)
        else:
            fill(224,224,224)
        text("Play Game", game.w//2.5, game.h-150)
        if game.w//2.5 < mouseX < game.w//2.5 + 200 and game.h-120 < mouseY < game.h-90:
            fill(160,160,160)
        else:
            fill(224,224,224)
        text("Instructions", game.w//2.5, game.h-100)
        
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
            if game.w//2.5+70 < mouseX < game.w//2.5 + 260 and game.h-50 < mouseY < game.h-10: #Use same ratios, but diff positions according to image used
                fill(224,224,224)
            else:
                fill(160,160,160)
            text("Play Game!", game.w//2.5+80, game.h-20)
            
    elif game.state=="win":
        background(255)
        image(game.ENDImg,0,0)
        game.winSound.play()
        game.music.pause()
     
def mouseClicked():
    if game.state=="menu" and game.w//2.5 < mouseX < game.w//2.5 + 200 and game.h-170 < mouseY < game.h-150:
        game.state="play"
        game.music.play()
    elif game.state=="menu" and game.w//2.5 < mouseX < game.w//2.5 + 200 and game.h-120 < mouseY < game.h-90:
        game.state="inst"
    elif game.state=="inst" and game.w//2.5+70 < mouseX < game.w//2.5 + 260 and game.h-50 < mouseY < game.h-10:
        game.state="play"
        game.music.play()
    
def keyPressed():
    if keyCode == LEFT:
        game.p1.keyHandler['LEFT']=True
    elif keyCode == RIGHT:
        game.p1.keyHandler['RIGHT']=True
    elif keyCode == UP:
        game.p1.keyHandler['UP']=True
    elif key in ['a','A']:
        game.p2.keyHandler['LEFT']=True
    elif key in ['d','D']:
        game.p2.keyHandler['RIGHT']=True
    elif key in ['w','W']:
        game.p2.keyHandler['UP']=True
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
        game.p1.keyHandler['LEFT']=False
    elif keyCode == RIGHT:
        game.p1.keyHandler['RIGHT']=False   
    elif keyCode == UP:
        game.p1.keyHandler['UP']=False
    elif key in ['a','A']:
        game.p2.keyHandler['LEFT']=False
    elif key in ['d','D']:
        game.p2.keyHandler['RIGHT']=False
    elif key in ['w','W']:
        game.p2.keyHandler['UP']=False
