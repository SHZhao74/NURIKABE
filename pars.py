import random

try:
  infile = open('unparse.txt', 'r')
  outfile = open('puzzle20.txt', 'w')
except IOError as e:
  print str(e)
  sys.exit(1)
s=''
x = 1
size = 20
while x <= size**2:
	d = random.randint(1,7)
	s += str(d)
	r = random.randint(1,25)
	#print x, r
	for y in xrange(0,r) :
		if x+y < size**2:
			s+='-'
		else: break
		#print x+y, s
	x += r+1

print len(s)
outfile.write(s)

print 'Done'
infile.close()
outfile.close()