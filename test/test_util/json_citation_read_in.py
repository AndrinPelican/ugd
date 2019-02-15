import numpy as np
import random
#
# creates the original graph for estimaton container
time_layer_list = [2018,2015,2012,2009]
def createGraph(imputPaperList, timeLayerList, firstJornalName):

    # preparation
    var_dict = {}
    has_dict = {}
    i = 0
    for paperNode in imputPaperList:
        if timerestriction_violation(paperNode):
            continue
        has_dict[paperNode['id']] = i
        i += 1
    adj_m = np.zeros((has_dict.__len__(), has_dict.__len__()))

    i = 0
    for paperNode in imputPaperList:
        if timerestriction_violation(paperNode):
            continue
        # Variable filling up
        inerdict = {}
        inerdict['journal'] = paperNode['journal']
        inerdict['timelayer']= isInTimelayer(paperNode['year'],time_layer_list)
        inerdict['rand'] = np.random.binomial(1, 0.5)
        var_dict[i] = inerdict

        for outhash in paperNode['references']:
            if outhash in has_dict:
                j = has_dict[outhash]
            else:
                continue # papers out of the timerange
            if j==i:
                print('selfcitaion')
                continue
            outnode = getNodeFromHash(outhash, imputPaperList)
            if isInTimelayer(paperNode['year'],time_layer_list)>=isInTimelayer(outnode['year'],time_layer_list):
                print('citation in timelayer violation')
                continue
            adj_m[i,j] = 1
        i +=1
    return adj_m, var_dict

def timerestriction_violation(paperNode):
    if int(paperNode['year']) < 2009:
        return True
    if int(paperNode['year']) >= 2018:
        return True
    return False



def isInTimelayer(year,timeLayerList):
    year = int(year)
    layer = None
    for i, iterYear in enumerate(timeLayerList[0:-1]):
        if year < timeLayerList[i] and year >= timeLayerList[i+1]:
            layer = i
            return layer
    return layer

def getNodeFromHash(has,imputPaperList ):
    for node in imputPaperList:
        if node['id']==has:
            return node
