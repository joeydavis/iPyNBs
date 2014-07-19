## {{{ http://code.activestate.com/recipes/578123/ (r1)
#!/usr/bin/env python
"""\
SVG.py - Construct/display SVG scenes.

This is an enhanced Version of Rick Muller's Code from http://code.activestate.com/recipes/325823-draw-svg-images-in-python/
"""

import os
import math
display_prog = "display"

class Scene:
    def __init__(self,name="svg",height=768,width=1024):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" height=\"%d\" width=\"%d\" >\n" % (self.height,self.width),
               " <g style=\"fill-opacity:1.0; stroke:black;\n",
               "  stroke-width:1;\">\n"]
        for item in self.items: var += item.strarray()            
        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

    def display(self,prog=display_prog):
        os.system("%s %s" % (prog,self.svgname))
        return        

class Line:
    def __init__(self,start,end,color,width):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" style=\"stroke:%s;stroke-width:%d\"/>\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1],colorstr(self.color),self.width)]

class Circle:
    def __init__(self,center,radius,fill_color,line_color,line_width):
        self.center = center
        self.radius = radius
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
        return

    def strarray(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;stroke:%s;stroke-width:%d\"  />\n" % (colorstr(self.fill_color),colorstr(self.line_color),self.line_width)]

class Ellipse:
    def __init__(self,center,radius_x,radius_y,fill_color,line_color,line_width):
        self.center = center
        self.radiusx = radius_x
        self.radiusy = radius_y
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
    def strarray(self):
        return ["  <ellipse cx=\"%d\" cy=\"%d\" rx=\"%d\" ry=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius_x,self.radius_y),
                "    style=\"fill:%s;stroke:%s;stroke-width:%d\"/>\n" % (colorstr(self.fill_color),colorstr(self.line_color),self.line_width)]

class Polygon:
    def __init__(self,points,fill_color,line_color,line_width):
        self.points = points
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
    def strarray(self):
        polygon="<polygon points=\""
        for point in self.points:
            polygon+=" %d,%d" % (point[0],point[1])
        return [polygon,\
               "\" \nstyle=\"fill:%s;stroke:%s;stroke-width:%d\"/>\n" %\
               (colorstr(self.fill_color),colorstr(self.line_color),self.line_width)]

class Rectangle:
    def __init__(self,origin,height,width,fill_color,line_color,line_width):
        self.origin = origin
        self.height = height
        self.width = width
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_width = line_width
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"fill:%s;stroke:%s;stroke-width:%d\" />\n" %\
                (self.width,colorstr(self.fill_color),colorstr(self.line_color),self.line_width)]

class OuterRectangle:
    def __init__(self,origin,height,width,line_color,line_width):
        self.origin = origin
        self.height = height
        self.width = width
        self.line_color = line_color
        self.line_width = line_width
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"fill:none;stroke:%s;stroke-width:%d\" />\n" %\
                (self.width,colorstr(self.line_color),self.line_width)]

class Text:
    def __init__(self,origin,text,size,color,angle):
        self.origin = origin
        self.text = text
        self.size = size
        self.color = color
        self.angle = angle
        return

    def strarray(self):
        return ["  <text transform=\"rotate(%d)\" x=\"%d\" y=\"%d\" font-family=\"Myriad Pro\" font-size=\"%d\" fill=\"%s\">\n" %\
                (self.angle, self.origin[0],self.origin[1],self.size,colorstr(self.color)),
                "   %s\n" % self.text,
                "  </text>\n"]

def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

def readCDTFileToMatrix(fileName):
    inputFile = open(fileName)
    fileLines = inputFile.readlines()
    i = 0
    matrix = dict()
    for line in fileLines:
        line = line.rstrip('\n')
        tokens = line.split('\t')
        j = 0
        matrix[i] = dict()
        while (j < len(tokens)):
            matrix[i][j] = tokens[j]
            j = j+1
        i = i+1
    return matrix

def readMatrixCDTFileToDict(matrix):
    data = dict()
    i = 4
    while i < len(matrix[0].keys()):
        fracName = matrix[0][i]
        data[fracName] = dict()
        j = 2
        while j < len(matrix.keys()):
            protName = matrix[j][1]
            value = matrix[j][i]
            #if float(value) == -10000000:
            #    value = ''
            data[fracName][protName] = value
            j = j+1
        i = i+1
    return data

