import platform
import pygame, sys
from pygame.locals import *
import os
from sys import exit
from random import *
import random
import time

# I using the UTF-8 symbols to build the board
board = ["╔═╤═╤═╤═╤═╤═╤═╤═╗",
         "║  │  │  │╲│╱│  │  │  ║",
         "╟─┼─┼─┼─┼─┼─┼─┼─╢",
         "║  │  │  │╱│╲│  │  │  ║",
         "╟─╬─┼─┼─┼─┼─┼─╬─╢",
         "║  │  │  │  │  │  │  │  ║",
         "╠─┼─╬─┼─╬─┼─╬─┼─╣",
         "║  │  │  │  │  │  │  │  ║",
         "╟─┴─┴─┴─┴─┴─┴─┴─╢",
         "║    楚    河      漢    界    ║",
         "╟─┬─┬─┬─┬─┬─┬─┬─╢",
         "║  │  │  │  │  │  │  │  ║",
         "╠─┼─╬─┼─╬─┼─╬─┼─╣",
         "║  │  │  │  │  │  │  │  ║",
         "╟─╬─┼─┼─┼─┼─┼─╬─╢",
         "║  │  │  │╲│╱│  │  │  ║",
         "╟─┼─┼─┼─┼─┼─┼─┼─╢",
         "║  │  │  │╱│╲│  │  │  ║",
         "╚═╧═╧═╧═╧═╧═╧═╧═╝",]

# using list to store the pieces
# define : NAME,COORDINATE,COLOR
piecesBlack=[['將',(4,0),(0,0,0)],['士',(3,0),(0,0,0)],['士',(5,0),(0,0,0)],
        ['象',(2,0),(0,0,0)],['象',(6,0),(0,0,0)],
        ['馬',(1,0),(0,0,0)],['馬',(7,0),(0,0,0)],
        ['車',(0,0),(0,0,0)],['車',(8,0),(0,0,0)],
        ['砲',(1,2),(0,0,0)],['砲',(7,2),(0,0,0)],
        ['卒',(0,3),(0,0,0)],['卒',(2,3),(0,0,0)],['卒',(4,3),(0,0,0)],['卒',(6,3),(0,0,0)],['卒',(8,3),(0,0,0)],]
piecesRed=[['帥',(4,9),(255,0,0)],['仕',(3,9),(255,0,0)],['仕',(5,9),(255,0,0)],
        ['相',(2,9),(255,0,0)],['相',(6,9),(255,0,0)],
        ['傌',(1,9),(255,0,0)],['傌',(7,9),(255,0,0)],
        ['俥',(0,9),(255,0,0)],['俥',(8,9),(255,0,0)],
        ['炮',(1,7),(255,0,0)],['炮',(7,7),(255,0,0)],
        ['兵',(0,6),(255,0,0)],['兵',(2,6),(255,0,0)],['兵',(4,6),(255,0,0)],['兵',(6,6),(255,0,0)],['兵',(8,6),(255,0,0)],]

#BLACK = ( 0, 0, 0)
#WHITE = (255, 255, 255)
#GREEN = (0, 255, 0)
#RED = ( 255, 0, 0)

# pygame for UI. keyboard and screen
pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)

DISPLAYSURF = pygame.display.set_mode((800, 600))
pygame.display.set_caption('奕棋子')

print (platform.system())

# different font in different platform
# the font must be monospaced and symbols included
fontSize=28
#myfont = pygame.font.Font(os.environ['SYSTEMROOT'] + "\\Fonts\\KAIU.TTF", fontSize)
if platform.system() == 'Linux':
    myfont = pygame.font.SysFont("MingLiu", fontSize)
if platform.system() == 'Windows':
    myfont = pygame.font.Font(os.environ['SYSTEMROOT'] + "\\Fonts\\mingliu.ttc", fontSize)
if platform.system() == 'Darwin':
    myfont = pygame.font.SysFont("MingLiu", fontSize)

'''
textsurface = myfont.render('0', True, (255,0,0))
screen.blit(textsurface,(0,0))
textsurface = myfont.render('28', True, (255,0,0))
screen.blit(textsurface,(28,0))
textsurface = myfont.render('56', True, (255,0,0))
screen.blit(textsurface,(56,0))
textsurface = myfont.render('84', True, (255,0,0))
screen.blit(textsurface,(84,0))
textsurface = myfont.render('112', True, (255,0,0))
screen.blit(textsurface,(112,0))
'''

# function for draw the board
def plotBoard():
    pygame.draw.circle(screen,(255,225,128),(600+fontSize,fontSize),22,0)
    pygame.draw.circle(screen,(0,0,0),(600+fontSize,fontSize),20,1)
    pygame.draw.circle(screen,(255,225,128),(600+int(fontSize*2.5),fontSize),22,0)
    pygame.draw.circle(screen,(0,0,0),(600+int(fontSize*2.5),fontSize),20,1)
    pygame.draw.circle(screen,(255,225,128),(600+fontSize*4,fontSize),22,0)
    pygame.draw.circle(screen,(0,0,0),(600+fontSize*4,fontSize),20,1)
    textsurface = myfont.render('奕 棋 子', True, (0,0,0))
    screen.blit(textsurface,(600+fontSize-fontSize/2,fontSize-fontSize/2))
    for line in range(0,19):
        textsurface = myfont.render(board[line], True, (255,255,255))
        screen.blit(textsurface,(fontSize,fontSize+(line*fontSize)))

    for piece in piecesBlack:
        newX = int(piece[1][0] * fontSize * 2 + fontSize + fontSize/2  ) 
        newY = int(piece[1][1] * fontSize * 2 + fontSize + fontSize/2 )
        pygame.draw.circle(screen,(255,225,128),(newX,newY),int(fontSize*.9),0)
        pygame.draw.circle(screen,(0,0,0),(newX,newY),int(fontSize*.8),1)
        textsurface = myfont.render(piece[0], True, piece[2])
        screen.blit(textsurface,(newX-fontSize/2,newY-fontSize/2))
        #print(piece[0],newX,newY)
    for piece in piecesRed:
        newX = int(piece[1][0] * fontSize * 2 + fontSize + fontSize/2  ) 
        newY = int(piece[1][1] * fontSize * 2 + fontSize + fontSize/2 )
        pygame.draw.circle(screen,(255,225,128),(newX,newY),int(fontSize*.9),0)
        pygame.draw.circle(screen,(0,0,0),(newX,newY),int(fontSize*.8),1)
        textsurface = myfont.render(piece[0], True, piece[2])
        screen.blit(textsurface,(newX-fontSize/2,newY-fontSize/2))

#pygame.display.update()

