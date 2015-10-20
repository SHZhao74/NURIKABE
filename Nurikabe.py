#!/usr/bin/env python

# Copyright (C) 2010 Paul Bourke <pauldbourke@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import sys
import random
from multiprocessing import Process

BOARD_SIZE = 5
RIVER = '0'
BLANK = '-'
ISLAND= "132456789"
EXTEND_ISLAND = '+'
updateBoardEvent = pygame.event.Event(pygame.USEREVENT)
pygame.init()
class PyGameBoard():
  """Represents the game's frontend using pygame"""
  def __init__(self, engine, windowSize, gridValues):
    #pygame.init()
    pygame.display.set_caption('Nurikabe~')
    self.__engine = engine
    self.__gridValues = gridValues
    self.__screen = pygame.display.set_mode(windowSize)
    background = pygame.image.load('55.png').convert()
    self.__screen.blit(background, (0,0))
    self.__tiles = self.__createTiles(12,12)
    self.__drawUI()
    self.__draw()
    

  def __draw(self):
    """Handles events and updates display buffer"""
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
          self.__handleMouse(event.pos)
        elif event.type == updateBoardEvent:
          print "USEREVENT"
          self.__updateBoard(self.__gridValues)
      pygame.display.flip()


  def __drawUI(self):
    '''Draws the text buttons along the right panel'''
    font = pygame.font.Font('Monaco.ttf', 38)
    font.set_underline(True)
    self.__titleText = font.render('NURIKABE', 1, (0, 0, 0))
    self.__titleTextRect = self.__titleText.get_rect()
    self.__titleTextRect.centerx = 600
    self.__titleTextRect.centery = 30
    self.__screen.blit(self.__titleText, self.__titleTextRect)

    font = pygame.font.Font('Monaco.ttf', 18)
    self.__titleText = font.render('Shou-Hao Zhao2015', 1, (0, 0, 0))
    self.__titleTextRect = self.__titleText.get_rect()
    self.__titleTextRect.centerx = 600
    self.__titleTextRect.centery = 60 
    self.__screen.blit(self.__titleText, self.__titleTextRect)

    font = pygame.font.Font('gunny.ttf', 30)
    self.__newGameText = font.render('-New Game-', 1, (0, 0, 0))
    self.__newGameTextRect = self.__newGameText.get_rect()
    self.__newGameTextRect.centerx = 595 
    self.__newGameTextRect.centery = 180
    self.__screen.blit(self.__newGameText, self.__newGameTextRect)

    self.__solveText = font.render('-Solve-', 1, (0, 0, 0))
    self.__solveTextRect = self.__solveText.get_rect()
    self.__solveTextRect.centerx = 595
    self.__solveTextRect.centery = 220
    self.__screen.blit(self.__solveText, self.__solveTextRect) 

  def __handleMouse(self, (x,y)):
    if self.__newGameTextRect.collidepoint(x,y):
      self.__engine.startNewGame()

    elif self.__solveTextRect.collidepoint(x,y): #Start to slove the puzzle
      #linePuzzle = self.__engine.gridToLine(self.__gridValues)
      sys.stdout.flush()
      print 'Getting solution.. ',
      linePuzzle = self.__engine.solve(self.__gridValues) 
      pygame.event.post(updateBoardEvent)
      print 'Done'
      self.__updateBoard(linePuzzle)
      #self.__unhightlightBoard()
    
  def __updateBoard(self, gridValues):
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        self.__tiles[i][j].updateValue(gridValues[i][j])
        if gridValues[i][j] == RIVER: #if it is one of River, change it into black
          self.__tiles[i][j].updateColor(pygame.color.THECOLORS['black'])
        #elif gridValues[i][j] == EXTEND_ISLAND:
        #  self.__tiles[i][j].updateColor(pygame.color.THECOLORS['gray'])
    

  def __unhightlightBoard(self):
    for i in range(9):
      for j in range(9):
        self.__tiles[i][j].unhighlight()

  def __createTiles(self, initX=0, initY=0):
    """Set up a list of tiles corresponding to the grid, along with
       each ones location coordinates on the board"""
    square_size = 90
    tiles = list()
    x = y = 0
    for i in range(0,BOARD_SIZE):
      row = list()
      for j in range(0,BOARD_SIZE):  
        x = (j * 96) + initX
        y = (i * 96) + initY
        tile = Tile(self.__gridValues[i][j], (x, y), (i, j), square_size)
        row.append(tile)
      tiles.append(row)
    self.__currentTile = tiles[0][0]
    return tiles
  
  
