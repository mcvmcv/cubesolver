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
	
overlaps			= {block: [block2 for block2 in blocks if not block.isdisjoint(block2)] for block in blocks}

def solve(attempttuples,overlaps):
#	print attempttuples
	nextsolutions	= []
	for solution,potentials in attempttuples:
		print len(solution),
		if len(solution) == 24:
			print solution
		if len(solution) + len(potentials) >= 24:
			nextsolutions.append((solution + [potentials[0]],[p for p in potentials if p not in overlaps[potentials[0]]]))
#			print 'I: ', nextsolutions[-1]
			nextsolutions.append((solution,[p for p in potentials if p != potentials[0]]))
#			print 'E: ', nextsolutions[-1]
#		print nextsolutions[-1][0]
	solve(nextsolutions,overlaps)
	
	
if __name__ == '__main__': 
	attempttuples = [([],blocks)]
	solve(attempttuples,overlaps)
