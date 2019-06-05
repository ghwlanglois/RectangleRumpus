'''
RectangleRumpus - Nuvalence Programming Exercise
Written by Gabriel Langlois June 2019
'''
'''''''''''''''''''''''''''''''''''''''''''''''''''START OF IMPORTED CODE'''''''''''''''''''''''''''''''''''''''''''''''''''
import os

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
        
'''''''''''''''''''''''''''''''''''''''''''''''''''
| Imported script to restart the program          |
'''''''''''''''''''''''''''''''''''''''''''''''''''
def ResetProgram():
    os.execl(sys.executable, sys.executable, *sys.argv)

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
rectangle_prev = None
intersect_point_ovals = [None, None, None, None]
intersect_point_radius = 10
overlap_rectangle = None
log_text = ""

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
    global rectangle
    
    rec1_contains_rec2 = RectangleContainsAnotherHelper(rec1, rec2)
    rec2_contains_rec1 = RectangleContainsAnotherHelper(rec2, rec1)
    
    if (rec1_contains_rec2 and rec2_contains_rec1):
        return "Orange and Gray are exactly the same"
    elif rec2_contains_rec1:
        if (rectangle_prev != None):
            canvas.tag_raise(rectangle_prev)
        return "Orange contains Gray"
    
    elif rec1_contains_rec2:
        return "Gray contains Orange"
    
    return "Neither rectangle completely contains the other"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Helper Function that determines whether a larger rectangle is contained inside a smaller one            |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def RectangleContainsAnotherHelper(rectangle_big, rectangle_small):
    if (rectangle_small.points[0].x >= rectangle_big.points[0].x and
        rectangle_small.points[3].x <= rectangle_big.points[3].x and
        rectangle_small.points[0].y >= rectangle_big.points[0].y and
        rectangle_small.points[3].y <= rectangle_big.points[3].y):
        return True
    
    return False

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Helper Function that detects if 2 rectangles are adjacent to each other                                     |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def RectanglesAdjacent(rectangle1, rectangle2):
    if (rectangle2.points[1].y >= rectangle1.points[0].y and
        rectangle2.points[3].y <= rectangle1.points[2].y and
        rectangle1.points[0].x == rectangle2.points[1].x):
        return "Orange is Left-Adjacent to Gray"
    
    elif (rectangle2.points[0].y >= rectangle1.points[0].y and
        rectangle2.points[2].y <= rectangle1.points[2].y and
        rectangle1.points[1].x == rectangle2.points[0].x):
        return "Orange is Right-Adjacent to Gray"
    
    elif (rectangle2.points[2].x >= rectangle1.points[0].x and
        rectangle2.points[3].x <= rectangle1.points[1].x and
        rectangle1.points[0].y == rectangle2.points[2].y):
        return "Orange is Top-Adjacent to Gray"
    
    elif (rectangle2.points[0].x >= rectangle1.points[2].x and
        rectangle2.points[1].x <= rectangle1.points[3].x and
        rectangle1.points[2].y == rectangle2.points[0].y):
        return "Orange is Bottom-Adjacent to Gray"
    
    return "Rectangles are not adjacent"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Function that identifies the points of intersection between 2 rectangles in a list, if any                  |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def RectanglesIntersectingPoints(r1, r2):
    points = RectanglesIntersectingPointsHelper(r1, r2)
    if (len(points) == 2):
        return [points[0], points[1]]
    if (len(points) == 4):
        return [points[0], points[1], points[2], points[3]]
    return []

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Helper Function that identifies the points of intersection between 2 rectangles in a list, if any           |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def RectanglesIntersectingPointsHelper(r1, r2):
    global grid_size
    
    points = []
    top_left_corner     =  r2.points[0].x >= r1.points[0].x and\
                           r2.points[0].y >= r1.points[0].y and\
                           r2.points[0].x <= r1.points[3].x and\
                           r2.points[0].y <= r1.points[3].y
    top_right_corner    =  r2.points[1].x >= r1.points[0].x and\
                           r2.points[1].y >= r1.points[0].y and\
                           r2.points[1].x <= r1.points[3].x and\
                           r2.points[1].y <= r1.points[3].y
    bottom_right_corner =  r2.points[3].x >= r1.points[0].x and\
                           r2.points[3].y >= r1.points[0].y and\
                           r2.points[3].x <= r1.points[3].x and\
                           r2.points[3].y <= r1.points[3].y
    bottom_left_corner  =  r2.points[2].x >= r1.points[0].x and\
                           r2.points[2].y >= r1.points[0].y and\
                           r2.points[2].x <= r1.points[3].x and\
                           r2.points[2].y <= r1.points[3].y
    verticals_inside    =  r2.points[0].x >= r1.points[0].x and\
                           r2.points[3].x <= r1.points[3].x and\
                           r2.points[3].y >= r1.points[3].y and\
                           r2.points[0].y <= r1.points[0].y
    horizontals_inside  =  r2.points[0].y >= r1.points[0].y and\
                           r2.points[3].y <= r1.points[3].y and\
                           r2.points[3].x >= r1.points[3].x and\
                           r2.points[0].x <= r1.points[0].x
    
    if (verticals_inside):
        points = [Point(r2.points[0].x, r1.points[0].y),
                  Point(r2.points[1].x, r1.points[0].y),
                  Point(r2.points[0].x, r1.points[3].y),
                  Point(r2.points[1].x, r1.points[3].y)]
    elif (horizontals_inside):
        points = [Point(r1.points[0].x, r2.points[0].y),
                  Point(r1.points[1].x, r2.points[0].y),
                  Point(r1.points[0].x, r2.points[3].y),
                  Point(r1.points[1].x, r2.points[3].y)]
    elif (top_left_corner and bottom_left_corner):
        points = [Point(r1.points[1].x, r2.points[1].y),
                  Point(r1.points[1].x, r2.points[3].y)]
    elif (top_left_corner and top_right_corner):
        points = [Point(r2.points[0].x, r1.points[2].y),
                  Point(r2.points[1].x, r1.points[2].y)]
    elif (top_right_corner and bottom_right_corner):
        points = [Point(r1.points[0].x, r2.points[3].y),
                  Point(r1.points[0].x, r2.points[1].y)]
    elif (bottom_left_corner and bottom_right_corner):
        points = [Point(r2.points[0].x, r1.points[0].y),
                  Point(r2.points[1].x, r1.points[0].y)]
    elif (top_left_corner):
        points = [Point(r1.points[1].x, r2.points[0].y),
                  Point(r2.points[0].x, r1.points[2].y)]
    elif (top_right_corner):
        points = [Point(r1.points[0].x, r2.points[0].y),
                  Point(r2.points[3].x, r1.points[2].y)]      
    elif (bottom_right_corner):
        points = [Point(r1.points[0].x, r2.points[3].y),
                  Point(r2.points[3].x, r1.points[0].y)]    
    elif (bottom_left_corner):
        points = [Point(r1.points[1].x, r2.points[3].y),
                  Point(r2.points[0].x, r1.points[0].y)]
    
    return points

