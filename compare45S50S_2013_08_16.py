"""
Created on Mon Apr  1 23:13:53 2013

@author: jhdavis
"""

import pylab
import vizLib
import numpy
import qMS
import glob

def plotDataSets(files, names, num, den, subunits, title, yLabel, colors, saveName=None, 
                 yMax=1.25, figSize=(22,7), median=False, legendLoc='upper left',
                legendCols=3, normProtein=None):
                    
    ax = vizLib.makePlotWithFileList(files, num, den, AllProteins=subunits, yMax=yMax, 
                                     names=names, colors=colors, figSize=figSize, 
                                     median=median, normProtein=normProtein)
                                     
    pylab.legend(loc=legendLoc, ncol=legendCols)
    pylab.xticks(numpy.arange(1,len(AllSubunits)+1,1), [item[4:] for item in AllSubunits], rotation=45)
    ax.set_title(title, multialignment='center')
    ax.set_ylabel(yLabel)
    pylab.tight_layout()
    if not (saveName is None):
        pylab.savefig(saveName)
    return ax

##################Initialize Varibles###########################    
if __name__ == "__main__":
    vizLib.setRcs(scale=12)
    
    ##########GLOBAL VARIABLES##########
    SmallSubunit = ['BSubS02', 'BSubS03', 'BSubS04', 'BSubS05', 'BSubS06', 'BSubS07', 'BSubS08', 'BSubS09', 'BSubS10',
                    'BSubS11', 'BSubS12', 'BSubS13', 'BSubS14', 'BSubS15', 'BSubS16', 'BSubS17', 'BSubS18', 'BSubS20']
                    
    LargeSubunit = ['BSubL01', 'BSubL02', 'BSubL03', 'BSubL04', 'BSubL05', 'BSubL06', 'BSubL09', 'BSubL10', 'BSubL11',
                    'BSubL12', 'BSubL13', 'BSubL14', 'BSubL15', 'BSubL16', 'BSubL17', 'BSubL18', 'BSubL19', 'BSubL20', 'BSubL21',
                    'BSubL22', 'BSubL23', 'BSubL24', 'BSubL27', 'BSubL28', 'BSubL29', 'BSubL30', 'BSubL31a', 'BSubL32',
                    'BSubL33a', 'BSubL34', 'BSubL35', 'BSubL36']
    Inter45S =      ['BSubL01', 'BSubL02', 'BSubL03', 'BSubL04', 'BSubL05', 'BSubL06', 'BSubL10', 'BSubL11',
                    'BSubL12', 'BSubL13', 'BSubL14', 'BSubL15', 'BSubL17', 'BSubL18', 'BSubL19', 'BSubL20', 'BSubL21',
                    'BSubL22', 'BSubL23', 'BSubL24', 'BSubL29', 'BSubL30']
    
    AllSubunits = LargeSubunit + SmallSubunit
    
    rootPath = '/home/jhdavis/McMasterMSUDataSets/45Svs50S/'
    
    figWidth = 22
    
   ##########Open Files##########
    files50SIF2 = qMS.sort_nicely([i for i in glob.glob(rootPath+'45Sfiltered/*.csv')])
    files45S = qMS.sort_nicely([i for i in glob.glob(rootPath+'50Sfiltered/*.csv')])
    
    filesMy70S = qMS.sort_nicely([i for i in glob.glob(rootPath+'my70Sfiltered/*.csv')])
    filesMy50S = qMS.sort_nicely([i for i in glob.glob(rootPath+'my50Sfiltered/*.csv')])
    
    files50SIF2Pulse = qMS.sort_nicely([i for i in glob.glob(rootPath+'45Sfiltered/pulse/*.csv')])
    files45SPulse = qMS.sort_nicely([i for i in glob.glob(rootPath+'50Sfiltered/pulse/*.csv')])
    
    names50SIF2 = qMS.sort_nicely([i.split('/')[-1] for i in glob.glob(rootPath+'45Sfiltered/*.csv')])
    names45S = qMS.sort_nicely([i.split('/')[-1] for i in glob.glob(rootPath+'50Sfiltered/*.csv')])

    namesMy70S = qMS.sort_nicely([i.split('/')[-1] for i in glob.glob(rootPath+'my70Sfiltered/*.csv')])
    namesMy50S = qMS.sort_nicely([i.split('/')[-1] for i in glob.glob(rootPath+'my50Sfiltered/*.csv')])
    
    names50SIF2Pulse = qMS.sort_nicely([i.split('/')[-1] for i in glob.glob(rootPath+'45Sfiltered/pulse/*.csv')])
    names45SPulse = qMS.sort_nicely([i.split('/')[-1] for i in glob.glob(rootPath+'50Sfiltered/pulse/*.csv')])
    
    reds = ['#fee5d9', '#fcbba1', '#fc9272', '#fb6a4a', '#de2d26', '#a50f15']
    blues = ['#eff3ff', '#c6dbef', '#93cae1', '#6baed6', '#3182bd', '#08519c']
    
