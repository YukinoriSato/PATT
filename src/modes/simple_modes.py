#!/usr/bin/env python

from util.util import *

def debug_mode(info):
	print('debug_mode start')

def no_tiling_mode(info):
	prebuild(info['c_source_list'], info['cc_options'], info['kernel_file'])
	make_measure_script(int(info['threads']))
	build('-debug -polly-tiling=false')
        this_time = measure(info, info['remote'], int(info['repetition']), info['huge_num'])
	print("final_best_perf_cost: " + str(this_time))
	print("final_best_para: " + str("no_tiling"))
def polly_default_size_mode(info):
	prebuild(info['c_source_list'], info['cc_options'], info['kernel_file'])
	make_measure_script(int(info['threads']))
	build('-debug')
        this_time = measure(info, info['remote'], int(info['repetition']), info['huge_num'])
	print("final_best_perf_cost: " + str(this_time))
	print("final_best_para: " + str("all32"))
def manual_size_mode(info):
	prebuild(info['c_source_list'], info['cc_options'], info['kernel_file'])
	make_measure_script(int(info['threads']))
	build('-debug --polly-tile-sizes=' + info['tile_size'])
        this_time = measure(info, info['remote'], int(info['repetition']), info['huge_num'])
	print("final_best_perf_cost: " + str(this_time))
	print("final_best_para: " + info['tile_size'])
