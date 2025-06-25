import random
import time
from collections import deque

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

    def solve(self, method=None):
        print(f"--- Solving maze using {method} ---")
        self.__reset_cells_visited()

        if method == "DFS":
            return self._solve_dfs(0, 0)
        if method == "BFS":
            return self._solve_bfs(0, 0)
        if method == "A*":
            return self._solve_astar(0, 0)

        print(f"Unknown solving method: {method}")
        return False

    def _solve_dfs(self, i, j):
        self.__animate()

        self.__cells[i][j].visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        moves = [
            (-1, 0, "has_left_wall"),
            (1, 0, "has_right_wall"),
            (0, -1, "has_top_wall"),
            (0, 1, "has_bottom_wall"),
        ]

        for di, dj, wall in moves:
            ni, nj = i + di, j + dj

            if (
                0 <= ni < self.__num_cols
                and 0 <= nj < self.__num_rows
                and not getattr(self.__cells[i][j], wall)
                and not self.__cells[ni][nj].visited
            ):
                self.__cells[i][j].draw_move(self.__cells[ni][nj])

                if self._solve_dfs(ni, nj):
                    return True
                else:
                    self.__cells[i][j].draw_move(self.__cells[ni][nj], True)

        return False

    def _solve_bfs(self, i, j):
        queue = deque()
        queue.append((i, j))
        self.__cells[i][j].visited = True
        path = {}

        while queue:
            qi, qj = queue.popleft()
            self.__animate()

            if qi == self.__num_cols - 1 and qj == self.__num_rows - 1:
                # goal found reconstruct path
                while (qi, qj) in path:
                    pi, pj = path[(qi, qj)]
                    self.__cells[pi][pj].draw_move(self.__cells[qi][qj])
                    qi, qj = pi, pj
                return True

            # neighbors
            moves = [
                (-1, 0, "has_left_wall"),
                (1, 0, "has_right_wall"),
                (0, -1, "has_top_wall"),
                (0, 1, "has_bottom_wall")
            ]

            for di, dj, wall in moves:
                ni, nj = qi + di, qj + dj
                if (
                    0 <= ni < self.__num_cols and
                    0 <= nj < self.__num_rows and
                    not getattr(self.__cells[qi][qj], wall) and
                    not self.__cells[ni][nj].visited
                ):
                    self.__cells[ni][nj].visited = True
                    path[(ni, nj)] = (qi, qj)
                    queue.append((ni, nj))
                    self.__cells[qi][qj].draw_move(self.__cells[ni][nj])

        return False

    def _solve_astar(self, i, j):
        print("A* logic will go here.")
        return
