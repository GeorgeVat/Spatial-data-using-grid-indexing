import csv
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt


def get_cells_in_window(bottom_left, top_right,grid,id):
    """
    Update the values of each cell in the grid dictionary with the IDs of the records, contained in each cell, 
    if the cell is overlaped or intersected with the window

    Args:
        bottom_left (tuple): Tuple containing the (x, y) coordinates of the bottom-left cell of the window.
        top_right (tuple): Tuple containing the (x, y) coordinates of the top-right cell of the window.
    """
    for x in range(10):  # Iterate over x-coordinates from 0 to 9
        for y in range(10):  # Iterate over y-coordinates from 0 to 9
            if bottom_left[0] <= x <= top_right[0] and bottom_left[1] <= y <= top_right[1]:
                # If current coordinates (x, y) are within the window, add the id to the specific cell
                grid[(x, y)].append(id)
    
def create_window(axisX,axisY,mbrX,mbrY): 
    """
    Constructing each corner of the window in the grid. Returns a tuple of the 
    bottom left or top right (x,y) coordinates depending on the mbrX,mbrY inputs

    Args:
        axisX (list): list of tuples containing the boundaries of each cell on the X-axis
        axisY (list): list of tuples containing the boundaries of each cell on the Y-axis

        mbrX (tuple): Tuple containing the min or max X coordinate
        mbrY (tuple): Tuple containing the min or max Y coordinate
    """
    for x,points in enumerate(axisX):
        if points[0] <= mbrX and points[1] >= mbrX:
            break
    for y,points in enumerate(axisY):
        if points[0] <= mbrY and points[1] >= mbrY:
            break
    return x,y
            
def referencePoint(recordMBR,axisx,axisy,queryWindow,cell):
    """
    Checking the window and the MBR for intersection and then 
    checking if the botom left corner of the mbr record is contained in the cell
    calculate the new mbr of the inersection between the MBR and the window

    """
    
    left = max(recordMBR[0], queryWindow[0])
    bottom = max(recordMBR[1], queryWindow[1])
    right = min(recordMBR[2], queryWindow[2])
    top = min(recordMBR[3], queryWindow[3])

    if left < right and bottom < top: #check for intersection
        #check if the reference point is inside the cell
        if (axisx[cell[0]][0] <= left and axisx[cell[0]][1] >= left) and (axisy[cell[1]][0]<= bottom and axisy[cell[1]][1]>= bottom): 
            return True
    return False

csvPath = '/Users/georgevatalis/Desktop/Projects/Spatial Data 2023/tiger_roads.csv'

#Read the file and save it into a list
file = open(csvPath, "r")
data = list(csv.reader(file, delimiter=","))
file.close()

data = np.array(data, dtype=object)
data = np.delete(data,(0),axis = 0) #delete the first item from the array (the number of coordinates)

data = [([tuple(map(float, i.split(' '))) for i in list]) for list in data] # creating the (x,y) coordinates into tuples

records = []

#We want to bring the records array in this form 
#[ ID, [ [MBRminX, MBRminY],[MBRmaxX, MBRmaxY] ],[ (x1,y1),(x2,y2)... ] ]

for id,list in enumerate(data,start = 1):

    #returns the tuple with the max or min XY
    MBRminX = min(list, key=lambda tup: tup[0])[0] 
    MBRmaxX = max(list, key=lambda tup: tup[0])[0]

    MBRminY = min(list, key=lambda tup: tup[1])[1]
    MBRmaxY = max(list, key=lambda tup: tup[1])[1]

    records.append([id,[[MBRminX,MBRminY],[MBRmaxX,MBRmaxY]],list])
    

#creating a dictionary with 10x10 cells 
grid = {(i,j):[] for i in range(10) for j in range(10)}

#creating the grid
#finding the min max (x,y) from the whole dataset
maxX = max(map(lambda x: x[1][1][0], records))
maxY = max(map(lambda x: x[1][1][1], records))

minX = min(map(lambda x: x[1][0][0], records))
minY = min(map(lambda x: x[1][0][1], records))

xaxis = []
yaxis = []

#creating the x,y axis 
for i in range(11):
    yaxis.append(minY + i *(maxY-minY)/10 )
    xaxis.append(minX + i *(maxX-minX)/10 )

#convert the x,y axis list into a list of tuples by two
#each tuple represent the x or y boundries of each cell in the grid
xaxis = [(xaxis[i], xaxis[i+1]) for i in range(len(xaxis)-1)]
yaxis = [(yaxis[i], yaxis[i+1]) for i in range(len(yaxis)-1)]


#we construct a window with the MBRs of each record, by finding the bottom left and top rigth corner in the grid
# and then we check what cells are overlaped or intersected with that.
for rec in records:
    #for each record take the MBR values
    MBRmaxY = rec[1][1][1]
    MBRminX = rec[1][0][0]

    MBRmaxX = rec[1][1][0]
    MBRminY = rec[1][0][1]
    
    #left point 
    x,y = create_window(xaxis,yaxis,MBRminX,MBRminY)
    bottomLeftCell = (x,y)

    #right point 
    x,y = create_window(xaxis, yaxis, MBRmaxX, MBRmaxY)
    topRightCell = (x,y)

    #update the values of each cell in the grid dictionary with the IDs of the records, contained in each cell, 
    #if the cell is overlaped or intersected with the window
    get_cells_in_window(bottomLeftCell, topRightCell,grid,rec[0])

#creating a dictionary for the records, The key is the id and the value the rest of 
#the elements in the list, this will help us take the values for each id 
recordsDict = {row[0]: row[1:] for row in records}
        
with open('queries.txt', 'r') as f:
    queries = f.readlines()


for q in queries:
    
    q = q.split(',')
    
    #extracting the MBR from the query
    MBRminX ,MBRmaxX, MBRminY, MBRmaxY  = map(float, q[1].split())
    queryWindow = [MBRminX ,MBRminY, MBRmaxX, MBRmaxY]

    #get the query number
    queryNum = q[0]

    #left point 
    x,y = create_window(xaxis,yaxis,MBRminX,MBRminY)
    bottomLeftCell = (x,y)

    #right point 
    x,y = create_window(xaxis, yaxis, MBRmaxX, MBRmaxY)
    topRightCell = (x,y)

    
    #we get the cells that are overlaped or intersected with the query window
    intercectedCells = []
    for x in range(10):  # Iterate over x-coordinates from 0 to 9
        for y in range(10):  # Iterate over y-coordinates from 0 to 9
            if bottomLeftCell[0] <= x <= topRightCell[0] and bottomLeftCell[1] <= y <= topRightCell[1]:
                intercectedCells.append((x,y))    
    
    #for each id in every cell that is intersected or overlaped 
    #with the query window, check if its intersected with the window
    intercectedIDS = []
    for cell in intercectedCells:
        for id in grid[cell]:

            recordObj = recordsDict[id]
            
            MBRmaxY = recordObj[0][1][1]
            MBRminX = recordObj[0][0][0]

            MBRmaxX = recordObj[0][1][0]
            MBRminY = recordObj[0][0][1]

            recordMBR = [MBRminX, MBRminY, MBRmaxX, MBRmaxY]
            if referencePoint(recordMBR,xaxis,yaxis,queryWindow,cell):
                intercectedIDS.append(id)

    print('Query', queryNum, 'results:')
    print(intercectedIDS)
    print('Cells', len(intercectedCells))
    print('Results', len(intercectedIDS))

