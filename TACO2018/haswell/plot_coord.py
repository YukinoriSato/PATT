#!/usr/bin/env python

import sys
#import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set()


def plot_coord(input_file):


	df = pd.read_csv(input_file, header=None)
	df.columns = ['outer', 'inner']
	ax = sns.regplot(data=df, x='inner', y='outer', fit_reg=False)

	plt.title('Hello')
	plt.savefig(input_file + '.png')
	plt.close()

	print('Hello')
	sys.exit()


	df = pd.read_csv(input_file, header=None)
	df.columns = ['i', 'j', 'k', 'value']
	#print(df)

	iall_list = []
	index_len = len(df.index)
	for i in range(0, index_len):
		num = int(df.ix[i,'i'])
		if num not in iall_list:
			iall_list.append(num)
	#print(iall_list)

	df_new = pd.DataFrame()
	count=0
	for ia in iall_list:
		#extract each i dataframe
		df_i = df.ix[df.ix[:,'i']==ia, :].reset_index(drop=True)
		#print(df_i)

		if count == 0:
			#df_new['j'] = df_i['j']
			#df_new['k'] = df_i['k']
			df_new['j*k'] = df_i['j'] * df_i['k']
			count += 1

		df_new['{0:04d}'.format(ia)+'_'+'value'] = df_i['value']
	#print(df_new)

	for ia in iall_list:
		#ax = sns.regplot(data=df_new, x='j*k', y='{0:04d}'.format(ia)+'_'+'value', ci=None)
		ax = sns.regplot(data=df_new, x='j*k', y='{0:04d}'.format(ia)+'_'+'value')
		sx = sns.plt.ylim(0,df['value'].max())
		sx = sns.plt.xlim(0,)
		#sns.plt.show()
		sns.plt.title(fig_name + ' (i==' + '{0:4d}'.format(ia) + ')')
		sns.plt.savefig('plot_' + fig_name + '_' + '{0:04d}'.format(ia)+'.png')
		sns.plt.close()


if __name__ == '__main__':
	argc = len(sys.argv) 
	if (argc != 2):
		print 'Usage: %s <inputFile>' % sys.argv[0]
		exit()
	plot_coord(sys.argv[1])



