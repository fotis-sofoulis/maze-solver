from tkinter import LEFT, Button, Frame, Label, Radiobutton, StringVar

from graphics import Window
from maze import Maze


def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)
    root = win._Window__root

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)

    controls_frame = Frame(root)
    controls_frame.pack(side="bottom", fill="x", pady=10)

    selection_frame = Frame(controls_frame)
    selection_frame.pack(side="top", fill="x", pady=5)

    algorithm_var = StringVar(value="DFS")

    Label(selection_frame, text="Algorithm:", font=("Arial", 12)).pack(side=LEFT)

    Radiobutton(
        selection_frame,
        text="DFS",
        variable=algorithm_var,
        value="DFS",
        font=("Arial", 10),
    ).pack(side=LEFT)
    Radiobutton(
        selection_frame,
        text="BFS",
        variable=algorithm_var,
        value="BFS",
        font=("Arial", 10),
    ).pack(side=LEFT)
    Radiobutton(
        selection_frame,
        text="A*",
        variable=algorithm_var,
        value="A*",
        font=("Arial", 10),
    ).pack(side=LEFT)

    button_frame = Frame(controls_frame)
    button_frame.pack(side="bottom", fill="x", pady=5)

    reset_button = Button(
        button_frame, text="Reset Maze", font=("Arial", 12, "bold"), command=maze.reset
    )
    reset_button.pack(side="left", padx=(250, 10))

    go_button = Button(
        button_frame, text="Go!", font=("Arial", 12, "bold"), command=maze.solve
    )
    go_button.pack(side="right", padx=(10, 250))

    root.update_idletasks()

    total_height = screen_y + controls_frame.winfo_reqheight() + 50

    root.geometry(f"{screen_x}x{total_height}")

    win.wait_for_close()


if __name__ == "__main__":
    main()