def GetNormalizedRectangle(origin_x, origin_y, mouse_x, mouse_y):
    ##(Base Case) Bottom right quadrant from rectangle's origin
    top_left_point = Point(origin_x, origin_y)
    bottom_right_point = Point(mouse_x, mouse_y)
    
    ##Top left quadrant from rectangle's origin
    if (origin_x > mouse_x and origin_y > mouse_y):
        top_left_point = Point(mouse_x, mouse_y)
        bottom_right_point = Point(origin_x, origin_y)   
        
    ##Bottom left quadrant from rectangle's origin
    elif (origin_x > mouse_x):
        top_left_point = Point(mouse_x, origin_y)
        bottom_right_point = Point(origin_x, mouse_y) 
        
    ##Top right quadrant from rectangle's origin
    elif (origin_y > mouse_y):
        top_left_point = Point(origin_x, mouse_y)
        bottom_right_point = Point(mouse_x, origin_y)
    
    return Rectangle([top_left_point, bottom_right_point])

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
| Function that creates lines on a grid behind the GUI in order to show mouse grid lock                       |
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def DrawGrid(grid_size):
    global canvas, cursor
    
    cursor = canvas.create_oval(-4, -4, 4, 4, fill="white")
    num_rows = canvas.width / grid_size
    num_cols = canvas.height / grid_size
    
    for x in range(num_rows):
        canvas.create_line(grid_size*x, 0, grid_size*x, canvas.height, fill="darkgray", dash=(4, 4))
        
        for y in range(num_cols):
            canvas.create_line(0, grid_size*y, canvas.width, grid_size*y, fill="darkgray", dash=(4, 4))

