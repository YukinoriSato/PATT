#!/usr/bin/env python

import sys
import subprocess
import os

s=''

all_result_dir = ('result_L_12', 'result_L_4')

for result_dir in all_result_dir:
	s+=result_dir+'\n'
	all_kernels = os.listdir(result_dir+'/')
	for kernel in all_kernels:
		with open(result_dir+'/'+kernel+'/s_patt_plus_1', 'r') as f:
			line = f.readline()
			f_time = 'null'
			f_size = 'null'
			f_meas = 'null'
			while line:
				if '[iterative_search] current fastest time: ' in line:
					f_time = line.replace('[iterative_search] current fastest time: ', '').strip()
				elif 'final blocking size (alignment): ' in line:
					f_size = line.replace('final blocking size (alignment): ', '').replace(', ', '_').strip()
				elif 'final_meas_num: ' in line:
					f_meas = line.replace('final_meas_num: ', '').strip()
				line = f.readline()

		s+=kernel+','+f_time+','+f_meas+','+f_size+'\n'

with open('collected_data.csv', 'w') as f_out:
	f_out.write(s)






