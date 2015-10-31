import sys
import random
import copy
#from multiprocessing import Process


BOARD_SIZE = 5
numPuzzles = 5
puzzleSize = BOARD_SIZE**2
RIVER = '0' 
BLANK = '-'
ISLAND= "123456789ABCDE"
SUB_ISLAND = '+'
dic = {'A':10,'B':11,'C':12,'D':13,'E':14}
CNT=0

class Grid():
  def __init__(self, val):
    self.val = val
    self.subisland_list =list()
    self.left_sub_island = 0
    if val in ISLAND:
      '''if the grid is an island, 
      set the number which how many sub_island don't be placed yet'''
      self.left_sub_island = int(val)-1
      

class Nurikabe():
  """Represents the game's frontend using pygame"""
  def __init__(self, puzzleFile):
    #pygame.init()
    self._puzzleFile = puzzleFile
    self._startNewGame()
    
  
  def _startNewGame(self):
    self.cnt =0
    self._linePuzzle = self._loadPuzzle(self._puzzleFile)
    #print 'max_island_num=',self.max_island_num, 'island_num=', self.island_num
    self._gridValues = self.lineToGrid(self._linePuzzle)
    self.grids = self._createGrid()
    display(self.grids)
    self.solve()
    #board = Process(target=PyGameBoard, args=(self, (700,500), gridValues))
    #board.start()
    #board.join(1)
    #board.setValues(gridValues) 
  def _loadPuzzle(self, fileName):
    """Read in a random puzzle from the puzzle file"""
    ret = []
    
    seekTo = (random.randint(0, numPuzzles)*(puzzleSize+1))
    seekTo = 52
    print "Puzzle No.",seekTo/(puzzleSize+1)+1
    try:
      file = open(fileName, 'r')
    except IOError as e:
      print str(e)
      sys.exit(1)
    file.seek(seekTo)
    linePuzzle = file.readline().strip()
    #print len(linePuzzle)
    file.close()
    self.island_num = 0     #how many grods have been tagged as island or sub island
    self.max_island_num = 0 #how many grids should be island or sub island
    for i in linePuzzle:
      if i in ISLAND:
        self.max_island_num += int(i)
        self.island_num+=1
    #print ret
    return linePuzzle
  
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


  """Represents the game's backend and logic"""

  def checkSolution(self,b,n):
    x= y= -1
    tag = list()
    for i in range(0,BOARD_SIZE):
      row = list()
      for j in range(0,BOARD_SIZE):  
        row.append(0)
      tag.append(row)

    for i in xrange(0, BOARD_SIZE-1):
      for j in xrange(0, BOARD_SIZE-1):
        if b[i][j].val == RIVER:
          x,y = i,j
          break
    qq =self.checkCont(tag,b,x,y)
          
    if  BOARD_SIZE**2- self.max_island_num != qq or n != self.max_island_num:
      return False
    

    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if b[i][j].val in ISLAND and b[i][j].val is not '1':
          #tag[i][j] =1
          #a = self.checkIslandCont(tag,b,i,j+1)
          a = [self.checkIslandCont(tag,b,i-1,j),self.checkIslandCont(tag,b,i+1,j),self.checkIslandCont(tag,b,i,j+1),self.checkIslandCont(tag,b,i,j-1)]
          aa =1+sum(a)
          
          #raw_input()
          if int(b[i][j].val) is not aa:
            #tag[i][j] =0
            return False
          #print b[i][j].val,a
    #display(b)
    return True
    
  def checkIslandCont(self,tag,b,i,j):
    #print 'i,j=%d,%d'%(i,j),b[i][j].val,
    if i<0 or i>=BOARD_SIZE or j<0 or j>= BOARD_SIZE:
      return 0
    if tag[i][j] is 1 or b[i][j].val is not SUB_ISLAND:
      tag[i][j]=0
      return 0
    else:
      tag[i][j]=1
      a = self.checkIslandCont(tag,b,i-1,j)+self.checkIslandCont(tag,b,i+1,j)+ self.checkIslandCont(tag,b,i,j+1)+self.checkIslandCont(tag,b,i,j-1)
      #print 'sum=',a
      return 1+a
  def checkCont(self, tag,b,i,j):
    if i<0 or i>=BOARD_SIZE or j<0 or j>= BOARD_SIZE or tag[i][j]is 1 or b[i][j].val is not RIVER:
      return 0
    else:
      tag[i][j]=1
      return 1+self.checkCont(tag,b,i-1,j)+self.checkCont(tag,b,i+1,j)+ self.checkCont(tag,b,i,j+1)+self.checkCont(tag,b,i,j-1)
      

  def check2x2(self,grids):
    for i in xrange(0, BOARD_SIZE-1):
      for j in xrange(0, BOARD_SIZE-1):
        if grids[i][j].val is RIVER :
          if grids[i+1][j].val is RIVER and grids[i][j+1].val is RIVER and grids[i+1][j+1].val is RIVER:
            return False
          
    
    return True
  def solve(self):
    self.grids = self.slove_step1(self.grids)
    self.grids = self.neverTouch()
    self.only1WayOut()

    #print self.max_island_num, self.island_num
    if self.DFS(self.grids,self.island_num):
      return
      #for x in self.grids:
      #  print x
      #print self.max_island_num, self.island_num
    else:
      print "can not solve"
    #self.checkSolution()

  def slove_step1(self, grids):
    '''use the simplest method to detect which grid shoud be river'''
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if grids[i][j].val == '1': 
          '''first black the blank arround the no.1 island'''
          #print i,j
          if i>0: #up
            grids[i-1][j].val = RIVER
          if i < BOARD_SIZE-1: #down
            grids[i+1][j].val = RIVER
          if j > 0: #left
            grids[i][j-1].val = RIVER         
          if j < BOARD_SIZE-1: #right
            grids[i][j+1].val = RIVER
        elif grids[i][j].val == BLANK :
          '''dectect each blank whether connect multi island'''
          cnt=0
          if i > 0 and grids[i-1][j].val != RIVER and grids[i-1][j].val !=BLANK:
            cnt+=1
          if i < BOARD_SIZE-1 and grids[i+1][j].val != RIVER and grids[i+1][j].val != BLANK:
            cnt+=1
          if j > 0 and grids[i][j-1].val != RIVER and grids[i][j-1].val != BLANK:
            cnt+=1
          if j < BOARD_SIZE-1 and  grids[i][j+1].val != RIVER and  grids[i][j+1].val != BLANK:
            cnt+=1
          
          if cnt>1:
            grids[i][j].val = RIVER
    return grids

  def neverTouch(self):
    '''detect some blank will never be subisland_list ,so it must be a RIVER
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
        if self.grids[i][j].val in ISLAND:
          #print i, j
          value = int(self.grids[i][j].val)
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
          self.grids[i][j].val = RIVER

    return self.grids

  def is_island_finish(self, i, j):
    '''detect if a island has been completely extended'''
    if self.grids[i][j].left_sub_island == 0:
      return True
    else: return False

  def island1way(self, i, j):
    '''Recursivly extend island if it have only 1 direction can extend,
       and stop if have extended same quantity of sub_island with island number'''
    cnt = 0
    who = 0
    if i > 0            and self.grids[i-1][j].val == BLANK:
      cnt+= 1
      who = 0
    if i < BOARD_SIZE-1 and self.grids[i+1][j].val == BLANK:
      cnt+= 1
      who = 1
    if j > 0            and self.grids[i][j-1].val == BLANK:
      cnt+= 1
      who = 2
    if j < BOARD_SIZE-1 and self.grids[i][j+1].val == BLANK:
      cnt+= 1
      who = 3          
    if cnt==1:
      if self.is_island_finish(i,j):
        if who ==0:
            self.grids[i-1][j].val = RIVER
        elif who ==1:
            self.grids[i+1][j].val = RIVER
        elif who ==2:
            self.grids[i][j-1].val = RIVER
        elif who ==3:
            self.grids[i][j+1].val = RIVER
        return self.grids
      else:
        if who ==0:

          self.grids[i][j].subisland_list.append((i-1,j))
          self.grids[i-1][j].val = SUB_ISLAND
          self.grids[i-1][j].left_sub_island = self.grids[i][j].left_sub_island-1
          self.island1way(i-1,j)
        elif who ==1:
          self.grids[i][j].subisland_list.append((i+1,j))
          self.grids[i+1][j].val = SUB_ISLAND
          self.grids[i+1][j].left_sub_island = self.grids[i][j].left_sub_island-1
          self.island1way(i+1,j)
          
      
        elif who ==2:
          self.grids[i][j].subisland_list.append((i,j-1))
          self.grids[i][j-1].val = SUB_ISLAND
          self.grids[i][j-1].left_sub_island = self.grids[i][j].left_sub_island-1
          self.island1way(i,j-1)
        elif who ==3:
          self.grids[i][j].subisland_list.append((i,j+1))
          self.grids[i][j+1].val = SUB_ISLAND
          self.grids[i][j+1].left_sub_island = self.grids[i][j].left_sub_island-1
          self.island1way(i,j+1)
        self.grids[i][j].left_sub_island-=1
        self.island_num+=1
        if self.grids[i][j].val is '2':
          x,y = self.grids[i][j].subisland_list.pop()
          if x > 0            and self.grids[x-1][y].val == BLANK:
            self.grids[x-1][y].val = RIVER
          if x < BOARD_SIZE-1 and self.grids[x+1][y].val == BLANK:
            self.grids[x+1][y].val = RIVER
          if y > 0            and self.grids[x][y-1].val == BLANK:
            self.grids[x][y-1].val = RIVER
          if y < BOARD_SIZE-1 and self.grids[x][y+1].val == BLANK:
            self.grids[x][y+1].val = RIVER
          self.grids[i][j].subisland_list.append((x,y))
      
    #else: 
      #return self.grids

  

  def only1WayOut (self):
    '''detect if islands and river which can only extend one direction '''
    linePuzzle = copy.deepcopy(self.grids) #use this syntax can clone datas to a new list, not just copy reference
    
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if self.grids[i][j].val in ISLAND and self.grids[i][j].val is not '1':
          self.island1way(i,j)
          #print self.grids[i][j].subisland_list
    
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if self.grids[i][j].val == RIVER:
          cnt=0
          who=0
          if i > 0 and self.grids[i-1][j].val ==BLANK:
            cnt+= 1
            who = 0
          if i < BOARD_SIZE-1 and self.grids[i+1][j].val == BLANK:
            cnt+= 1
            who = 1
          if j > 0 and self.grids[i][j-1].val == BLANK:
            cnt+= 1
            who = 2
          if j < BOARD_SIZE-1 and self.grids[i][j+1].val == BLANK:
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
    


  def DFS(self,boards,num):
    '''comput all possible extending of islands and try and error'''
    #print 'num=',num
    self.cnt+=1
    tmp_b, tmp_n = self.extendAll(boards,num)
    if len(tmp_n) is 0:#leaf node
      print self.cnt
      #print 'leaf node:'
      #display(boards)
      if self.checkSolution(boards,num):
        print num
        self.grids = copy.deepcopy(boards)
        self.island_num = num
        #print "Find answer"
        return True #boards[0], num[0]
      else:
        #print 'error answer'
        return False
    else:#not leaf node
      for b,n in zip(tmp_b,tmp_n):
        #print "next recursive len=",len(tmp_n)
        if self.DFS(b,n):
            return True
         
  def extendAll(self,b,n):
    tmp_b = list()
    tmp_n = list()
    for i in xrange(0, BOARD_SIZE):
      for j in xrange(0, BOARD_SIZE):
        if b[i][j].val is BLANK:
          b[i][j].val = RIVER
          if self.check2x2(b):
            tmp_b.append(copy.deepcopy(b))
            tmp_n.append(copy.deepcopy(n))
          
          b[i][j].val = SUB_ISLAND
          tmp_b.append(copy.deepcopy(b))
          tmp_n.append(copy.deepcopy(n+1))

          #b[i][j].val = BLANK
    return tmp_b, tmp_n
            
          
    

def display(grids):
  for i in xrange(0,BOARD_SIZE):
    for j in xrange(0,BOARD_SIZE):
      print grids[i][j].val,
    print ''
  print '=========='
def isInTheBoard (i,j):
  if i < 0 or i >= BOARD_SIZE or j < 0 or j>= BOARD_SIZE:
    return False
  return True
def main():
  newGame = Nurikabe('puzzle'+str(BOARD_SIZE)+'.txt')
  newGame.result()
if __name__ == '__main__':
  main()
