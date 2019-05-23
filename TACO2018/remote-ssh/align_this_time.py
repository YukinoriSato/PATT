#!/usr/bin/env python

import sys
import re
#import numpy as np

def extract(input_file):
	s=''
	cf = 10000.0 #current_fastest
	with open(input_file, 'r') as f:
		line = f.readline()
		while line:
			if '[measure] this_time: ' in line:
				this_time = float(line.replace('[measure] this_time: ','').strip())
				if this_time < cf:
					cf = this_time
				s += str(cf) + '\n'

			line = f.readline()

	with open(input_file+'_aligned', 'w') as f_out:
		f_out.write(s)


if __name__ == '__main__':
	argc = len(sys.argv) 
	if (argc != 2):
		print 'Usage: %s <inputFile>' % sys.argv[0]
		exit()
	extract(sys.argv[1])



