#!/usr/bin/env python

import sys
import re
#import numpy as np

def extract(input_file):
	s=''
	with open(input_file, 'r') as f:
		line = f.readline()
		while line:
			if '[build] polly_additional_passes: ' in line:
				s += line
				#line_s = line.strip() #eliminate \n
				#line_s = line_s.replace('', '')
			elif '[measure] meas_num: ' in line:
				s += line
			elif '[measure] this_time: ' in line:
				s += line
			elif '[get_perf_cost] para_s: ' in line:
				s += line
			elif '[get_perf_cost] perf_cost: ' in line:
				s += line
			elif '[get_perf_cost] skip_num: ' in line:
				s += line
			elif 'final_meas_num: ' in line:
				s += line
			elif 'final_skip_num: ' in line:
				s += line
			elif 'final_best_perf_cost: ' in line:
				s += line
			elif 'final_best_para: ' in line:
				s += line
			elif '[product_recur] update fastest_time' in line:
				s += line
			elif '[iterative_search] current fastest time: ' in line:
				s += line
			elif '[iterative_search] current fastest tile: ' in line:
				s += line
			elif 'final blocking size (alignment): ' in line:
				s += line
			elif 'update the best' in line:
				s += line
			elif 'sorted_simplex_cost: ' in line:
				s += line

			line = f.readline()

	with open(input_file+'_extracted', 'w') as f_out:
		f_out.write(s)


if __name__ == '__main__':
	argc = len(sys.argv) 
	if (argc != 2):
		print 'Usage: %s <inputFile>' % sys.argv[0]
		exit()
	extract(sys.argv[1])



