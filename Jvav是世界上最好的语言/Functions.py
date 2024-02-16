from Settings import *

def sgn(x:int)->int:
    if (x>0):
        return 1
    elif (x<0):
        return -1
    else:
        return 0

def Hash(row:int,column:int,maxSize:int)->int:
    return row*maxSize+column

def GetRow(hashNumber:int,maxSize:int)->int:
    return hashNumber//maxSize

def GetColumn(hashNumber:int,maxSize:int)->int:
    return hashNumber%maxSize

def CostTextMake(cost:int)->str:
    if (cost>=0):
        return str("Value:")+str(cost)+str(" coins")
    else:
        return str("All coins(>=")+str(-cost)+")"