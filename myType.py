import pygame
import pygame.gfxdraw as gfxdraw
import math
import numpy as np
import random

pygame.init()
# setup 
screen = pygame.display.set_mode((800, 600), pygame.SRCALPHA)
pygame.display.set_caption("myType")
icon = pygame.image.load("data/type.png")
pygame.display.set_icon(icon)

startTime = pygame.time.get_ticks()
loadingImg = pygame.image.load("data/typing.png")

aiImg = pygame.image.load("data/AI symbol.png")
brainImg = pygame.image.load("data/brain.png")

def genFont(f, size):
    return pygame.font.Font(f, size)

def text(x, y, font, txt, c):
    t = font.render(txt, True, c)
    tr = t.get_rect()
    tr.center = (x, y)
    screen.blit(t, tr)

# var naming from JS habit fooBar not foo_bar\

# scene & input vars
scene = 1
mX = 0
mY = 0
clicked = False
pastPress = False

# transition vars
ty = 2
down = True
transitioning = False
nextScene = 2

# OOP vars
menubuttons = []
donebuttons = []
customizebuttons = []
statsbuttons = []
settingsbuttons = []
infobuttons = []
bubbles = []

# Type vars
typeString = ""
onWord = 0
correctLetters = 0
typeStart = 0
totalLetters = 0

# Custom vars
showNum = 6
fontsArr = [15, 20, 25, 30]
fontSize = 1
useBackground = True

# AI part of the project: predicting type speeds 
txtfile = open(r"data\textdata.txt", "r+")
wordarr = txtfile.readlines()
wordbank = random.sample(range(1, len(wordarr)), 300)
txtfile.close()

wpms = open("data\wpms.txt", 'r')
wpmarrs = wpms.readlines()
wpms.close()

sum = 0
last10 = 0
best = 0
if len(wpmarrs) > 0:
    for i in range(len(wpmarrs)):
        num = int(wpmarrs[i][:len(wpmarrs[i]) - 1])
        sum += num
        if i >= len(wpmarrs) - 10:
            last10 += num
        best = max(best, num)
    last10 /= min(10, len(wpmarrs))
    sum /= len(wpmarrs)

def ellipse(x, y, w, h, c):
    x = round(x)
    y = round(y)
    w = round(w)
    h = round(h)
    gfxdraw.aaellipse(screen, x, y, w, h, c)
    gfxdraw.filled_ellipse(screen, x, y, w, h, c)
    return

class bubble:
    def __init__(self, x, y, r, d, s, c):
        self.x = x
        self.y = y
        self.r = r
        self.xs = math.cos(math.radians(d)) * s
        self.ys = math.sin(math.radians(d)) * s
        self.c = c
    
    def draw(self):
        ellipse(self.x, self.y, self.r, self.r, self.c)
    def update(self):
        self.x += self.xs
        self.y += self.ys
        if (self.x >= 800 or self.x <= 0):
            self.xs *= -1
            
        if (self.y >= 600 or self.y <= 0):
            self.ys *= -1

    def init(self):
        self.draw()
        self.update()

