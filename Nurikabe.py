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
class PyGameBoard():
  """Represents the game's frontend using pygame"""
  def __init__(self, engine, windowSize, gridValues):
    pygame.init()
    pygame.display.set_caption('Sudoku')
    self.__engine = engine
    self.__gridValues = gridValues
    self.__screen = pygame.display.set_mode(windowSize)
    background = pygame.image.load('55.png').convert()
    self.__tiles = self.__createTiles(12,12)
    
    self.__draw()

  def __draw(self):
    """Handles events and updates display buffer"""
    
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit() 
      self.__tiles[3][2].toBlack()
      pygame.display.flip()

 
       
  def __updateBoard(self, gridValues):
    for i in range(9):
      for j in range(9):
        self.__tiles[i][j].updateValue(gridValues[i][j])

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
    if self.__value is not '-': 
      self.__readOnly = True 
    self.__draw()
  
  def toBlack(self):
    self.__colorSquare.fill(pygame.color.THECOLORS['black'], None, pygame.BLEND_RGB_ADD)
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
    if self.__value == '-': 
      value = ''
    font = pygame.font.Font('Monaco.ttf', 60)
    text = font.render(str(value), 1, self.__fontColor)
    textpos = text.get_rect()
    textpos.centerx = self.__rect.centerx
    textpos.centery = self.__rect.centery
    self.__screen.blit(self.__colorSquare, self.__colorSquareRect)
    self.__screen.blit(text, textpos)

class Sudoku:
  """Represents the game's backend and logic"""
  def __init__(self, puzzleFile):
    self.__puzzleFile = puzzleFile
    self.startNewGame()

  def startNewGame(self):
    self.__linePuzzle = self.__loadPuzzle(self.__puzzleFile)
    gridValues = self.lineToGrid(self.__linePuzzle)
    board = Process(target=PyGameBoard, args=(self, (500,500), gridValues))
    board.start()
    #board.join()
    print 'Getting solution.. ',
    sys.stdout.flush()
    #self.__solution = self.__solve(self.__linePuzzle)
    
    print 'Done' 
    
    #board.setValues(gridValues)
    
  def __loadPuzzle(self, fileName):
    """Read in a random puzzle from the puzzle file"""
    ret = []
    numPuzzles = 1012 
    puzzleSize = BOARD_SIZE*BOARD_SIZE
    seekTo = 0#(random.randint(0, puzzleSize*numPuzzles)/82)*82 
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
    #print ret, "len ret ="+str(len(ret))
    return ret 

  def gridToLine(self, grid):
    linePuzzle = '' 
    for i in range(9):
      for j in range(9):
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

  def __solve(self, linePuzzle):
    linePuzzle = ''.join(linePuzzle)
    i = linePuzzle.find('-')
    if i == -1:
      return linePuzzle

    excluded_numbers = set()
    for j in range(81):
      if self.sameRow(i,j) or self.sameCol(i,j) or self.sameBlock(i,j):
        excluded_numbers.add(linePuzzle[j])

    for m in '123456789':
      if m not in excluded_numbers:
        funcRet = self.__solve(linePuzzle[:i]+m+linePuzzle[i+1:])
        if funcRet is not None:
          return funcRet
      
  def sameRow(self, i, j): 
    return (i/5 == j/5)

  def sameCol(self, i, j): 
    return (i-j) % 5 == 0
  
  def sameBlock(self, i, j): 
    return (i/27 == j/27 and i%9/3 == j%9/3)
  
  def checkSolution(self, attemptGrid):
    attemptLine = self.gridToLine(attemptGrid)
    assert (len(attemptLine) == 81)
    ret = []
    for i in range(81):
      if attemptLine[i] == '-':
        ret.append(True) 
        continue
      if attemptLine[i] == self.__solution[i]:
        ret.append(True)
      else:
        ret.append(False) 
    return ret
    
def main():
  newGame = Sudoku('puzzle.txt')

if __name__ == '__main__':
  main()