#!/usr/bin/env python

#This script is for python2, llvm4.0
#patt.py v3.0.6
#2017/10/25(yyyy/mm/dd)
#written by T.Y

# for i-PATT
grain=8
depth=100
grain_cut=True
depth_cut=False


import sys
import subprocess
import os
import pprint
#modes
from modes.simple_modes import *
from modes.patt_modes import *
from modes.exhaustive_modes import *
from modes.static_modes import *
#from modes.scipy_optimize_modes import *
from modes.sa_modes import *
from modes.nm_modes import *
from util.util import *


def parse(argv):
	info = {}
	info['c_source_list'] = []
	#info['ll_source_list'] = []
	info['cc_options'] = ''

        info['grain']=grain
        info['depth']=depth
        info['grain_cut']=grain_cut
        info['depth_cut']=depth_cut


	for i in range(1, len(argv)):
		if '-patt-setting=' in argv[i]:
			patt_setting_file = argv[i].replace('-patt-setting=', '')
		elif argv[i][0] == '-':
			info['cc_options'] += argv[i] + ' '
		elif argv[i][-2:] == '.c':
			info['c_source_list'].append(argv[i])
		#elif argv[i][-3:] == '.ll':
		#	info['ll_source_list'].append(argv[i])
		else:
			print("argument error")
			sys.exit()
        print patt_setting_file
	with open(patt_setting_file, 'r') as f:
		line = f.readline()
		while line:
			#ignore
			if line[0] == '#':
				line = f.readline()
				continue
			if len(line) >= 3 and line[0:3] == "\'\'\'":
				while True:
					line = f.readline()
					if len(line) >= 3 and line[0:3] == "\'\'\'":
						break
			if line.find('=') == -1:
				line = f.readline()
				continue

			#remember
			line = line.strip()
			tlist = line.split('=')
			info[tlist[0]] = tlist[1]
			line = f.readline()

	#some utility numbers
	info['huge_num'] = 10000
	info['timeout_num'] = info['huge_num']-1
	info['error_num'] = info['huge_num']-2
	info['pass_num'] = info['huge_num']-3

	info['meas_num'] = 0
	info['skip_num'] = 0

	info['all_perf_cost_dict'] = {}

	return info


def patt(argv):
        tm_init()
	#print('[patt progress] patt start')


	if os.path.exists('patt_result'):
		#print('Please delete ./patt_files directory')
		#sys.exit()
		cmd = 'rm -r patt_result'
		subprocess.call(cmd, shell=True)
	cmd = 'mkdir patt_result'
	subprocess.call(cmd, shell=True)
	cmd = 'mkdir patt_result/temp'
	subprocess.call(cmd, shell=True)

	info = parse(argv)
	print('all infomation:')        
	pprint.pprint(info)

	eval(info['mode'] + '_mode')(info)


	#print('[patt progress] patt end')
        tm_print()

if __name__ == '__main__':
	patt(sys.argv)


