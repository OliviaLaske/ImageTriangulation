# Imports
import math
import matplotlib
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import numpy as np
import random
import pylab as pl
from matplotlib import collections as mc

# Plot formatting
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
fontsize = 18
params = {
   'axes.labelsize': fontsize,
   'font.size': fontsize,
   'legend.fontsize': 12,
   'xtick.labelsize': fontsize,
   'ytick.labelsize': fontsize,
   'axes.titlesize':fontsize,
   'lines.linewidth':1,  
   'xtick.direction':'in',
   'ytick.direction':'in',
   'font.family':'Serif',
   'font.serif':'Hoefler Text',
   'axes.grid':False,
   'figure.figsize': (6.75, 4),
   'figure.dpi':250,
   'mathtext.fontset':'cm'
}

for param in params.keys():
    matplotlib.rcParams[param] = params[param]

class Point:
    '''
    Represents a point
    '''
    def __init__(self, x, y):
        '''
        Initialize point

        PARAMETERS
        ----------
        x : double
            x-coordinate of point
        y: double
            y-coordinate of point
        '''
        self.x = x
        self.y = y
        self.point = [x, y]
            
    def findEdge(self, edges):
        '''
        Determines which existing edge the point lies on

        PARAMETERS
        ----------
        edges : array
            array of edges to search
        
        RETURNS
        -------
        edge
            the edge the point is on
            0 if none
        '''
        for edge in edges:
            # Get coordinates of points defining edge
            Ax = edge.A[0]
            Ay = edge.A[1]
            Bx = edge.B[0]
            By = edge.B[1]
            if Ax == Bx: # vertical edge
                if self.x == Ax and self.x == Bx:
                    return edge
            elif Ay == By: # horizontal edge
                if self.y == Ay and self.y == By:
                    return edge
            else: # diagonal edge
                m = (By - Ay)/(Bx - Ax) # slope of edge
                if m > 0: # positive slope
                    # if point fits equation of line passing through edge and is within edge bounds
                    if self.y == m*self.x - m*Ax + Ay and self.x >= Ax and self.x <= Bx and self.y >= Ay and self.y <= By:
                        return edge
                elif m < 0: # negative slope
                    # if point fits equation of line passing through edge and is within edge bounds
                    if self.y == m*self.x - m*Ax + Ay and self.x >= Ax and self.x <= Bx and self.y <= Ay and self.y >= By:
                        return edge
                else:
                    continue
        return 0
                
    def inTriangle(self, triangles, edges):
        '''
        Determines which existing triangle the point is in

        PARAMETERS
        ----------
        triangles : array
            array of triangles to search

        edges : array
            array of existing edges

        RETURNS
        -------
        array
            the triangle the point is in
            if between triangles, the triangles the point is adjacent to
        '''
        between = []
        for triangle in triangles:
            try: # point is in triangle
                # Connect point with triangle vertices
                tABP = Triangle(Point(triangle.A[0], triangle.A[1]), Point(triangle.B[0], triangle.B[1]), self)
                tBCP = Triangle(Point(triangle.B[0], triangle.B[1]), Point(triangle.C[0], triangle.C[1]), self)
                tCAP = Triangle(Point(triangle.C[0], triangle.C[1]), Point(triangle.A[0], triangle.A[1]), self)
                areaABP = tABP.area
                areaBCP = tBCP.area
                areaCAP = tCAP.area
                if(areaABP + areaBCP + areaCAP == triangle.area):
                    PDist = math.dist(self.point, triangle.centroid)
                    ADist = math.dist(triangle.A, triangle.centroid)
                    BDist = math.dist(triangle.B, triangle.centroid)
                    CDist = math.dist(triangle.C, triangle.centroid)
                    if PDist <= max([ADist, BDist, CDist]): # point is a valid distance from triangle centroid
                        return [triangle]
            except: # point is on edge
                onEdge = self.findEdge(edges) # determine which edge the point is on
                if onEdge == 0: # point outside bounds
                    continue
                nextTo = onEdge.findAdjacent(triangles) # determine which triangles the edge is adjacent to
                for adjacentTriangle in nextTo:
                    between.append(adjacentTriangle)
        return between
        