# funciton for draw the cursor
def plotCursor(x,y):
    textsurface = myfont.render('┌', True, (255,0,0))
    screen.blit(textsurface,(int(x * fontSize * 2   ) ,int(y * fontSize * 2  )))
    textsurface = myfont.render('└', True, (255,0,0))
    screen.blit(textsurface,(int(x * fontSize * 2   ) ,int(y * fontSize * 2 + fontSize + fontSize )))
    textsurface = myfont.render('┘', True, (255,0,0))
    screen.blit(textsurface,(int(x * fontSize * 2 + fontSize + fontSize  ) ,int(y * fontSize * 2 + fontSize + fontSize )))
    textsurface = myfont.render('┐', True, (255,0,0))
    screen.blit(textsurface,(int(x * fontSize * 2 + fontSize + fontSize  ) ,int(y * fontSize * 2  )))

# funciton for draw the candidate path mark
def plotCandidate(x,y):
    textsurface = myfont.render('┌', True, (0,255,0))
    screen.blit(textsurface,(int(x * fontSize * 2   ) ,int(y * fontSize * 2  )))
    textsurface = myfont.render('└', True, (0,255,0))
    screen.blit(textsurface,(int(x * fontSize * 2   ) ,int(y * fontSize * 2 + fontSize + fontSize )))
    textsurface = myfont.render('┘', True, (0,255,0))
    screen.blit(textsurface,(int(x * fontSize * 2 + fontSize + fontSize  ) ,int(y * fontSize * 2 + fontSize + fontSize )))
    textsurface = myfont.render('┐', True, (0,255,0))
    screen.blit(textsurface,(int(x * fontSize * 2 + fontSize + fontSize  ) ,int(y * fontSize * 2  )))

# funciton for draw the attack position mark  
def plotAttack(x,y):
    textsurface = myfont.render('┌', True, (255,255,0))
    screen.blit(textsurface,(int(x * fontSize * 2   ) ,int(y * fontSize * 2  )))
    textsurface = myfont.render('└', True, (255,255,0))
    screen.blit(textsurface,(int(x * fontSize * 2   ) ,int(y * fontSize * 2 + fontSize + fontSize )))
    textsurface = myfont.render('┘', True, (255,255,0))
    screen.blit(textsurface,(int(x * fontSize * 2 + fontSize + fontSize  ) ,int(y * fontSize * 2 + fontSize + fontSize )))
    textsurface = myfont.render('┐', True, (255,255,0))
    screen.blit(textsurface,(int(x * fontSize * 2 + fontSize + fontSize  ) ,int(y * fontSize * 2  )))

plotBoard()
plotCursor(0,0)
#print(piecesBlack,piecesRed)

# funciton for compare the given postion and piece in the list
# input : postion to collection detect
# for black side
def collectionDetectBlack(x,y):
    for piece in piecesBlack:
        #print(piece[1],(x,y))
        if piece[1] == (x,y):
            return (x,y)
    return False

# for red side
def collectionDetectRed(x,y):
    for piece in piecesRed:
        #print(piece[1],(x,y))
        if piece[1] == (x,y):
            return (x,y)
    return False

# for all pieces
def collectionDetect(x,y):
    for piece in piecesBlack:
        #print(piece[1],(x,y))
        if piece[1] == (x,y):
            return (x,y)
    for piece in piecesRed:
        #print(piece[1],(x,y))
        if piece[1] == (x,y):
            return (x,y)
    return False

