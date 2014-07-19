import csv
import math
import matplotlib.pyplot as pylab
from matplotlib import mpl
from mpl_toolkits.mplot3d import Axes3D
import scipy.linalg as sl
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd
import scipy.cluster.vq as scv
import numpy as np
from matplotlib.mlab import PCA
import numpy.linalg as npla
import string
import time
import sys, os
import getopt
from mpl_toolkits.mplot3d import proj3d
from string import ascii_letters
import networkx as nx
import matplotlib.colors as mpc
import random
import matplotlib._pylab_helpers

def readDataFile(filename, scale=1.0):
    """readDataFile reads a datafile. The datafile should be tab separated and have both column and row headers listing the proteins/fractions.
    Empty values should be empty, they will be treated as np.NAN - see lambda below
    readDataFile takes an optional scale that will multiply the data by the specified factor - useful for "scaling" error

    :param filename: a string of the filename to be read
    :type filename: string
    :param scale: a float indicating how to scale the data, default is unscaled (1)
    :type scale: float
    :returns:  a data ditionary. 'data', 'fractions', 'proteins' are filled in, others are None

    """
    with open(filename, 'rb') as inputFile:
        csvFile = list(csv.reader(inputFile, delimiter = '\t'))
        header = csvFile[0]
        proteins = [row[0] for row in csvFile[1:]]
        insertValue2 = lambda x, y: np.NAN if x=='' else float(x)*y
        data = np.array([[insertValue2(col, scale) for col in row[1:]] for row in csvFile[1:]])
        inputFile.close()
        return {'fractions':header[1:], 'proteins':proteins, 'fi':None, 'pi':None, 'data':data}

########################
def drawHeatMap(xdat, name="unnamed", x=3, y=15, colors=pylab.cm.autumn_r, dendro=False, protColors=None, cIndex=None, km=None):
    """drawHeatMap produces a colored heatmap in a new figure window

    :param xdat: a data object (must contain fields 'data', 'fractions', 'proteins')
    :type xdat: dict
    :param colors: a color scale (a cmap)
    :type colors: cmap
    :param name: figure name and title
    :type name: str.
    :param dendro: a boolean to draw the dendrogram on the left
    :type dendro: bool.
    :param protColors: a color map used to label the protein names with group colors
    :type protColors: cmap
    :param cIndex: a list of groupIds for the proteins
    :type cIndex: list
    :param km: if present, will draw the kmeans cluster profiles at the top of the figure- input is a 2d-matrix - rowVectors for each centroid, each column is a fraction
    :type km: matrix
    :returns:  int -- the return code.
    :raises: AttributeError, KeyError
    :returns: a figure object

    """

    data = xdat['data']
    fractions = xdat['fractions']
    proteins = xdat['proteins']
    ##Draw heatmap
    fig = pylab.figure(figsize=(x,y))
    axData = fig.add_subplot(111)
    for i in range(len(fractions)):
        axData.text(i, -0.5 , ' '+str(fractions[i]), rotation=270, verticalalignment="top", horizontalalignment="center", fontsize=8)
    for i in range(len(proteins)):
        axData.text(-0.75, i, '  '+str(proteins[i]), verticalalignment="center", horizontalalignment="right", fontsize=4)

    figData = axData.matshow(data, aspect='auto', cmap=colors, vmin=0, vmax=1.25)

    #figData = heatMapAxes(data, dims = [xStart, yStart, xLength, yLength], fractions=fractions, proteins=proteins, protColors=protColors, cIndex=cIndex, fig=fig)
    axData.set_xticks([])
    axData.set_yticks([])
    
    ##Draw colorbar
    cbar = fig.colorbar(figData)
    cbar.set_ticks([0.0, 0.25, 0.50, 0.75, 1.00, 1.25])
    cbar.set_ticklabels([0.0, 0.25, 0.50, 0.75, 1.00, 1.25])
    

    return fig

def heatMapAxes(data, dims=[0.1, 0.1, 0.7, 0.7], colors=pylab.cm.autumn, fractions=None, proteins=None, protColors=None, cIndex=None, fig=None):
    """heatMapAxes draws a heatmap

    :param data: a datamatrix to draw
    :type xdat: a 2D Matrix
    :param dims: the size of the plot to draw - defaults to full window
    :type dims: list (4 elements)
    :param colors: color index to use - defaults to redblue
    :type colors: cmap
    :param fractions: fraction names
    :type fractions: list
    :param proteins: protein names
    :type proteins: list
    :param protColors: a color map used to label the protein names with group colors
    :type protColors: cmap
    :param cIndex: a list of groupIds for the proteins
    :type cIndex: list
    :param fig: where to plot the axes (which figure); defaults to new figure
    :type fig: matplotlib figure
    :returns:  an axes

    """
    if fig is None:
        fig = pylab.figure()
    axData = fig.add_axes(dims)
    for i in range(len(fractions)):
        axData.text(i, -0.5 , ' '+str(fractions[i]), rotation=270, verticalalignment="top", horizontalalignment="center", fontsize=12)
    for i in range(len(proteins)):
        axData.text(-0.75, i, '  '+str(proteins[i]), verticalalignment="center", horizontalalignment="right", fontsize=12)

    figData = axData.matshow(data, aspect='auto', origin='lower', cmap=colors, vmin=0, vmax=1.25)
    #fig.colorbar(figData)
    axData.set_xticks([])
    axData.set_yticks([])

    return figData


if __name__ == '__main__':
####initialize stuff####
    colors = pylab.cm.autumn
    fileToRead = 'merged_mean_noMSUPellet_no70S.txt'
    showPlots = True
    savePlots = True

    pylab.close('all')

    fileToRead = 'merged_mean.txt'
    rawData = readDataFile(fileToRead, 1)
    rawMap = drawHeatMap(rawData, name="rawMap", x=3, y=15)
    
    fileToRead = 'merged_mean_noMSUPellet.txt'
    rawData = readDataFile(fileToRead, 1)
    rawMap = drawHeatMap(rawData, name="rawMap", x=3, y=18)

    fileToRead = 'merged_mean_noMSUPellet_no70S.txt'
    rawData = readDataFile(fileToRead, 1)
    rawMap = drawHeatMap(rawData, name="rawMap", x=3, y=22.5)
    
    if savePlots:
        figures=[manager.canvas.figure for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
        for i, figure in enumerate(figures):
            figure.savefig('figure%d.eps' % i, bbox_inches='tight')
    if showPlots:
        pylab.show() # show the plot
        
        
