"""
Created on Mon Apr  1 23:13:53 2013

@author: jhdavis
"""

import pylab
import vizLib
import qMS
import qMSDefs
import glob
import numpy

def plotDataSetsFiles(files, names, num, den, title, yLabel, colors, subunits=None, saveName=None, 
                 yMax=1.25, figSize=(22,5), median=False, legendLoc='upper left', legend=True,
                legendCols=3, normProtein=None, markerSize=None, noFill=False, mew=1):

    ax = vizLib.makePlotWithFileList(files, num, den, subunits=subunits, yMax=yMax, 
                                     names=names, colors=colors, figSize=figSize, 
                                     median=median, normProtein=normProtein, markerSize=markerSize,
                                     noFill=noFill, mew=mew)

    if legend:
        pylab.legend(loc=legendLoc, ncol=legendCols)
    ax.set_title(title, multialignment='center')
    ax.set_ylabel(yLabel)
    pylab.tight_layout()
    if not (saveName is None):
        pylab.savefig(saveName)
    return ax
    
    
def plotDataSetsStatsDictDict(statsDictDict, yLabel, subunits=None, saveName=None,
                   yMax=1.25, median=False, namesList=None, colors=None,
                   figSize=(22,5), markerSize=None, noFill=False, mew=1,legend=True,
                   legendLoc='upper left', legendCols=3, title="noTitle"):

    ax = vizLib.makePlotWithStatsDictDict(statsDictDict, subunits=subunits, yMax=yMax, 
                         median=median, namesList=namesList, colors=colors, figSize=figSize, markerSize=markerSize, noFill=noFill, mew=mew)
    if legend:
        pylab.legend(loc=legendLoc, ncol=legendCols)
    ax.set_title(title, multialignment='center')
    ax.set_ylabel(yLabel)
    pylab.tight_layout()
    if not (saveName is None):
        pylab.savefig(saveName)
    return ax

def calculateMedian(statsDictDict, orderedListOfDictKeys, subunits, defaultValue=0.0):
    proteinList = {}    
    for p in subunits:
            proteinList[p] = []
    
    for n in orderedListOfDictKeys:
        for p in subunits:
            try:
                proteinList[p].append(qMS.getProtMedValue(statsDictDict[n], p))
            except KeyError:
                proteinList[p].append(defaultValue)
    return proteinList

def correctAndPlotDataSets(refSet, filesToPlot, plotNames, num, den, yLabel, subunits, yMax=1.25,
                           median=False, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, saveName=None, legend=True,
                           legendLoc='upper left', legendcols=4, title='noTitle'):

    if colors is None:
        colors = [pylab.cm.jet(float(i)/float(len(filesToPlot))) for i in range(len(filesToPlot))]

    correctedDFsDict = qMS.correctListOfFiles(refSet, filesToPlot)
    correctedStats = qMS.multiStatsDictFromDF(correctedDFsDict, num, den, 
                                              namesList=None, normalization=normalization, 
                                              offset=offset, normProtein=normProtein)
    namesList = [[filesToPlot[i], plotNames[i]] for i in range(0, len(plotNames))]
    
    plotDataSetsStatsDictDict(correctedStats, yLabel, subunits=subunits, saveName=saveName,
                   yMax=yMax, median=median, namesList=namesList, colors=colors,
                   figSize=figSize, markerSize=markerSize, noFill=noFill, mew=mew,
                   legendLoc=legendLoc, legendCols=legendcols, title=title, legend=legend)

