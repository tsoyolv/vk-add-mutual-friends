outFileLimit = 100
inFileLimit = 100
endFile = False

inFileCnt = 0
outFileCnt = 0

print('1')
while not endFile :
	friendsDict = []
	print('2')
	with open('friendsss.txt') as ff:
		print('3')
        line = ff.readline()
		inFileCnt += 1
		#if not line :
		#	endFile = True
		#	break
		if inFileCnt > inFileLimit :
			break
		
		
		


print('END!!!!!!!')				
input('Please enter to exit.')