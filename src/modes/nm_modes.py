#!/usr/bin/env python

#----------------------------------------------------------------
#----------------------------------------------------------------
#Copyright 2017 University of Oregon
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#----------------------------------------------------------------
#----------------------------------------------------------------
#Significantly modified by T.Y. 2017/10/25
#----------------------------------------------------------------
#----------------------------------------------------------------
from util.util import *
import sys
import functools

#----------------------------------------------------------------
def init_simplex(init_coord, all_list_list):
	
        #print('[patt progress] init_simplex() start')
	# initialize a right-angled simplex in the search space


        print init_coord, all_list_list


	x0 = init_coord
	dim_uplimits = map(len, all_list_list)
	sim_size = max(dim_uplimits)

	coord = list(x0)
	for i in range(0, len(x0)):
		iuplimit = dim_uplimits[i]
		#if coord[i] >= iuplimit:
		#   coord[i] = iuplimit-1
		#elif coord[i] < 0:
		#   coord[i] = 0
		if coord[i] >= iuplimit or coord[i] < 0:
			print('msimplex: initial point x0 out of bound!')
			sys.exit()

	simplex = [coord]

	for i in range(0, len(x0)):
		coord = list(x0)

		axis = coord[i]
		iuplimit = dim_uplimits[i]
		pos = iuplimit - axis - 1
		neg = axis

		prefer = sim_size-1

		if prefer <= pos:
			coord[i] += prefer
		elif prefer <= neg:
			coord[i] -= prefer
		elif pos >= neg:
			#coord[i] += pos
			coord[i] += 4 #1,2,4 any others
		else:
			#coord[i] -= neg
			coord[i] -= 4 #1,2,4 any others

		#coord[i] += self.sim_size-1
		#iuplimit = self.dim_uplimits[i]
		#if coord[i] >= iuplimit:
		#    coord[i] = iuplimit-1

		simplex.append(coord)

	#Error check for duplicate coords is yet to be implemented
	#if self.__dupCoord(simplex):
		#err('msimplex: simplex created has duplicate!!')

	return simplex

def init_random_simplex():
	print('yet to be implemented')
	sys.exit()

#----------------------------------------------------------------
def get_centroid(coords):
	#Return a centroid coordinate
	total_coords = len(coords)
	centroid = coords[0]
	for c in coords[1:]:
		centroid = add_coords(centroid, c)
	centroid = mul_coords((1.0/total_coords), centroid)
	return centroid

def get_reflection(refl_coefs, coord, centroid):
	#Return a reflection coordinate
	sub_coord = sub_coords(centroid, coord)
	return map(lambda x: add_coords(centroid, mul_coords(x, sub_coord)), refl_coefs)
    
def get_expansion(exp_coefs, coord, centroid):
	#Return an expansion coordinate
	sub_coord = sub_coords(coord, centroid)
	return map(lambda x: add_coords(centroid, mul_coords(x, sub_coord)), exp_coefs)
    
def get_contraction(cont_coefs, coord, centroid):
	#Return a contraction coordinate
	sub_coord = sub_coords(coord, centroid)
	return map(lambda x: add_coords(centroid, mul_coords(x, sub_coord)), cont_coefs)

def get_shrinkage(shri_coef, coord, rest_coords):
	#Return a shrinkage simplex
	return map(lambda x: add_coords(coord, mul_coords(shri_coef, sub_coords(x, coord))), rest_coords)

#----------------------------------------------------------------
def sub_coords(coord1, coord2):
	#coord1 - coord2
	return map(lambda x,y: x-y, coord1, coord2)

def add_coords(coord1, coord2):
	#coord1 + coord2
	return map(lambda x,y: x+y if x+y>=0 else 0, coord1, coord2)

def mul_coords(coef, coord):
	#coef * coord
	return map(lambda x: int(round(1.0*coef*x)), coord)

