'''''''''''''''''''''''''''''''''''''''''''''''''''
| Imported script to parse numbers from text      |
'''''''''''''''''''''''''''''''''''''''''''''''''''
import re
def getNumbers(str): 
    array = re.findall(r'[0-9]+', str) 
    return array

'''''''''''''''''''''''''''''''''''''''''''''''''''
| Point Class containing x,y coordinate variables |
'''''''''''''''''''''''''''''''''''''''''''''''''''
class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Rectangle Class containing a list of 2 Points                                               |
| *Assumes order of constructor points argument to be [topleft, bottomright]                  |
| *Automatically populates points list with 4 points extrapolated from constructor arguments  |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class Rectangle:
    points = []
    def __init__(self, points):
        self.points = [points[0],
                       Point(points[1].x, points[0].y),
                       Point(points[0].x, points[1].y),
                       points[1]]

'Function that determines whether a rectangle contains another agnostic to the order depending on size'
def RectangleContainsAnother(rec1, rec2):
    rec1_contains_rec2 = RectangleContainsAnotherHelper(rec1, rec2)
    rec2_contains_rec1 = RectangleContainsAnotherHelper(rec2, rec1)
    if rec2_contains_rec1:
        return " is contained by "
    elif rec1_contains_rec2:
        return " contains "
    else:
        return " does not contain "

'Helper Function that determines whether a larger rectangle is contained inside a smaller one'
def RectangleContainsAnotherHelper(rectangle_big, rectangle_small):
    if (rectangle_small.points[0].x > rectangle_big.points[0].x and
        rectangle_small.points[3].x < rectangle_big.points[3].x and
        rectangle_small.points[0].y > rectangle_big.points[0].y and
        rectangle_small.points[3].y < rectangle_big.points[3].y):
        return True
    return False

'Function that detects if 2 rectangles are adjacent to each other agnostic to their order in the arguments'
def RectanglesAdjacent(rec1, rec2):
    case1 = RectanglesAdjacentHelper(rec1, rec2)
    case2 = RectanglesAdjacentHelper(rec2, rec1)
    if (case1 == "NotAdjacent" and case2 == "NotAdjacent"):
        return " is not adjacent to "
    elif (case2 == "NotAdjacent"):
        return ParseAdjacencyText(case1)
    elif (case1 == "NotAdjacent"):
        return ParseAdjacencyText(case2)
    else:
        return " is not adjacent to "
        
'Parser function to present the user with readable text'
def ParseAdjacencyText(txt):
    if (txt == "LeftAdjacent"):
        return " is Left-Adjacent to "
    if (txt == "RightAdjacent"):
        return " is Right-Adjacent to "
    if (txt == "TopAdjacent"):
        return " is Top-Adjacent to "
    if (txt == "BottomAdjacent"):
        return " is Bottom-Adjacent to "
    
'Helper Function that detects if 2 rectangles are adjacent to each other'
def RectanglesAdjacentHelper(rectangle1, rectangle2):
    if (rectangle2.points[1].y >= rectangle1.points[0].y and
        rectangle2.points[3].y <= rectangle1.points[2].y and
        rectangle1.points[0].x == rectangle2.points[1].x and
        rectangle1.points[2].x == rectangle2.points[3].x):
        return "LeftAdjacent"

    elif (rectangle2.points[0].y >= rectangle1.points[1].y and
        rectangle2.points[2].y <= rectangle1.points[3].y and
        rectangle1.points[1].x == rectangle2.points[0].x and
        rectangle1.points[3].x == rectangle2.points[2].x):
        return "RightAdjacent"
    
    elif (rectangle2.points[2].x >= rectangle1.points[0].x and
        rectangle2.points[3].x <= rectangle1.points[1].x and
        rectangle1.points[0].y == rectangle2.points[2].y and
        rectangle1.points[1].y == rectangle2.points[3].y):
        return "TopAdjacent"
    
    elif (rectangle2.points[0].x >= rectangle1.points[2].x and
        rectangle2.points[1].x <= rectangle1.points[3].x and
        rectangle1.points[2].y == rectangle2.points[0].y and
        rectangle1.points[3].y == rectangle2.points[1].y):
        return "BottomAdjacent"    
    
    else:
        return "NotAdjacent"

'Helper function to determine whether a single point is inside of a rectangle'
def IsSinglePointInsideRectangle(rectangle_points, rectangle_base):
    for p in rectangle_points.points:
        if (p.x >= rectangle_base.points[0].x and
            p.x <= rectangle_base.points[3].x and
            p.y >= rectangle_base.points[0].y and
            p.y <= rectangle_base.points[3].y):
            return True
    return False

'Function that identifies the points of intersection between 2 rectangles in a list, if any'
def RectanglesIntersecting(rectangle1, rectangle2):
    if (IsSinglePointInsideRectangle(rectangle2, rectangle1)):
        return " intersects with "
    return " does not intersect with "

'Input function to ensure that the user enters a valid input before proceeding'
def GetCoordInputFromUser():
    coords = []
    while(coords == []):
        coords = GetValidRectangleInput()
    return coords

'Helper Input Function that queries the user for 2 coordinate point entries to construct a rectangle'
def GetValidRectangleInput():
    coords = []
    txt = raw_input("Type in the top left and bottom right coordinates of the rectangle like so: (1,2) (7,8)\n")
    coords = getNumbers(txt)
    print(coords)
    return [Point(coords[0],coords[1]),Point(coords[2],coords[3])]

'''''''''''''''''''''''''''MAIN'''''''''''''''''''''''''''''
rec_name1 = raw_input("What would you like to name your first rectangle?\n")
coords1 = GetCoordInputFromUser()
rec1 = Rectangle(coords1)
rec_name2 = raw_input("What would you like to name your second rectangle?\n")
coords2 = GetCoordInputFromUser()
rec2 = Rectangle(coords2)
print(rec_name1 + RectanglesIntersecting(rec1, rec2) + rec_name2)
print(rec_name1 + RectangleContainsAnother(rec1, rec2) + rec_name2)
print(rec_name1 + RectanglesAdjacent(rec1, rec2) + rec_name2)
'''''''''''''''''''''''''''END MAIN'''''''''''''''''''''''''''''