for i in range(10):
    bubbles.append(bubble(random.randint(0, 800), random.randint(0, 600), random.randint(20, 50), random.randint(0, 360), random.random(), pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
def loading():
    global time
    angle = -time/5 % 360
    rotatedImg = pygame.transform.rotate(loadingImg, angle) 
    imgX = time/5 - loadingImg.get_size()[0]
    imgY = 400 - abs(math.sin(math.radians(time/7))) * 200
    ellipse(imgX + loadingImg.get_size()[0]/2, 500, (imgY - 100)/2, (imgY - 100)/4, pygame.Color(50, 50, 50, 100))
    screen.blit(rotatedImg, rotatedImg.get_rect(center=loadingImg.get_rect(topleft=(imgX, imgY)).center).topleft)

    if time > 3500/2:
        text(400, 300, genFont('data\consola.ttf', 64), 'myType', (0, 0, 0))
        text(550, 300, genFont('data\consola.ttf', 64), ' ' if time % 1000 < 500 else '_', (0, 0, 0))
    if time > 9500/2:
        global transitioning
        transitioning = True
        global nextScene 
        nextScene = 2
    return

def rectColl(x, y, a, b, w, h):
    if (x >= a and y >= b and x <= a + w and y <= b + h):
        return True
    return False

class button:
    def __init__(self, x, y, w, h, f, text, tc, c, hov, sceneLink, pic = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = f
        self.text = text
        self.txtColor = tc
        self.c = c
        self.color = c
        self.hover = hov
        self.link = sceneLink
        self.pic = False if pic == False else pygame.image.load(pic)
        

    def checkPress(self):
        global mX
        global mY   
        global clicked
        global scene
        if (rectColl(mX, mY, self.x, self.y, self.w, self.h)):
            self.color = self.hover
            if (clicked):
                scene = self.link

        else:
            self.color = self.c

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        if self.pic != False:
            screen.blit(self.pic, (self.x + self.w/2 - self.pic.get_size()[0]/2, self.y + self.h/2 - self.pic.get_size()[1]/2))
        text(self.x + self.w/2, self.y + (self.h * 3/4 if self.h >= self.w else self.h/2), self.font, self.text, self.txtColor)

    def init(self):
        self.checkPress()
        self.draw()

class customButton:
    def __init__(self, x, y, w, h, f, text, tc, c, hov):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = f
        self.text = text
        self.txtColor = tc
        self.c = c
        self.color = c
        self.hover = hov

    def checkPress(self):
        global mX
        global mY   
        global clicked
        global scene
        self.color = self.c
        if (rectColl(mX, mY, self.x, self.y, self.w, self.h)):
            self.color = self.hover
            if (clicked):
                return True

        return False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        text(self.x + self.w/2, self.y + (self.h * 3/4 if self.h >= self.w else self.h/2), self.font, self.text, self.txtColor)
        
menubuttons.append(button(150, 200, 350, 100, genFont("data\calibriz.ttf", 50), "Play", (0, 0, 0), (20, 20, 255), (20, 20, 200), 3, "data/typing.png"))
menubuttons.append(button(520, 200, 200, 300, genFont("data\\trebuc.ttf", 40), "Stats", (255, 255, 255), (255, 0, 0), (255, 100, 0), 4, "data/award.png"))
menubuttons.append(button(150, 320, 165, 180, genFont("data\\consola.ttf", 30), "Settings", (0, 0, 0), (0, 255, 255), (50, 255, 255), 5, "data/gear.png"))
menubuttons.append(button(50, 0, 50, 50, genFont("data\\trebuc.ttf", 15), "Info", (0, 0, 0), (255, 255, 255), (200, 200, 200), 6, "data/question.png"))
menubuttons.append(button(335, 320, 165, 180, genFont("data\comic.ttf", 30), "Customize", (255, 255, 255), (0, 255, 0), (50, 225, 50), 7, "data/paint.png"))

def mainmenu():
    global onWord
    global typeString
    global correctLetters
    global totalLetters
    global typeStart
    text(400, 100, genFont("data\\trebucit.ttf", 50), "MyType", (0, 0, 0))
    if typeStart > 0:
        wpmData = open("data\wpms.txt","a") #append mode 
        wpmData.write(str(round(correctLetters/5))+" \n") 
        wpmData.close() 
        typeString = ""
        onWord = 0
        correctLetters = 0
        typeStart = 0
        totalLetters = 0
    return 
def game():
    pygame.draw.rect(screen, pygame.Color(200, 200, 200), (200, 200, 400, 200))
    pygame.draw.rect(screen, pygame.Color(200, 200, 200), (200, 450, 400, 50))

    global onWord
    global typeString
    global correctLetters
    global totalLetters
    global typeStart
    global scene
    
    typeTime = 0 if typeStart == 0 else (pygame.time.get_ticks() - typeStart)/1000
    text(230, 150, genFont("data\\trebuc.ttf", 20), "Accuracy: " + str(round(correctLetters)) + "/" + str(totalLetters), (0, 0, 0))
    text(380, 150, genFont("data\\trebuc.ttf", 20), "WPM: " + str(0 if typeTime < 2 else round(correctLetters * 12/typeTime)), (0, 0, 0))
    text(500, 150, genFont("data\\trebuc.ttf", 20), "Time: " + str(round(typeTime * 10)/10), (0, 0, 0))

    if typeTime >= 60:
        scene = 8

    for i in range(showNum):
        word = wordarr[wordbank[onWord + i]][:len(wordarr[wordbank[onWord + i]]) - 1]
        text(400, 220 + i * 30, genFont("data\calibrib.ttf" if i == 0 else "data\calibri.ttf", fontsArr[fontSize]), word, (0, 0, 0))

    text(400, 480, genFont("data\consola.ttf", 20), typeString, (0, 0, 0))

    return
statsbuttons.append(button(300, 500, 200, 50, genFont("data\\trebuc.ttf", 40), "Back >>", (0, 0, 0), (240, 240, 240), (200, 200, 200), 2))
def stats():
    screen.blit(brainImg, (400 - brainImg.get_size()[0]/2, 100))
    global wpmarrs
    global sum
    global last10
    global best
    wpms = open("data\wpms.txt", 'r')
    wpmarrs = wpms.readlines()
    wpms.close()
    sum = 0
    last10 = 0
    best = 0
    if len(wpmarrs) > 0:
        for i in range(len(wpmarrs)):
            num = int(wpmarrs[i][:len(wpmarrs[i]) - 1])
            sum += num
            if i >= len(wpmarrs) - 10:
                last10 += num
            best = max(best, num)
        last10 /= min(10, len(wpmarrs))
        sum /= len(wpmarrs)
        text(400, 200, genFont("data\consola.ttf", 20), "Total races: " + str(len(wpmarrs)), (0, 0, 0))
        text(400, 250, genFont("data\consola.ttf", 20), "Best WPM: " + str(best), (0, 0, 0))
        text(400, 300, genFont("data\consola.ttf", 20), "Average WPM (Last 10 Races): " + str(round(last10)), (0, 0, 0))
        text(400, 350, genFont("data\consola.ttf", 20), "Average WPM (All time): " + str(round(sum)), (0, 0, 0))
        text(400, 400, genFont("data\consola.ttf", 20), "Last WPM: " + str(wpmarrs[len(wpmarrs) - 1][:len(wpmarrs[len(wpmarrs) - 1]) - 1]), (0, 0, 0))
    else:
        text(400, 300, genFont("data\consola.ttf", 20), "No data yet. Practice to see your stats!", (0, 0, 0))

    return
settingsbuttons.append(customButton(100, 200, 600, 50, genFont("data\\trebuc.ttf", 40), "Use animated background?", (0, 0, 0), (240, 240, 240), (200, 200, 200)))
settingsBack = button(300, 500, 200, 50, genFont("data\\trebuc.ttf", 40), "Back >>", (0, 0, 0), (240, 240, 240), (200, 200, 200), 2)
def settings():
    for i in range(len(settingsbuttons)):
        if settingsbuttons[i].checkPress():
            global useBackground
            useBackground = False if useBackground == True else True
        settingsbuttons[i].draw()
    settingsBack.init()
    return
infobuttons.append(button(300, 500, 200, 50, genFont("data\\trebuc.ttf", 40), "Back >>", (0, 0, 0), (240, 240, 240), (200, 200, 200), 2))
def info():
    screen.blit(aiImg, (100, 300))

    text(400, 100, genFont("data\\trebucbd.ttf", 50), "Welcome to MyType!", (0, 0, 0))
    text(400, 220, genFont("data\\trebuc.ttf", 20), "Here you can train your typing skills in a nice GUI environment", (0, 0, 0))
    text(400, 250, genFont("data\\trebuc.ttf", 20), "You can also take advantage of our machine learning AI", (0, 0, 0))
    text(400, 300, genFont("data\\trebuc.ttf", 20), "It uses your typing data to predict, analyze", (0, 0, 0))
    text(400, 330, genFont("data\\trebuc.ttf", 20), "and help improve your typing speed!", (0, 0, 0))
    text(400, 380, genFont("data\\trebuc.ttf", 20), "You can observe your predicted speeds", (0, 0, 0))
    text(400, 410, genFont("data\\trebuc.ttf", 20), "And get personalized data on what letters you need improvements on!", (0, 0, 0))

    return 

fontSizeButton = customButton(300, 100, 200, 50, genFont("data\\trebuc.ttf", 40), "Font Size: " + str(fontsArr[fontSize]), (0, 0, 0), (240, 240, 240), (200, 200, 200))
showNumButton = customButton(200, 200, 400, 50, genFont("data\\trebuc.ttf", 40), "Words Shown: " + str(showNum), (0, 0, 0), (240, 240, 240), (200, 200, 200))
customizeBack = button(300, 500, 200, 50, genFont("data\\trebuc.ttf", 40), "Back >>", (0, 0, 0), (240, 240, 240), (200, 200, 200), 2)

def customize():
    global fontsArr
    global showNum
    global fontSize
    if fontSizeButton.checkPress():
        fontSize += 1
        if (fontSize > 3):
            fontSize = 0
    fontSizeButton.font = genFont("data\calibri.ttf", fontsArr[fontSize])
    fontSizeButton.text = "Font Size: " + str(fontsArr[fontSize])
    fontSizeButton.draw()
    if showNumButton.checkPress():
        showNum += 1
        if (showNum > 6):
            showNum = 1
    showNumButton.text = "Words Shown: " + str(showNum)
    showNumButton.draw()
    customizeBack.init()
    return 
donebuttons.append(button(300, 500, 200, 50, genFont("data\\trebuc.ttf", 40), "Back >>", (0, 0, 0), (240, 240, 240), (200, 200, 200), 2))
def done():
    global onWord
    global correctLetters
    global totalLetters
    pygame.draw.rect(screen, pygame.Color(200, 200, 200), (100, 150, 600, 300))
    text(400, 100, genFont("data\\trebuc.ttf", 50), "Congrats!", (0, 0, 0))
    text(300, 150, genFont("data\\trebuc.ttf", 20), "Predicted WPM: " + str(max(30, last10 + 5)), (0, 0, 0))
    text(400, 250, genFont("data\\trebuc.ttf", 50), "Accuracy: " + str(0 if totalLetters == 0 else round(correctLetters * 10/totalLetters) * 10) + "%", (0, 0, 0))
    text(400, 350, genFont("data\\trebuc.ttf", 50), "WPM: " + str(round(correctLetters/5)), (255, 0, 0))
    return

def transition():
    global ty
    global scene
    global nextScene
    global transitioning
    global down
    global onWord
    global typeString
    global correctWords
    global typeStart
    if (down):
        ty += 3
    else:
        ty -= 2
    if (ty > 596):
        down = False
        scene = nextScene
    if (ty < 1):
        transitioning = False  
        down = True
        ty = 2
        
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 800, ty))


# Draw loop
running = True
while running:
    # frameCount
    time = (pygame.time.get_ticks() - startTime)
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and transitioning == False and scene == 3:
            if pygame.key.name(event.key) == "return" or pygame.key.name(event.key) == "space":
                if typeString == wordarr[wordbank[onWord]][:len(wordarr[wordbank[onWord]]) - 1]:
                    correctLetters += len(typeString)
                else:
                    for i in range(min(len(typeString), len(wordarr[wordbank[onWord]][:len(wordarr[wordbank[onWord]]) - 1]))):
                        if typeString[i] == wordarr[wordbank[onWord]][:len(wordarr[wordbank[onWord]]) - 1][i]:
                            correctLetters += 0.5
                totalLetters += len(typeString)
                onWord += 1
                typeString = ""
                if onWord == 1:
                    typeStart = pygame.time.get_ticks()
            elif pygame.key.name(event.key) == "backspace" and len(typeString) > 0:
                typeString = typeString[:len(typeString) - 1]
            else:
                al = "abcdefghijklmnopqrstuvwxyz"
                for i in range(len(al)):
                    if pygame.key.name(event.key) == al[i]:
                        typeString += al[i]
                        break

    if (pastPress and pygame.mouse.get_pressed()[0] == False and transitioning == False):
        clicked = True
    pastPress = pygame.mouse.get_pressed()[0]   
    # Check if was pressing in the last frame but not in this frame which implies a click
    mX, mY = pygame.mouse.get_pos()

    # 1 - load, 2 - menu, 3 - practice, 4 - stats, 5 - settings, 6 - info, 7 - customize
    # if only python had switch T.T
    if scene == 1:
        loading()
    elif useBackground:
        for i in range(len(bubbles)):
            bubbles[i].init()

    if scene == 2:
        mainmenu()
        for i in range(len(menubuttons)):
            menubuttons[i].init()
    if scene == 3:
        game()
    if scene == 4:
        stats()
        for i in range(len(statsbuttons)):
            statsbuttons[i].init()
    if scene == 5:
        settings()
    if scene == 6:
        info()
        for i in range(len(infobuttons)):
            infobuttons[i].init()
    if scene == 7:
        customize()
    if scene == 8:
        done()
        for i in range(len(donebuttons)):
            donebuttons[i].init()

    if transitioning:
        transition()

    pygame.display.update()

    clicked = False