#----------------------------------------------------------------
def orio_nm_mode(info):
	#print('[patt progress] orio_nm_mode start')

	prebuild(info['c_source_list'], info['cc_options'], info['kernel_file'])
	make_measure_script(int(info['threads']))


	loop_size = info['loop_size'].split(' ')
	loop_size = map(int, loop_size)
        loop_1=range(4,loop_size[0],4)
        loop_2=range(4,loop_size[1],4)
	all_list_list = []
	all_list_list.append(loop_1)
	all_list_list.append(loop_2)
        if len(loop_size)==3:
                loop_3=range(4,loop_size[2],4)
                init_coord=[7,7,7]
                all_list_list.append(loop_3)
        else:
                init_coord=[7,7]
        info['all_list_list']=all_list_list

	dim_num = len(init_coord)


	#default init vars used in orio
	#local_distance = 0

	refl_coefs = [1.0]* dim_num
	exp_coefs = [2.0]* dim_num
	cont_coefs = [0.5]* dim_num
	shri_coef = 0.5

	#x0 = [0] * self.total_dims
	#sim_size = max(self.dim_uplimits)


	# initialize a storage to remember all initial simplexes that have been explored
	simplex_records = {}

	# record the global best coordinate and its performance cost
	best_global_coord = None
	best_global_perf_cost = info['huge_num']

	simplex = None

	# list of the last several moves (used for termination criteria)
	last_simplex_moves = []

	# initialize a simplex in the search space
	if simplex == None:
		simplex = init_simplex(init_coord, all_list_list)
	else:
		#simplex = init_random_simplex(simplex_records)
		print('yet to be implemented')
		sys.exit()

	print('init simplex: '+str(simplex))

	get_perf_cost_fixed = functools.partial(get_perf_cost, info)

	# get the performance cost of each coordinate in the simplex
	perf_costs = map(get_perf_cost_fixed, simplex)
	print('init simplex perf_costs: '+str(perf_costs))

	#----------------main loop start----------------
	simplex_it_num=0
	while True:
		simplex_it_num += 1
		#print('[patt progress] start new simplex loop: ' +str(simplex_it_num))


		# sort the simplex coordinates in an increasing order of performance costs
		sorted_simplex_cost = zip(simplex, perf_costs)
		sorted_simplex_cost.sort(lambda x,y: cmp(x[1],y[1]))
		print('sorted_simplex_cost: '+str(sorted_simplex_cost))

		# unbox the coordinate-cost tuples
		simplex, perf_costs = zip(*sorted_simplex_cost)
		simplex = list(simplex)
		perf_costs = list(perf_costs)

		#I don't know the commens below
		# record time elapsed vs best perf cost found so far in a format that could be read in by matlab/octave
		#progress = 'init' if best_global_coord == None else 'continue'
		#if best_global_coord == None:
			#best_global_coord = 'notNone'
		#result = perf_costs[0] if perf_costs[0] < best_global_perf_cost else best_global_perf_cost
		#best_coord_thus_far = simplex[0] if perf_costs[0] < best_global_perf_cost else best_global_coord
		#IOtime = Globals().stats.record(time.time()-start_time, result, best_coord_thus_far, progress)
		# don't include time on recording data in the tuning time
		#start_time += IOtime

		#The following is not necessary to do
		'''
		# remove bogus values (0 time)
		indicestoremove = []
		for i in range(0,len(perf_costs)):
			if perf_costs[i] > 0.0: continue
			else: indicestoremove.append(i)

		for i in indicestoremove:
			del perf_costs[i]
			del simplex[i]
		'''

		print('simplex: '+str(simplex))

		# termination criteria: a loop is present
		if str(simplex) in last_simplex_moves:
			print('This simplex is looked within last 10 times. NM Main Loop END')
			break

		# record the last several simplex moves (used for the termination criteria)
		last_simplex_moves.append(str(simplex))
		#while len(last_simplex_moves) > 10:
		while len(last_simplex_moves) > 3:
			last_simplex_moves.pop(0)

		# best coordinate
		best_coord = simplex[0]
		best_perf_cost = perf_costs[0]
		print('curren best_coord: '+str(best_coord))
		print('curren best_perf_cost: '+str(best_perf_cost))

		# worst coordinate
		worst_coord = simplex[len(simplex)-1]
		worst_perf_cost = perf_costs[len(perf_costs)-1]

		# 2nd worst coordinate
		second_worst_coord = simplex[len(simplex)-2]
		second_worst_perf_cost = perf_costs[len(perf_costs)-2]

		# calculate centroid
		centroid = get_centroid(simplex[:len(simplex)-1])
		print('centroid: '+str(centroid))

		# reflection
		refl_coords = get_reflection(refl_coefs, worst_coord, centroid)
		print('refl_coords: '+str(refl_coords))
		refl_perf_costs = map(get_perf_cost_fixed, refl_coords)

		refl_perf_cost = min(refl_perf_costs)
		ipos = refl_perf_costs.index(refl_perf_cost)
		refl_coord = refl_coords[ipos]

		# the replacement of the worst coordinate
		next_coord = None
		next_perf_cost = None

		# if cost(best) <= cost(reflection) < cost(2nd_worst)
		if best_perf_cost <= refl_perf_cost < second_worst_perf_cost:
			next_coord = refl_coord
			next_perf_cost = refl_perf_cost
			print('--> reflection to %s' % next_coord )

		# if cost(reflection) < cost(best)
		elif refl_perf_cost < best_perf_cost:

			# expansion
			exp_coords = get_expansion(exp_coefs, refl_coord, centroid)
			print('exp_coords: '+str(exp_coords))
			exp_perf_costs = map(get_perf_cost_fixed, exp_coords)

			exp_perf_cost = min(exp_perf_costs)
			ipos = exp_perf_costs.index(exp_perf_cost)
			exp_coord = exp_coords[ipos]

			# if cost(expansion) < cost(reflection)
			if exp_perf_cost < refl_perf_cost:
				next_coord = exp_coord
				next_perf_cost = exp_perf_cost
				print('--> expansion to %s' % next_coord )
			else:
				next_coord = refl_coord
				next_perf_cost = refl_perf_cost
				print('--> reflection to %s' % next_coord )

		# if cost(reflection) < cost(worst)
		elif refl_perf_cost < worst_perf_cost:
			# outer contraction
			cont_coords = get_contraction(cont_coefs, refl_coord, centroid)
			print('cont_coords: '+str(cont_coords))
			cont_perf_costs = map(get_perf_cost_fixed, cont_coords)

			cont_perf_cost = min(cont_perf_costs)
			ipos = cont_perf_costs.index(cont_perf_cost)
			cont_coord = cont_coords[ipos]

			# if cost(contraction) < cost(reflection)
			if cont_perf_cost < refl_perf_cost:
				next_coord = cont_coord
				next_perf_cost = cont_perf_cost
				print('--> outer contraction to %s' % next_coord )

		# if cost(reflection) >= cost(worst)
		else:
			# inner contraction
			cont_coords = get_contraction(cont_coefs, worst_coord, centroid)
			print('cont_coords: '+str(cont_coords))
			cont_perf_costs = map(get_perf_cost_fixed, cont_coords)

			cont_perf_cost = min(cont_perf_costs)
			ipos = cont_perf_costs.index(cont_perf_cost)
			cont_coord = cont_coords[ipos]

			# if cost(contraction) < cost(worst)
			if cont_perf_cost < worst_perf_cost:
				next_coord = cont_coord
				next_perf_cost = cont_perf_cost
				print('--> inner contraction to %s' % next_coord )

		# if shrinkage is needed
		if next_coord == None and next_perf_cost == None:

			# shrinkage
			simplex = get_shrinkage(shri_coef, best_coord, simplex)
			print('shrinkage_coords: '+str(simplex))
			perf_costs = map(get_perf_cost_fixed, simplex)

			print('--> shrinkage on %s' % best_coord )

		# replace the worst coordinate with the better coordinate
		else:
			simplex.pop()
			perf_costs.pop()
			simplex.append(next_coord)
			perf_costs.append(next_perf_cost)

	#----------------main loop end----------------

	# get the best simplex coordinate and its performance cost
	best_simplex_coord = simplex[0]
	best_simplex_perf_cost = perf_costs[0]

	print('final_meas_num: '+ str(info['meas_num']))
	print('final_skip_num: '+ str(info['skip_num']))
	print('final_best_coord: ' +str(best_simplex_coord))
	print('final_best_perf_cost: ' +str(best_simplex_perf_cost))
	fastest_para = []
	for i in range(len(best_simplex_coord)):
		fastest_para.append(info['all_list_list'][i][best_simplex_coord[i]])
	print('final_best_para: ' +str(fastest_para))
	build('--polly-tile-sizes=' + ','.join(map(str, fastest_para)))

