# Spatial-data-using-grid-indexing
 
Spatial Data

The goal of the assignment is to develop an indexing technique for spatial data using grid and then efficiently search for data.

The tiger_roads.csv  file contains the coordinates of 35667 linestrings which are roads in the US (some roads exist more than once in the dataset, however, we consider each copy as unique). The first line of the file contains the number of linestrings. From the next line onwards, each line has the sequence of coordinates (X Y) of a road, separated by a comma. I  write a program that creates a simple spatial index based on a grid. The grid divides the space covered by the points into 10*10=100 equal-sized rectangles (cells).
I read the records from the file and for each one, storing 
a) an identifier number 
b) the min, max points of its MBR
c) the points of the linestring
The identifier will correspond to the line where the linestring is located in the tiger_roads.csv file. For example, the linestring <-86.449493 32.425501,-86.449391 32.425472,...> will have identifier 1, because it is located on line 1 of the file (without counting the line with the number of linestrings).
To create the grid,I divide the range of values for each coordinate into 10 equal value intervals, creating 100 cells. Then, for each MBR of the objects,I determine which cells of the grid it intersects and assign it to those cells. Some MBRs may touch more than one cell of the grid, so we create copies of them and store them in each cell they touch.
 

Afterwards, the program will read window queries from the file queries.txt and, for each query, it will calculate and print to the output the number of objects and their IDs whose MBR intersects with the window (i.e., has at least one common point with the window).
For each query, the program will examine the contents of each cell that intersects with the window (ignoring completely cells that have no overlap with the window). The program will locate the data of the cell's objects in the memory structure used and will check their MBRs to see if they overlap with the chosen window.
Note that since some objects may exist as duplicates in more than one cell, they may be counted more than once in the final results. To avoid this,I assign the reference point of each object to be the lower left point of the intersection between its MBR and the query window. Then, each individual object will be reported as a result only if its reference point is inside the cell being examined at that moment.

 
