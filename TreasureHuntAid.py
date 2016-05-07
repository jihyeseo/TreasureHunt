#
# In development by Jihye Sofia Seo https://www.linkedin.com/in/jihyeseo
# forked from the code of another game Slide Puzzle by Al Sweigart  
# http://inventwithpython.com/pygame/chapter4.html 
# whose books are very helpful for learning Python and PyGame. Many thanks!
#
# The final goal is an autoplay with computer vision, 
# so that one can earn more scores in a mobile game "Tiny Farm - Safari Game"  
# http://tinyfarm.wikia.com/wiki/Tiny_Zoo
#
# Any comments are welcome at jihyeseo@post.harvard.edu 
# upload: May 7 2016 Berlin Germany
#

import pygame, sys, random, math
from pygame.locals import *
 
BOARDWIDTH = 6  # number of columns in the board
BOARDHEIGHT = 6 # number of rows in the board
numOfTreasure = 15
TILESIZE = 80
WINDOWWIDTH = 1000
WINDOWHEIGHT = 550
FPS = 30
waitingTime = 100
ABCs = 26
BLANK = None

def numToLabel(nat):
    string = ""  
    string += numToDigit(nat) 
    next = int(nat / ABCs)
    if next != 0:
        string += numToDigit(next)
        nnext = int(next / ABCs)
        if nnext != 0:
            string += numToDigit(nnext) 
    return string 
     
def numToDigit(nat):  
    return chr(nat % ABCs + ord('A'))

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
 
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - 450 - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

openAt =  [[False for x in range(BOARDWIDTH)] for x in range(BOARDWIDTH)]
treasureAt =  [[False for x in range(BOARDWIDTH)] for x in range(BOARDWIDTH)]
infoAt =  [[0 for x in range(BOARDWIDTH)] for x in range(BOARDWIDTH)] 
groupID =  [[0 for x in range(BOARDWIDTH)] for x in range(BOARDWIDTH)]
                         
                        
def reGroup(tilex,tiley):  
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT): 
            groupID[x][y] *= 2
    for nbLoc in neighbors(tilex,tiley):
        groupID[nbLoc[0]][nbLoc[1]] += 1 

def makeText(text, color, bgcolor, top, left, chosenFONT):
    # create the Surface and Rect objects for some text.
    textSurf = chosenFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)
    
def plantTreasureAt(tryX,tryY):
    if treasureAt[tryX][tryY] == False:        
        treasureAt[tryX][tryY] = True 
        for nbLoc in neighbors(tryX,tryY) :
            infoAt[nbLoc[0]][nbLoc[1]] += 1 
        return True
    else:
        return False       
 
def neighbors(locX,locY):
    neighborList = []
    for incX in range(-1,2):
        for incY in range(-1,2) :    
            newX = incX + locX
            newY = incY + locY 
            if (not((incX == 0) and (incY == 0 ))) and (newX in range(BOARDWIDTH)) and (newY in range(BOARDHEIGHT)):
                neighborList.append([newX, newY])
    return neighborList      

def plantAllTreasures():
    print("\n \t When you click on a tile, it will say Schatz if it is a treasure. \n \t Otherwise, it will show how many treasures are hidden in (up to 8) neighboring tiles. \n \t The computer is helping your play by showing probability. \n \t The autoplay mode is in development phase, any comment is welcome at jihyeseo@post.harvard.edu" ) 
    currentTreasure =  0 
    while(True):
        (x,y) = (random.randint(0,BOARDWIDTH-1),random.randint(0,BOARDHEIGHT-1))
        if plantTreasureAt(x,y): currentTreasure += 1
        if currentTreasure == numOfTreasure: break 
            
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BigFONT, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    global currentTreasure
    currentTreasure    = 0 # what is this variable for?
   
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Treasure Hunt (computer assisted play, in development)')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    BigFONT = pygame.font.Font('freesansbold.ttf', 2*BASICFONTSIZE)
  
    plantAllTreasures()
    pygame.display.update() 
    
    while True: # main game loop    
        drawBoard()
        pygame.display.update()
        pygame.time.wait(waitingTime)
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
         
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(event.pos[0], event.pos[1])
                if (spotx != None) and (spoty != None) and (openAt[spotx][spoty] ==False):
                    openAt[spotx][spoty] = True 
                    if (treasureAt[spotx][spoty] == False):
                        reGroup(spotx,spoty)

        
        drawBoard()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

