#!/usr/bin/env python

# /******************************************************************
# PATT: Polyhedral compilation-based AuTo Tile size optimizer
#
# Copyright (C)   2017-2018,   Yukinori Sato
# All Rights Reserved. 
# University of Illinois/NCSA Open Source License
# ******************************************************************/


from util.util import *
import math
import sys
import os

def product_recur(info, patt_util, exp_list, exp_all_list, para, count, pass_flag):
	print('[patt progress] product_recur start')
	pf = pass_flag #True: do pass == don't try
	fastest_time = patt_util['huge_num']
	fastest_para = 0

	exp_list_allnum = 1
	for dim_list in exp_list:
		exp_list_allnum *= len(dim_list)

	for i in exp_list[count]:
		para.append(i)
		this_time = patt_util['huge_num']

		if len(exp_list)-1 == count:
			para2 = copy.deepcopy(para)

			if pf:
				#pass
				this_time = patt_util['pass_num']
			else:
				#try
				print('plain para: '+str(para2))
				para2_aligned = copy.deepcopy(para2)
				for index_num in range(len(para2_aligned)):
					while para2_aligned[index_num] % patt_util['alignment'] != 0:
						para2_aligned[index_num] += 1
				para2_aligned_s = ','.join(map(str, para2_aligned))
				print('aligned para: '+para2_aligned_s)

				if para2_aligned_s in patt_util['all_data_dict']:
					#have already tried
					this_time = patt_util['all_data_dict'][para2_aligned_s]
					print("reused: para2_aligned_s" + para2_aligned_s)
					print("reused: time" + str(patt_util['all_data_dict'][para2_aligned_s]))
				else:
					#haven't tried yet
					#alignment
					build('--polly-tile-sizes=' + ','.join(map(str, para2_aligned)))

					if info['grain_cut'] == True:
						this_time = measure(info, info['remote'], int(info['repetition']), fastest_time * patt_util['alpha'])
					else:
						this_time = measure(info, info['remote'], int(info['repetition']), patt_util['huge_num'])

					patt_util['all_data_dict'][para2_aligned_s] = this_time

			exp_all_list.append([para2, float(str(this_time))])
			print(str(len(exp_all_list)) + '/' + str(exp_list_allnum) + ': ' + str([para2, float(str(this_time))]))

		else:
			this_time = product_recur(info, patt_util, exp_list, exp_all_list, para, count+1, pf)

		if this_time > fastest_time * patt_util['alpha']:
			print("[product_recur] grain_cut")
			if info['grain_cut'] == True:
				pf = True
		elif this_time < fastest_time:
			print("[product_recur] update fastest_time")
			fastest_time = this_time
		else:
			print("[product_recur] continue")
			#i.e. fastest_time <= this_time <= fastest_time * alpha 
			#the case of a little slow
			#NOT grain_cut and NOT update fastest
			pass

		para.pop()

	return fastest_time


