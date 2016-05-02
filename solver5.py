#! venv/bin/python

from copy import deepcopy
import sys
sys.setrecursionlimit(50000)

def makeBlock(pos1,orientation):
	pos1				= list(pos1)
	(i,j,k,l)			= orientation
	
	pos2				= deepcopy(pos1)
	pos3				= deepcopy(pos2)
	pos4				= deepcopy(pos3)
	
	pos2[i]				= pos3[i] + j
	pos3[i]				= pos2[i] + j
	pos4[i]				= pos3[i] + j
	
	pos5				= deepcopy(pos3)
	pos5[(k+i)%2]		= pos3[(k+i)%2] + l
	return frozenset({tuple(pos1),tuple(pos2),tuple(pos3),tuple(pos4),tuple(pos5)})

axis			= [0,1,2]
directions		= [-1,1]
orientations	= [[i,j,k,l] for i in axis for j in directions for k in directions for l in directions]
cubies			= [(x,y,z) for x in range(5) for y in range(5) for z in range(5)]
blocks			= []

for i,j,k,l in orientations:
	legalInd				= [[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4]]
	legalInd[i]				= ([0,1,2,3,4],[0,1],[3,4])[j]
	legalInd[(i+k)%2]		= ([0,1,2,3,4],[0,1,2,3],[1,2,3,4])[l]
	
	legalCubies				= [(x,y,z) for x in legalInd[0] for y in legalInd[1] for z in legalInd[2]]
	for legalCubie in legalCubies:
		blocks.append(makeBlock(legalCubie,[i,j,k,l]))
	
overlaps					= {}
for block in blocks:
	overlaps[block]			= [block2 for block2 in blocks if not block.isdisjoint(block2)]

solution = []

def addNext(solution,blocks,overlaps):
	block					= blocks[0]
#	print 'Block: ', block
	solution.append(block)
#	print 'Overlaps: ', overlaps[block]
	for overlapped in overlaps[block]:
		try:		blocks.remove(overlapped)
		except:		pass
	return (solution,blocks,overlaps)
		
def solve(solution,blocks,overlaps):
	if len(blocks) == 0:
		if len(solution) == 25:
			print solution
	else:
		block				= blocks[0]
		print block
		solution.append(block)
		for overlapped in overlaps[block]:
			try:		blocks.remove(overlapped)
			except:		pass
		solve(solution,blocks[1:],overlaps)
		solution.remove(block)
		solve(solution,blocks[1:],overlaps)

#solve(solution,blocks,overlaps)

########################################################################
elements = 10
array = []

def function(elements,array):
	if len(array) == elements:
		print array
	else:
		for i in range(0,elements):
			free = 1
			for entries in array:
				if i == entries:
					free = 0
					break
			if free == 1:
				array.append(i)
				function(elements,array)
				del array[-1]

#function(elements,array)

########################################################################
def solve(solution,blocks,overlaps):
	if len(blocks) == 0:
		print solution
	for block in blocks:
		
		solution.append(block)
		for overlapped in overlaps[block]:
			try:		blocks.remove(overlapped)
			except:		pass
		solve(solution,blocks,overlaps)
		solution.remove(block)
		

#solve(solution,blocks,overlaps)

########################################################################

solution1 	= 	[]
blocks1 		=	[frozenset([(0,0,0),(0,1,0)]),
				frozenset([(1,0,0),(1,1,0)]),
				frozenset([(0,0,1),(0,1,1)]),
				frozenset([(1,0,1),(1,1,1)]),
				frozenset([(0,0,0),(1,0,0)]),
				frozenset([(0,1,0),(1,1,0)]),
				frozenset([(0,0,1),(1,0,1)]),
				frozenset([(0,1,1),(1,1,1)]),
				frozenset([(0,0,0),(0,0,1)]),
				frozenset([(0,1,0),(0,1,1)]),
				frozenset([(1,0,0),(1,0,1)]),
				frozenset([(1,1,0),(1,1,1)])]
overlaps1	=	{block: [block2 for block2 in blocks1 if not block.isdisjoint(block2)] for block in blocks1}



def addNext(solution,blocks,overlaps):
	block = blocks[0]
	solution.append(block)
	for overlapped in overlaps[block]:
		try:	blocks.remove(overlapped)
		except:	pass
	return solution,blocks,overlaps

def solve(solution,blocks,overlaps):
	if blocks != []:
		yesblocks		= [block for block in blocks if block not in overlaps[blocks[0]]]
		yessolution		= solution + [blocks[0]]
		solve(yessolution,yesblocks,overlaps)
		noblocks		= [block for block in blocks if block != blocks[0]]
		nosolution		= solution
		solve(nosolution,noblocks,overlaps)
	else:
		if len(solution) >= 19:
			print len(solution),
		if len(solution) >= 24:
			with open('greater24.txt','a') as f:
				f.write(str(len(solution)) + '\n')
				for block in solution:
					f.write(str(block))
		
def main():
	solve(solution,blocks,overlaps)

if __name__ == '__main__':
	main()
