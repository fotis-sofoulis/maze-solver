from graphics import Line, Point


class Cell:
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

        if self.__win is None:
            return

        def draw_wall(condition, p1, p2):
            line = Line(p1, p2)
            if condition:
                self.__win.drawline(line)
            else:
                self.__win.drawline(line, "black")

        draw_wall(self.has_left_wall, Point(x1, y1), Point(x1, y2))
        draw_wall(self.has_right_wall, Point(x2, y1), Point(x2, y2))
        draw_wall(self.has_top_wall, Point(x1, y1), Point(x2, y1))
        draw_wall(self.has_bottom_wall, Point(x1, y2), Point(x2, y2))

    def get_center(self):
        return ((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return
        start = Point(*self.get_center())
        end = Point(*to_cell.get_center())
        fill_color = "gray" if undo else "red"
        line = Line(start, end)
        self.__win.drawline(line, fill_color)