# find all possibility of piece move
# return : all cordinate of possibility
def findRoads(piece):
    candidateArray = []
    pieceX = piece[1][0]
    pieceY = piece[1][1]
    ####################
    if piece[0] == '將':
        if pieceY-1 >=0:
            if not collectionDetect(pieceX,pieceY-1):
                #plotCandidate(pieceX,pieceY-1)
                candidateArray.append([pieceX,pieceY-1])
        if pieceY+1 <=2:
            if not collectionDetect(pieceX,pieceY+1):
                #plotCandidate(pieceX,pieceY+1)
                candidateArray.append([pieceX,pieceY+1])
        if pieceX-1 >=3:
            if not collectionDetect(pieceX-1,pieceY):
                #plotCandidate(pieceX+1,pieceY)
                candidateArray.append([pieceX-1,pieceY])
        if pieceX+1 <=5:
            if not collectionDetect(pieceX+1,pieceY):
                #plotCandidate(pieceX+1,pieceY)
                candidateArray.append([pieceX+1,pieceY])
    if piece[0] == '帥':
        if pieceY-1 >=7:
            if not collectionDetect(pieceX,pieceY-1):
                #plotCandidate(pieceX,pieceY-1)
                candidateArray.append([pieceX,pieceY-1])
        if pieceY+1 <=9:
            if not collectionDetect(pieceX,pieceY+1):
                #plotCandidate(pieceX,pieceY+1)
                candidateArray.append([pieceX,pieceY+1])
        if pieceX-1 >=3:
            if not collectionDetect(pieceX-1,pieceY):
                #plotCandidate(pieceX-1,pieceY)
                candidateArray.append([pieceX-1,pieceY])
        if pieceX+1 <=5:
            if not collectionDetect(pieceX+1,pieceY):
                #plotCandidate(pieceX+1,pieceY)
                candidateArray.append([pieceX+1,pieceY])
    ####################
    if piece[0] == '士':
        if pieceX-1 >=3 and pieceY-1 >=0:
            if not collectionDetect(pieceX-1,pieceY-1):
                #plotCandidate(pieceX-1,pieceY-1)
                candidateArray.append([pieceX-1,pieceY-1])
        if pieceX-1 >=3 and pieceY+1 <=2:
            if not collectionDetect(pieceX-1,pieceY+1):
                #plotCandidate(pieceX-1,pieceY+1)
                candidateArray.append([pieceX-1,pieceY+1])
        if pieceX+1 <=5 and pieceY-1 >=0:
            if not collectionDetect(pieceX+1,pieceY-1):
                #plotCandidate(pieceX+1,pieceY-1)
                candidateArray.append([pieceX+1,pieceY-1])
        if pieceX+1 <=5 and pieceY+1 <=2:
            if not collectionDetect(pieceX+1,pieceY+1):
                #plotCandidate(pieceX+1,pieceY+1)
                candidateArray.append([pieceX+1,pieceY+1])
    if piece[0] == '仕':
        if pieceX-1 >=3 and pieceY-1 >=7:
            if not collectionDetect(pieceX-1,pieceY-1):
                #plotCandidate(pieceX-1,pieceY-1)
                candidateArray.append([pieceX-1,pieceY-1])
        if pieceX-1 >=3 and pieceY+1 <=9:
            if not collectionDetect(pieceX-1,pieceY+1):
                #plotCandidate(pieceX-1,pieceY+1)
                candidateArray.append([pieceX-1,pieceY+1])
        if pieceX+1 <=5 and pieceY-1 >=7:
            if not collectionDetect(pieceX+1,pieceY-1):
                #plotCandidate(pieceX+1,pieceY-1)
                candidateArray.append([pieceX+1,pieceY-1])
        if pieceX+1 <=5 and pieceY+1 <=9:
            if not collectionDetect(pieceX+1,pieceY+1):
                #plotCandidate(pieceX+1,pieceY+1)
                candidateArray.append([pieceX+1,pieceY+1])
    ####################
    if piece[0] == '象':
        if pieceX-2 >=0 and pieceY-2 >=0 and not collectionDetect(pieceX-1,pieceY-1):
            if not collectionDetect(pieceX-2,pieceY-2):
                #plotCandidate(pieceX-2,pieceY-2)
                candidateArray.append([pieceX-2,pieceY-2])
        if pieceX-2 >=0 and pieceY+2 <= 4 and not collectionDetect(pieceX-1,pieceY+1):
            if not collectionDetect(pieceX-2,pieceY+2):
                #plotCandidate(pieceX-2,pieceY+2)
                candidateArray.append([pieceX-2,pieceY+2])
        if pieceX+2 <=8 and pieceY-2 >=0 and not collectionDetect(pieceX+1,pieceY-1):
            if not collectionDetect(pieceX+2,pieceY-2):
                #plotCandidate(pieceX+2,pieceY-2)
                candidateArray.append([pieceX+2,pieceY-2])
        if pieceX+2 <=8 and pieceY+2 <= 4 and not collectionDetect(pieceX+1,pieceY+1):
            if not collectionDetect(pieceX+2,pieceY+2):
                #plotCandidate(pieceX+2,pieceY+2)
                candidateArray.append([pieceX+2,pieceY+2])
    if piece[0] == '相':
        if pieceX-2 >=0 and pieceY-2 >=5 and not collectionDetect(pieceX-1,pieceY-1):
            if not collectionDetect(pieceX-2,pieceY-2):
                #plotCandidate(pieceX-2,pieceY-2)
                candidateArray.append([pieceX-2,pieceY-2])
        if pieceX-2 >=0 and pieceY+2 <= 9 and not collectionDetect(pieceX-1,pieceY+1):
            if not collectionDetect(pieceX-2,pieceY+2):
                #plotCandidate(pieceX-2,pieceY+2)
                candidateArray.append([pieceX-2,pieceY+2])
        if pieceX+2 <=8 and pieceY-2 >=5 and not collectionDetect(pieceX+1,pieceY-1):
            if not collectionDetect(pieceX+2,pieceY-2):
                #plotCandidate(pieceX+2,pieceY-2)
                candidateArray.append([pieceX+2,pieceY-2])
        if pieceX+2 <=8 and pieceY+2 <= 9 and not collectionDetect(pieceX+1,pieceY+1):
            if not collectionDetect(pieceX+2,pieceY+2):
                #plotCandidate(pieceX+2,pieceY+2)
                candidateArray.append([pieceX+2,pieceY+2])
    ####################
    if piece[0] == '卒':
        if pieceY <= 4:
            if not collectionDetect(pieceX,pieceY+1):
                #plotCandidate(pieceX,pieceY+1)
                candidateArray.append([pieceX,pieceY+1])
        else:
            if pieceY+1 <= 9 and not collectionDetect(pieceX,pieceY+1):
                #plotCandidate(pieceX,pieceY+1)
                candidateArray.append([pieceX,pieceY+1])
            if pieceX-1 >=0 and not collectionDetect(pieceX-1,pieceY):
                #plotCandidate(pieceX-1,pieceY)
                candidateArray.append([pieceX-1,pieceY])
            if pieceX+1 <=8 and not collectionDetect(pieceX+1,pieceY):
                #plotCandidate(pieceX+1,pieceY)
                candidateArray.append([pieceX+1,pieceY])
    if piece[0] == '兵':
        if pieceY >=5:
            if not collectionDetect(pieceX,pieceY-1):
                #plotCandidate(pieceX,pieceY-1)
                candidateArray.append([pieceX,pieceY-1])
        else:
            if pieceY-1 >0 and not collectionDetect(pieceX,pieceY-1):
                #plotCandidate(pieceX,pieceY-1)
                candidateArray.append([pieceX,pieceY-1])
            if pieceX-1 >=0 and not collectionDetect(pieceX-1,pieceY):
                #plotCandidate(pieceX-1,pieceY)
                candidateArray.append([pieceX-1,pieceY])
            if pieceX+1 <=8 and not collectionDetect(pieceX+1,pieceY):
                #plotCandidate(pieceX+1,pieceY)
                candidateArray.append([pieceX+1,pieceY])
    #########################################
    if piece[0] == '馬' or piece[0] == '傌' :
        #
        if pieceY-2 >= 0 and pieceX-1 >= 0 and not collectionDetect(pieceX,pieceY-1):
            if not collectionDetect(pieceX-1,pieceY-2):
                #plotCandidate(pieceX-1,pieceY-2)
                candidateArray.append([pieceX-1,pieceY-2])
        if pieceY-2 >= 0 and pieceX+1 < 9 and not collectionDetect(pieceX,pieceY-1):
            if not collectionDetect(pieceX+1,pieceY-2):
                #plotCandidate(pieceX+1,pieceY-2)
                candidateArray.append([pieceX+1,pieceY-2])
        #
        if pieceY+2 < 10 and pieceX-1 >= 0 and not collectionDetect(pieceX,pieceY+1):
            if not collectionDetect(pieceX-1,pieceY+2):
                #plotCandidate(pieceX-1,pieceY+2)
                candidateArray.append([pieceX-1,pieceY+2])
        if pieceY+2 < 10 and pieceX+1 < 9 and not collectionDetect(pieceX,pieceY+1):
            if not collectionDetect(pieceX+1,pieceY+2):
                #plotCandidate(pieceX+1,pieceY+2)
                candidateArray.append([pieceX+1,pieceY+2])
        #
        if pieceX-2 >= 0 and pieceY-1 >= 0 and not collectionDetect(pieceX-1,pieceY):
            if not collectionDetect(pieceX-2,pieceY-1):
                #plotCandidate(pieceX-2,pieceY-1)
                candidateArray.append([pieceX-2,pieceY-1])
        if pieceX-2 >= 0 and pieceY+1 < 10 and not collectionDetect(pieceX-1,pieceY):
            if not collectionDetect(pieceX-2,pieceY+1):
                #plotCandidate(pieceX-2,pieceY+1)
                candidateArray.append([pieceX-2,pieceY+1])
        #
        if pieceX+2 < 9 and pieceY-1 >= 0 and not collectionDetect(pieceX+1,pieceY):
            if not collectionDetect(pieceX+2,pieceY-1):
                #plotCandidate(pieceX+2,pieceY-1)
                candidateArray.append([pieceX+2,pieceY-1])
        if pieceX+2 < 9 and pieceY+1 < 10 and not collectionDetect(pieceX+1,pieceY):
            if not collectionDetect(pieceX+2,pieceY+1):
                #plotCandidate(pieceX+2,pieceY+1)
                candidateArray.append([pieceX+2,pieceY+1])
    #########################################
    if piece[0] == '車' or piece[0] == '俥' :
        #print (piece[1])
        # up direction
        for scanY in range(pieceY-1,-1,-1):
            #print ("▲",scanY)
            if collectionDetect(pieceX,scanY) != False:
                #print("hit")
                break
            #plotCandidate(pieceX,scanY)
            candidateArray.append([pieceX,scanY])
        # down direction
        for scanY in range(pieceY+1,10,1):
            #print ("▼",scanY)
            if collectionDetect(pieceX,scanY) != False:
                #print("hit")
                break
            #plotCandidate(pieceX,scanY)
            candidateArray.append([pieceX,scanY])
        # left direction
        for scanX in range(pieceX-1,-1,-1):
            #print(collectionDetect(scanX,piece[1][1]))
            #print ("◀",scanX,piece[1][1])
            if collectionDetect(scanX,pieceY) != False:
                #print("hit")
                break
            #plotCandidate(scanX,pieceY)
            candidateArray.append([scanX,pieceY])
        # right direction
        for scanX in range(pieceX+1,9,1):
            #print ("▶",scanX)
            if collectionDetect(scanX,pieceY) != False:
                #print("hit")
                break
            #plotCandidate(scanX,pieceY)
            candidateArray.append([scanX,pieceY])
    #########################################
    if piece[0] == '砲' or piece[0] == '炮' :
        #print (piece[1])
        # up direction
        for scanY in range(pieceY-1,-1,-1):
            #print ("▲",scanY)
            if collectionDetect(pieceX,scanY) != False:
                #print("hit")
                break
            #plotCandidate(pieceX,scanY)
            candidateArray.append([pieceX,scanY])
        # down direction
        for scanY in range(pieceY+1,10,1):
            #print ("▼",scanY)
            if collectionDetect(pieceX,scanY) != False:
                #print("hit")
                break
            #plotCandidate(pieceX,scanY)
            candidateArray.append([pieceX,scanY])
        # left direction
        for scanX in range(pieceX-1,-1,-1):
            #print(collectionDetect(scanX,piece[1][1]))
            #print ("◀",scanX,piece[1][1])
            if collectionDetect(scanX,pieceY) != False:
                #print("hit")
                break
            #plotCandidate(scanX,pieceY)
            candidateArray.append([scanX,pieceY])
        # right direction
        for scanX in range(pieceX+1,9,1):
            #print ("▶",scanX)
            if collectionDetect(scanX,pieceY) != False:
                #print("hit")
                break
            #plotCandidate(scanX,pieceY)
            candidateArray.append([scanX,pieceY])
    return candidateArray

