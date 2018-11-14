#!/usr/bin/env python

# /******************************************************************
# PATT: Polyhedral compilation-based AuTo Tile size optimizer
#
# Copyright (C)   2017-2018,   Yukinori Sato
# All Rights Reserved. 
# University of Illinois/NCSA Open Source License
# ******************************************************************/


import sys
import math
from util.util import *



def ComputeTileFactor(cSize, lSize, n, M, N, W, sizeDataType):
	CLS = lSize/sizeDataType
	nSets = cSize/(lSize*n)
	w = N/CLS
	r = 0

	print 'ComputeTileFactor  %d %d %d %d' % (nSets, w, CLS, W)


	fillCache = [0.0] * nSets
	for r in range(0, M):
		for c in range(0, w):
			s = (r*w+c)%nSets
			#print s, r, c
			if fillCache[s] == W:
				return r
			else:
				fillCache[s]+=1
	return M


def TurboTileSelection(cSizeL2, cSizeLLC, nL2, nLLC, lSize, M, N, P, s1, s2, r, sizeDataType, ne, W):
	print r,W,cSizeLLC,nLLC,sizeDataType
	cond_right = (2*r*W*cSizeLLC / (nLLC*sizeDataType))
	print 'cond_right = %d' % cond_right
	if M*N > cond_right:
		I = ComputeTileFactor(cSizeLLC, lSize, nLLC, M, N, W, sizeDataType)
		print 'I = %d' % I 
		if I < 4:
			#tss()
			print('I == ' + str(I))
			print('Require implementation of TSS')
			exit()
		else:
			granularity = M/(I*r)
			g=float(M)/(I*r)
			print '(granularity, g) = %d %f ' % (granularity, g)
			if granularity < g:
				if granularity==0:
					print 'Error: granularity becomes zero'
					exit(1)
				print (float(M)/granularity), math.floor(M/granularity)
				while (float(M)/granularity) != math.floor(M/granularity):
					granularity+=1
					print 'inc granularity = %d ' % (granularity)

				I = M/(granularity*r)
				print 'adjusted to (granularity, I) = %d %d ' % (granularity, I)

			K = ComputeTileFactor(cSizeL2, lSize, nL2, P, N, ne, sizeDataType)
			print 'K = %d' % K 
	else:
		print 'M*N is smaller than condition; %d %f' % (M*N, cond_right)
		I = 4
		#K = P
		K = ComputeTileFactor(cSizeL2, lSize, nL2, P, N, ne, sizeDataType)
		print 'K = %d' % K 

	print ('Ended successfully(TTS)')
	return (I, K, N)


def turbo_tiling_mode(info):
	cSizeL2 = int(info['cSizeL2'])
	cSizeLLC = int(info['cSizeLLC'])
	nL2 = int(info['nL2'])
	nLLC = int(info['nLLC'])
	lSize = int(info['lSize'])
	M = int(info['M'])
	N = int(info['N'])
	P = int(info['P'])
	s1 = int(info['s1'])
	s2 = int(info['s2'])
	r = int(info['r'])
	sizeDataType = int(info['sizeDataType'])

	#calculation
	ne = math.floor(float(nL2)/s1-1)
	W = math.floor(float(nLLC)/(r*s2))-1
	d=0

	while ne==0:
	  d+=2
	  ne = math.floor(float(nL2)*d/s1-1)
	  cSizeL2=cSizeL2/d
	  print 'd is multiplied to ne, %d . cSizeL2 = %d ' % (ne, cSizeL2)

	while W==0:
	  d+=2
	  W = math.floor(float(nLLC)*d/(r*s2))-1
	  cSizeLLC=cSizeLLC/d
	  print 'd is multiplied to W, %d . cSizeLLC = %d ' % (W, cSizeLLC)

	print '(cSizeL2, cSizeLLC, nL2, nLLC, lSize, M, N, P, s1, s2, r, sizeDataType)'
	print '(%d %d %d %d %d %d %d %d %d %d %d %d)' % (cSizeL2, cSizeLLC, nL2, nLLC, lSize, M, N, P, s1, s2, r, sizeDataType)
	print '(ne, W) = %d %d' %(ne, W)

	I, K, N = TurboTileSelection(cSizeL2, cSizeLLC, nL2, nLLC, lSize, M, N, P, s1, s2, r, sizeDataType, ne, W)

	IKN_s = str(I) + ',' + str(K) + ',' + str(N)
	#IKN_s = str(int(I)) + ',' + str(int(K)) + ',' + str(int(N))
	print('real I,K,N == '+IKN_s)

	I = I if I > 0 else 1
	K = K if K > 0 else 1
	N = N if N > 0 else 1
	IKN_s = str(I) + ', ' + str(K) + ', ' + str(N)
	INK = str(I) + ', ' + str(N) + ', ' + str(K) 
	print('adjusted I,K,N == '+IKN_s)
	print('tiling size == '+INK)

	prebuild(info['c_source_list'], info['cc_options'], info['kernel_file'])
	build('-debug --polly-tile-sizes=' + str(I)+','+str(N)+','+str(K))
	make_measure_script(int(info['threads']))
	this_time = measure(info, info['remote'], int(info['repetition']), info['huge_num'])
        print("final_best_perf_cost: " + str(this_time))
        print("final_best_para: " + INK)

        '''
	IKN_ic = str(I) + ', ' + str(N) + ', ' + str(K)
	print('interchanged I,K,N == '+IKN_ic)

	build('-debug --polly-tile-sizes=' + str(I)+','+str(N)+','+str(K))
	this_time2 = measure(info, info['remote'], int(info['repetition']), info['huge_num'])

        if this_time < this_time2 :
                print("final_best_perf_cost: " + str(this_time))
                print("final_best_para: " + IKN_s)
        else:
                print("final_best_perf_cost: " + str(this_time2))
                print("final_best_para: " + IKN_ic)
        '''


