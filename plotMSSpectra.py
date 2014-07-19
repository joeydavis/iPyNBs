import os
import pprint
import random
import wx
import csv
import string
import qMS
import sets
import numpy
import matplotlib as mpl
import matplotlib.pyplot as pylab
from mpl_toolkits.mplot3d import Axes3D

def randrange(n, vmin, vmax):
    return (vmax-vmin)*numpy.random.rand(n) + vmin

def readFile(datapath):
    data = list(csv.reader( open(datapath, 'rU'), delimiter=' '))
    xs = []
    ys = []
    for line in data:
        xs.append(float(line[0]))
        ys.append(float(line[1]))
    return [xs, ys, datapath]

#fileList = ["P14577_68_82_0_437.25472286707_44.54105.txt",
#            "P14577_68_82_0_437.25472286707_44.5441846153846.txt"]

fileList = ["P05657_53_61_0_502.762172006605_29.574325.txt",
            "P05657_53_61_0_502.762172006605_29.5607625.txt"]

#fileList = ["P12876_33_42_0_544.3131832768_49.06385_mc4long.txt",
#            "P12876_33_42_0_544.3131832768_49.1642727272727_mc3long.txt"]


pylab.close('all')
fig = pylab.figure()
ax = fig.add_subplot(111, projection='3d')

[xs, ys, name] = readFile(fileList[1])
xtest = numpy.array(xs)
ytest = numpy.array(ys)
zs = [2]*len(xtest)
ztest = numpy.array(zs)
ax.plot(xtest,ztest,ytest, color='#0091d0', lw=1.5, label="50S")

top = float(max(ytest))

[xs, ys, name] = readFile(fileList[0])
xtest = numpy.array(xs)
ytest = numpy.array(ys)
zs = [1]*len(xtest)
ztest = numpy.array(zs)
ax.plot(xtest,ztest,ytest, color = '#db4140', lw=1.5, label="45S")

top = max([top, float(max(ytest))])

ax.w_xaxis.pane.set_visible(False)
ax.w_yaxis.pane.set_visible(False)
ax.w_zaxis.pane.set_visible(False)

#ax.w_xaxis.gridlines.set_visible(False)
#ax.w_yaxis.gridlines.set_visible(False)
#ax.w_zaxis.gridlines.set_visible(False)

ax.w_xaxis.gridlines.set_linewidth(2)
ax.w_yaxis.gridlines.set_linewidth(2)
ax.w_zaxis.gridlines.set_linewidth(2)

[i.set_linewidth(2) for i in ax.w_xaxis.get_ticklines()]
[i.set_linewidth(2) for i in ax.w_yaxis.get_ticklines()]
[i.set_linewidth(2) for i in ax.w_zaxis.get_ticklines()]

ax.w_xaxis.line.set_linewidth(2)
ax.w_yaxis.line.set_linewidth(2)
ax.w_zaxis.line.set_linewidth(2)
           
ax.set_yticks([1,2])

ax.set_zticks([0, top/3, 2*top/3, top])
ax.set_zlim3d([0, top])

ax.set_xlabel("mass")
ax.set_zlabel("intensity")

ax.view_init(10, -67)

pylab.ylim(0.5, 2.5)
pylab.legend()
pylab.show()
