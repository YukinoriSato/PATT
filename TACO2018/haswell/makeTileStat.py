#!/usr/bin/env python

import sys
import re
#import numpy as np
import os

data=[]
metrics=[]
files_dir=[]
modes=[]

def extract(resultDir, bench, mode):
        ftime=""
        ftile=""
        fiter=""

        fileName=resultDir+"/"+bench+"/"+mode
        print fileName
	with open(fileName, 'r') as f:
		line = f.readline()
		while line:
                        if '[iterative_search] current fastest time: ' in line:
				ftime= line
			elif 'final blocking size (alignment): ' in line:
				ftile= line
                        elif 'final_best_perf_cost:' in line:
				ftime= line
                        elif 'final_best_para:' in line:
				ftile= line
                        elif 'final_meas_num:' in line:
				fiter= line
			line = f.readline()


        print ftime,ftile,fiter
        t=ftime.split(":")
        stime=float(t[1].replace("\n",""))
        t=ftile.split(":")
        tmp0=t[1].replace("]"," ");
        tmp1=tmp0.replace("["," ");
        tmp2=tmp1.replace("\n","")
        stile=tmp2.replace(" ","")
        t=fiter.split(":")
        siter=float(t[1].replace("\n",""))
        print stime,stile,siter
        i=modes.index(mode)
        j=files_dir.index(bench)
        data[i][j].append(stime)
        data[i][j].append(stile)
        data[i][j].append(siter)
        #print i,j,k,data[i][j][k]
        #data[mode][bench]['tile']=stile

if __name__ == '__main__':
	argc = len(sys.argv) 
	if (argc > 2):
		print 'Usage: %s [resultDir]' % sys.argv[0]
		print '             default resultDir=./result'
		exit()
        elif argc==2:
                resultDir=sys.argv[1]
        else:
                resultDir='./result'

        #files = os.listdir(resultDir)

        #files_dir = [f for f in files if os.path.isdir(os.path.join(resultDir, f))]
        #files_dir.sort()

        files_dir="gemm","gemver","gesummv","mvt","2mm","3mm","syrk","syr2k","atax","covariance","correlation","jacobi-2d"

        #os.remove(resultDir+'/summary.out')

        modes=["s_patt_plus_1", "i_patt_1"]
        #modes=["i_patt_1", "orio_nm_1", "orio_sa_1"]  #, "orio_sa_2","orio_sa_3","orio_sa_4","orio_sa_5"]
        #modes=["orio_sa_1", "orio_sa_2","orio_sa_3","orio_sa_4"]
        #,"orio_sa_6","orio_sa_7","orio_sa_8","orio_sa_9","orio_sa_10"]
	#modes=["polly_default_size_1", "no_tiling_1", "i_patt_1", "orio_nm_1", "orio_sa_1"]

        #modes=["polly_default_size_1", "no_tiling_1"]

        #modes=["i_patt_1"]

        metrics=['time', 'tile']

        #print data

        for m in modes:
                data.append([])
                for bench in files_dir:
                        data[modes.index(m)].append([])
                        extract(resultDir, bench,m)

        #print data

	with open(resultDir+'/tile.csv', 'w') as f_out:
                f_out.write(': : ')
                for bench in files_dir:
                        #for m in metrics:
                        j=files_dir.index(bench)
                        ss="%s: " % files_dir[j]
                        #print ss
                        f_out.write(ss)
                f_out.write('\n')


                for mode in modes:
                        print mode
                        f_out.write(mode)
                        f_out.write(': nSearchStep: ')
                        for bench in files_dir:
                                #for m in metrics:
                                i=modes.index(mode)
                                j=files_dir.index(bench)
                                #ss="%f %s" % (data[i][j][0],data[i][j][1])
                                ss="%f: " % (data[i][j][2])
                                #print ss
                                f_out.write(ss)
                        f_out.write('\n')
                        f_out.write(mode)
                        f_out.write(': tile: ')
                        for bench in files_dir:
                                #for m in metrics:
                                i=modes.index(mode)
                                j=files_dir.index(bench)
                                #ss="%f %s" % (data[i][j][0],data[i][j][1])
                                ss="%s: " % (data[i][j][1])
                                #print ss
                                f_out.write(ss)
                        f_out.write('\n')


"""


                                
"""
