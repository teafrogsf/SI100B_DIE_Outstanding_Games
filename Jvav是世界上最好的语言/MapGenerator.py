import time
import random
import typing
import pygame
from Settings import *
from Functions import *

def GenerateRoughMap(roomCount:int,maxSize:int)->typing.List[int]:
    answerList=[]
    nxtx=[1,-1,0,0]
    nxty=[0,0,1,-1]
    sx=random.randint(0,maxSize-1)
    sy=random.randint(0,maxSize-1)
    answerList.append(Hash(sx,sy,maxSize))

    currentCnt=roomCount-1
    times=0
    while currentCnt>0 and times<=1000:
        times+=1
        random.shuffle(answerList)
        for roomHash in answerList:
            x=GetRow(roomHash,maxSize)
            y=GetColumn(roomHash,maxSize)
            randomIList=[0,1,2,3]
            random.shuffle(randomIList)
            for i in randomIList:
                nx=x+nxtx[i]
                ny=y+nxty[i]
                if (nx<0 or nx>=maxSize or ny<0 or ny>=maxSize):
                    continue
                flagNumber=random.random()
                for j in range(3):
                    if (i==j):
                        continue
                    if (not Hash(x+nxtx[j],y+nxty[j],maxSize) in answerList):
                        flagNumber*=2
                if ((times>=950 or flagNumber>=random.random()) and (not Hash(nx,ny,maxSize) in answerList) and currentCnt>0):
                    answerList.append(Hash(nx,ny,maxSize))
                    currentCnt-=1
    return answerList

