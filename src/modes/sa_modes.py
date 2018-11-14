#!/usr/bin/env python

#----------------------------------------------------------------
#----------------------------------------------------------------
#Copyright 2017 University of Oregon
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#----------------------------------------------------------------
#----------------------------------------------------------------
#Significantly modified by T.Y. 2017/10/10
#----------------------------------------------------------------
#----------------------------------------------------------------

from util.util import *
import random
import math
import sys
import itertools


def get_random_coord(all_list_list):
	random_coord = []
	for all_list in all_list_list:
		random_coord.append(random.randint(0, len(all_list)-1))
	return random_coord


def get_random_neighbor(all_list_list, coord, distance):
	#Return a random neighboring coordinate, that is different from the given coordinate.
	#If no neighboring coordinate is found (after many attempts), return the given coordinate.
	neigh_coord = None
	total_trials = 1000
	for trial in range(total_trials):
		n_coord = coord[:]
		for i in range(len(all_list_list)):
			ipoint = coord[i] + random.randint(-distance, distance)
			if 0 <= ipoint < len(all_list_list[i]):
				n_coord[i] = ipoint
		if n_coord != coord:
			return n_coord
	return neigh_coord


def init_temperature(info):
	#Provide an estimation of the initial temperature by taking the average of the performance-cost differences among randomly chosen coordinates

	#randomly pick several random coordinates with their performance costs
	max_random_coords = 10
	result_dict = {}
	for i in range(max_random_coords):
		coord = get_random_coord(info['all_list_list'])
		print('random_coord: '+str(coord))
		perf_cost = get_perf_cost(info, coord)
		result_dict[str(coord)] = perf_cost
		print('random_coord_perf_cost: '+str(perf_cost))

	#compute the average performance-cost difference
	min_cost = min(result_dict.values())
	sum_diff = 0.0
	for key, value in result_dict.iteritems():
		sum_diff += value - min_cost
	avg_diff = sum_diff / float(len(result_dict))
	if avg_diff == 0.0:
		print('error: diff is 0')
		sys.exit()

	#select an initial temperature value that results in a 80% acceptance probability
	#the acceptance probability formula: p = e^(-delta/temperature)
	#hence, temperature = -delta/ln(p)
	#where the delta is the average performance-cost difference relative to the minimum cost
	init_temp = -avg_diff / math.log(0.8, math.e)

	print('init_temperature() debug info')
	print('result_dict: '+str(result_dict))
	print('min_cost: '+str(min_cost))
	print('avg_diff: '+str(avg_diff))
	print('init_temp: '+str(init_temp))

	#return the initial temperature
	return init_temp


def search_best_neighbor(info, coord, perf_cost, distance):
	all_neighbor=[]
	for i in range(len(coord)):
		all_neighbor_1dim = []
		for j in range(-distance, distance+1,1): #e.g.[-2,-1,0,1,2]
			if 0 <= coord[i]+j < len(info['all_list_list'][i]):
				all_neighbor_1dim.append(coord[i]+j)
		all_neighbor.append(all_neighbor_1dim)
	print('all_neighbor coord: ' +str(all_neighbor))

	all_product = list(itertools.product(*all_neighbor))
	print('all_product coord: ' +str(all_product))

	best_coord = coord
	best_perf_cost = perf_cost
	print('old_best_perf_cost: ' +str(best_perf_cost))
	for para in all_product:
		perf_cost = get_perf_cost(info, para)
		print('perf_cost: ' +str(perf_cost))
		if perf_cost < best_perf_cost:
			best_coord = para
			best_perf_cost = perf_cost
	print('new_best_perf_cost: ' +str(best_perf_cost))

	#recursively apply this local search, if new best neighboring coordinate is found
	if best_coord != coord:
		return search_best_neighbor(info, best_coord, best_perf_cost, distance)

	return (best_coord, best_perf_cost)


