
def isInTheBoard (i,j):
  if i < 0 or i >= BOARD_SIZE or j < 0 or j>= BOARD_SIZE:
    return False
  return True

BOARD_SIZE=5
i=j=2
value = 3
tmpBoard =[]
for x in xrange(0,BOARD_SIZE):
  raw = []
  for y in xrange(0,BOARD_SIZE):
    raw.append(0)
  tmpBoard.append(raw)


for x in xrange(1,value+1): #upper part
  skip = abs(x-value)
  
  for y in xrange(0, x*2-1):
    if isInTheBoard(i-(value-x), j-(value-1)+skip+y):
      tmpBoard[i-(value-x)][j-(value-1)+skip+y]+=1

loop = range((value)*2-1, 0, -2)
print loop
for x in xrange(value+1,value*2): #lower part
  skip = abs(x-value)
  print x, skip

  for y in xrange(0,loop[skip]):
    if isInTheBoard(i-(value-x), j-(value-1)+skip+y):
      tmpBoard[i-(value-x)][j-(value-1)+skip+y]+=1


for i in xrange(0, BOARD_SIZE):
  print tmpBoard[i]
 