def readErrors(fileName, low, scaleZeros):
    inputFile = open(fileName)
    fileLines = inputFile.readlines()
    firstLine = fileLines[0].rstrip('\n')
    fractionNames = firstLine.split('\t')
    errors = dict()
    i = 1
    while (i < len(fractionNames)):
        errors[fractionNames[i]] = dict()
        i = i+1
    j = 1
    while (j < len(fileLines)):
        line = fileLines[j].rstrip('\n')
        tokens = line.split('\t')
        proteinName = tokens[0]
        i = 1
        while (i < len(tokens)):
            if not (tokens[i] == '' or tokens[i] == '#VALUE!' or tokens[i] == '-1' or (float(tokens[i]) == 0.0 and scaleZeros)):
                errors[fractionNames[i]][proteinName] = tokens[i]
            else:
                errors[fractionNames[i]][proteinName] = -1
            i = i+1
        j = j+1
    maxError = 0.0
    for frac in errors.keys():
        for prot in errors[frac].keys():
            if (float(errors[frac][prot]) > float(maxError)):
                maxError = errors[frac][prot]
    for frac in errors.keys():
        for prot in errors[frac].keys():
            errors[frac][prot] = math.fabs(low - float(errors[frac][prot])/float(maxError))
    errors['zzMaxzz'] = float(maxError)
    return errors   

def getFracOrder(CDT):
    fracNames = CDT[0].values()[4:]
    return fracNames

def getProtOrder(CDT):
    i = 2
    prots = []
    proteins = len(CDT.keys())
    while i < proteins:
        protName = CDT[i][1]
        prots.append(protName)
        i = i+1
    return prots

def scaleColor(value, colorZero, colorOne):
    if value > 1:
        value = 1
    colorRange = abs(colorZero - colorOne)
    addition = value*float(colorRange)
    if colorZero < colorOne:
        toReturn = colorZero+int(addition)
    else:
        toReturn = colorZero-int(addition)
    if toReturn < 0 or toReturn >255:
        print "error"
    return toReturn

def writeXScaleValues(scene, number, high, size, low):
    sceneWidth = scene.width
    for i in range(1, number+1, 1):
        width = float(float(i)/float(number))*size
        printValue = math.fabs(low - float(i)/float(number))*high
        scene.add(Rectangle((sceneWidth-7*size,(i+1)*size), size, width, [125,125,125], (0,0,0),2))
        scene.add(Text((sceneWidth-6*size,(i+1)*size+3*size/4), str(printValue)[0:5], size*0.75, (0,0,0),0))
    return scene

def writeYScaleValues(scene, number, high, size, low):
    sceneWidth = scene.width
    for i in range(1, number+1, 1):
        height = float(float(i)/float(number))*size
        printValue = math.fabs(low - float(i)/float(number))*high
        scene.add(Rectangle((sceneWidth-3*size,(i+1)*size), height, size, [125,125,125], (0,0,0),2))
        scene.add(Text((sceneWidth-2*size,(i+1)*size+3*size/4), str(printValue)[0:5], size*0.75, (0,0,0),0))
    return scene



def writeScaleValues(scene, number, lowColor, highColor, lowValue, highValue, size):
    sceneWidth = scene.width
    if number%2 == 1:
        number = number-1
    y = 1
    for i in range(number/2,0,-1):
        fracRange = float(i)/(float(number)/2.0)
        colorr = scaleColor(fracRange, zeroColor[0], highColor[0])
        colorb = scaleColor(fracRange, zeroColor[1], highColor[1])
        colorg = scaleColor(fracRange, zeroColor[2], highColor[2])
        color = [colorr, colorb, colorg]
        scene.add(Rectangle((sceneWidth-11*size, (y+1)*size), size, size, color, (0,0,0),2))
        printValue = highValue*fracRange
        scene.add(Text((sceneWidth-10*size, (y+1)*size+3*size/4), str(printValue)[0:5], size*0.75, (0,0,0),0))
        y = y+1
                  
    scene.add(Rectangle((sceneWidth-11*size, size*(number/2+2)), size, size, zeroColor, (0,0,0),2))
    scene.add(Text((sceneWidth-10*size, (number/2+2)*size+3*size/4), 0.0, size*0.75, (0,0,0),0))

    y = number/2+2
    for i in range(1,number/2+1,1):
        fracRange = float(i)/(float(number)/2.0)
        colorr = scaleColor(fracRange, zeroColor[0], lowColor[0])
        colorb = scaleColor(fracRange, zeroColor[1], lowColor[1])
        colorg = scaleColor(fracRange, zeroColor[2], lowColor[2])
        color = [colorr, colorb, colorg]
        scene.add(Rectangle((sceneWidth-11*size, (y+1)*size), size, size, color, (0,0,0),2))
        printValue = lowValue*fracRange
        scene.add(Text((sceneWidth-10*size, (y+1)*size+3*size/4), str(printValue)[0:6], size*0.75, (0,0,0),0))
        y = y+1
    return scene