#----------------------------------------------------------------

	#yet to be implemented local search
	#if intend to implement, should be similar to the algorithm using in sa_modes
	#the code below is orio's default local search code
	'''
	old_best_simplex_perf_cost = best_simplex_perf_cost
	# perform a local search on the best simplex coordinate
	(best_simplex_coord,
		best_simplex_perf_cost) = search_best_neighbor(best_simplex_coord,
		self.local_distance)

	best_simplex_perf_cost = best_simplex_perf_cost[0]

	# if the neighboring coordinate has a better performance cost
	if best_simplex_perf_cost < old_best_simplex_perf_cost:
		print('---> better neighbor found: %s, cost: %e' %
			(best_simplex_coord, best_simplex_perf_cost))
	else:
		best_simplex_coord = simplex[0]
		best_simplex_perf_cost = old_best_simplex_perf_cost

	# compare to the global best coordinate and its performance cost
	if best_simplex_perf_cost < best_global_perf_cost:
		best_global_coord = best_simplex_coord
		best_global_perf_cost = best_simplex_perf_cost
		print('>>>> best coordinate found: %s, cost: %e' %
			(best_global_coord, best_global_perf_cost))

	# return the best coordinate
	return best_global_coord, best_global_perf_cost, runs
	'''

#----------------------------------------------------------------


