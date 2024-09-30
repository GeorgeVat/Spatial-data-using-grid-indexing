# Spatial Data Using Grid Indexing

## Overview

This project aims to implement an efficient indexing technique for spatial data by leveraging a grid-based indexing approach. The task is to create a spatial index for a set of US road coordinates (represented as linestrings) and then perform efficient spatial queries on this data.

### Dataset Overview: `tiger_roads.csv`

The dataset, `tiger_roads.csv`, contains the coordinates of **35,667** linestrings representing roads across the United States. While some roads may appear more than once, each instance is considered unique for this task. 

- **File Format:** 
  - The first line contains the number of linestrings.
  - Each subsequent line contains the sequence of coordinates `(X, Y)` for a road, with each pair separated by a comma.

### Task Outline

The goal is to build a **spatial index** using a **grid** to divide the space into smaller sections (cells). This will allow us to efficiently store and search through the spatial data using **Minimum Bounding Rectangles (MBRs)** of the linestrings.

### Steps to Implement

1. **Grid Construction:**
   - The spatial area covered by the roads will be divided into a grid of **10 x 10 = 100 cells**, where each cell is a rectangle of equal size.
   - To achieve this, the range of values for each coordinate (X and Y) is divided into 10 equal intervals.

2. **Reading and Storing Spatial Data:**
   - For each linestring in the dataset:
     - Assign a unique **identifier** corresponding to its line number in `tiger_roads.csv` (ignoring the first line with the count).
     - Compute the **Minimum Bounding Rectangle (MBR)**, i.e., the smallest rectangle that fully encloses the linestring.
     - Store:
       - The identifier.
       - The MBR (min, max points).
       - The actual points that make up the linestring.
   - Each MBR is then assigned to the cells of the grid that it intersects. Since some MBRs may span across multiple cells, they are duplicated and stored in every cell they touch.

3. **Query Handling:**
   - The program will process **window queries** from a file named `queries.txt`. Each query defines a rectangular window, and the goal is to find all linestrings whose MBR intersects with this window.
   
4. **Query Execution:**
   - For each query:
     - Identify the grid cells that intersect with the query window. Cells that have no overlap with the window are ignored.
     - For each relevant cell:
       - Retrieve the stored objects.
       - Check if their MBRs intersect with the query window.
     - Some objects might appear in multiple cells due to overlapping MBRs. To ensure unique results:
       - Assign a **reference point** to each object, defined as the lower-left corner of the intersection between its MBR and the query window.
       - An object will only be reported if its reference point lies inside the current cell being examined.

5. **Output:**
   - For each query, the program will output:
     - The number of objects whose MBR intersects with the query window.
     - The list of object identifiers for these objects.

### Key Concepts

- **Linestring:** A sequence of points representing a road segment.
- **MBR (Minimum Bounding Rectangle):** The smallest rectangle that fully encloses a spatial object.
- **Grid Indexing:** A spatial indexing technique that divides the space into a grid of fixed-size cells to accelerate spatial searches.
- **Window Query:** A spatial query that defines a rectangular window, aiming to find all objects that intersect with it.

### Considerations

- Objects might be stored in multiple cells, so care must be taken to avoid duplicate reporting in query results.
- The reference point strategy helps ensure that each object is reported only once per query.

By using this grid-based indexing approach, spatial queries on the large dataset of roads can be handled much more efficiently than searching through all objects sequentially.

---

This solution aims to provide both efficient indexing and fast query response times for spatial data, leveraging the simplicity and power of grid-based spatial indexing.