class Tile():
  """Represents a graphical tile on the board"""
  def __init__(self, value, coords, gridLoc, size):
    xpos = coords[0]
    ypos = coords[1]
    self.__fontColor = pygame.color.THECOLORS["black"] 
    self.__readOnly = False
    self.__colorSquare = pygame.Surface((size, size)).convert()
    self.__colorSquare.fill(pygame.color.THECOLORS['white'], None, pygame.BLEND_RGB_ADD)
    self.__colorSquareRect = self.__colorSquare.get_rect()
    self.__colorSquareRect = self.__colorSquareRect.move(xpos+1, ypos+1)
    self.__value = value
    self.__gridLoc = gridLoc
    self.__screen = pygame.display.get_surface()
    self.__rect = pygame.Rect(xpos, ypos, size, size)
    self.__isCorrect = True
    if self.__value is not BLANK: 
      self.__readOnly = True 
    self.__draw()
  
  def updateColor(self, color):
    self.__colorSquare.fill(color)
    self.__draw()

  def updateValue(self, value):
    self.__value = value
    self.__draw() 
   
  def isCorrect(self):
    return self.__isCorrect

  def setCorrect(self, isCorrect):
    self.__isCorrect = isCorrect
  
  def setFontColor(self, fontColor):
    self.__fontColor = fontColor

  def getValue(self):
    return self.__value
  
  def getRect(self):
    return self.__rect
  
  def getGridLoc(self):
    return self.__gridLoc

  def isReadOnly(self):
    return self.__readOnly

  def highlight(self, color):
    if self.__readOnly is True:
      return
    self.__colorSquare.fill(color)
    self.__draw()

  def unhighlight(self):
    self.__colorSquare.fill((255, 225, 255), None, pygame.BLEND_RGB_ADD)
    self.__draw()

  def __draw(self):
    value = self.__value
    if self.__value == BLANK: 
      value = ''
    font = pygame.font.Font('Monaco.ttf', 60)
    text = font.render(str(value), 1, self.__fontColor)
    textpos = text.get_rect()
    textpos.centerx = self.__rect.centerx
    textpos.centery = self.__rect.centery
    self.__screen.blit(self.__colorSquare, self.__colorSquareRect)
    self.__screen.blit(text, textpos)

