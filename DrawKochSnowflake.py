import math
import sys, argparse
import turtle

class KochSnowFlake:
    '''Produces a list of points defining a KochSnowFlake. The detail of the 
    snowflake depends on the level. A level of 0 produces an equilateral triangle.
    A level of one adds one more triangle to make a six sided figure. '''

    def __init__(self, xc, yc, xv, yv):
        ''' Specifiy the centroid and a single vertex of the triangle that is to 
        start the snowflake.'''
        self.M = (xc, yc)
        self.VertexA = (xv, yv)

        #Shift our vertex and centroid so the centroid is at the origin
        x1 = xv - xc
        y1 = yv - yc

        # Apply formula to obtain the other two vertices
        # We use a matrix to rotate 120 degrees clockwise and counterclockwise
        # to generate an equilateral triangle.
        sin120 = math.sqrt(3)/2.0  
        cos120 = -0.5
        self.VertexB = (cos120 * x1 - sin120 * y1 + xc,
                  sin120 * x1 + cos120 * y1 + yc)
        self.VertexC = (cos120 * x1 + sin120 * y1 + xc,
                  -sin120 * x1 + cos120 * y1 + yc)

    def splitSegment(self, s1, s2):
        ''' Return 4 points given the line segment s1s2. The segment is
        divided into 3 equal parts given by s1-p1, p1-p3, and p3-s2. An
        equilateral triangle is drawn using p1-p3 as its base. The third
        vertex of this triangle is p2. Note that this vertex could be drawn
        on either side of our segment s1-s2. We need to make sure the vertex
        is furthest from the point self.M. This method returns the list
        p1,p2,p3,s2.'''

        x1,y1,x2,y2 = s1[0],s1[1],s2[0],s2[1]
        # Get the equation for the segment
        if x2 != x1:
            m = (y2 - y1)/(x2 - x1)
            # Make slopes that are close to zero equal zero and
            # slopes that are close to vertical equal to vertical
            if abs(m) < 0.00001:
                m = 0
                b = y2
            elif abs(m) > 1000000:
                m = None
                b = None
            else:
                b = y2 - m * x2
        else:
            m = None   # We have a vertical line
            b = None
        
        # Get the midpoint on the base of the triangle we will construct
        pa = ((x2+x1)/2, (y2+y1)/2)

        # Get a line perpindicular to our side that passes through pa
        if m is None:
            ma = 0  # Make a horizontal line
            ba = pa[1]
        elif m == 0:
            ma = None  # Vertical line
            ba = None
        else:
            ma = -1/m
            ba = pa[1] - (ma * pa[0])

        # Find the two endpoints of the base of our new triangle
        if m is not None:
            len = (x2 - x1) / 3.0
            p1 = (x1 + len, m * (x1 + len) + b)
            p3 = (p1[0] + len, m * (p1[0] + len) + b )
        else:
            len = (y2 - y1) / 3.0
            p1 = (x1, y1 + len)
            p3 = (x1, p1[1] + len)

        # Find point p2 on the altitude line that creates a segment the same length as p1pa
        # We scale this distance up by Tan(60)
        deltaY = pa[1] - p1[1]
        if ma is None:
             x = pa[0] 
             y = pa[1] - math.sqrt(3) * (pa[0] - p1[0])
        elif ma == 0:
            # For the perpindicular, we will change x by deltaY
            x = pa[0] + (math.sqrt(3) * deltaY)
            y = ma * x + ba
        else:
            # For the perpindicular, we will change x by deltaY
            x = pa[0] + (math.sqrt(3) * deltaY)
            y = ma * x + ba

        p2 = (x, y)

        return [p1,p2,p3,s2]

    def generateSide(self, vertex1, vertex2, level):
        ''' Generate the points needed to draw one 'side' of a Koch snowflake.
        We start with an equilateral triangle. We give this method each side
        of the triangle to create the snowflake. The method needs to be called
        at least three times - once for each side.'''
        if level > 1:
            points = self.splitSegment(vertex1, vertex2)
            side = self.generateSide(vertex1, points[0], level-1)
            side.extend(self.generateSide(points[0], points[1], level-1))
            side.extend(self.generateSide(points[1], points[2], level-1))
            side.extend(self.generateSide(points[2], vertex2, level-1))
        elif level == 1:
            side = self.splitSegment(vertex1, vertex2)
        else:
            side = [vertex2]

        return side
       
class DrawFlake:
    ''' Uses the Turtle module to draw snowflakes'''

    def __init__(self):
        self.t = turtle.Turtle()
        self.s = turtle.Screen()
        # set cursor shape
        self.t.shape('turtle')
        # set to 80% screen width
        self.s.setup(width=0.8)
        self.s.title("Koch Snowflake")

    def draw(self, xc, yc, xv, yv, level):
        ''' Draw a snowflake with the specified center, vertex, and level '''
        flake = KochSnowFlake(xc, yc, xv, yv) 
        self.t.up()
        self.t.setpos(flake.VertexA)
        self.t.down()
        edges = flake.generateSide(flake.VertexA, flake.VertexB, level)
        for point in edges:
            self.t.setpos(point)
        edges = flake.generateSide(flake.VertexB, flake.VertexC, level)
        for point in edges:
            self.t.setpos(point)
        edges = flake.generateSide(flake.VertexC, flake.VertexA, level)
        for point in edges:
            self.t.setpos(point)


def TestSnowflake():
    ''' Draws a series of concentric Koch snowflakes with consecutive levels '''
    print('Generating snowflakes...')

    flake = DrawFlake()
    color = ('black', 'red', 'green', 'blue')  
    # We will center the snowflake at the origin with one vertex on the y axis
    xc = 0.0
    yc = 0.0
    xv = 0.0
    yv = 20.0
    # Set the number of snowflakes to draw.
    N = 7  
    # Draw our snowflakes
    for i in range(N):
        flake.t.color(color[i%len(color)])
        # Set the altitude of our triangle to ever increasing heights
        yv = yv + i * 10
        # Draw the snowflake using level i
        flake.draw(xc,yc,xv,yv,i)

    # Keep the window open
    flake.s.mainloop()

# call main
if __name__ == '__main__':
    TestSnowflake()        