def writeFractionLabels(scene, fracOrder, size):
    i = 0
    for frac in fracOrder:
        scene.add(Text(((scene.height-4.9*size), -(i+1)*size-1*size/4), frac, size*0.75, (0,0,0), 90))
        i = i+1
    return scene
    

def writeSquares(data, sizeX, sizeY, fracOrder, protOrder, lowColor, highColor, zeroColor, lowValue, highValue):
    lineSize = size/40
    i = 0
    for protein in protOrder:
        j = 0
        for fraction in fracOrder:
            x = j*size
            y = i*size
            value = data[fraction][protein]
            if not (value == ''):
                sX = sizeX[fraction][protein]*size
                sY = sizeY[fraction][protein]*size
            else:
                sX = size/2
                sY = size/2

            if value == '':
                colorr = 125
                colorb = 125
                colorg = 125
            elif float(value) == 0:
                colorr = zeroColor[0]
                colorg = zeroColor[1]
                colorb = zeroColor[2]
            elif float(value) > 0:
                vR = float(value)/float(highValue)
                colorr = scaleColor(vR, int(zeroColor[0]), int(highColor[0]))
                colorb = scaleColor(vR, int(zeroColor[1]), int(highColor[1]))
                colorg = scaleColor(vR, int(zeroColor[2]), int(highColor[2]))
            elif float(value) < 0:
                vR = float(abs(float(value))/float(abs(lowValue)))
                colorr = scaleColor(vR, zeroColor[0], lowColor[0])
                colorb = scaleColor(vR, zeroColor[1], lowColor[1])
                colorg = scaleColor(vR, zeroColor[2], lowColor[2])
                color = [colorr, colorb, colorg]
            else:
                print "error in datafile"
            color = [colorr, colorb, colorg]
            scene.add(Rectangle(center(x+size,y+size, sX, sY, size),sY, sX,(color),(0,0,0),lineSize))
            #scene.add(OuterRectangle(center(x+size,y+size, size, size, size),size, size,(0,0,0),lineSize))
            j = j+1
        scene.add(Text((x+size*2.1, y+size*1.75),protein, size*0.75, (0,0,0),0))
        i = i+1
    return scene

def center(oriX, oriY, sX, sY, size):
    lineSize = float(size/40)
    xOff = float(math.floor(float(size-sX)/2.0))
    yOff = float(math.floor(float(size-sY)/2.0))+lineSize/2
    return (oriX+xOff, oriY+yOff)

def writeLabels(scene, size, d, x, y):
    width = scene.width
    height = scene.height
    scene.add(Text((width-14*size, -height+4.5*size), d, size*0.5, (0,0,0),90))
    scene.add(Text((width-14*size, -height+0.5*size), x, size*0.5, (0,0,0),90))
    scene.add(Text((width-14*size, -height-3.5*size), y, size*0.5, (0,0,0),90))
    return scene

##############Main Program################
dataName = "medNormL24_45SAnalysisOnly_frac.cdt"
xScaleName = "medNormL24_45SAnalysisOnly_sqrtObs.txt"
yScaleName = "medNormL24_45SAnalysisOnly_sqrtObs.txt"
outputName = "medNormL24_45SAnalysisOnly"


#######Need to be adjusted########
highColor = [255,0,0]
lowColor = [0, 255, 0]
zeroColor = [0, 0, 0]
lowValue = -1
highValue = 1
xLow = 0
yLow = 0
size = 40
scaleNumber = 9
scaleZeros = 1
#######Need to be adjusted########

CDT = readCDTFileToMatrix(dataName)
data = readMatrixCDTFileToDict(CDT)

fracOrder = getFracOrder(CDT)
protOrder = getProtOrder(CDT)
errorX = readErrors(xScaleName, xLow, scaleZeros)
maxErrorX = errorX['zzMaxzz']
errorY = readErrors(yScaleName, yLow, scaleZeros)
maxErrorY = errorY['zzMaxzz']

#######Setup scene########
height = size*len(protOrder)
width = size*len(fracOrder)
sceneWidth = width+16*size
sceneHeight = height + 6*size
scene = Scene(outputName, sceneHeight, sceneWidth)

scene = writeScaleValues(scene, scaleNumber, lowColor, highColor, lowValue,highValue, size)
scene = writeSquares(data, errorX, errorY, fracOrder, protOrder, lowColor, highColor, zeroColor, lowValue, highValue)
scene = writeFractionLabels(scene, fracOrder, size)
scene = writeXScaleValues(scene, scaleNumber, maxErrorX, size, xLow)
scene = writeYScaleValues(scene, scaleNumber, maxErrorY, size, yLow)
scene = writeLabels(scene, size, dataName, xScaleName, yScaleName)

scene.write_svg()