'''''''''''''''''''''''''''GUI EVENTS'''''''''''''''''''''''
def LeftClick(event):
    global clickindex,\
           prev_coords,\
           rec1,\
           rec2,\
           gui_rectangle,\
           top_right_point,\
           bottom_left_point,\
           rectangle,\
           log_text,\
           intersect_point1_oval,\
           intersect_point2_oval,\
           intersect_point_radius,\
           rectangle_prev,\
           grid_size,\
           overlap_rectangle
           
    input_x = myround(event.x)
    input_y = myround(event.y)
    
    if (clickindex == 0 or clickindex == 2):
        if (clickindex == 2):
            if (gui_rectangle != None):
                canvas.delete(gui_rectangle)
                canvas.delete(top_right_point)
                canvas.delete(bottom_left_point)
                canvas.delete(log_text)
                for oval in intersect_point_ovals:
                    canvas.delete(oval)
                
        top_right_point = canvas.create_oval(input_x-2, input_y-2, input_x+2, input_y+2, fill="white")
        prev_coords = [input_x, input_y]
        
        col = "orange"
        if (clickindex == 0):
            col = "gray"
            
        rectangle = canvas.create_rectangle(prev_coords[0], prev_coords[1], input_x+50, input_y+50, fill=col, width=2, outline="black")
        clickindex = (clickindex + 1) % 4
        
    elif (clickindex == 1 or clickindex == 3):
        bottom_left_point = canvas.create_oval(input_x-2, input_y-2, input_x+2, input_y+2, fill="white")
        
        if (clickindex == 1):
            rec1 = GetNormalizedRectangle(prev_coords[0], prev_coords[1], input_x, input_y)
            rectangle_prev = rectangle
            
        elif (clickindex == 3):
            rec2 = GetNormalizedRectangle(prev_coords[0], prev_coords[1], input_x, input_y)
            gui_rectangle = rectangle
            contains_text = RectangleContainsAnother(rec1, rec2)
            
            if (contains_text == "Neither rectangle completely contains the other"):
                txt = ""
                adjacent_text = RectanglesAdjacent(rec1, rec2)
                intersect_points = RectanglesIntersectingPoints(rec1, rec2)
                
                if (adjacent_text != "Rectangles are not adjacent"):
                    txt = adjacent_text + "\n"
                
                if (intersect_points != []):
                    intersect_point_ovals[0] = canvas.create_oval(intersect_points[0].x-intersect_point_radius, intersect_points[0].y-intersect_point_radius, intersect_points[0].x+intersect_point_radius, intersect_points[0].y+intersect_point_radius, fill="red")
                    intersect_point_ovals[1] = canvas.create_oval(intersect_points[1].x-intersect_point_radius, intersect_points[1].y-intersect_point_radius, intersect_points[1].x+intersect_point_radius, intersect_points[1].y+intersect_point_radius, fill="red")
                    txt += "Gray and Orange intersect at points (" + str(intersect_points[0].x/grid_size) + "," + str(intersect_points[0].y/grid_size) + ") and (" + str(intersect_points[1].x/grid_size) + "," + str(intersect_points[1].y/grid_size) + ")"
                    
                    if (len(intersect_points) > 2):
                        intersect_point_ovals[2] = canvas.create_oval(intersect_points[2].x-intersect_point_radius, intersect_points[2].y-intersect_point_radius, intersect_points[2].x+intersect_point_radius, intersect_points[2].y+intersect_point_radius, fill="red")
                        intersect_point_ovals[3] = canvas.create_oval(intersect_points[3].x-intersect_point_radius, intersect_points[3].y-intersect_point_radius, intersect_points[3].x+intersect_point_radius, intersect_points[3].y+intersect_point_radius, fill="red")                        
                        txt += " and (" + str(intersect_points[2].x/grid_size) + "," + str(intersect_points[2].y/grid_size) + ") and (" + str(intersect_points[3].x/grid_size) + "," + str(intersect_points[3].y/grid_size) + ")"
                
                log_text = canvas.create_text(25, 85, anchor=W, text=txt, fill="white")
                
            else:
                log_text = canvas.create_text(25, 85, anchor=W, text=contains_text, fill="white")
        
        canvas.tag_raise(log_text)
        rectangle = None
        prev_coords = []
        clickindex = 2
        
    canvas.addtag_all("all")
    canvas.tag_raise(cursor)

def MoveMouse(event):
    global mouse_x, mouse_y, cursor, canvas, prev_coords, rectangle
    mouse_x = myround(event.x)
    mouse_y = myround(event.y)
    canvas.coords(cursor, mouse_x-8, mouse_y-8, mouse_x+8, mouse_y+8)
    canvas.tag_raise(cursor)
    if (rectangle != None):
        if (prev_coords[0] == mouse_x and prev_coords[1] == mouse_y):
            canvas.coords(rectangle, prev_coords[0], prev_coords[1], mouse_x+50, mouse_y+50)
        elif (prev_coords[0] == mouse_x):
            canvas.coords(rectangle, prev_coords[0], prev_coords[1], mouse_x+50, mouse_y)
        elif (prev_coords[1] == mouse_y):
            canvas.coords(rectangle, prev_coords[0], prev_coords[1], mouse_x, mouse_y+50)
        else:
            canvas.coords(rectangle, prev_coords[0], prev_coords[1], mouse_x, mouse_y)

grid_size = 50
DrawGrid(grid_size)
ResetButton = Button(canvas, text="Reset", activebackground="black", bg="black", fg="white", padx=25, pady=10, command=ResetProgram)
ResetButton.place(x=25, y=25)

top_left_label = Label(root, text="0,0", bg="black", fg="white")
top_left_label.place(x=4, y=4)
bottom_left_label = Label(root, text="0,"+str(canvas.height/grid_size), bg="black", fg="white")
bottom_left_label.place(x=4, y=canvas.height-24)
top_right_label = Label(root, text=str(canvas.width/grid_size)+",0", bg="black", fg="white")
top_right_label.place(x=canvas.width-32, y=4)
bottom_right_label = Label(root, text=str(canvas.width/grid_size)+","+str(canvas.height/grid_size), bg="black", fg="white")
bottom_right_label.place(x=canvas.width-36, y=canvas.height-24)

root.bind('<Motion>', MoveMouse)
canvas.bind("<Button-1>", LeftClick)
root.mainloop()