# find all possibility for piece attack
# return : all cordinate of possibility
def findAttacks(piece):
    candidateArray = []
    pieceX = piece[1][0]
    pieceY = piece[1][1]
    ####################
    if piece[0] == '將':
        if pieceY-1 >=0:
            enemySideHit = collectionDetectRed(pieceX,pieceY-1)
            mySideHit = collectionDetectBlack(pieceX,pieceY-1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX,pieceY-1)
                candidateArray.append([pieceX,pieceY-1])
        if pieceY+1 <=2:
            enemySideHit = collectionDetectRed(pieceX,pieceY+1)
            mySideHit = collectionDetectBlack(pieceX,pieceY+1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX,pieceY+1)
                candidateArray.append([pieceX,pieceY+1])
        if pieceX-1 >=3:
            enemySideHit = collectionDetectRed(pieceX-1,pieceY)
            mySideHit = collectionDetectBlack(pieceX-1,pieceY)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+1,pieceY)
                candidateArray.append([pieceX-1,pieceY])
        if pieceX+1 <=5:
            enemySideHit = collectionDetectRed(pieceX+1,pieceY)
            mySideHit = collectionDetectBlack(pieceX+1,pieceY)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+1,pieceY)
                candidateArray.append([pieceX+1,pieceY])
    if piece[0] == '帥':
        if pieceY-1 >=7:
            enemySideHit = collectionDetectBlack(pieceX,pieceY-1)
            mySideHit = collectionDetectRed(pieceX,pieceY-1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX,pieceY-1)
                candidateArray.append([pieceX,pieceY-1])
        if pieceY+1 <=9:
            enemySideHit = collectionDetectBlack(pieceX,pieceY+1)
            mySideHit = collectionDetectRed(pieceX,pieceY+1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX,pieceY+1)
                candidateArray.append([pieceX,pieceY+1])
        if pieceX-1 >=3:
            enemySideHit = collectionDetectBlack(pieceX-1,pieceY)
            mySideHit = collectionDetectRed(pieceX-1,pieceY)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-1,pieceY)
                candidateArray.append([pieceX-1,pieceY])
        if pieceX+1 <=5:
            enemySideHit = collectionDetectBlack(pieceX+1,pieceY)
            mySideHit = collectionDetectRed(pieceX+1,pieceY)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+1,pieceY)
                candidateArray.append([pieceX+1,pieceY])
    ####################
    if piece[0] == '士':
        if pieceX-1 >=3 and pieceY-1 >=0:
            enemySideHit = collectionDetectRed(pieceX-1,pieceY-1)
            mySideHit = collectionDetectBlack(pieceX-1,pieceY-1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-1,pieceY-1)
                candidateArray.append([pieceX-1,pieceY-1])
        if pieceX-1 >=3 and pieceY+1 <=2:
            enemySideHit = collectionDetectRed(pieceX-1,pieceY+1)
            mySideHit = collectionDetectBlack(pieceX-1,pieceY+1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-1,pieceY+1)
                candidateArray.append([pieceX-1,pieceY+1])
        if pieceX+1 <=5 and pieceY-1 >=0:
            enemySideHit = collectionDetectRed(pieceX+1,pieceY-1)
            mySideHit = collectionDetectBlack(pieceX+1,pieceY-1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+1,pieceY-1)
                candidateArray.append([pieceX+1,pieceY-1])
        if pieceX+1 <=5 and pieceY+1 <=2:
            enemySideHit = collectionDetectRed(pieceX+1,pieceY+1)
            mySideHit = collectionDetectBlack(pieceX+1,pieceY+1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+1,pieceY+1)
                candidateArray.append([pieceX+1,pieceY+1])
    if piece[0] == '仕':
        if pieceX-1 >=3 and pieceY-1 >=7:
            enemySideHit = collectionDetectBlack(pieceX-1,pieceY-1)
            mySideHit = collectionDetectRed(pieceX-1,pieceY-1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-1,pieceY-1)
                candidateArray.append([pieceX-1,pieceY-1])
        if pieceX-1 >=3 and pieceY+1 <=9:
            enemySideHit = collectionDetectBlack(pieceX-1,pieceY+1)
            mySideHit = collectionDetectRed(pieceX-1,pieceY+1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-1,pieceY+1)
                candidateArray.append([pieceX-1,pieceY+1])
        if pieceX+1 <=5 and pieceY-1 >=7:
            enemySideHit = collectionDetectBlack(pieceX+1,pieceY-1)
            mySideHit = collectionDetectRed(pieceX+1,pieceY-1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+1,pieceY-1)
                candidateArray.append([pieceX+1,pieceY-1])
        if pieceX+1 <=5 and pieceY+1 <=9:
            enemySideHit = collectionDetectBlack(pieceX+1,pieceY+1)
            mySideHit = collectionDetectRed(pieceX+1,pieceY+1)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+1,pieceY+1)
                candidateArray.append([pieceX+1,pieceY+1])
    ####################
    if piece[0] == '象':
        if pieceX-2 >=0 and pieceY-2 >=0 and not collectionDetect(pieceX-1,pieceY-1):
            enemySideHit = collectionDetectRed(pieceX-2,pieceY-2)
            mySideHit = collectionDetectBlack(pieceX-2,pieceY-2)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-2,pieceY-2)
                candidateArray.append([pieceX-2,pieceY-2])
        if pieceX-2 >=0 and pieceY+2 <= 4 and not collectionDetect(pieceX-1,pieceY+1):
            enemySideHit = collectionDetectRed(pieceX-2,pieceY+2)
            mySideHit = collectionDetectBlack(pieceX-2,pieceY+2)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-2,pieceY+2)
                candidateArray.append([pieceX-2,pieceY+2])
        if pieceX+2 <=8 and pieceY-2 >=0 and not collectionDetect(pieceX+1,pieceY-1):
            enemySideHit = collectionDetectRed(pieceX+2,pieceY-2)
            mySideHit = collectionDetectBlack(pieceX+2,pieceY-2)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+2,pieceY-2)
                candidateArray.append([pieceX+2,pieceY-2])
        if pieceX+2 <=8 and pieceY+2 <= 4 and not collectionDetect(pieceX+1,pieceY+1):
            enemySideHit = collectionDetectRed(pieceX+2,pieceY+2)
            mySideHit = collectionDetectBlack(pieceX+2,pieceY+2)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+2,pieceY+2)
                candidateArray.append([pieceX+2,pieceY+2])
    if piece[0] == '相':
        if pieceX-2 >=0 and pieceY-2 >=5 and not collectionDetect(pieceX-1,pieceY-1):
            enemySideHit = collectionDetectBlack(pieceX-2,pieceY-2)
            mySideHit = collectionDetectRed(pieceX-2,pieceY-2)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-2,pieceY-2)
                candidateArray.append([pieceX-2,pieceY-2])
        if pieceX-2 >=0 and pieceY+2 <= 9 and not collectionDetect(pieceX-1,pieceY+1):
            enemySideHit = collectionDetectBlack(pieceX-2,pieceY+2)
            mySideHit = collectionDetectRed(pieceX-2,pieceY+2)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX-2,pieceY+2)
                candidateArray.append([pieceX-2,pieceY+2])
        if pieceX+2 <=8 and pieceY-2 >=5 and not collectionDetect(pieceX+1,pieceY-1):
            enemySideHit = collectionDetectBlack(pieceX+2,pieceY-2)
            mySideHit = collectionDetectRed(pieceX+2,pieceY-2)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+2,pieceY-2)
                candidateArray.append([pieceX+2,pieceY-2])
        if pieceX+2 <=8 and pieceY+2 <= 9 and not collectionDetect(pieceX+1,pieceY+1):
            enemySideHit = collectionDetectBlack(pieceX+2,pieceY+2)
            mySideHit = collectionDetectRed(pieceX+2,pieceY+2)
            if enemySideHit and not mySideHit:
                #plotAttack(pieceX+2,pieceY+2)
                candidateArray.append([pieceX+2,pieceY+2])
    ####################
    if piece[0] == '卒':
        if pieceY <= 4:
            if collectionDetect(pieceX,pieceY+1):
                enemySideHit = collectionDetectRed(pieceX,pieceY+1)
                mySideHit = collectionDetectBlack(pieceX,pieceY+1)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX,pieceY+1)
                    candidateArray.append([pieceX,pieceY+1])
        else:
            if pieceY+1 <= 9 and collectionDetect(pieceX,pieceY+1):
                enemySideHit = collectionDetectRed(pieceX,pieceY+1)
                mySideHit = collectionDetectBlack(pieceX,pieceY+1)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX,pieceY+1)
                    candidateArray.append([pieceX,pieceY+1])
            if pieceX-1 >=0 and collectionDetect(pieceX-1,pieceY):
                enemySideHit = collectionDetectRed(pieceX-1,pieceY)
                mySideHit = collectionDetectBlack(pieceX-1,pieceY)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX-1,pieceY)
                    candidateArray.append([pieceX-1,pieceY])
            if pieceX+1 <=8 and collectionDetect(pieceX+1,pieceY):
                enemySideHit = collectionDetectRed(pieceX+1,pieceY)
                mySideHit = collectionDetectBlack(pieceX+1,pieceY)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX+1,pieceY)
                    candidateArray.append([pieceX+1,pieceY])
    if piece[0] == '兵':
        if pieceY >=5:
            if collectionDetect(pieceX,pieceY-1):
                enemySideHit = collectionDetectBlack(pieceX,pieceY-1)
                mySideHit = collectionDetectRed(pieceX,pieceY-1)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX,pieceY-1)
                    candidateArray.append([pieceX,pieceY-1])
        else:
            if pieceY-1 >=0 and collectionDetect(pieceX,pieceY-1):
                enemySideHit = collectionDetectBlack(pieceX,pieceY-1)
                mySideHit = collectionDetectRed(pieceX,pieceY-1)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX,pieceY-1)
                    candidateArray.append([pieceX,pieceY-1])
            if pieceX-1 >=0 and collectionDetect(pieceX-1,pieceY):
                enemySideHit = collectionDetectBlack(pieceX-1,pieceY)
                mySideHit = collectionDetectRed(pieceX-1,pieceY)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX-1,pieceY)
                    candidateArray.append([pieceX-1,pieceY])
            if pieceX+1 <=8 and collectionDetect(pieceX+1,pieceY):
                enemySideHit = collectionDetectBlack(pieceX+1,pieceY)
                mySideHit = collectionDetectRed(pieceX+1,pieceY)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX+1,pieceY)
                    candidateArray.append([pieceX+1,pieceY])
    #########################################
    if piece[0] == '馬' or piece[0] == '傌' :
        #
        if pieceY-2 >= 0 and pieceX-1 >= 0 and not collectionDetect(pieceX,pieceY-1):
            if collectionDetect(pieceX-1,pieceY-2):
                if piece[0] == '馬':
                    enemySideHit = collectionDetectRed(pieceX-1,pieceY-2)
                    mySideHit = collectionDetectBlack(pieceX-1,pieceY-2)
                if piece[0] == '傌':
                    enemySideHit = collectionDetectBlack(pieceX-1,pieceY-2)
                    mySideHit = collectionDetectRed(pieceX-1,pieceY-2)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX-1,pieceY-2)
                    candidateArray.append([pieceX-1,pieceY-2])
        if pieceY-2 >= 0 and pieceX+1 < 9 and not collectionDetect(pieceX,pieceY-1):
            if collectionDetect(pieceX+1,pieceY-2):
                if piece[0] == '馬':
                    enemySideHit = collectionDetectRed(pieceX+1,pieceY-2)
                    mySideHit = collectionDetectBlack(pieceX+1,pieceY-2)
                if piece[0] == '傌':
                    enemySideHit = collectionDetectBlack(pieceX+1,pieceY-2)
                    mySideHit = collectionDetectRed(pieceX+1,pieceY-2)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX+1,pieceY-2)
                    candidateArray.append([pieceX+1,pieceY-2])
        #
        if pieceY+2 < 10 and pieceX-1 >= 0 and not collectionDetect(pieceX,pieceY+1):
            if collectionDetect(pieceX-1,pieceY+2):
                if piece[0] == '馬':
                    enemySideHit = collectionDetectRed(pieceX-1,pieceY+2)
                    mySideHit = collectionDetectBlack(pieceX-1,pieceY+2)
                if piece[0] == '傌':
                    enemySideHit = collectionDetectBlack(pieceX-1,pieceY+2)
                    mySideHit = collectionDetectRed(pieceX-1,pieceY+2)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX-1,pieceY+2)
                    candidateArray.append([pieceX-1,pieceY+2])
        if pieceY+2 < 10 and pieceX+1 < 9 and not collectionDetect(pieceX,pieceY+1):
            if collectionDetect(pieceX+1,pieceY+2):
                if piece[0] == '馬':
                    enemySideHit = collectionDetectRed(pieceX+1,pieceY+2)
                    mySideHit = collectionDetectBlack(pieceX+1,pieceY+2)
                if piece[0] == '傌':
                    enemySideHit = collectionDetectBlack(pieceX+1,pieceY+2)
                    mySideHit = collectionDetectRed(pieceX+1,pieceY+2)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX+1,pieceY+2)
                    candidateArray.append([pieceX+1,pieceY+2])
        #
        if pieceX-2 >= 0 and pieceY-1 >= 0 and not collectionDetect(pieceX-1,pieceY):
            if collectionDetect(pieceX-2,pieceY-1):
                if piece[0] == '馬':
                    enemySideHit = collectionDetectRed(pieceX-2,pieceY-1)
                    mySideHit = collectionDetectBlack(pieceX-2,pieceY-1)
                if piece[0] == '傌':
                    enemySideHit = collectionDetectBlack(pieceX-2,pieceY-1)
                    mySideHit = collectionDetectRed(pieceX-2,pieceY-1)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX-2,pieceY-1)
                    candidateArray.append([pieceX-2,pieceY-1])
        if pieceX-2 >= 0 and pieceY+1 < 10 and not collectionDetect(pieceX-1,pieceY):
            if collectionDetect(pieceX-2,pieceY+1):
                if piece[0] == '馬':
                    enemySideHit = collectionDetectRed(pieceX-2,pieceY+1)
                    mySideHit = collectionDetectBlack(pieceX-2,pieceY+1)
                if piece[0] == '傌':
                    enemySideHit = collectionDetectBlack(pieceX-2,pieceY+1)
                    mySideHit = collectionDetectRed(pieceX-2,pieceY+1)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX-2,pieceY+1)
                    candidateArray.append([pieceX-2,pieceY+1])
        #
        if pieceX+2 < 9 and pieceY-1 >= 0 and not collectionDetect(pieceX+1,pieceY):
            if collectionDetect(pieceX+2,pieceY-1):
                if piece[0] == '馬':
                    enemySideHit = collectionDetectRed(pieceX+2,pieceY-1)
                    mySideHit = collectionDetectBlack(pieceX+2,pieceY-1)
                if piece[0] == '傌':
                    enemySideHit = collectionDetectBlack(pieceX+2,pieceY-1)
                    mySideHit = collectionDetectRed(pieceX+2,pieceY-1)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX+2,pieceY-1)
                    candidateArray.append([pieceX+2,pieceY-1])
        if pieceX+2 < 9 and pieceY+1 < 10 and not collectionDetect(pieceX+1,pieceY):
            if collectionDetect(pieceX+2,pieceY+1):
                if piece[0] == '馬':
                    enemySideHit = collectionDetectRed(pieceX+2,pieceY+1)
                    mySideHit = collectionDetectBlack(pieceX+2,pieceY+1)
                if piece[0] == '傌':
                    enemySideHit = collectionDetectBlack(pieceX+2,pieceY+1)
                    mySideHit = collectionDetectRed(pieceX+2,pieceY+1)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX+2,pieceY+1)
                    candidateArray.append([pieceX+2,pieceY+1])
    #########################################
    if piece[0] == '車' or piece[0] == '俥' :
        # up direction
        for scanY in range(pieceY-1,-1,-1):
            if collectionDetect(pieceX,scanY):
                if piece[0] == '車':
                    enemySideHit = collectionDetectRed(pieceX,scanY)
                    mySideHit = collectionDetectBlack(pieceX,scanY)
                if piece[0] == '俥':
                    enemySideHit = collectionDetectBlack(pieceX,scanY)
                    mySideHit = collectionDetectRed(pieceX,scanY)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX,scanY)
                    candidateArray.append([pieceX,scanY])
                break
        # down direction
        for scanY in range(pieceY+1,10,1):
            if collectionDetect(pieceX,scanY):
                if piece[0] == '車':
                    enemySideHit = collectionDetectRed(pieceX,scanY)
                    mySideHit = collectionDetectBlack(pieceX,scanY)
                if piece[0] == '俥':
                    enemySideHit = collectionDetectBlack(pieceX,scanY)
                    mySideHit = collectionDetectRed(pieceX,scanY)
                if enemySideHit and not mySideHit:
                    #plotAttack(pieceX,scanY)
                    candidateArray.append([pieceX,scanY])
                break
        # left direction
        for scanX in range(pieceX-1,-1,-1):
            if collectionDetect(scanX,pieceY):
                # piece touched
                if piece[0] == '車':
                    enemySideHit = collectionDetectRed(scanX,pieceY)
                    mySideHit = collectionDetectBlack(scanX,pieceY)
                if piece[0] == '俥':
                    enemySideHit = collectionDetectBlack(scanX,pieceY)
                    mySideHit = collectionDetectRed(scanX,pieceY)
                if enemySideHit and not mySideHit:
                    #plotAttack(scanX,pieceY)
                    candidateArray.append([scanX,pieceY])
                break
        # right direction
        for scanX in range(pieceX+1,9,1):
            if collectionDetect(scanX,pieceY):
                if piece[0] == '車':
                    enemySideHit = collectionDetectRed(scanX,pieceY)
                    mySideHit = collectionDetectBlack(scanX,pieceY)
                if piece[0] == '俥':
                    enemySideHit = collectionDetectBlack(scanX,pieceY)
                    mySideHit = collectionDetectRed(scanX,pieceY)
                if enemySideHit and not mySideHit:
                    #plotAttack(scanX,pieceY)
                    candidateArray.append([scanX,pieceY])
                break
    #########################################
    if piece[0] == '砲' or piece[0] == '炮' :
        # up direction
        for scanY in range(pieceY-1,-1,-1):
            hitPieceXY = collectionDetect(pieceX,scanY)
            if hitPieceXY != False:
                for scanY in range(hitPieceXY[1]-1,-1,-1):
                    if piece[0] == '砲':
                        enemySideHit = collectionDetectRed(pieceX,scanY)
                        mySideHit = collectionDetectBlack(pieceX,scanY)
                    if piece[0] == '炮':
                        enemySideHit = collectionDetectBlack(pieceX,scanY)
                        mySideHit = collectionDetectRed(pieceX,scanY)
                    if mySideHit:
                        break
                    if enemySideHit:
                        #plotAttack(pieceX,scanY)
                        candidateArray.append([pieceX,scanY])
                        break
                break
        # down direction
        for scanY in range(pieceY+1,10,1):
            hitPieceXY = collectionDetect(pieceX,scanY)
            if hitPieceXY != False:
                for scanY in range(hitPieceXY[1]+1,10,1):
                    if piece[0] == '砲':
                        enemySideHit = collectionDetectRed(pieceX,scanY)
                        mySideHit = collectionDetectBlack(pieceX,scanY)
                    if piece[0] == '炮':
                        enemySideHit = collectionDetectBlack(pieceX,scanY)
                        mySideHit = collectionDetectRed(pieceX,scanY)
                    if mySideHit:
                        break
                    if enemySideHit:
                        #plotAttack(pieceX,scanY)
                        candidateArray.append([pieceX,scanY])
                        break
                break
        # left direction
        for scanX in range(pieceX-1,-1,-1):
            hitPieceXY = collectionDetect(scanX,pieceY)
            if hitPieceXY != False:
                # piece touched
                # jump over the touched and keep going search
                for scanX in range(hitPieceXY[0]-1,-1,-1):
                    if piece[0] == '砲':
                        enemySideHit = collectionDetectRed(scanX,pieceY)
                        mySideHit = collectionDetectBlack(scanX,pieceY)
                    if piece[0] == '炮':
                        enemySideHit = collectionDetectBlack(scanX,pieceY)
                        mySideHit = collectionDetectRed(scanX,pieceY)
                    if mySideHit:
                        break
                    if enemySideHit:
                        #plotAttack(scanX,pieceY)
                        candidateArray.append([scanX,pieceY])
                        break
                break
        # right direction
        for scanX in range(pieceX+1,9,1):
            hitPieceXY = collectionDetect(scanX,pieceY)
            if hitPieceXY != False:
                for scanX in range(hitPieceXY[0]+1,9,1):
                    if piece[0] == '砲':
                        enemySideHit = collectionDetectRed(scanX,pieceY)
                        mySideHit = collectionDetectBlack(scanX,pieceY)
                    if piece[0] == '炮':
                        enemySideHit = collectionDetectBlack(scanX,pieceY)
                        mySideHit = collectionDetectRed(scanX,pieceY)
                    if mySideHit:
                        break
                    if enemySideHit:
                        #plotAttack(scanX,pieceY)
                        candidateArray.append([scanX,pieceY])
                        break
                break
    return candidateArray