##################Initialize Varibles###########################    
if __name__ == "__main__":
    vizLib.setRcs(scale=15, legendScale=15)
    
    rootPath = '/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/'    
    
    filesRefSet = qMS.sort_nicely([i for i in glob.glob(rootPath+'refSets/*.csv')])
    filesStdCurve = qMS.sort_nicely([i for i in glob.glob(rootPath+'stdCurve/*.csv')])
    filesWTGrad = qMS.sort_nicely([i for i in glob.glob(rootPath+'wtGradient/*.csv')])
    files1hrGrad = qMS.sort_nicely([i for i in glob.glob(rootPath+'1hrGradient/*.csv')])
    files6hrGrad = qMS.sort_nicely([i for i in glob.glob(rootPath+'6hrGradient/*.csv')])

    '''
    print [i.split('/')[-1] for i in filesRefSet]
    print [i.split('/')[-1] for i in filesStdCurve]
    print [i.split('/')[-1] for i in filesWTGrad]
    print [i.split('/')[-1] for i in files1hrGrad]
    print [i.split('/')[-1] for i in files6hrGrad]
    '''

    figWidth = 22
    largeSubunit = qMSDefs.positionLabels50S[1:]
    smallSubunit = qMSDefs.positionLabels30S[1:]
    allSubunits = smallSubunit+largeSubunit[1:]
    colors = [pylab.cm.jet(float(i)/float(len(filesStdCurve))) for i in range(len(filesStdCurve))]

