#!/usr/bin/env python

import sys
#import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set()
import subprocess


def heatmap_generator(input_file, fig_name, zooms, x_axis, y_axis, time_axis):
	df = pd.read_csv(input_file, header=None)
	df.columns = ['i', 'j', 'k', 'value']
	#print(df)

	ta_list = []
	index_len = len(df.index)
	for i in range(0, index_len):
		num = int(df.ix[i,time_axis])
		if num not in ta_list:
			ta_list.append(num)
	#print(ta_list)

	zoom_list = zooms.split(',')
	zoom_list = map(int, zoom_list)

	for zoom in zoom_list:
		cmd = 'mkdir patt_result/zoom' + str(zoom)
		subprocess.call(cmd, shell=True)

		all_min = df['value'].min()
		all_max = df['value'].max()
		mm_range = all_max - all_min
		zoom_i = int(zoom)
		all_max = all_max - mm_range * (zoom_i-1)/zoom_i
		#all_min = all_min + mm_range/2

		for ta in ta_list:
			#extract time_axis dataframe
			df_ta = df.ix[df.ix[:,time_axis]==ta, :]

			df_ta_pivot = pd.pivot_table(data=df_ta, values='value', columns=x_axis, index=y_axis)
			#print(df_ta_pivot)

			#ax = sns.heatmap(df_ta_pivot, vmin=all_min, vmax=all_max, cmap='Blues', annot=True)
			ax = sns.heatmap(df_ta_pivot, vmin=all_min, vmax=all_max, cmap='jet', annot=False, xticklabels=8, yticklabels=8)
			#ax = sns.heatmap(df_ta_pivot, vmin=all_min, vmax=all_max, cmap='hot', annot=False, xticklabels=16, yticklabels=4)
			#sns.plt.show()
			#sns.plt.title(fig_name + ' (' + time_axis + '==' + '{0:4d}'.format(ta) + ')')
			#sns.plt.savefig('heatmap' + '{0:04d}'.format(ta)+'.png')
			#sns.plt.close()
			plt.title(fig_name + ' (' + time_axis + '==' + '{0:4d}'.format(ta) + ')')
			#plt.savefig('patt_result/' + 'heatmap' + '{0:04d}'.format(ta)+'.png')
			plt.savefig('patt_result/zoom'+str(zoom)+'/heatmap' + '{0:04d}'.format(ta)+'_zoom'+str(zoom)+'.png')
			plt.close()


