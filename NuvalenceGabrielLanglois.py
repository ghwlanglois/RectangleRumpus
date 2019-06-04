'''
RectangleRumpus - Developed for Nuvalence
Written by Gabriel Langlois June 2019
'''
'''''''''''''''''''''''''''''''''''''''''''''''''''START OF IMPORTED CODE'''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''
| Imported Tkinter for GUI implementation         |
'''''''''''''''''''''''''''''''''''''''''''''''''''
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

'''''''''''''''''''''''''''''''''''''''''''''''''''
| Imported script to parse numbers from text      |
'''''''''''''''''''''''''''''''''''''''''''''''''''
import re
def getNumbers(str): 
    array = re.findall(r'[0-9]+', str) 
    return array

'''''''''''''''''''''''''''''''''''''''''''''''''''
| Imported script to round to the nearest mutiple |
'''''''''''''''''''''''''''''''''''''''''''''''''''
def myround(x, base=50):
    return int(base * round(float(x)/base))

'''''''''''''''''''''''''''''''''''''''''''''''''''
| Imported script to resize window dynamically    |
'''''''''''''''''''''''''''''''''''''''''''''''''''
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)
'''''''''''''''''''''''''''''''''''''''''''''''''''END OF IMPORTED CODE'''''''''''''''''''''''''''''''''''''''''''''''''''

'''''''''''''''''''''''''''''''''''''''''''''''''''
| Initialize the GUI                              |
'''''''''''''''''''''''''''''''''''''''''''''''''''
clickindex = 0
root = Tk()
myframe = Frame(root)
myframe.pack(fill=BOTH, expand=YES)
canvas = ResizingCanvas(myframe,width=1250, height=750, bg="black", highlightthickness=0)
canvas.pack(fill=BOTH, expand=YES)

mouse_x = 0
mouse_y = 0
prev_coords = []
gui_rectangle = None
top_right_point = None
bottom_left_point = None
cursor = None
rectangle = None

'''''''''''''''''''''''''''''''''''''''''''''''''''
| Point Class containing x,y coordinate variables |
'''''''''''''''''''''''''''''''''''''''''''''''''''
class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Rectangle Class containing a list of 2 Points                                                           |
| *Assumes order of constructor points argument to be [topleft, bottomright]                              |
| *Automatically populates points list with 4 points extrapolated from constructor arguments              |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class Rectangle:
    points = []
    def __init__(self, points):
        self.points = [points[0],
                       Point(points[1].x, points[0].y),
                       Point(points[0].x, points[1].y),
                       points[1]]
        
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Function that determines whether a rectangle contains another agnostic to the order depending on size   |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def RectangleContainsAnother(rec1, rec2):
    rec1_contains_rec2 = RectangleContainsAnotherHelper(rec1, rec2)
    rec2_contains_rec1 = RectangleContainsAnotherHelper(rec2, rec1)
    if rec2_contains_rec1:
        return "Orange contains Gray"
    elif rec1_contains_rec2:
        return "Gray contains Orange"
    else:
        return "Neither rectangle contains the other"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Helper Function that determines whether a larger rectangle is contained inside a smaller one            |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def RectangleContainsAnotherHelper(rectangle_big, rectangle_small):
    if (rectangle_small.points[0].x > rectangle_big.points[0].x and
        rectangle_small.points[3].x < rectangle_big.points[3].x and
        rectangle_small.points[0].y > rectangle_big.points[0].y and
        rectangle_small.points[3].y < rectangle_big.points[3].y):
        return True
    return False

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Function that detects if 2 rectangles are adjacent to each other agnostic to their order in the arguments   |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def RectanglesAdjacent(rec1, rec2):
    case1 = RectanglesAdjacentHelper(rec1, rec2)
    case2 = RectanglesAdjacentHelper(rec2, rec1)
    if (case1 == "NotAdjacent" and case2 == "NotAdjacent"):
        return "Rectangles are not adjacent"
    elif (case1 == "NotAdjacent"):
        return ParseAdjacencyText(case2)
    elif (case2 == "NotAdjacent"):
        return ParseAdjacencyText(case1)
    else:
        return "Rectangles are not adjacent"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Parser function to present the user with readable text                                                      |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def ParseAdjacencyText(txt):
    if (txt == "LeftAdjacent"):
        return "Orange is Left-Adjacent to Gray"
    if (txt == "RightAdjacent"):
        return "Orange is Right-Adjacent to Gray"
    if (txt == "TopAdjacent"):
        return "Orange is Top-Adjacent to Gray"
    if (txt == "BottomAdjacent"):
        return "Orange is Bottom-Adjacent to Gray"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Helper Function that detects if 2 rectangles are adjacent to each other                                     |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Function that identifies the points of intersection between 2 rectangles in a list, if any                  |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def RectanglesIntersecting(rectangle1, rectangle2):
    return "Orange does not intersect Gray"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Function that creates lines on a grid behind the GUI in order to show mouse grid lock                       |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def DrawGrid(grid_size):
    global canvas, cursor
    cursor = canvas.create_oval(-4, -4, 4, 4, fill="white")
    num_rows = canvas.width / grid_size
    num_cols = canvas.height / grid_size
    for x in range(num_rows):
        canvas.create_line(grid_size*x, 0, grid_size*x, canvas.height, fill="white", dash=(4, 4))
        for y in range(num_cols):
            canvas.create_line(0, grid_size*y, canvas.width, grid_size*y, fill="white", dash=(4, 4))

'''''''''''''''''''''''''''GUI EVENTS'''''''''''''''''''''''
def LeftClick(event):
    global clickindex, prev_coords, rec1, rec2, gui_rectangle, top_right_point, bottom_left_point, rectangle
    input_x = myround(event.x)
    input_y = myround(event.y)
    if (clickindex == 0 or clickindex == 2):
        if (clickindex == 2):
            if (gui_rectangle != None):
                canvas.delete(gui_rectangle)
                canvas.delete(top_right_point)
                canvas.delete(bottom_left_point)
        top_right_point = canvas.create_oval(input_x-2, input_y-2, input_x+2, input_y+2, fill="white")
        prev_coords = [input_x, input_y]
        col = "orange"
        if (clickindex == 0):
            col = "darkgray"
        rectangle = canvas.create_rectangle(prev_coords[0], prev_coords[1], input_x+50, input_y+50, fill=col)
        clickindex = (clickindex + 1) % 4
    elif (clickindex == 1 or clickindex == 3):
        bottom_left_point = canvas.create_oval(input_x-2, input_y-2, input_x+2, input_y+2, fill="white")
        if (clickindex == 1):
            rec1 = Rectangle([Point(prev_coords[0], prev_coords[1]), Point(input_x, input_y)])
        elif (clickindex == 3):
            rec2 = Rectangle([Point(prev_coords[0], prev_coords[1]), Point(input_x, input_y)])
            gui_rectangle = rectangle
            print(RectanglesIntersecting(rec1, rec2))
            print(RectangleContainsAnother(rec1, rec2))
            print(RectanglesAdjacent(rec1, rec2))
        rectangle = None
        prev_coords = []
        clickindex = 2
    canvas.addtag_all("all")
    canvas.tag_raise(cursor)

def MoveMouse(event):
    global mouse_x, mouse_y, cursor, canvas, prev_coords, rectangle
    mouse_x = myround(event.x)
    mouse_y = myround(event.y)
    canvas.coords(cursor, mouse_x-10, mouse_y-10, mouse_x+10, mouse_y+10)
    canvas.tag_raise(cursor)
    if (rectangle != None):
        if (mouse_x < prev_coords[0] or mouse_y <prev_coords[1]):
            mouse_x = prev_coords[0]+50
            mouse_y = prev_coords[1]+50
        canvas.coords(rectangle, prev_coords[0], prev_coords[1], mouse_x, mouse_y)
    
DrawGrid(50)
root.bind('<Motion>', MoveMouse)
canvas.bind("<Button-1>", LeftClick)
root.mainloop()