##################Plot the datasets########################### 
    pylab.close('all')

    yMax=1.25
    figSize=(22,5)
    median=False    
    
    num = ['AMP_U']
    den = ['AMP_S', 'AMP_U']
    yLabel = '14N/[14N+15N]'
    
    refNames = ['Spike Alone : run 1', 'Spike Alone : run 2', 'Spike Alone : run 3']
    stdCurveNames = ['80 pmol', '40 pmol', '20 pmol', '10 pmol', '5 pmol', '2.5 pmol', '1.25 pmol', '0 pmol']
    wtFracNames = ['34', '36', '38', '40', '42', '44', '46', '48', '50', '52', '54', '56', '58', '62']
    fracNames1hr = ['30', '32', '34', '36', '38', '40', '42', '44', '46', '48', '50', '52', '54', '58']
    fracNames6hr = ['31', '33', '35', '37', '38', '41', '43', '45', '47', '49', '51', '60',]

    '''
    plotDataSetsFiles(filesRefSet, refNames, num, den, 'Spike Alone', yLabel,
                               colors=None, subunits=allSubunits, saveName=None, yMax=0.5, 
                               figSize=figSize, median=median, legendLoc='upper left',
                               legendCols=3, normProtein=None, markerSize=10, noFill=False, mew=2)    
    
    
    plotDataSetsFiles(filesStdCurve, stdCurveNames, num, den, 'Standard curve [uncorrected]', yLabel, 
                               colors=None, subunits=allSubunits, saveName=None, yMax=yMax, 
                               figSize=figSize, median=median, legendLoc='upper left', 
                               legendCols=4, normProtein=None, markerSize=10, noFill=False, mew=2)


    correctAndPlotDataSets(filesRefSet[1], filesStdCurve, stdCurveNames, num, den, yLabel, allSubunits, yMax=1.25,
                           median=False, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, saveName=None,
                           legendLoc='upper left', legendcols=4, title='Standard curve [corrected]')
    '''
    '''
    correctAndPlotDataSets(filesRefSet[1], filesWTGrad, wtFracNames, num, den, yLabel, largeSubunit, yMax=0.8,
                           median=False, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='WT gradient [corrected]', saveName='wt_L_corr.png')
    correctAndPlotDataSets(filesRefSet[1], filesWTGrad, wtFracNames, num, den, yLabel, largeSubunit, yMax=0.8,
                           median=True, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='WT gradient [corrected_median]', saveName='wt_L_corr_med.png')
    correctAndPlotDataSets(filesRefSet[1], filesWTGrad, wtFracNames, num, den, yLabel, smallSubunit, yMax=0.8,
                           median=False, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='WT gradient [corrected]', saveName='wt_S_corr.png')
    correctAndPlotDataSets(filesRefSet[1], filesWTGrad, wtFracNames, num, den, yLabel, smallSubunit, yMax=0.8,
                           median=True, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='WT gradient [corrected_median]', saveName='wt_S_corr_med.png')
                           
    correctAndPlotDataSets(filesRefSet[1], files1hrGrad, fracNames1hr, num, den, yLabel, largeSubunit, yMax=0.8,
                           median=False, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='1 hr gradient [corrected]', saveName='1hr_L_corr.png')
    correctAndPlotDataSets(filesRefSet[1], files1hrGrad, fracNames1hr, num, den, yLabel, largeSubunit, yMax=0.8,
                           median=True, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='1 hr gradient [corrected_median]', saveName='1hr_L_corr_med.png')
    correctAndPlotDataSets(filesRefSet[1], files1hrGrad, fracNames1hr, num, den, yLabel, smallSubunit, yMax=0.8,
                           median=False, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='1 hr gradient [corrected]', saveName='1hr_S_corr.png')
    correctAndPlotDataSets(filesRefSet[1], files1hrGrad, fracNames1hr, num, den, yLabel, smallSubunit, yMax=0.8,
                           median=True, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='1 hr gradient [corrected_median]', saveName='1hr_S_corr_med.png')
                           
    correctAndPlotDataSets(filesRefSet[1], files6hrGrad, fracNames6hr, num, den, yLabel, largeSubunit, yMax=0.8,
                           median=False, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='6 hr gradient [corrected]', saveName='6hr_L_corr.png')
    correctAndPlotDataSets(filesRefSet[1], files6hrGrad, fracNames6hr, num, den, yLabel, largeSubunit, yMax=0.8,
                           median=True, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='6 hr gradient [corrected_median]', saveName='6hr_L_corr_med.png')
    correctAndPlotDataSets(filesRefSet[1], files6hrGrad, fracNames6hr, num, den, yLabel, smallSubunit, yMax=0.8,
                           median=False, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='6 hr gradient [corrected]', saveName='6hr_S_corr.png')
    correctAndPlotDataSets(filesRefSet[1], files6hrGrad, fracNames6hr, num, den, yLabel, smallSubunit, yMax=0.8,
                           median=True, colors=None, figSize=(22,5), markerSize=10, noFill=False, mew=1,
                           normalization=1.0, normProtein=None, offset=0.0, legend=True,
                           legendLoc='upper left', legendcols=7, title='6 hr gradient [corrected_median]', saveName='6hr_S_corr_med.png')

    '''
    '''
    correctedDFsDict = qMS.correctListOfFiles(filesRefSet[1], filesWTGrad)
    qMS.outputDataMatrixFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/wtSmall.csv', 
                             correctedDFsDict, filesWTGrad, smallSubunit, num, den, 
                             normalization=1.0, offset=0.0)
    qMS.outputDataMatrixFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/wtLarge.csv', 
                             correctedDFsDict, filesWTGrad, largeSubunit, num, den, 
                             normalization=1.0, offset=0.0)
    
    correctedDFsDict = qMS.correctListOfFiles(filesRefSet[1], files1hrGrad)
    qMS.outputDataMatrixFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/1hrSmall.csv', 
                             correctedDFsDict, files1hrGrad, smallSubunit, num, den, 
                             normalization=1.0, offset=0.0)
    qMS.outputDataMatrixFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/1hrLarge.csv', 
                             correctedDFsDict, files1hrGrad, largeSubunit, num, den, 
                             normalization=1.0, offset=0.0)
    
    correctedDFsDict = qMS.correctListOfFiles(filesRefSet[1], files6hrGrad)
    qMS.outputDataMatrixFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/6hrSmall.csv', 
                             correctedDFsDict, files6hrGrad, smallSubunit, num, den, 
                             normalization=1.0, offset=0.0)
    qMS.outputDataMatrixFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/6hrLarge.csv', 
                             correctedDFsDict, files6hrGrad, largeSubunit, num, den, 
                             normalization=1.0, offset=0.0)
    '''
    
    rawData = qMS.readDataFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/wtSmall.csv', 1.0)
    rawMap = vizLib.drawHeatMap(rawData, "wtGradient", nameList=wtFracNames, colors=pylab.cm.autumn, scale='14N/[14N+15N]', saveName='wtSmallHeat.png')
    
    rawData = qMS.readDataFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/wtLarge.csv', 1.0)
    rawMap = vizLib.drawHeatMap(rawData, "wtGradient", nameList=wtFracNames, colors=pylab.cm.autumn, scale='14N/[14N+15N]', saveName='wtLargeHeat.png')
    
    
    rawData = qMS.readDataFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/1hrSmall.csv', 1.0)
    rawMap = vizLib.drawHeatMap(rawData, "1hrGradient", nameList=fracNames1hr, colors=pylab.cm.autumn, scale='14N/[14N+15N]', saveName='1hrSmallHeat.png')
    
    rawData = qMS.readDataFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/1hrLarge.csv', 1.0)
    rawMap = vizLib.drawHeatMap(rawData, "1hrGradient", nameList=fracNames1hr, colors=pylab.cm.autumn, scale='14N/[14N+15N]', saveName='1hrLargeHeat.png')
    
    
    rawData = qMS.readDataFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/6hrSmall.csv', 1.0)
    rawMap = vizLib.drawHeatMap(rawData, "6hrGradient", nameList=fracNames6hr, colors=pylab.cm.autumn, scale='14N/[14N+15N]', saveName='6hrSmallHeat.png')
    
    rawData = qMS.readDataFile('/home/jhdavis/data/2013_08_08-JStokesESITOFAnalysis/6hrLarge.csv', 1.0)
    rawMap = vizLib.drawHeatMap(rawData, "6hrGradient", nameList=fracNames6hr, colors=pylab.cm.autumn, scale='14N/[14N+15N]', saveName='6hrLargeHeat.png')
    
    
    '''
    stdCurveCorrectedDFsDict = qMS.correctListOfFiles(filesRefSet[1], filesStdCurve)
    stdCurveCorrectedStats = qMS.multiStatsDictFromDF(stdCurveCorrectedDFsDict, num, den, 
                                                      namesList=None, normalization=1.0, 
                                                      offset=0.0, normProtein=None)                                                      
    namesList = [[filesStdCurve[i], curveNames[i]] for i in range(0, len(curveNames))]
    
    plotDataSetsStatsDictDict(stdCurveCorrectedStats, yLabel, subunits=allSubunits, saveName=None, normProtein=None,
                   yMax=1.25, median=False, namesList=namesList, colors=None,
                   figSize=(22,5), markerSize=10, noFill=False, mew=1,
                   legendLoc='upper left', legendCols=4, title="Standard curve [corrected]")
    '''
    '''
    num = ['AMP_U']
    den = ['AMP_S']
    yLabel = '14N/15N'

    stdCurveCorrectedDFsDict = qMS.correctListOfFiles(filesRefSet[1], filesStdCurve)
    stdCurveCorrectedStats = qMS.multiStatsDictFromDF(stdCurveCorrectedDFsDict, num, den, 
                                                      namesList=None, normalization=1.0, 
                                                      offset=0.0, normProtein=None)                                                      
    
    values = numpy.array([80, 40, 20, 10, 5, 2.5, 1.25, 0])
    smallSubunitList = calculateMedian(stdCurveCorrectedStats, filesStdCurve, smallSubunit)
    largeSubunitList = calculateMedian(stdCurveCorrectedStats, filesStdCurve, largeSubunit[1:])
    allSubunitList = calculateMedian(stdCurveCorrectedStats, filesStdCurve, allSubunits)
    

    sc = vizLib.proteinScatterPlot(smallSubunitList, values, xMin=-1, xMax=84.0, yMin=-.5, yMax=5.0,
                       title='Small subunit\nstandard curve [corrected]', xLabel='pmol 14N', yLabel=yLabel, colors=None, 
                       figSize=(10,10), markerSize=60, legend=False, linestyle='--', xTicks=[0, 5, 10, 20, 40, 80])    
    sc = vizLib.proteinScatterPlot(largeSubunitList, values, xMin=-1, xMax=84.0, yMin=-.5, yMax=4.0,
                       title='Large subunit\nstandard curve [corrected]', xLabel='pmol 14N', yLabel=yLabel, colors=None, 
                       figSize=(10,10), markerSize=60, legend=False, linestyle='--', xTicks=[0, 5, 10, 20, 40, 80])
    sc = vizLib.proteinScatterPlot(allSubunitList, values, xMin=-1, xMax=84.0, yMin=-.5, yMax=5.0,
                       title='70S subunit\nstandard curve [corrected]', xLabel='pmol 14N', yLabel=yLabel, colors=None, 
                       figSize=(10,10), markerSize=60, legend=False, linestyle='--', xTicks=[0, 5, 10, 20, 40, 80])



    wtCurveCorrectedDFsDict = qMS.correctListOfFiles(filesRefSet[1], filesWTGrad)
    stdCurveCorrectedStats = qMS.multiStatsDictFromDF(stdCurveCorrectedDFsDict, num, den, 
                                                      namesList=None, normalization=1.0, 
                                                      offset=0.0, normProtein=None)                                                      
    namesList = [[filesStdCurve[i], curveNames[i]] for i in range(0, len(curveNames))]
    
    plotDataSetsStatsDictDict(stdCurveCorrectedStats, yLabel, subunits=allSubunits, saveName=None, normProtein=None,
                   yMax=1.25, median=False, namesList=namesList, colors=None,
                   figSize=(22,5), markerSize=10, noFill=False, mew=1,
                   legendLoc='upper left', legendCols=4, title="Standard curve [corrected]")


    wtGradientStats = {}
    wtGradientNamesList = []
    for i in filesWTGrad:
        currentDF = qMS.readIsoCSV(i)
        currentDF = subtractDoubleSpike(refDF, currentDF)
        wtGradientStats[i] = qMS.calcStatsDict(currentDF, num, den)
        wtGradientNamesList.append((i, i.split('/')[-1]))
    
    vizLib.makePlotWithStatsDictList(wtGradientStats, AllProteins=largeSubunit, normProtein=None, yMax=yMax, 
                         median=False, namesList=wtGradientNamesList, colors=colors, figSize=(22,5), markerSize=18, noFill=True, mew=2)
                         
    refDF = qMS.readIsoCSV(filesRefSet[1])
    stdCurveStats = {}
    stdCurveNamesList = []
    for i in filesStdCurve:
        currentDF = qMS.readIsoCSV(i)
        currentDF = subtractDoubleSpike(refDF, currentDF)
        stdCurveStats[i] = qMS.calcStatsDict(currentDF, num, den)
        stdCurveNamesList.append((i, i.split('/')[-1]))
    
    vizLib.makePlotWithStatsDictList(stdCurveStats, AllProteins=largeSubunit, normProtein=None, yMax=yMax, 
                         median=False, namesList=stdCurveNamesList, colors=colors, figSize=(22,5), markerSize=18, noFill=True, mew=2)
    
    wtGradientStats = {}
    wtGradientNamesList = []
    for i in filesWTGrad:
        currentDF = qMS.readIsoCSV(i)
        currentDF = subtractDoubleSpike(refDF, currentDF)
        wtGradientStats[i] = qMS.calcStatsDict(currentDF, num, den)
        wtGradientNamesList.append((i, i.split('/')[-1]))
    
    vizLib.makePlotWithStatsDictList(wtGradientStats, AllProteins=largeSubunit, normProtein=None, yMax=yMax, 
                         median=False, namesList=wtGradientNamesList, colors=colors, figSize=(22,5), markerSize=18, noFill=True, mew=2)
    '''
    pylab.show('all')