def orio_sa_mode(info):
	#hybrid argorithm: orio sa.py and hand coding

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

        local_distance=0
        neigbor_distance=1
        cooling_factor=0.95
        final_temp_ratio=0.005


	#init temp
	#init_temp = init_temperature(info)
	init_temp = 0.1
	final_temp = float(final_temp_ratio) * init_temp
	print('init_temp: '+str(init_temp))
	print('final_temp: '+str(final_temp))


	#init coord
	#coord = get_random_coord(info['all_list_list'])

	coord = init_coord
	perf_cost = get_perf_cost(info, coord)
	best_coord = coord
	best_perf_cost = perf_cost
	print('init_coord: ' +str(coord))
	print('init_coord perf_cost: ' +str(perf_cost))

	#the sa loop
	print('[patt progress] sa loop start')
	temp = init_temp
	while temp > final_temp:
		#the trial loop (i.e. the Metropolis Monte Carlo simulation loop)
		max_trial = 1
		for trial in range(max_trial):
			#get a new coordinate (i.e. a random neighbor)
			new_coord = get_random_neighbor(info['all_list_list'], coord, neigbor_distance)
			#get the performance cost of the new coordinate
			new_perf_cost = get_perf_cost(info, new_coord)
			print('new_coord: ' +str(new_coord))
			print('new_perf_cost: ' +str(new_perf_cost))

			#compare to the best result so far
			if new_perf_cost < best_perf_cost:
				best_coord = new_coord
				best_perf_cost = new_perf_cost
				print('update the best')
				print('best_coord: ' +str(best_coord))
				print('best_perf_cost: ' +str(best_perf_cost))

			#calculate the performance cost difference
			delta = new_perf_cost - perf_cost

			if delta < 0:
				print('better')
				#if the new coordinate has a better performance cost
				#100% move
				coord = new_coord
				perf_cost = new_perf_cost
			else:
				print('worse')
				#n% move
				#compute the acceptance probability (i.e. the Boltzmann probability or the Metropolis criterion) to see whether a move to the new coordinate is needed
				#the acceptance probability formula: p = e^(-delta/temperature)

				#count the probability of moving to the new coordinate
				#delta = 13124314.0 #huge number, hill climbing
				#delta = 10000.0 #adjustment
				p = math.exp(-delta / temp)
				#print('random test: ' +str(random.uniform(0,1)))
				print('probability: ' +str(p))
				if random.uniform(0,1) < p:
					coord = new_coord
					perf_cost = new_perf_cost
					print('worse move')
				else:
					print('not worse move')

		#reduce the temperature (i.e. the cooling/sa schedule)
		temp *= float(cooling_factor)
		print('update temp: '+str(temp))

	print('sa loop end')

	#perform a local search on the best sa coordinate
	local_best_coord, local_best_perf_cost = search_best_neighbor(info, best_coord, best_perf_cost, local_distance)
	#if the neighboring coordinate has a better performance cost
	if local_best_perf_cost < best_perf_cost:
		print('update best(search_best_neighbor)')
		print('best_coord: ' +str(best_coord))
		print('best_perf_cost: ' +str(best_perf_cost))
		print('local_best_coord: ' +str(local_best_coord))
		print('local_best_perf_cost: ' +str(local_best_perf_cost))
		best_coord = local_best_coord
		best_perf_cost = local_best_perf_cost
	else:
		print('no update best(search_best_neighbor)')

	print('final_meas_num: '+ str(info['meas_num']))
	print('final_skip_num: '+ str(info['skip_num']))
	print('final_best_coord: ' +str(best_coord))
	print('final_best_perf_cost: ' +str(best_perf_cost))
	fastest_para = []
	for i in range(len(best_coord)):
		fastest_para.append(info['all_list_list'][i][best_coord[i]])
	print('final_best_para: ' +str(fastest_para))
	build('--polly-tile-sizes=' + ','.join(map(str, fastest_para)))