class Edge:
    '''
    Represents an edge
    '''
    def __init__(self, point1, point2):
        '''
        Initialize edge

        PARAMETERS
        ----------
        point1 : Point
            first endpoint of edge
        point2 : Point
            second endpoint of edge
        '''
        self.points = sorted([point1.point, point2.point])
        self.A = self.points[0]
        self.B = self.points[1]
        self.length = math.sqrt((self.B[0] - self.A[0])**2 + (self.B[1] - self.A[1])**2)
        
    def findAdjacent(self, triangles):
        '''
        Finds triangles adjacent to the edge

        PARAMETERS
        ----------
        triangles : array
            array of triangles to search

        RETURNS
        -------
        array
            array of adjacent triangles
        '''
        adjacent = []
        for triangle in triangles:
            if self.points in triangle.edges: # edge is in triangle
                adjacent.append(triangle)
        return adjacent

class Triangle:
    '''
    Represents a triangle
    '''
    def __init__(self, point1, point2, point3):
        '''
        Initialize triangle

        PARAMETERS
        ----------
        point1 : Point
            first triangle vertex
        point2 : Point
            second triangle vertex
        point3 : Point
            third triangle vertex
        '''
        # Triangle points
        self.points = sorted([point1.point, point2.point, point3.point])
        self.A = self.points[0]
        self.B = self.points[1]
        self.C = self.points[2]
        
        # Triangle edges
        self.edgeAB = Edge(Point(self.A[0], self.A[1]), Point(self.B[0], self.B[1])).points
        self.edgeBC = Edge(Point(self.B[0], self.B[1]), Point(self.C[0], self.C[1])).points
        self.edgeCA = Edge(Point(self.C[0], self.C[1]), Point(self.A[0], self.A[1])).points
        self.edges = [self.edgeAB, self.edgeBC, self.edgeCA]
    
        # Triangle area
        ux = self.A[0] - self.C[0]
        uy = self.A[1] - self.C[1]
        vx = self.B[0] - self.C[0]
        vy = self.B[1] - self.C[1]
        self.area = abs((ux*vy - uy*vx)/2)
        
        # Triangle centroid coordinates
        self.centroid = [(self.A[0] + self.B[0] + self.C[0])/3, (self.A[1] + self.B[1] + self.C[1])/3]
        
        # Length of each triangle edge
        lAB = Edge(Point(self.A[0], self.A[1]), Point(self.B[0], self.B[1])).length
        lBC = Edge(Point(self.B[0], self.B[1]), Point(self.C[0], self.C[1])).length
        lCA = Edge(Point(self.C[0], self.C[1]), Point(self.A[0], self.A[1])).length
        
        # Triangle angles
        self.angleA = math.acos((lAB**2 + lCA**2 - lBC**2)/(2*lAB*lCA))
        self.angleB = math.acos((lBC**2 + lAB**2 - lCA**2)/(2*lBC*lAB))
        self.angleC = math.acos((lCA**2 + lBC**2 - lAB**2)/(2*lCA*lBC))
        
        # Radius of the triangle circumcircle
        self.cRadius = lBC/(2*math.sin(self.angleA))

        # Triangle circumcenter
        self.ox = (self.A[0]*math.sin(2*self.angleA) + self.B[0]*math.sin(2*self.angleB) + self.C[0]*math.sin(2*self.angleC))/(math.sin(2*self.angleA) + math.sin(2*self.angleB) + math.sin(2*self.angleC))
        self.oy = (self.A[1]*math.sin(2*self.angleA) + self.B[1]*math.sin(2*self.angleB) + self.C[1]*math.sin(2*self.angleC))/(math.sin(2*self.angleA) + math.sin(2*self.angleB) + math.sin(2*self.angleC))
    
    def findAdjacent(self, edge, triangles):
        '''
        Finds the triangle adjacent along the specified edge

        PARAMETERS
        ----------
        edge : Edge
            specified edge
        triangles : array
            array of triangles to search
        
        RETURNS
        -------
        array
            triangle adjacent along the specified edge
        '''
        if(edge.points not in self.edges): # only allow an edge in the triangle
            print('Invalid input')
            return []
        for triangle in triangles:
            if triangle.points != self.points: # triangle cannot be adjacent to itself
                edgeAB = triangle.edgeAB
                edgeBC = triangle.edgeBC
                edgeCA = triangle.edgeCA
                edge = edge.points
                if edgeAB == edge or edgeBC == edge or edgeCA == edge: # shares an edge with the triangle
                    return triangle
        return []
    