class Nurikabe:
  """Represents the game's backend and logic"""
  def __init__(self, puzzleFile):
    self.__puzzleFile = puzzleFile
    self.startNewGame()

  def startNewGame(self):

    self.__linePuzzle = self.__loadPuzzle(self.__puzzleFile)
    gridValues = self.lineToGrid(self.__linePuzzle)
    #board = Process(target=PyGameBoard, args=(self, (700,500), gridValues))
    #board.start()
    #board.join(1)
    board = PyGameBoard(self, (700,500), gridValues)
    '''print 'Getting solution.. ',
    sys.stdout.flush()
    GRID_VALUES = self.__solution = self.__solve(gridValues)
    pygame.event.post(updateBoardEvent)
    print 'Done' 
    '''
    #board.setValues(gridValues)
    
  def __loadPuzzle(self, fileName):
    """Read in a random puzzle from the puzzle file"""
    ret = []
    numPuzzles = 3 
    puzzleSize = BOARD_SIZE**2
    seekTo = (random.randint(0, numPuzzles)*(puzzleSize+1))
    print "Puzzle No.",seekTo
    try:
      file = open(fileName, 'r')
    except IOError as e:
      print str(e)
      sys.exit(1)
    file.seek(seekTo)
    linePuzzle = file.readline().strip()
    file.close()
    for i in linePuzzle:
      ret.append(i)
    #print ret
    return ret 

  def gridToLine(self, grid):
    linePuzzle = '' 
    for i in range(BOARD_SIZE):
      for j in range(BOARD_SIZE):
        linePuzzle += grid[i][j]
    return linePuzzle

  def lineToGrid(self, linePuzzle):
    assert (len(linePuzzle) == BOARD_SIZE**2)
    grid = []
    for i in xrange(0, BOARD_SIZE**2, BOARD_SIZE):
      grid.append(linePuzzle[i:i+BOARD_SIZE])
    return grid 

  def getSolution(self):
    return self.__solution

  def checkSolution(self, attemptGrid):
    attemptLine = self.gridToLine(attemptGrid)
    assert (len(attemptLine) == 81)
    ret = []
    for i in range(81):
      if attemptLine[i] == BLANK:
        ret.append(True) 
        continue
      if attemptLine[i] == self.__solution[i]:
        ret.append(True)
      else:
        ret.append(False) 
    return ret

  def solve(self, linePuzzle):
    #linePuzzle = ''.join(linePuzzle)
    answer = self.slove_step1(linePuzzle)
    #answer = self.only1WayOut(answer)
    print answer
    return answer
  def slove_step1(self, linePuzzle):
    '''use the simplest method to detect which grid shoud be river'''
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if linePuzzle[i][j] == '1': 
          '''first black the blank arround the no.1 island'''
          if i>0: #up
            linePuzzle[i-1][j] = RIVER
          if i < BOARD_SIZE-1: #down
            linePuzzle[i+1][j] = RIVER
          if j > 0: #left
            linePuzzle[i][j-1] = RIVER         
          if j < BOARD_SIZE-1: #right
            linePuzzle[i][j+1] = RIVER
        elif linePuzzle[i][j] == BLANK :
          '''dectect each blank whether connect multi island'''
          cnt=0
          if i > 0 and linePuzzle[i-1][j] != RIVER and linePuzzle[i-1][j] !=BLANK:
            cnt+=1
          if i < BOARD_SIZE-1 and linePuzzle[i+1][j] != RIVER and linePuzzle[i+1][j] != BLANK:
            cnt+=1
          if j > 0 and linePuzzle[i][j-1] != RIVER and linePuzzle[i][j-1] != BLANK:
            cnt+=1
          if j < BOARD_SIZE-1 and  linePuzzle[i][j+1] != RIVER and  linePuzzle[i][j+1] != BLANK:
            cnt+=1
          
          if cnt>1:
            linePuzzle[i][j] = RIVER
    return linePuzzle

  def only1WayOut (self, linePuzzle):
    '''detect if islands and river have only one direction can extend''' 
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if linePuzzle[i][j] == RIVER:
          cnt = 0
          who = 0
          if i > 0 and linePuzzle[i-1][j] ==BLANK:
            cnt+= 1
            who = 0
          if i < BOARD_SIZE-1 and linePuzzle[i+1][j] == BLANK:
            cnt+= 1
            who = 1
          if j > 0 and linePuzzle[i][j-1] == BLANK:
            cnt+= 1
            who = 2
          if j < BOARD_SIZE-1 and linePuzzle[i][j+1] == BLANK:
            cnt+= 1
            who = 3          
          if cnt==1:
            if who ==0:
              linePuzzle[i-1][j] = RIVER
            elif who ==1:
              linePuzzle[i+1][j] = RIVER
            elif who ==2:
              linePuzzle[i][j-1] = RIVER
            elif who ==3:
              linePuzzle[i][j+1] = RIVER

        elif linePuzzle[i][j] in ISLAND and linePuzzle[i][j]!='1':
          cnt = 0
          who = 0
          if i > 0 and linePuzzle[i-1][j] ==BLANK:
            cnt+= 1
            who = 0
          if i < BOARD_SIZE-1 and linePuzzle[i+1][j] == BLANK:
            cnt+= 1
            who = 1
          if j > 0 and linePuzzle[i][j-1] == BLANK:
            cnt+= 1
            who = 2
          if j < BOARD_SIZE-1 and linePuzzle[i][j+1] == BLANK:
            cnt+= 1
            who = 3          
          if cnt==1:
            if who ==0:
              linePuzzle[i-1][j] = EXTEND_ISLAND
            elif who ==1:
              linePuzzle[i+1][j] = EXTEND_ISLAND
            elif who ==2:
              linePuzzle[i][j-1] = EXTEND_ISLAND
            elif who ==3:
              linePuzzle[i][j+1] = EXTEND_ISLAND
    return linePuzzle
def main():
  newGame = Nurikabe('puzzle.txt')

if __name__ == '__main__':
  main()
