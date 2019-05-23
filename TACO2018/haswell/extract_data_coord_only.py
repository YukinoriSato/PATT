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
				line_s = line.replace('[build] polly_additional_passes: --polly-tile-sizes=', '')
				line_list = line_s.split(',')
				if len(line_list) == 3:
					s += line_list[1]+','+line_list[2]
				elif len(line_list) ==2:
					s += line_list[0]+','+line_list[1]
				else:
					print('Error')
					sys.exit()
			line = f.readline()

	with open(input_file+'_only_coord', 'w') as f_out:
		f_out.write(s)


if __name__ == '__main__':
	argc = len(sys.argv) 
	if (argc != 2):
		print 'Usage: %s <inputFile>' % sys.argv[0]
		exit()
	extract(sys.argv[1])



