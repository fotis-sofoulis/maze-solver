import random
import time

from cell import Cell


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        if seed:
            random.seed(seed)

        self.__create_maze()

    def __create_maze(self):
        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for col in range(self.__num_cols):
            self.__cells.append([])
            for row in range(self.__num_rows):
                self.__cells[col].append(Cell(self.__win))
                self.__draw_cell(col, row)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.02)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True

        while True:
            visit = []
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for di, dj in directions:
                ci, cj = i + di, j + dj
                if 0 <= ci < self.__num_cols and 0 <= cj < self.__num_rows:
                    if not self.__cells[ci][cj].visited:
                        visit.append((ci, cj))

            if len(visit) == 0:
                self.__draw_cell(i, j)
                return

            random_direction = random.randrange(len(visit))
            next_idx = visit[random_direction]

            if next_idx[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False

            if next_idx[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False

            if next_idx[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False

            if next_idx[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False

            self.__break_walls_r(next_idx[0], next_idx[1])

    def __reset_cells_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def reset(self):
        if self.__win:
            self.__win.clear()
        self.__create_maze()
        print("Maze has been reset!")

    def solve(self, method):
        """
        Public-facing solve method. Acts as a dispatcher.
        """
        print(f"--- Solving maze using {method} ---")
        # Reset cell visited state before starting a new solve
        self.__reset_cells_visited()

        # Dispatch to the correct internal solver
        if method == "DFS":
            return self._solve_dfs()
        if method == "BFS":
            return self._solve_bfs()
        if method == "A*":
            return self._solve_astar()

        print(f"Unknown solving method: {method}")
        return False

    def _solve_dfs(self):
        """Placeholder for the Depth-First Search algorithm."""
        print("DFS logic will go here.")
        # When you implement this, it will likely call a recursive helper method.
        # For now, we just return to show it was called.
        return

    def _solve_bfs(self):
        """Placeholder for the Breadth-First Search algorithm."""
        print("BFS logic will go here.")
        return

    def _solve_astar(self):
        """Placeholder for the A* (A-star) algorithm."""
        print("A* logic will go here.")
        return
