#!/usr/bin/env python

from scipy.optimize import basinhopping
#from scipy.optimize import brute
#import scipy.optimize
#import scipy
#from scipy.optimize import minimize, rosen, rosen_der
#from scipy import optimize
from util.util import *

#incompletion
def basinhopping_mode(info):
	prebuild(info['c_source_list'], info['cc_options'], info['kernel_file'])
	make_measure_script(int(info['threads']))

	#minimizer_kwargs = {"method": "BFGS"}
	#ret = basinhopping(testfunc, [1.], minimizer_kwargs=minimizer_kwargs, niter=200)
	#print(ret.x)
	#print(ret.fun)

	#minimizer_kwargs = {"args": 1.0}
	#ret = basinhopping(testfunc, [1.], minimizer_kwargs=minimizer_kwargs, stepsize=1)

	#rranges = (slice(-4, 4, 0.25), slice(-4, 4, 0.25))
	#ret = brute(testfunc, rranges, full_output=True, finish=scipy.optimize.fmin)
	#print("global minimum: x = %.4f, f(x0) = %.4f" % (ret.x, ret.fun))
	#print(ret)

	#x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
	#res = minimize(rosen, x0, method='Nelder-Mead', tol=1e-6)
	#print(res)

	#scipy.optimize.basinhopping(func, x0, niter=100, T=1.0, stepsize=0.5, minimizer_kwargs=None, take_step=None, accept_test=None, callback=None, interval=50, disp=False, niter_success=None, seed=None)

	#x0 = [10, 10, 10, 10, 10]
	#res = minimize(rosen, x0, method='Nelder-Mead', tol=1e-6)
	#res = minimize(rosen, x0, args=(), method='Nelder-Mead', jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)
	#print(res)

	#params = (2, 3, 7)
	#rranges = (slice(-4, 4, 0.25), slice(-4, 4, 0.25))
	#ret = optimize.brute(testfunc, rranges, args=params, full_output=True, finish=optimize.fmin)
	#print(ret)

	#x0 = [32, 32, 32]
	#ret = basinhopping(testfunc, x0, niter=30, T=1.0, stepsize=10, minimizer_kwargs=None, take_step=None, accept_test=None, callback=None, interval=50, disp=True, niter_success=None, seed=None)
	#ret = basinhopping(testfunc, x0, niter=300, T=1.0, stepsize=10, minimizer_kwargs=None, take_step=None, accept_test=None, callback=None, interval=50, disp=True, niter_success=None, seed=None)
	#print(ret)

	minimizer_kwargs = {"args": (info, info['remote'], int(info['repetition']), info['huge_num'])}
	#ret = basinhopping(testfunc, [32,32,32], niter=300, T=1.0, stepsize=10, minimizer_kwargs=minimizer_kwargs, take_step=None, accept_test=None, callback=None, interval=50, disp=True, niter_success=None, seed=None)
	ret = basinhopping(evalfunc, [32,32,32], niter=10, T=1.0, stepsize=10, minimizer_kwargs=minimizer_kwargs, take_step=None, accept_test=None, callback=None, interval=50, disp=True, niter_success=None, seed=None)
	print(ret)


def testfunc(x, *params):
	print("testfunc start")
	print(x)
	x = map(round, x)
	print(x)
	return x[0]**2 + x[1]**2 + x[2]**2
	#return (x[0]/100)**2 + (x[1]/100)**2 + (x[2]/100)**2

def evalfunc(x, *params):
	print("evalfunc start")

	print("original x")
	print(x)

	x = map(round, x)
	x = map(int, x)
	while x[0] % 4 != 0:
		x[0] += 1
	while x[1] % 4 != 0:
		x[1] += 1
	while x[2] % 4 != 0:
		x[2] += 1
	x = map(lambda a: a if a>=8 else 8, x)

	print("modified x")
	print(x)

	build('--polly-tile-sizes=' + ','.join(map(str,x)))
	info, remote, repetition, huge_num = params
	time = measure(info, remote, repetition, huge_num)
	print(time)

	return time