COLORSCHEMES = [(150, 200, 255),   
                (97, 215, 164)  ,  #lightGr 
                (0, 125, 50) ,#darkGr
                (23, 149, 195) , # light ocean
                (81, 85 , 141), # lightPur
                (147, 3, 167) , # purple
                (241, 109, 149), # jindalle 
                (255, 180, 115), # tangerine
                (166, 147, 0)  # tangerine?   
                ]
       
def getSpotClicked(x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(BOARDWIDTH):
        for tileY in range(BOARDHEIGHT):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None) 
    
def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
     
     
def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)
  
def drawTile(tilex, tiley, info, tileCOLOR, textCOLOR, chosenFONT, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, tileCOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = chosenFONT.render(str(info), True, textCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)
 
def drawBoard():
    foundTreasure = 0
    fieldSize = 0 
  #  sumNumbers = 0
    DISPLAYSURF.fill(BGCOLOR)  
        
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT): 
            if openAt[tilex][tiley] == True :
                if treasureAt[tilex][tiley] == False:
                    drawTile(tilex, tiley, infoAt[tilex][tiley], WHITE, BLACK,BigFONT)
   #                 sumNumbers += infoAt[tilex][tiley]
                else  : 
                    drawTile(tilex, tiley, "Schatz", WHITE, BLACK,BASICFONT)
                    foundTreasure += 1 
                        
            else :
                drawTile(tilex, tiley, numToLabel(groupID[tilex][tiley]), COLORSCHEMES[groupID[tilex][tiley] % len(COLORSCHEMES)], WHITE,BASICFONT)
                if groupID[tilex][tiley] == 0 :
                    fieldSize += 1

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
              
    height = 5 
    formulas = []
    formulas.append("Total treasure: "+str(numOfTreasure))
        
    fieldHiddenTreasure = 0 
    
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT): 
            if (openAt[tilex][tiley] == True) & (treasureAt[tilex][tiley] == False):
                RHS = infoAt[tilex][tiley]
                LHS = []
                for nbLoc in neighbors(tilex,tiley) :
                    if (openAt[nbLoc[0]][nbLoc[1]]) & (treasureAt[nbLoc[0]][nbLoc[1]]):
                        RHS -= 1
                    elif (openAt[nbLoc[0]][nbLoc[1]] == False) :
                        LHS.append(numToLabel(groupID[nbLoc[0]][nbLoc[1]]))
                #
                if len(LHS) > 0:
                    if homElem(LHS):
                        formulas.append(LHS[0]+" has probability "+str(RHS/len(LHS)))
                    else : 
                        formulas.append(str(LHS)+str(RHS))                 
                    fieldHiddenTreasure += RHS 
 #   formulas.append("Hidden in field ("+str(fieldSize)+ " A\'s):" +str(numOfTreasure - foundTreasure - fieldHiddenTreasure))
    if fieldSize != 0:
        formulas.append("A has probability: "+str((numOfTreasure - foundTreasure - fieldHiddenTreasure)/(fieldSize)))
#    formulas.append("Hidden treasure: "+str((numOfTreasure - foundTreasure)))
                    
    for form in formulas:        
        textSurf, textRect = makeText(form, MESSAGECOLOR, BGCOLOR, 550, height, BASICFONT)
        height += 50 
        DISPLAYSURF.blit(textSurf, textRect)

def homElem(list) :
    first = list[0]
    for i in range(1,len(list)):
        if list[i] != first:
            return False
    else:
        return True
            
    
        
if __name__ == '__main__':
    main()