def iterative_search(info, patt_util, width_list, depth, prev_eval, finest_flags):
	print('[patt progress] iterative_search start (depth:' + str(depth) + ')')
	end_flag = True
	grain = int(info['grain'])

	exp_list = []
	for i in range(len(width_list)):
		exp_list.append([])
		start = width_list[i][0]
		end = width_list[i][1]
		width_len = end - start
		step = width_len // (grain-1)

		if step == 0:
			finest_flags[i] = True
		if finest_flags[i] == True:
			if start == patt_util['margin'] and width_len>0:
				for smallnum in range(1, patt_util['margin'], 1):
					exp_list[i].append(smallnum)
			for j in range(0, width_len+1, 1):
				exp_list[i].append(start+j)
		else:
			for j in range(grain):
				exp_list[i].append(start + step*j)
			end_flag = False
	print('each para list: ' + str(exp_list))

	exp_all_list = []
	fastest_time = product_recur(info, patt_util, exp_list, exp_all_list, [], 0, False)
	print('# tiles that have already evaluated: ' + str(len(exp_all_list)))
	print('alreadly evaluated list: ' + str(exp_all_list))
	print('[iterative_search] current fastest time: ' + str(fastest_time))

	fastest_para = []
	for i in exp_all_list:
		if fastest_time == i[1]:
			fastest_para = i[0]
			break
	print('[iterative_search] current fastest tile: ' + str(fastest_para))

	#end check (region)
	if all(map(lambda x: x==1, map(len,exp_list))):
		#all len==1
		end_flag = True

	if end_flag:
		print("enough range. stop here.")
		print("enough depth(region). depth:" + str(depth) + "->1")
		depth = 1

	#end check2 (time)
	end_flag2 = False
	if info['depth_cut'] == True and (fastest_time >= prev_eval[1] * patt_util['alpha']):
		print("this time fastest:" + str(fastest_time) + ", and prev fastest:" + str(prev_eval[1]))
		print("enough depth(time). depth:" + str(depth) + "->1")
		fastest_time = prev_eval[1]
		depth = 1
		end_flag2 = True

	if end_flag2:
		fastest_para = prev_eval[0]
	else:
		fastest_para_idx = []
		for i in range(len(exp_list)):
			for j in range(len(exp_list[i])):
				if fastest_para[i] == exp_list[i][j]:
					fastest_para_idx.append(j)
					break
		print('fastest para idx: ' + str(fastest_para_idx))

	if (not end_flag) and (not end_flag2):
		if fastest_time >= prev_eval[1]:
			print('prev faster than new')
			print("this time fastest_time:" + str(fastest_time) + ", and prev fastest_time:" + str(prev_eval[1]))
			print("this time fastest_para(not aligned):" + str(fastest_para) + ", and prev fastest_para:" + str(prev_eval[0]))
			fastest_time = prev_eval[1]
			fastest_para = prev_eval[0]

		#width_list update
		print('prev width list: ' + str(width_list))
		for i in range(len(width_list)):
			start = width_list[i][0]
			end = width_list[i][1]
			width_len = end - start
			step = width_len // ((grain-1)*2)
			new_start = start
			new_end = end
                        print "dim%d step %d" %(i,step)
			if step == 0:
				if finest_flags[i] == True:
					#end
					if fastest_time >= prev_eval[1]:
						new_start = prev_eval[0][i]
						new_end = prev_eval[0][i]
					else:
						new_start = fastest_para[i]
						new_end = fastest_para[i]
				else:
					#last one more time
					finest_flags[i] = True

			elif fastest_time >= prev_eval[1]:
				if prev_eval[0][i] == start:
					#start point
					new_start = start
					new_end = start + step
				elif prev_eval[0][i] == end:
					#end point
					new_start = end - step
					new_end = end
				else:
					#middle point
					new_start = prev_eval[0][i] - step
					new_end = prev_eval[0][i] + step
			else:
				if fastest_para_idx[i] == 0:
					#start point
					new_start = start
					new_end = start + step
				elif fastest_para_idx[i] == len(exp_list[i])-1:
					#end point
					new_start = end - step
					new_end = end
				else:
					#middle point
					new_start = fastest_para[i] - step
					new_end = fastest_para[i] + step

			width_list[i] = [new_start, new_end]
		print('new width list: ' + str(width_list))

	#depth recursion
	if depth >= 2:
		iterative_search(info, patt_util, width_list, depth-1, [fastest_para, fastest_time], finest_flags)
	else:
		#make_executable(c_source_list, options, kernel_file, fastest_para)

		alignment_fastest_para = []
		first_time = True
		for i in fastest_para:
			if (first_time) and (len(fastest_para) == 3):
				alignment_fastest_para.append(i)
				first_time = False
			else:
				new_i = i
				while new_i % patt_util['alignment'] != 0:
					new_i += 1
				alignment_fastest_para.append(new_i)

		#print('blocking size (fastest_para): ' + str(fastest_para))
		print('final blocking size (alignment): ' + str(alignment_fastest_para))
		print('final_meas_num: ' + str(info['meas_num']))
		#build('-debug --polly-tile-sizes=' + ','.join(map(str, alignment_fastest_para)))
		build('--polly-tile-sizes=' + ','.join(map(str, alignment_fastest_para)))


#----------------------------------------------------------------
def patt_start(info, patt_util):
	#all data stock dictionary for reuse
	patt_util['all_data_dict'] = {}
	#timeout init val
	patt_util['huge_num'] = 10000
	#pruned(passed) case
	patt_util['pass_num'] = patt_util['huge_num']-3
	#left-side boundary
	patt_util['margin'] = 8
	#multiple number (x modulo alignemnt = 0)
	patt_util['alignment'] = 4
	#extra time coefficient for timeout and grain_cut
	patt_util['alpha'] = 1.05

	#preparation
	prebuild(info['c_source_list'], info['cc_options'], info['kernel_file'])
	make_measure_script(int(info['threads']))


def i_patt_mode(info):
	patt_util = {}
	patt_start(info, patt_util)

	#i_patt specific
        
	loop_size = info['loop_size'].split(' ')
	loop_size = map(int, loop_size)

	if len(loop_size) == 3:
	#if len(loop_size) == 3 or len(loop_size) == 2:
		temp_fastest_time = patt_util['huge_num']
		temp_fastest_i = 32
		#for i in [1,2,3,4,8,12,16,20,24,28,32]:
		for i in [4,8,12,16,20,24,28,32]:
			temp_para = [i,32,32]
			print('temp_para: '+str(temp_para))
			build('--polly-tile-sizes=' + ','.join(map(str, temp_para)))
			temp_time = measure(info, info['remote'], int(info['repetition']), temp_fastest_time)
			print('temp_time: '+str(temp_time))
			if temp_time < temp_fastest_time:
				temp_fastest_time = temp_time
				temp_fastest_i = i
	
		fastest_i = temp_fastest_i
		print("fastest i: " + str(fastest_i))

	if len(loop_size) == 3:
		print("i_patt: 3 loop mode")
		width_list = [[fastest_i,fastest_i],[patt_util['margin'],loop_size[1]],[patt_util['margin'],loop_size[2]]]
	elif len(loop_size) == 2:
		print("i_patt: 2 loop mode")
		#width_list = [[fastest_i,fastest_i],[patt_util['margin'],loop_size[1]]]
		width_list = [[patt_util['margin'],loop_size[0]],[patt_util['margin'],loop_size[1]]]
	else:
		print('error: len(loop_size) must be 2 or 3')
		sys.exit()

	init_finest_flags=[False]*len(loop_size)
	iterative_search(info, patt_util, width_list, int(info['depth']), [[32,32,32],10000], init_finest_flags)


