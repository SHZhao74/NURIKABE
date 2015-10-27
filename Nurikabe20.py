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
import copy
from multiprocessing import Process


BOARD_SIZE = 5
RIVER = '0'
BLANK = '-'
ISLAND= "132456789"
SUB_ISLAND = '+'
updateBoardEvent = pygame.event.Event(pygame.USEREVENT)
pygame.init()

class Grid():
  def __init__(self, val):
    self.val = val
    self.sub_islands = list()
    self.left_sub_island = 0
    if val in ISLAND:
      '''if the grid is an island, 
      set the number which how many sub_island don't be placed yet'''
      self.left_sub_island = int(val)-1
      

class PyGameBoard():
  """Represents the game's frontend using pygame"""
  def __init__(self, puzzleFile):
    #pygame.init()
    self._puzzleFile = puzzleFile
    self._startNewGame()
  
  def _startNewGame(self):

    self._linePuzzle = self._loadPuzzle(self._puzzleFile)
    print 'max_island_num=',self.max_island_num, 'island_num=', self.island_num
    self._gridValues = self.lineToGrid(self._linePuzzle)
    self.grids = self._createGrid()
    self.answer = Nurikabe(self.grids)
    #board = Process(target=PyGameBoard, args=(self, (700,500), gridValues))
    #board.start()
    #board.join(1)
    
    '''print 'Getting solution.. ',
    sys.stdout.flush()
    GRID_VALUES = self.__solution = self.__solve(gridValues)
    pygame.event.post(updateBoardEvent)
    print 'Done' 
    '''
    #board.setValues(gridValues) 
  def _loadPuzzle(self, fileName):
    """Read in a random puzzle from the puzzle file"""
    ret = []
    numPuzzles = 9
    puzzleSize = BOARD_SIZE**2
    seekTo = (random.randint(0, numPuzzles)*(puzzleSize+1))
    #seekTo =0
    print "Puzzle No.",seekTo/(puzzleSize+1)
    try:
      file = open(fileName, 'r')
    except IOError as e:
      print str(e)
      sys.exit(1)
    file.seek(seekTo)
    linePuzzle = file.readline().strip()
    file.close()

    self.island_num = 0     #how many grods have been tagged as island or sub island
    self.max_island_num = 0 #how many grids should be island or sub island
    for i in linePuzzle:
      ret.append(i)
      if i in ISLAND:
        self.max_island_num += int(i)
        self.island_num+=1
    #print ret
    return ret
  
  def _createGrid(self):
    grids = list()
    for i in range(0,BOARD_SIZE):
      row = list()
      for j in range(0,BOARD_SIZE):  
        tile = Grid(self._gridValues[i][j])
        row.append(tile)
      grids.append(row)
    return grids
  def result(self):
    print 'Final answer:'
    for i in xrange(0,BOARD_SIZE):
      for j in xrange(0,BOARD_SIZE):
        print self.grids[i][j].val,
      print ''

  def __updateBoard(self):
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        #self.__tiles[i][j].updateValue(gridValues[i][j])
        if self.tiles[i][j].value == RIVER: #if it is one of River, change it into black
          self.tiles[i][j].updateColor(pygame.color.THECOLORS['black'])
        elif self.tiles[i][j].value == SUB_ISLAND:
          self.tiles[i][j].updateColor(pygame.color.THECOLORS['white'])
  
  def lineToGrid(self, linePuzzle):
    assert (len(linePuzzle) == BOARD_SIZE**2)
    grid = []
    for i in xrange(0, BOARD_SIZE**2, BOARD_SIZE):
      grid.append(linePuzzle[i:i+BOARD_SIZE])
    return grid 
  
  def gridToLine(self, grid):
    linePuzzle = '' 
    for i in range(BOARD_SIZE):
      for j in range(BOARD_SIZE):
        linePuzzle += grid[i][j]
    return linePuzzle