# find both moving and attack
# return : [MOVE COORDINATE ARRAY,ATTACK COORDINATE ARRAY]
def checkPath(x,y):
    result=[]
    for piece in piecesBlack:
        if piece[1][0] == x and piece[1][1] == y:
            result.append(findRoads(piece))
            result.append(findAttacks(piece))
            #print (piece[0])
    for piece in piecesRed:
        if piece[1][0] == x and piece[1][1] == y:
            result.append(findRoads(piece))
            result.append(findAttacks(piece))
            #print (piece[0])
    return result

# variables for keep the postion of cursor
cursorX = 0
cursorY = 0

pieceTake = -1
loopMain=True
result=[]
side='red'
randomSwitch = 'off'
# MAIN LOOP
while loopMain:
    if randomSwitch == 'on':
        if piecesRed == [] or piecesBlack == []:
            randomSwitcj = 'off'
            break
        result = []
        if side == 'red':
            loopCount=0
            while(result == [] or result[0] == [] or loopCount < 100):
                loopCount+=1
                randPiece = random.choice(piecesRed)
                randCursorX = randPiece[1][0]
                randCursorY = randPiece[1][1]
                result=checkPath(randCursorX,randCursorY)
            #plotCursor(randCursorX,randCursorY)
            side='black'
        else:
            loopCount=0
            while(result == [] or result[0] == [] or loopCount < 100):
                loopCount+=1
                randPiece = random.choice(piecesBlack)
                randCursorX = randPiece[1][0]
                randCursorY = randPiece[1][1]
                result=checkPath(randCursorX,randCursorY)
            #plotCursor(randCursorX,randCursorY)
            side='red'
        if len(result):
             if len(result[0]):
                 for i in result[0]:
                     plotCandidate(i[0],i[1])
             if len(result[1]):
                 for i in result[1]:
                     plotAttack(i[0],i[1])
        plotCursor(randCursorX,randCursorY)
        print(result)
        pygame.display.update()
        time.sleep(1)
        # eat
        if len(result) > 1 and len(result[1]) > 0:
            randXY = random.choice(result[1])
            pieceTake = randPiece
            movePiece = [pieceTake[0],(randXY[0],randXY[1]),pieceTake[2]]
            # move
            if pieceTake in piecesBlack:
                piecesBlack.remove(pieceTake)
                piecesBlack.append(movePiece)
            if pieceTake in piecesRed:
                piecesRed.remove(pieceTake)
                piecesRed.append(movePiece)
            # eat
            for i in piecesBlack:
                if i[1] == (randXY[0],randXY[1]) and i != movePiece:
                    piecesBlack.remove(i)
            for i in piecesRed:
                if i[1] == (randXY[0],randXY[1]) and i != movePiece:
                    piecesRed.remove(i)
        else:
            # move
            randXY = random.choice(result[0])
            pieceTake = randPiece
            movePiece = [pieceTake[0],(randXY[0],randXY[1]),pieceTake[2]]
            if pieceTake in piecesBlack:
                piecesBlack.remove(pieceTake)
                piecesBlack.append(movePiece)
            if pieceTake in piecesRed:
                piecesRed.remove(pieceTake)
                piecesRed.append(movePiece)
        DISPLAYSURF.fill((0,0,0))
        plotBoard()           
        pygame.display.update()
        #time.sleep(1)
    for event in pygame.event.get():
        if event.type == QUIT:
            loopMain=False
        if event.type == pygame.KEYDOWN:
            DISPLAYSURF.fill((0,0,0))
            if event.key == pygame.K_r:
                if randomSwitch == 'off':
                    randomSwitch = 'on'
                else:
                    randomSwitch = 'off'
                    result = []
            if event.key == pygame.K_UP:
                if cursorY > 0:
                    cursorY-=1
                print ("up")
            elif event.key == pygame.K_DOWN:
                if cursorY < 9:
                    cursorY+=1
                print ("down")
            elif event.key == pygame.K_LEFT:
                if cursorX > 0:
                    cursorX-=1
                print ("left")
            elif event.key == pygame.K_RIGHT:
                if cursorX < 8:
                    cursorX+=1
                print ("right")
            elif event.key == pygame.K_RETURN:
                if pieceTake == -1:
                    # first ENTER pressed
                    # pick up the piece if exist
                    # run rules and return list
                    # result[0] : move list
                    # result[1] : attack list
                    result=checkPath(cursorX,cursorY)
                    for piece in piecesBlack:
                        if piece[1][0] == cursorX and piece[1][1] == cursorY:
                            pieceTake = piece
                            break
                    for piece in piecesRed:
                        if piece[1][0] == cursorX and piece[1][1] == cursorY:
                            pieceTake = piece
                            break
                else:
                    # second ENTER pressed
                    # move and attack in the different list
                    # result[0] : move list
                    # result[1] : attack list
                    # move, just move
                    if [cursorX,cursorY] in result[0]:
                        movePiece = [pieceTake[0],(cursorX,cursorY),pieceTake[2]]
                        # move
                        if pieceTake in piecesBlack:
                            piecesBlack.remove(pieceTake)
                            piecesBlack.append(movePiece)
                        if pieceTake in piecesRed:
                            piecesRed.remove(pieceTake)
                            piecesRed.append(movePiece)
                    # attack, move then eat
                    if len(result) > 1 and len(result[1]) > 0:
                        if  [cursorX,cursorY] in result[1]:
                            movePiece = [pieceTake[0],(cursorX,cursorY),pieceTake[2]]
                            # move
                            if pieceTake in piecesBlack:
                                piecesBlack.remove(pieceTake)
                                piecesBlack.append(movePiece)
                            if pieceTake in piecesRed:
                                piecesRed.remove(pieceTake)
                                piecesRed.append(movePiece)
                            # eat
                            for i in piecesBlack:
                                if i[1] == (cursorX,cursorY) and i != movePiece:
                                    piecesBlack.remove(i)
                            for i in piecesRed:
                                if i[1] == (cursorX,cursorY) and i != movePiece:
                                    piecesRed.remove(i)
                    pieceTake = -1
                    result = []
                    #print(piecesBlack)
                    #print(piecesRed)
            elif event.key == pygame.K_ESCAPE:
                pieceTake = -1
                result = []
            plotBoard()
            # 
            if len(result):
                if len(result[0]):
                    for i in result[0]:
                        plotCandidate(i[0],i[1])
                if len(result[1]):
                    for i in result[1]:
                        plotAttack(i[0],i[1])
            plotCursor(cursorX,cursorY)
            
    pygame.display.update()