def s_patt_mode(info):
	patt_util = {}
	patt_start(info, patt_util)

	loop_size = info['loop_size'].split(' ')
	loop_size = map(int, loop_size)

	#s_patt specific
	if len(loop_size) == 3:
	#if len(loop_size) == 3 or len(loop_size) == 2:
		if loop_size[0] // (int(info['threads'])*8) >= 8:
			#8blockiing and 1thread 8iteration
			loop_size[0] = loop_size[0] // (int(info['threads'])*8)
		else:
			#1thread just 1iteration
			loop_size[0] = int(math.ceil(1.0 * loop_size[0] / int(info['threads'])))
	
		aligned_i = loop_size[0]
		#while aligned_i % 4 != 0:
		#	aligned_i += 1
	
		print("static calculate i: " + str(loop_size[0]))
		print("static calculate i aligned: " + str(aligned_i))

	if len(loop_size) == 3:
		print("s_patt: 3 loop mode")
		width_list = [[aligned_i,aligned_i],[patt_util['margin'],loop_size[1]],[patt_util['margin'],loop_size[2]]]
	elif len(loop_size) == 2:
		print("s_patt: 2 loop mode")
		#width_list = [[aligned_i,aligned_i],[patt_util['margin'],loop_size[1]]]
		width_list = [[patt_util['margin'],loop_size[0]],[patt_util['margin'],loop_size[1]]]
	else:
		print('error: len(loop_size) must be 2 or 3')
		sys.exit()

	init_finest_flags=[False]*len(loop_size)

	iterative_search(info, patt_util, width_list, int(info['depth']), [[32,32,32],10000], init_finest_flags)


def s_patt_plus_mode(info):
	patt_util = {}
	patt_start(info, patt_util)

	#i_patt specific
	loop_size = info['loop_size'].split(' ')
	loop_size = map(int, loop_size)

	if len(loop_size) == 3:
	#if len(loop_size) == 3 or len(loop_size) == 2:
		temp_fastest_time = patt_util['huge_num']
		temp_fastest_i = 32

		n_ipt_list = [1,2,4,8]
		i_list = []
		#loop_size[0] = int(math.ceil(1.0 * loop_size[0] / int(info['threads'])))
		for n_ipt in n_ipt_list:
			temp_i = int(math.ceil(1.0 * loop_size[0] / (1.0 * n_ipt * int(info['threads']))))
			if temp_i == 1:
				for it in range(0,2,1):
					i_list.append(temp_i+it)
			else:
				for it in range(-1,2,1):
					i_list.append(temp_i+it)
		#for i in [1,2,3,4,8,12,16,20,24,28,32]:
		#for i in [4,8,12,16,20,24,28,32]:
		print('i_list: '+str(i_list))
		for i in i_list:
			temp_para = [i,32,32]
			print('temp_para: '+str(temp_para))
			real_build('--polly-tile-sizes=' + ','.join(map(str, temp_para)))
			while not os.path.isfile('./patt_result/temp/build/kernel_polly_exe'):
				i = i+1
				temp_para = [i,32,32]
				print('build failed, increment i, rebuild temp_para: '+str(temp_para))
				real_build('--polly-tile-sizes=' + ','.join(map(str, temp_para)))
			temp_time = measure(info, info['remote'], int(info['repetition']), temp_fastest_time)
			print('temp_time: '+str(temp_time))
			if temp_time < temp_fastest_time:
				temp_fastest_time = temp_time
				temp_fastest_i = i
	
		fastest_i = temp_fastest_i
		print("fastest i: " + str(fastest_i))

	if len(loop_size) == 3:
		print("i_patt: 3 loop mode")
		width_list = [[fastest_i,fastest_i],[patt_util['margin'],loop_size[1]],[patt_util['margin'],loop_size[2]]]
	elif len(loop_size) == 2:
		print("i_patt: 2 loop mode")
		#width_list = [[fastest_i,fastest_i],[patt_util['margin'],loop_size[1]]]
		width_list = [[patt_util['margin'],loop_size[0]],[patt_util['margin'],loop_size[1]]]
	else:
		print('error: len(loop_size) must be 2 or 3')
		sys.exit()

	init_finest_flags=[False]*len(loop_size)
	iterative_search(info, patt_util, width_list, int(info['depth']), [[32,32,32],10000], init_finest_flags)


def d_patt_mode(info):
	#for debug
	patt_util = {}
	patt_start(info, patt_util)

	loop_size = info['loop_size'].split(',')
	loop_size = map(int, loop_size)
	width_list = [[24,24],[1,loop_size[1]],[1,loop_size[2]]]

	#iterative_search(info, patt_util, width_list, int(info['depth']), [[32,32,32],10000])

