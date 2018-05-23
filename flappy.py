from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH  = 512
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
PIPEHEIGHT   = 300
PIPEWIDTH    = 50
BASEY        = SCREENHEIGHT * 0.79
BASEX        = 0

try:
    xrange
except NameError:
    xrange = range

class Player:
    def __init__(self):
        self.x = int(SCREENWIDTH * 0.2)
        self.width = 20
        self.height = 20

        maxValue = int((SCREENHEIGHT - self.height) / SCREENHEIGHT * 100)
        minValue = int(self.height / SCREENHEIGHT * 100)
        self.y = int((SCREENHEIGHT - self.height) * random.randint(minValue, maxValue) / 100 )

         # player velocity, max velocity, downward accleration, accleration on flap
        self.velY    =  -9   # player's velocity along Y, default same as playerFlapped
        self.maxVelY =  10   # max vel along Y, max descend speed
        self.accY    =   1   # players downward accleration
        self.flapAcc =  -9   # players speed on flapping
        self.flapped = False # True when player flaps

        self.score = 0

    def update(self, event):
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            if self.y > -2 * self.height:
                self.velY = self.flapAcc
                self.flapped = True

def main():
    global SCREEN, FPSCLOCK, myfont
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')
    myfont = pygame.font.SysFont("Comic Sans MS", 30)

    while True:
        crashInfo = mainGame()
        showGameOverScreen(crashInfo)

def mainGame():
    players = []
    for i in range(0,1):
        players.append(Player())
    
    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    # newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        newPipe1[0],
        # newPipe2[0],
    ]

    # list of lowerpipe
    lowerPipes = [
        newPipe1[1],
        # newPipe2[1],
    ]

    pipeVelX = -4

    while True:
        playerEvent = type('', (object,),{ 'type': 0, 'key': 0})
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                playerEvent = event

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -PIPEWIDTH:
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.fill((0,0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            pygame.draw.rect(SCREEN,(255,255,255), (uPipe['x'], uPipe['y'],PIPEWIDTH,PIPEHEIGHT))
            pygame.draw.rect(SCREEN,(255,255,255), (lPipe['x'], lPipe['y'],PIPEWIDTH,PIPEHEIGHT))

        pygame.draw.rect(SCREEN,(255,255,255), (BASEX, BASEY,SCREENWIDTH,BASEY))

        for player in players:
            player.update(playerEvent)
            # check for crash here
            crashTest = checkCrash(player,
                                upperPipes, lowerPipes)
            if crashTest[0]:
                players.remove(player)
                if len(players) ==0:
                    return {
                        'player': player,
                        'upperPipes': upperPipes,
                        'lowerPipes': lowerPipes,
                    }

            # check for score
            playerMidPos = player.x + player.width / 2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + PIPEWIDTH / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    player.score += 1

            # player's movement
            if player.velY < player.maxVelY and not player.flapped:
                player.velY += player.accY
            if player.flapped:
                player.flapped = False

            player.y += min(player.velY, BASEY - player.y - player.height)

           
            # print score so player overlaps the score
            showScore(player.score)
            pygame.draw.ellipse(SCREEN, (255,255,255,200), (player.x, player.y, player.width, player.width), 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """crashes the player down ans shows gameover image"""
    player = crashInfo['player']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

        # draw sprites
        SCREEN.fill((0,0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            pygame.draw.rect(SCREEN,(255,255,255), (uPipe['x'], uPipe['y'],PIPEWIDTH, PIPEHEIGHT))
            pygame.draw.rect(SCREEN,(255,255,255), (lPipe['x'], lPipe['y'],PIPEWIDTH, PIPEHEIGHT))

        pygame.draw.rect(SCREEN,(255,255,255), (BASEX, BASEY,SCREENWIDTH,BASEY))
        showScore(player.score)

        pygame.draw.ellipse(SCREEN, (255,255,255,200), (player.x, player.y, player.width, player.width), 0)

        FPSCLOCK.tick(FPS)
        pygame.display.update()

def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - PIPEHEIGHT},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    label = myfont.render(str(score), 1, (255,255,255))
    SCREEN.blit(label, (10, 10))

def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""

    # if player crashes into ground
    if player.y + player.height >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player.x, player.y,
                      player.width, player.height)

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], PIPEWIDTH, PIPEHEIGHT)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], PIPEWIDTH, PIPEHEIGHT)

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect)
            lCollide = pixelCollision(playerRect, lPipeRect)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    return True

if __name__ == '__main__':
    main()
