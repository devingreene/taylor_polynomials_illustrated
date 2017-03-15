# vim: set ai tw=60:
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi,sin,cos,exp,log

curve = deriv = deriv2 = deriv3 = order = figure_extent = \
taylor_curve = xvalues = at_x = fig = ax = None

warnings = [
	"Second degree Taylor polynomial\
equivalent to function.  Using first degree Taylor polynomial.",
	"Third degree Taylor polynomial\
equivalent to function.  Using second degree Taylor polynomial."
]


# Function for selecting function
def selector(n):
	global curve,deriv,deriv2,deriv3
	if n==0:
		curve = lambda x: x**2
		deriv = lambda x:2*x
		deriv2,deriv3 = None,None
	elif n==1:
		curve = lambda x: x**3
		deriv = lambda x:3*x**2
		deriv2 = lambda x:6*x
		deriv3 = None
	elif n==2:
		curve = lambda x: sin(x)
		deriv = lambda x: cos(x)
		deriv2 = lambda x: -sin(x)
		deriv3 = lambda x: -cos(x)
	elif n==3:
		curve = lambda x: log(x)
		deriv = lambda x: 1/x
		deriv2 = lambda x: -1/x**2
		deriv3 = lambda x: 2/x**3
	elif n==4:
		curve = lambda x: exp(x)
		deriv = lambda x: exp(x)
		deriv2= lambda x: exp(x)
		deriv3= lambda x: exp(x)
	elif n==5:
		curve = lambda x: x*sin(3*pi*x)
		deriv = lambda x: 3*pi*x*cos(3*pi*x) + sin(3*pi*x)
		deriv2= lambda x: 3*pi*(-3*pi*x*sin(3*pi*x) + 2*cos(3*pi*x))
		deriv3= lambda x: -27*pi**2*(pi*x*cos(3*pi*x) + sin(3*pi*x))
	

def plotpicture(xmin,xmax,ymin=None,ymax=None):
	
	global fig,ax,curve,xvalues,figure_extent

	# Clear what was before.  Make new figure if none
	# exists.
	if fig:
		fig.clear()
	else:
		fig = plt.figure()

	# Plotting parameters
	
	ax = plt.axes()
	
	xlength = xmax - xmin
	ax.set_xlim(xmin - 0.1*xlength, xmax + 0.1*xlength)
	xvalues = np.linspace(xmin,xmax,251)
	
	if curve:
		graph, = ax.plot(xvalues,curve(xvalues),'y')
	else:
		print("Please use `selector' to choose a curve")
		return
	
	if ymin and ymax:
		ax.set_ylim(ymin,ymax)
	
	ymin,ymax = ax.get_ylim()
	ylength = ymax - ymin
	ax.set_ylim(ymin-0.1*ylength, ymax + 0.1*ylength)

	plt.grid()

	figure_extent = (xlength**2  + ylength**2)**0.5

	fig.show()

	# bind key and mouse events to choice and movement of
	# Taylor polynomial
	plt.connect('motion_notify_event',update_taylor)	
	plt.connect('key_press_event',update_degree)

def update_degree(event):
	global order
	if event.key=='1':
		order = 1
	elif event.key == '2':
		if not deriv2:
			#"degree Taylor polynomial equivalent to function.  Using"
			#"derivative
			print(warnings[0])
			order = 1
		else:
			order = 2
	elif event.key == '3':
		if not deriv2:
			print(warnings[0])
			order=1
		elif not deriv3:
			print(warnings[1])
			order=2
		else:
			order=3
		

def update_taylor(event):
	global fig,ax,deriv,deriv2,taylor_curve,at_x,xvalues,order
	if taylor_curve and ax and taylor_curve in \
	ax.get_children():
		taylor_curve.remove()
	at_x = event.xdata
	if order == 1:
		try:
			taylor_curve, = ax.plot(xvalues,curve(at_x) + \
						(xvalues-at_x)*deriv(at_x),'r-')
		except:
			return
	if order == 2:
		try:	
			taylor_curve, = ax.plot(xvalues, curve(at_x) + \
						(xvalues-at_x)*deriv(at_x) + \
						(xvalues-at_x)**2*deriv2(at_x)/2,'r-')
		except:
			return
	if order == 3:
		try:	
			taylor_curve, = ax.plot(xvalues, curve(at_x) + \
						(xvalues-at_x)*deriv(at_x) + \
						(xvalues-at_x)**2*deriv2(at_x)/2+
						(xvalues - at_x)**3/6*deriv3(at_x),'r-')
		except:
			return

	fig.show()

