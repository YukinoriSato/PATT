#!/usr/bin/env python

import sys
from util.util import *
#from util.heatmap_generator import *


def exhaustive_search(info):
	print("exhaustive search start")
	fastest_time = info['huge_num']
	fastest_para = []

	prebuild(info['c_source_list'], info['cc_options'], info['kernel_file'])
	make_measure_script(int(info['threads']))

	for i in info['all_list_list'][0]:
		for j in info['all_list_list'][1]:
			for k in info['all_list_list'][2]:
				para = [i,j,k]
				build('--polly-tile-sizes=' + ','.join(map(str, para)))
				if info['mode'] == 'heatmap':
					this_time = measure(info, info['remote'], int(info['repetition']), info['huge_num'])
					print >> info['file'], ','.join(map(str, para)) +','+str(this_time)
				else:
					this_time = measure(info, info['remote'], int(info['repetition']), fastest_time)
				print(str(para) + ": " + str(this_time))
				if this_time < fastest_time:
					fastest_time = this_time
					fastest_para = para

	print("fastest time: " + str(fastest_time))
	print("final blocking size: " + str(fastest_para))
	build('--polly-tile-sizes=' + ','.join(map(str, fastest_para)))


def brute_force_mode(info):
	print('search paras:')
	print(info['all_list_list'])
	exhaustive_search(info)


def heatmap_mode(info):
	info['file'] = open('patt_result/heatmap_data.csv','w')
	brute_force_mode(info)
	info['file'].close()

	axis = info['axis'].split(',')
	heatmap_generator('patt_result/heatmap_data.csv', 'Time', info['zoom'], axis[0], axis[1], axis[2])