# Generate randomized point cloud
S = []
numPoints = 100
xMin = 0
xMax = 1000
yMin = 0
yMax = 1000
for i in range(numPoints):
    x = random.randint(xMin, xMax)
    y = random.randint(yMin, yMax)
    if [x, y] in S:
        x = random.randint(xMin + 1, xMax - 1)
        y = random.randint(yMin + 1, yMax - 1)
    S.append([x, y])

S.append([xMin, yMin])
S.append([xMin, yMax])
S.append([xMax, yMin])
S.append([xMax, yMax])

# Initialization
points = []
edges = []
triangles = []

# Starting points
p1 = Point(xMin, yMin)
p2 = Point(xMin, yMax)
p3 = Point(xMax, yMax)
p4 = Point(xMax, yMin)

points.append(p1)
points.append(p2)
points.append(p3)
points.append(p4)

# Starting edges
edges.append(Edge(p1, p2))
edges.append(Edge(p2, p3))
edges.append(Edge(p3, p1))
edges.append(Edge(p1, p4))
edges.append(Edge(p3, p4))

# Starting triangles
triangles.append(Triangle(p1, p2, p3))
triangles.append(Triangle(p1, p3, p4))

# Transfer to array of added points
S.remove(p1.point)
S.remove(p2.point)
S.remove(p3.point)
S.remove(p4.point)

def findIllegalEdges(edge, addedPoint):
    '''
    Determines if specified edge is illegal when a point is added

    PARAMETERS
    ----------
    edge : Edge
        specified edge
    addedPoint : Point
        newly added point
    '''
    adjacentTriangles = edge.findAdjacent(triangles) # triangle adjacent to edge form a quadrilateral with a potentially illegal edge
    if len(adjacentTriangles) == 2: # point is not on convex hull of point cloud
        t1 = adjacentTriangles[0]
        t2 = adjacentTriangles[1]
        for point in t1.points:
            if point not in t2.points:
                t1Unique = point
        for point in t2.points:
            if point not in t1.points:
                t2Unique = point
        sharedPoints = edge.points # points defining the shared edge between the two triangles, existing edge
        nonSharedPoints = [t1Unique, t2Unique] # points unique to each triangle, edge to be flipped if illegal
        testingPoint = t1Unique
        if testingPoint == addedPoint:
            testingPoint = t2Unique # define testing point as the newly added point
        X = sharedPoints[0]
        Y = sharedPoints[1]
        # Determine if testing point is in circumcircle of other three points
        if math.dist([t1.ox, t1.oy], [t2Unique[0], t2Unique[1]]) < t1.cRadius or math.dist([t2.ox, t2.oy], [t1Unique[0], t1Unique[1]]) < t2.cRadius:
            for addedEdge in edges:
                if edge.points == addedEdge.points:
                    edges.remove(addedEdge) # remove original edge
            edges.append(Edge(Point(t1Unique[0], t1Unique[1]), Point(t2Unique[0], t2Unique[1]))) # flip edge
            # Replace original triangles with newly created ones
            triangles.remove(t1)
            triangles.remove(t2)
            triangles.append(Triangle(Point(t1Unique[0], t1Unique[1]), Point(t2Unique[0], t2Unique[1]), Point(X[0], X[1])))
            triangles.append(Triangle(Point(t1Unique[0], t1Unique[1]), Point(t2Unique[0], t2Unique[1]), Point(Y[0], Y[1])))
            # Look for newly created illegal edges
            findIllegalEdges(Edge(Point(edge.points[0][0], edge.points[0][1]), Point(testingPoint[0], testingPoint[1])), addedPoint)
            findIllegalEdges(Edge(Point(edge.points[1][0], edge.points[1][1]), Point(testingPoint[0], testingPoint[1])), addedPoint)

