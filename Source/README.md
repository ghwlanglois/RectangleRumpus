# Rectangle Rumpus

RectangleRumpus allows the user to draw 2 rectangles and determine if:.

  - They intersect, and at which points
  - One contains the other
  - They share a side

# Input

  - Click to place an origin point for the first rectangle
  - Drag and click again to place the opposite corner of the rectangle
  - Repeat the previous two steps to place another rectangle
  - Results will show where they intersect, if they contain one another, and if they share a side

### Imports

Rectangle Rumpus is written by Gabriel Langlois (2019) and uses the following imports:

* [Tkinter] - GUI implementation api
* [os] - Referenced to restart the program
* [re] - Used for parsing strings into numbers
* [ResizingCanvas] - Used to instantiate a dynamic window

This code is open source.

### Running the program

Rectangle Rumpus can be run via the shortcuts in the root folder for Windows and Linux (via python).

### Classes
```sh
class Point:
    x = 0
    y = 0
```
```sh
class Rectangle:
    points = [topleftpoint, toprightpoint, bottomleftpoint, bottomrightpoint]
```

### Functions
```
RectanglesIntersectingPoints(rectangle1, rectangle2)
```
```
RectangleContainsAnother(rectangle1, rectangle2)
```
```
RectanglesAdjacent(rectangle1, rectangle2)
```