def GenerateMapShape(levelID:int): # return (mapShape,roomTypes,spawnRoom,bossRoom,roughShape)
    nxtx=[1,-1,0,0,1,1,-1,-1]
    nxty=[0,0,1,-1,1,-1,1,-1]

    roomCount=MapSettings.ROOM_COUNT[levelID]
    maxSize=MapSettings.MAX_MAP_LENGTH[levelID]
    maxLength=MapSettings.MAX_SIDE_LENGTH
    maxType=MapSettings.MAX_TYPE_COUNT
    roomTypes=[] # -1->spawnRoom 0->bossRoom
    roughShape=GenerateRoughMap(roomCount,maxSize)
    mapShape=[[-1 for _tempi in range(maxLength*maxSize)] for _tempj in range(maxLength*maxSize)]
    '''
        -1  Void
        0   Wall
        1   Room
        2   SpawnRoom
        3   BossRoom
        4   Gate
    '''

    # Generate road and create the graph
    minDis=[[100 for _tempi in range(len(roughShape))] for _tempj in range(len(roughShape))]
    for i in range(len(minDis)):
        minDis[i][i]=0
    roomDegree=[0 for _tempi in range(len(roughShape))]
    for i in range(len(roughShape)):
        hashNum=roughShape[i]
        roomX=GetRow(hashNum,maxSize)
        roomY=GetColumn(hashNum,maxSize)
        coorX=maxLength*GetRow(hashNum,maxSize)+maxLength//2
        coorY=maxLength*GetColumn(hashNum,maxSize)+maxLength//2
        for k in range(4):
            nxtRoomX=roomX+nxtx[k]
            nxtRoomY=roomY+nxty[k]
            if (nxtRoomX<0 or nxtRoomX>=maxSize or nxtRoomY<0 or nxtRoomY>=maxSize):
                continue
            nxtRoomHash=Hash(nxtRoomX,nxtRoomY,maxSize)
            if (not nxtRoomHash in roughShape):
                continue
            coorNxtRoomX=maxLength*nxtRoomX+maxLength//2
            coorNxtRoomY=maxLength*nxtRoomY+maxLength//2
            if (nxtx[k]==0):
                for yIter in range(coorY,coorNxtRoomY,sgn(coorNxtRoomY-coorY)):
                    for xIter in range(coorX-2,coorX+3):
                        mapShape[xIter][yIter]=1
            else:
                for xIter in range(coorX,coorNxtRoomX,sgn(coorNxtRoomX-coorX)):
                    for yIter in range(coorY-2,coorY+3):
                        mapShape[xIter][yIter]=1
            # create the graph
            for j in range(len(roughShape)):
                if (roughShape[j]==nxtRoomHash):
                    minDis[i][j]=1
                    minDis[j][i]=1
                    roomDegree[i]+=1
                    roomDegree[j]+=1
                    break
        
    # Get the spawn and boss room
    for k in range(len(minDis)):
        for i in range(len(minDis)):
            for j in range(len(minDis)):
                if (minDis[i][j]>minDis[i][k]+minDis[k][j]):
                    minDis[i][j]=minDis[i][k]+minDis[k][j]
    spawnRoom=0
    bossRoom=1
    for i in range(len(roughShape)):
        for j in range(len(roughShape)):
            if (minDis[i][j]>minDis[spawnRoom][bossRoom]):
                spawnRoom=i
                bossRoom=j
            if (minDis[i][j]==minDis[spawnRoom][bossRoom]):
                if (max(roomDegree[i],roomDegree[j])<max(roomDegree[spawnRoom],roomDegree[bossRoom])):
                    spawnRoom=i
                    bossRoom=j
    
    # Generate Room
    for i in range(len(roughShape)):
        hashNum=roughShape[i]
        coorX=maxLength*GetRow(hashNum,maxSize)+maxLength//2
        coorY=maxLength*GetColumn(hashNum,maxSize)+maxLength//2
        curType=random.randint(0,maxType-1)
        roomLength=MapSettings.ROOM_LENGTH[curType]
        groundType=1
        if (i==spawnRoom):
            curType=-1
            roomLength=MapSettings.SPAWN_ROOM_LENGTH
            groundType=2
        if (i==bossRoom):
            curType=-2
            roomLength=MapSettings.BOSS_ROOM_LENGTH
            groundType=3
        roomTypes.append(curType)
        for x in range(coorX-roomLength//2,coorX+1+roomLength//2):
            for y in range(coorY-roomLength//2,coorY+1+roomLength//2):
                mapShape[x][y]=groundType
        
    # Generate Wall
    for xIter in range(maxLength*maxSize):
        for yIter in range(maxLength*maxSize):
            if (mapShape[xIter][yIter]>0):
                continue
            for i in range(8):
                nxtPointX=xIter+nxtx[i]
                nxtPointY=yIter+nxty[i]
                if (nxtPointX<0 or nxtPointX>=maxLength*maxSize or nxtPointY<0 or nxtPointY>=maxLength*maxSize):
                    continue
                if (mapShape[nxtPointX][nxtPointY]<=0):
                    continue
                mapShape[xIter][yIter]=0
    
    # Generate Gate
    for i in range(len(roughShape)):
        hashNum=roughShape[i]
        if (roomTypes[i]>=0):
            roomLength=MapSettings.ROOM_LENGTH[roomTypes[i]]
        elif (roomTypes[i]==-1):
            roomLength=MapSettings.SPAWN_ROOM_LENGTH
        else:
            roomLength=MapSettings.BOSS_ROOM_LENGTH
        coorX=maxLength*GetRow(hashNum,maxSize)+maxLength//2
        coorY=maxLength*GetColumn(hashNum,maxSize)+maxLength//2
        for xIter in range(coorX-1-roomLength//2,coorX+2+roomLength//2):
            for yIter in range(coorY-1-roomLength//2,coorY+2+roomLength//2):
                if (abs(xIter-coorX)<=roomLength//2 and abs(yIter-coorY)<=roomLength//2):
                    continue
                if (mapShape[xIter][yIter]<1):
                    continue
                mapShape[xIter][yIter]=4
    '''
    # TEST BEGIN
    print(roughShape)
    print(roomTypes)
    # TESTEND
    '''
    return (mapShape,roomTypes,roughShape[spawnRoom],roughShape[bossRoom],roughShape)

def GenerateMap(mapShape,LevelID:int):
    groundImages=[pygame.image.load(tile) for tile in MapImagePaths.GROUNDS[LevelID]]
    wallImages=[pygame.image.load(tile) for tile in MapImagePaths.WALLS[LevelID]]
    groundImages=[pygame.transform.scale(image,(SceneSettings.tileWidth,SceneSettings.tileHeight)) for image in groundImages]
    wallImages=[pygame.transform.scale(image,(SceneSettings.tileWidth,SceneSettings.tileHeight)) for image in wallImages]
    voidImage=pygame.transform.scale(pygame.image.load(MapImagePaths.VOID),(SceneSettings.tileWidth,SceneSettings.tileHeight))
    gateImage=pygame.transform.scale(pygame.image.load(MapImagePaths.GATE),(SceneSettings.tileWidth,SceneSettings.tileHeight))
    
    mapObj=[]
    borders=[]
    for xIter in range(len(mapShape)):
        rowObj=[]
        for yIter in range(len(mapShape)):
            if (mapShape[xIter][yIter]==-1): # Void
                rowObj.append(voidImage)
            elif (mapShape[xIter][yIter]==0): # Wall
                rowObj.append(wallImages[random.randint(0,len(wallImages)-1)])
                borders.append((xIter, yIter))
            elif (mapShape[xIter][yIter]==4): # Gate
                rowObj.append(gateImage)
            else:
                rowObj.append(groundImages[random.randint(0,len(groundImages)-1)])
        mapObj.append(rowObj)
    return mapObj,borders

'''
# TEST BEGIN
a,b,c,d,e=GenerateMapShape(0)
#print(len(GenerateMap(a,0)[0]))
with open('temp.txt','w',encoding='utf-8') as f:
    for i in range(len(a)):
        x=a[i]
        for j in range(len(x)):
            num=a[i][j]
            if (num==-1):
                f.write(' ')
            if (num==0):
                f.write('#')
            if (num==1):
                f.write('*')
            if (num==2):
                f.write('s')
            if (num==3):
                f.write('b')
            if (num==4):
                f.write('g')
        f.write('\n')
# TEST END
'''