while len(S) > 0:
    P = S.pop() # add point
    point = Point(P[0], P[1])
    points.append(point)
    triangle = point.inTriangle(triangles, edges) # determine which triangle the added point is in
    if len(triangle) == 1 and point.findEdge(edges) == 0: # point is inside triangle
        triangle = triangle[0]
        pointA = Point(triangle.A[0], triangle.A[1])
        pointB = Point(triangle.B[0], triangle.B[1])
        pointC = Point(triangle.C[0], triangle.C[1])
        # Connect point with triangle vertices
        edgePA = Edge(point, pointA)
        edgePB = Edge(point, pointB)
        edgePC = Edge(point, pointC)
        edges.append(edgePA)
        edges.append(edgePB)
        edges.append(edgePC)
        triangles.append(Triangle(point, pointA, pointB))
        triangles.append(Triangle(point, pointB, pointC))
        triangles.append(Triangle(point, pointC, pointA))
        triangles.remove(triangle)
        # Flip illegal edges
        findIllegalEdges(Edge(pointA, pointB), point)   
        findIllegalEdges(Edge(pointB, pointC), point)
        findIllegalEdges(Edge(pointC, pointA), point)
    else: # point is on edge
        onEdge = point.findEdge(edges) # edge the point is on
        edges.remove(onEdge) # remove edge (since it will be added back later)
        if len(triangle) == 1: # point is on convex hull of point cloud
            sharedPoints = onEdge.points
            for vertex in triangle[0].points:
                if vertex not in sharedPoints:
                    unique = vertex # point of triangle not on convex hull
            X = sharedPoints[0]
            Y = sharedPoints[1]
            pointA = Point(X[0], X[1])
            pointB = Point(Y[0], Y[1])
            pointC = Point(unique[0], unique[1])
            # Connect point to edge endpoints and unique
            edgePA = Edge(point, pointA)
            edgePB = Edge(point, pointB)
            edgePC = Edge(point, pointC)
            edges.append(edgePA)
            edges.append(edgePB)
            edges.append(edgePC)
            triangles.append(Triangle(point, pointA, pointC))
            triangles.append(Triangle(point, pointB, pointC))
            triangles.remove(triangle[0])
            # Flip illegal edges
            findIllegalEdges(Edge(pointA, pointC), point)
            findIllegalEdges(Edge(pointB, pointC), point)
        else: # point is on edge and is not on convex hull of point cloud
            sharedPoints = []
            for vertex in triangle[0].points:
                if vertex not in triangle[1].points:
                    t1Unique = vertex
                else:
                    sharedPoints.append(vertex) # vertex in onEdge
            for vertex in triangle[1].points:
                if vertex not in triangle[0].points:
                    t2Unique = vertex
            nonSharedPoints = [t1Unique, t2Unique] # triangle vertices not part of onEdge
            X = sharedPoints[0]
            Y = sharedPoints[1]
            # Reorder points either clockwise or counterclockwise
            pointA = Point(X[0], X[1])
            pointB = Point(t1Unique[0], t1Unique[1])
            pointC = Point(Y[0], Y[1])
            pointD = Point(t2Unique[0], t2Unique[1])
            # Connect point with four vertices
            edgePA = Edge(point, pointA)
            edgePB = Edge(point, pointB)
            edgePC = Edge(point, pointC)
            edgePD = Edge(point, pointD)
            edges.append(edgePA)
            edges.append(edgePB)
            edges.append(edgePC)
            edges.append(edgePD)
            triangles.append(Triangle(point, pointA, pointB))
            triangles.append(Triangle(point, pointB, pointC))
            triangles.append(Triangle(point, pointC, pointD))
            triangles.append(Triangle(point, pointD, pointA))
            triangles.remove(triangle[0])
            triangles.remove(triangle[1])
            # Flip illegal edges
            findIllegalEdges(Edge(pointA, pointB), point)   
            findIllegalEdges(Edge(pointB, pointC), point)
            findIllegalEdges(Edge(pointC, pointD), point)
            findIllegalEdges(Edge(pointD, pointA), point)