##################Extract the data###########################
    num = ['AMP_U']
    den = ['AMP_U', 'AMP_S']
    dataByProtein70S = qMS.multiStatsDict(files45S, num, den)

##################Plot the datasets###########################
    
    pylab.close('all')    

    yMax=1.5
    figSize=(figWidth,figWidth/3.0)
    median=False    
    
    num = ['AMP_U']
    den = ['AMP_U', 'AMP_S']
    filtPlots_45S = plotDataSets(files45S, names45S, num, den, AllSubunits, '45S', 'U/[U+S]', reds,
                 saveName=None, yMax=yMax, figSize=figSize, median=median, legendLoc='upper left', legendCols=2, normProtein='BSubL24')

    filtPlots_50SIF2 = plotDataSets(files50SIF2, names50SIF2, num, den, AllSubunits, '50S IF2', 'U/[U+S]', blues,
                 saveName=None, yMax=yMax, figSize=figSize, median=median, legendLoc='upper left', legendCols=2, normProtein='BSubL24')
    
    filtPlots_my70S = plotDataSets(filesMy70S, namesMy70S, num, den, AllSubunits, '50S JHD', 'U/[U+S]', blues,
                 saveName=None, yMax=yMax, figSize=figSize, median=median, legendLoc='upper left', legendCols=2, normProtein='BSubL24')

    filtPlots_my50S = plotDataSets(filesMy50S, namesMy50S, num, den, AllSubunits, '70S JHD', 'U/[U+S]', blues,
                 saveName=None, yMax=yMax, figSize=figSize, median=median, legendLoc='upper left', legendCols=2, normProtein='BSubL24')    
    
    num = ['AMP_L', 'AMP_U']
    den = ['AMP_U', 'AMP_L', 'AMP_S']
    
    filtPlots_45SPulse = plotDataSets(files45SPulse, names45SPulse, num, den, AllSubunits, '45S pulse', '[U+L]/[U+L+S]', reds,
                 saveName=None, yMax=yMax, figSize=figSize, median=median, legendLoc='upper left', legendCols=2, normProtein='BSubL01')

    filtPlots_50SIF2Pulse = plotDataSets(files50SIF2Pulse, names50SIF2Pulse, num, den, AllSubunits, '50S IF2 pulse', '[U+L/[U+L+S]', blues,
                 saveName=None, yMax=yMax, figSize=figSize, median=median, legendLoc='upper left', legendCols=2, normProtein='BSubL01')
##################Merge data###########################
    num = ['AMP_U']
    den = ['AMP_U', 'AMP_S']
    normProtein='BSubL24'
    
    merged45 = qMS.mergeFiles(files45S, num, den, normProtein)
    merged50 = qMS.mergeFiles(files50SIF2, num, den, normProtein)
    verifiedZero = ['BSubL16', 'BSubL28', 'BSubL36', 'BSubL31a']    
    for i in verifiedZero:
        merged45[i] = numpy.array([0.0])

##################Plot protein inventory data###########################

    myPlot = vizLib.plotStatsDict(merged45, name='45SMerged', proteins=LargeSubunit, offset=0.4, markerSize=12, color='#e31a1c', yMax = 1.5, median=False)
    myPlot = vizLib.addStatsDictToPlot(merged50, myPlot, name='50SMerged', offset=0.6, markerSize=12, color='#377db8', median=False)
    myPlot.set_ylabel('protein occupancy\nnormalized to L24', multialignment='center')
    myPlot.set_title('protein occupancy 45S vs. 50S')
    pylab.legend(loc='lower left', prop={'size':12})
    pylab.tight_layout()

    pylab.show('all')