# MAIN LOOP END
        
#for x in range(0,200):
#    print (x+0x2500,chr(x+0x2500),"xx") 

pygame.event.clear()
while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == KEYDOWN:
        break
pygame.quit()

print("╔═╤═╤═╤═╤═╤═╤═╤═╗")
print("║  │  │  │╲│╱│  │  │  ║")
print("╟─┼─┼─┼─┼─┼─┼─┼─╢")
print("║  │  │  │╱│╲│  │  │  ║")
print("╟─╬─┼─┼─┼─┼─┼─╬─╢")
print("║  │  │  │  │  │  │  │  ║")
print("╠─┼─╬─┼─╬─┼─╬─┼─╣")
print("║  │  │  │  │  │  │  │  ║")
print("╟─┴─┴─┴─┴─┴─┴─┴─╢")
print("║    楚    河      漢    界    ║")
print("╟─┬─┬─┬─┬─┬─┬─┬─╢")
print("║  │  │  │  │  │  │  │  ║")
print("╠─┼─╬─┼─╬─┼─╬─┼─╣")
print("║  │  │  │  │  │  │  │  ║")
print("╟─╬─┼─┼─┼─┼─┼─╬─╢")
print("║  │  │  │╲│╱│  │  │  ║")
print("╟─┼─┼─┼─┼─┼─┼─┼─╢")
print("║  │  │  │╱│╲│  │  │  ║")
print("╚═╧═╧═╧═╧═╧═╧═╧═╝")
