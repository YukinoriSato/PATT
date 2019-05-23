#!/usr/bin/env python

#utility functions

import subprocess
import os
#import numpy
import copy
import time

time_build=0.0
time_trial=0.0
time_other=0.0
time_prev=0.0
time_init=0.0

def tm_init():
        global time_prev, time_init
        t=time.time()
        time_prev=t
        time_init=t
        #print "tm_init()"
        return 


def tm_other():
        global time_other, time_prev
        t=time.time()
        #print "tm_other %f [s]" % (t-time_prev)
        time_other=t-time_prev+time_other
        time_prev=t
        return t-time_init
def tm_build():
        global time_build, time_prev
        t=time.time()
        #print "tm_build %f [s]" % (t-time_prev)
        time_build=t-time_prev+time_build
        time_prev=t
        return t-time_init

def tm_trial():
        global time_trial, time_prev
        t=time.time()
        #print "tm_trial %f [s]" % (t-time_prev)
        time_trial=t-time_prev+time_trial
        time_prev=t
        return t-time_init

def tm_print():
        global time_build, time_other, time_trial, time_prev
        t=time.time()
        print "time_build %f [s]" % (time_build)
        print "time_trial %f [s]" % (time_trial)
        print "time_other %f [s]" % (time_other)


def median(num_list):
        t = sorted(num_list)
        print "measured time = ", t
        return t[len(num_list)//2]

def min(num_list):
        t = sorted(num_list)
        return t[0]

def prebuild(c_source_list, cc_options, kernel_file):
        t=tm_other()
	#print('[patt progress] prebuild start %f' % t)

	cmd = 'mkdir patt_result/temp/prebuild'
	subprocess.call(cmd, shell=True)

	#driverX.o
	n = 0
	for i in c_source_list:
		if i == kernel_file:
			continue
		cmd = 'clang -O3 -c ' + cc_options + ' ' + i + ' -o ./patt_result/temp/prebuild/driver' + str(n) + '.o'
		subprocess.call(cmd, shell=True)
		n = n+1

	#kernel.ll
	cmd = 'clang -O1 -emit-llvm -S ' + cc_options + ' ' + kernel_file + ' -o ./patt_result/temp/prebuild/kernel.ll'
	subprocess.call(cmd, shell=True)
	#kernel.bc
	#cmd = 'llvm-as ./patt_result/temp/prebuild/kernel.ll -o ./patt_result/temp/prebuild/kernel.bc'
	#subprocess.call(cmd, shell=True)

        t=tm_build()
        #print('[patt progress] prebuild end %f'%t)


def build(polly_additional_passes):
	real_build(polly_additional_passes)

	new_polly_additional_passes = polly_additional_passes
	while not os.path.isfile('./patt_result/temp/build/kernel_polly_exe'):
		temp_list = new_polly_additional_passes.split('--polly-tile-sizes=')
		temp_list_i = temp_list[1].split(',')
		new_i = str(int(temp_list_i[0]) + 1)
		new_polly_additional_passes = new_polly_additional_passes.replace('--polly-tile-sizes='+temp_list_i[0], '--polly-tile-sizes='+new_i)
		print('[build] build failed, new pass:'+new_polly_additional_passes+', try rebuild')
		real_build(new_polly_additional_passes)


def real_build(polly_additional_passes):
        t=tm_other()
	#print('[patt progress] build start %f'%t)
	print('[build] polly_additional_passes: '+polly_additional_passes)

	if os.path.isdir('patt_result/temp/build'):
		cmd = 'rm -r patt_result/temp/build'
		subprocess.call(cmd, shell=True)
	cmd = 'mkdir patt_result/temp/build'
	subprocess.call(cmd, shell=True)

	#polly flow
	#all necessary files are included in patt_result/temp/prebuild

	#patt's default options
	polly_passes = '-debug '
	polly_passes += '-basicaa '
	polly_passes += '-polly-process-unprofitable '
	polly_passes += '-polly-ignore-aliasing '
	polly_passes += '-polly-allow-nonaffine '
	polly_passes += '-polly-opt-isl '
	polly_passes += '-polly-vectorizer=polly '
	polly_passes += '-polly-parallel '
	polly_passes += '-polly-pattern-matching-based-opts=false '
	#additional options
	#e.g. -debug --polly-tile-sizes=32,32,32 -polly-tiling=false
	polly_passes += ' '+polly_additional_passes+' '
	polly_passes += '-polly-codegen '

	#kernel_polly.o
	cmd = 'opt -S -polly-canonicalize ./patt_result/temp/prebuild/kernel.ll > ./patt_result/temp/build/kernel_polly1.ll'
	subprocess.call(cmd, shell=True)
	#cmd = 'llvm-as ./patt_result/temp/build/kernel_polly1.ll -o ./patt_result/temp/build/kernel_polly1.bc'
	#subprocess.call(cmd, shell=True)
	if '-debug' in polly_passes:
		cmd = 'opt ' + polly_passes + ' ./patt_result/temp/build/kernel_polly1.ll > ./patt_result/temp/build/kernel_polly2.bc 2>./patt_result/temp/build/kernel_polly_out.txt'
	else:
		cmd = 'opt ' + polly_passes + ' ./patt_result/temp/build/kernel_polly1.ll > ./patt_result/temp/build/kernel_polly2.bc'
	subprocess.call(cmd, shell=True)
	cmd = 'llvm-dis ./patt_result/temp/build/kernel_polly2.bc -o ./patt_result/temp/build/kernel_polly2.ll'
	subprocess.call(cmd, shell=True)
	cmd = 'opt -O3 ./patt_result/temp/build/kernel_polly2.bc > ./patt_result/temp/build/kernel_polly3.bc'
	subprocess.call(cmd, shell=True)
	cmd = 'llvm-dis ./patt_result/temp/build/kernel_polly3.bc -o ./patt_result/temp/build/kernel_polly3.ll'
	subprocess.call(cmd, shell=True)
	cmd = 'llc -mattr=+avx2 -O3 -filetype=obj -o ./patt_result/temp/build/kernel_polly.o ./patt_result/temp/build/kernel_polly3.bc'
	subprocess.call(cmd, shell=True)

	#kernel_polly_exe
	all_prebuild_files = os.listdir('./patt_result/temp/prebuild/')
	driver_files = filter(lambda x: 'driver' in x, all_prebuild_files)
	drivers=''
	for d in driver_files:
		drivers += './patt_result/temp/prebuild/' + d + ' '

	cmd = 'clang -lgomp -lm -o ./patt_result/temp/build/kernel_polly_exe ./patt_result/temp/build/kernel_polly.o ' + drivers
	subprocess.call(cmd, shell=True)
        t=tm_build()
        #print('[patt progress] build end %f'%t)


def make_measure_script(threads):
        t=tm_other()
	#print('[patt progress] make_measure_script start %f'%t)

	#exe name: kernel_polly_exe
	last_thread=threads-1
	cmd = 'echo \'' + \
		'#!/bin/bash\n' + \
		'export OMP_NUM_THREADS=' + str(threads) + '\n' + \
		'timeout $1 /usr/bin/time -f "%e" -o ./patt_result/temp/build/time_result taskset -c 0-'+str(last_thread)+' ./patt_result/temp/build/kernel_polly_exe &>/dev/null\n' + \
		'\' > ./patt_result/temp/prebuild/measure_exe.sh'
	subprocess.call(cmd, shell=True)
	cmd = 'chmod u+x ./patt_result/temp/prebuild/measure_exe.sh'
	subprocess.call(cmd, shell=True)

	#get current path
	cmd = 'pwd'
	subprocess.call(cmd, shell=True)
	popen_obj = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
	std_out_and_err = popen_obj.communicate()
	global current_path
	current_path = std_out_and_err[0].strip()
        t=tm_build()
        #print('[patt progress] make_measure_script end %f'%t)


current_path = ''
def measure(info, remote, repetition, timeout):
        t=tm_other()
	#print('[patt progress] measure start %f'%t)
	info['meas_num'] += 1
	print('[measure] meas_num: ' + str(info['meas_num']))
	huge_num = 10000
	timeout_num = huge_num-1
	error_num = huge_num-2
	#coefficient for timeout (super slightly)
	timeout *= 1.01

	if remote != '':
		global current_path
		ssh_cmd = 'ssh '+remote+' \'cd '+current_path+'; ./patt_result/temp/prebuild/measure_exe.sh '+str(timeout)+'\''
	else:
		#local
		ssh_cmd = './patt_result/temp/prebuild/measure_exe.sh ' + str(timeout)

	this_time_list = []
	for it in range(repetition):
	#for it in range(1):
		subprocess.call(ssh_cmd, shell=True)

		#get the result
		cmd = 'head -n 1 ./patt_result/temp/build/time_result'
		popen_obj = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
		std_out_and_err = popen_obj.communicate()
		if std_out_and_err[0].strip() == '':
			#timeout
			print('[measure] this_time: '+str(timeout_num))
                        t=tm_trial()
                        #print('[patt progress] measure end0  %f'%t)
			return timeout_num

		this_time_list_temp = float(std_out_and_err[0].strip())
		#print "it%d: %f[s]"  % (it, this_time_list_temp)
		this_time_list.append(this_time_list_temp)

        #this_time = numpy.median(this_time_list)
        this_time = median(this_time_list)
	#this_time = min(this_time_list)
	if this_time == 0.0:
		this_time = error_num

	print('[measure] this_time: '+str(this_time))

        t=tm_trial()
	#print('[patt progress] measure end1  %f'%t)
	return this_time


#for release
def get_perf_cost(info, coord):
	para = []
	for i in range(len(coord)):
		para.append(info['all_list_list'][i][coord[i]])
	para_s = ','.join(map(str, para))

	if para_s in info['all_perf_cost_dict']:
		#have already tried
		time = info['all_perf_cost_dict'][para_s]
		print('[get_perf_cost] have already trid. skip.')
		print('[get_perf_cost] para_s: '+para_s)
		print('[get_perf_cost] perf_cost: '+str(info['all_perf_cost_dict'][para_s]))
		info['skip_num'] += 1
		print('[get_perf_cost] skip_num: ' + str(info['skip_num']))
	else:
		#first time
		build('--polly-tile-sizes=' + para_s)
		time = measure(info, info['remote'], int(info['repetition']), info['huge_num'])
		info['all_perf_cost_dict'][para_s] = time

	return time


'''
#for debug
def get_perf_cost(info, coord):
	para = []
	for i in range(len(coord)):
		para.append(info['all_list_list'][i][coord[i]])
	x = (para[0])**2 + (para[1])**2 + (para[2])**2
	#print(para)
	#print(x)
	info['meas_num'] += 1
	print('meas_num: '+ str(info['meas_num']))
	return x
'''

'''
#for debug from csv data
import pandas as pd
df = pd.read_csv('result_Time_gemm.csv', header=None)
df.columns = ['i', 'j', 'k', 'value']
print(df)
def get_perf_cost(info, coord):
	#print(df.ix[3,3])
	#print(df.ix[df['i'].isin([str(info['all_list_list'][0][coord])])])
	#print(df.ix[df['i'].isin([16]), df['j'].isin([8, 16])])
	#print(df.loc[(df.i == 16) & (df.j == 8) & (df.k == 8)].value)
	#print(float(df.ix[(df.i == 16) & (df.j == 8) & (df.k == 8)].value))
	i = info['all_list_list'][0][coord[0]]
	j = info['all_list_list'][1][coord[1]]
	k = info['all_list_list'][2][coord[2]]
	#print('Hello')
	#print(i)
	#print(j)
	#print(k)
	x = float(df.ix[(df.i == i) & (df.j == j) & (df.k == k)].value)
	#print(x)
	info['meas_num'] += 1
	print('meas_num: '+ str(info['meas_num']))
	return x
	#sys.exit()
'''