class Nurikabe:
  """Represents the game's backend and logic"""
  def __init__(self, tiles):
    self.tiles = self.slove_step1(tiles)
    self.tiles = self.neverTouch()
    #self.tiles = self.only1WayOut()
    #print tiles[1][0].value
  #return self.tiles
  
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
    
  def slove_step1(self, tiles):
    '''use the simplest method to detect which grid shoud be river'''
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if tiles[i][j].val == '1': 
          '''first black the blank arround the no.1 island'''
          #print i,j
          if i>0: #up
            tiles[i-1][j].val = RIVER
          if i < BOARD_SIZE-1: #down
            tiles[i+1][j].val = RIVER
          if j > 0: #left
            tiles[i][j-1].val = RIVER         
          if j < BOARD_SIZE-1: #right
            tiles[i][j+1].val = RIVER
        elif tiles[i][j].val == BLANK :
          '''dectect each blank whether connect multi island'''
          cnt=0
          if i > 0 and tiles[i-1][j].val != RIVER and tiles[i-1][j].val !=BLANK:
            cnt+=1
          if i < BOARD_SIZE-1 and tiles[i+1][j].val != RIVER and tiles[i+1][j].val != BLANK:
            cnt+=1
          if j > 0 and tiles[i][j-1].val != RIVER and tiles[i][j-1].val != BLANK:
            cnt+=1
          if j < BOARD_SIZE-1 and  tiles[i][j+1].val != RIVER and  tiles[i][j+1].val != BLANK:
            cnt+=1
          
          if cnt>1:
            tiles[i][j].val = RIVER
    return tiles

  def neverTouch(self):
    '''detect some blank will never be sub_islands ,so it must be a RIVER
    e.g. no ISLAND can extend to the blank
    . . . 1 . . .
    . . 1 1 1 . .
    . 1 1 1 1 1 .
    1 1 1 4 1 1 1
    . 1 1 1 1 1 .
    . . 1 1 1 . .
    . . . 1 . . .

    '''
    tmpBoard =[]
    for i in xrange(0,BOARD_SIZE):
      raw = []
      for j in xrange(0,BOARD_SIZE):
        raw.append(0)
      tmpBoard.append(raw)

    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if self.tiles[i][j].val in ISLAND:
          #print i, j
          value = int(self.tiles[i][j].val)
          for x in xrange(1,value+1): #upper part
            skip = abs(x-value)
            for y in xrange(0,x*2-1):
              if isInTheBoard(i-(value-x), j-(value-1)+skip+y):
                tmpBoard[i-(value-x)][j-(value-1)+skip+y]+=1

          loop = range((value)*2-1, 0, -2)
          for x in xrange(value+1,value*2): #lower part
            skip = abs(x-value)
            for y in xrange(0,loop[skip]):
              if isInTheBoard(i-(value-x), j-(value-1)+skip+y):
                tmpBoard[i-(value-x)][j-(value-1)+skip+y]+=1   

    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if tmpBoard[i][j] is 0:
          self.tiles[i][j].val = RIVER

    return self.tiles

  def is_island_finish(self, i, j):
    '''detect if a island has been completely extended'''
    if self.tiles[i][j].left_sub_island == 0:
      return True
    else: return False
  def island1way(self, ori_puzzle, i, j):
    '''Recursivly extend island if it have only 1 direction can extend,
       and stop if have extended same quantity of sub_island with island number'''
    cnt = 0
    who = 0
    if i > 0            and ori_puzzle[i-1][j].val == BLANK:
      cnt+= 1
      who = 0
    if i < BOARD_SIZE-1 and ori_puzzle[i+1][j].val == BLANK:
      cnt+= 1
      who = 1
    if j > 0            and ori_puzzle[i][j-1].val == BLANK:
      cnt+= 1
      who = 2
    if j < BOARD_SIZE-1 and ori_puzzle[i][j+1].val == BLANK:
      cnt+= 1
      who = 3          
    if cnt==1:
      if who ==0:
        if self.is_island_finish(i,j):
          ori_puzzle[i-1][j].val = RIVER
        else:
          self.tiles[i][j].sub_islands = (i-1,j) 
          ori_puzzle[i-1][j].val = SUB_ISLAND
      elif who ==1:
        if self.is_island_finish(i,j):
          ori_puzzle[i+1][j].val = RIVER
        else:
          self.tiles[i][j].sub_islands = (i+1,j) 
          ori_puzzle[i+1][j].val = SUB_ISLAND
      elif who ==2:
        if self.is_island_finish(i,j):
          ori_puzzle[i][j-1].val = RIVER
        else:
          self.tiles[i][j].sub_islands = (i,j-1) 
          ori_puzzle[i][j-1].val = SUB_ISLAND
      elif who ==3:
        if self.is_island_finish(i,j):
          print "finish"
          ori_puzzle[i][j+1].val = RIVER
        else:
          self.tiles[i][j].sub_islands = (i,j+1) 
          ori_puzzle[i][j+1].val = SUB_ISLAND
          ori_puzzle[i][j+1].left_sub_island = ori_puzzle[i][j].left_sub_island-1

      
      return self.island1way(ori_puzzle, i, j)
    else: 
      return ori_puzzle

  

  def only1WayOut (self):
    '''detect if islands and river which can only extend one direction '''
    linePuzzle = copy.deepcopy(self.tiles) #use this syntax can clone datas to a new list, not just copy reference
   
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        cnt = 0
        who = 0
        if self.tiles[i][j].val in ISLAND and self.tiles[i][j].val is not '1' or self.tiles[i][j].val is SUB_ISLAND:
          print "tiles[%d][%d]= %s, %d" % (i,j,self.tiles[i][j].val, self.tiles[i][j].left_sub_island)
          if i > 0            and self.tiles[i-1][j].val == BLANK:
            cnt+= 1
            who = 0
          if i < BOARD_SIZE-1 and self.tiles[i+1][j].val == BLANK:
            cnt+= 1
            who = 1
          if j > 0            and self.tiles[i][j-1].val == BLANK:
            cnt+= 1
            who = 2
          if j < BOARD_SIZE-1 and self.tiles[i][j+1].val == BLANK:
            cnt+= 1
            who = 3          
          if cnt==1:
            if who ==0:
              if self.is_island_finish(i,j):
                linePuzzle[i-1][j].val = RIVER
              else:
                self.tiles[i][j].sub_islands = (i-1,j) 
                linePuzzle[i-1][j].val = SUB_ISLAND
                linePuzzle[i-1][j].left_sub_island = self.tiles[i][j].left_sub_island-1
            elif who ==1:
              if self.is_island_finish(i,j):
                linePuzzle[i+1][j].val = RIVER
              else:
                self.tiles[i][j].sub_islands = (i+1,j) 
                linePuzzle[i+1][j].val = SUB_ISLAND
                linePuzzle[i+1][j].left_sub_island = self.tiles[i][j].left_sub_island-1
            elif who ==2:
              if self.is_island_finish(i,j):
                linePuzzle[i][j-1].val = RIVER
              else:
                self.tiles[i][j].sub_islands = (i,j-1) 
                linePuzzle[i][j-1].val = SUB_ISLAND
                linePuzzle[i][j-1].left_sub_island = self.tiles[i][j].left_sub_island-1
            elif who ==3:
              if self.is_island_finish(i,j):
                print "finish"
                linePuzzle[i][j+1].val = RIVER
              else:
                self.tiles[i][j].sub_islands = (i,j+1) 
                linePuzzle[i][j+1].val = SUB_ISLAND
                linePuzzle[i][j+1].left_sub_island = self.tiles[i][j].left_sub_island-1
        elif self.tiles[i][j].val == RIVER:
         
          if i > 0 and self.tiles[i-1][j].val ==BLANK:
            cnt+= 1
            who = 0
          if i < BOARD_SIZE-1 and self.tiles[i+1][j].val == BLANK:
            cnt+= 1
            who = 1
          if j > 0 and self.tiles[i][j-1].val == BLANK:
            cnt+= 1
            who = 2
          if j < BOARD_SIZE-1 and self.tiles[i][j+1].val == BLANK:
            cnt+= 1
            who = 3          
          if cnt==1:
            if who ==0:
              linePuzzle[i-1][j].val = RIVER
            elif who ==1:
              linePuzzle[i+1][j].val = RIVER
            elif who ==2:
              linePuzzle[i][j-1].val = RIVER
            elif who ==3:
              linePuzzle[i][j+1].val = RIVER
          
        
    
    
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        print self.tiles[i][j].val,
      print ''
    print '~ ~ ~ ~ ~ ~ ~'
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        print linePuzzle[i][j].val,
      print '' 
    print '~ ~ ~ ~ ~ ~ ~'
      
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if linePuzzle[i][j].val != self.tiles[i][j].val:#if two list are not equal 
          #raw_input("ready to Recursive")
          for i in xrange(0, BOARD_SIZE):
            for j in xrange(0, BOARD_SIZE):  #pygame.Surface doesn't like deepcopy, thus, i only assign value one by one...
              self.tiles[i][j].val = linePuzzle[i][j].val
              self.tiles[i][j].left_sub_island = linePuzzle[i][j].left_sub_island
          return self.only1WayOut()
    #two list are equal. it means can do no more 
    return self.tiles

def isInTheBoard (i,j):
  if i < 0 or i >= BOARD_SIZE or j < 0 or j>= BOARD_SIZE:
    return False
  return True
def main():
  newGame = PyGameBoard('puzzle.txt')
  newGame.result()
if __name__ == '__main__':
  main()
