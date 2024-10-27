import tkinter as tk  # library for GUI
import numpy as np  # for matrix manipulation
import random  # generate random tiles and numbers
import time  # for timer

class Game2048:  # main logic
    def __init__(self, master):  # self allows access to attributes and methods within the class
        self.master = master  # This is the main window of the GUI, passed as an argument when creating the game.
        self.master.title("2048 Puzzle")  # name of the game

        # Initializations
        self.game_grid = np.zeros((4, 4), dtype=int)  # 4x4 grid (matrix) of zeros using NumPy, where each cell represents a tile on the grid. Initially, all cells are empty (set to 0).
        self.add_random_tile()  # Calls the function to add two random tiles (2 or 4)
        self.add_random_tile()
        self.score = 0  # Initializes the score at 0.
        self.time_elapsed = 0  # Initializes the time counter at 0.
        self.running = True  # This is a boolean flag that controls whether the game is still going (true)

        # UI Elements for time and score
        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=('Helvetica', 16))  # this creates a label in GUI
        self.score_label.grid(row=0, column=0, columnspan=2)  # Positions the label in the grid layout (first row, columns 0 and 1)

        self.time_label = tk.Label(master, text=f"Time: {self.time_elapsed} s", font=('Helvetica', 16))  # Time label
        self.time_label.grid(row=0, column=2, columnspan=2)  # Positions the time label in the same row as the score label

        self.grid_labels = [[tk.Label(master, text="", width=4, height=2, font=('Helvetica', 24), bg='lightgray') 
                             for _ in range(4)] for _ in range(4)]  # Creating 4x4 labels for the game grid 

        self.create_grid()  # Call a function to position the labels in the grid
        self.update_grid()  # Call a function to update the grid display
        self.update_timer()  # Start timer

        # Bind keys for moving tiles
        self.master.bind("<Up>", self.move_up)  # Up is a predefined event in tk library and move_up method defined to handle up arrow
        self.master.bind("<Down>", self.move_down)  # Down is a predefined event in tk library and move_down method defined to handle down arrow
        self.master.bind("<Left>", self.move_left)  # Left is a predefined event in tk library and move_left method defined to handle left arrow
        self.master.bind("<Right>", self.move_right)  # Right is a predefined event in tk library and move_right method defined to handle right arrow

    def create_grid(self):
        # The create_grid method arranges the game grid of labels (which represent the game tiles) in a 4x4 grid on the Tkinter window using the grid layout manager.
        # Each label is positioned with padding for spacing, and the game grid starts on the second row.
        for row in range(4):
            for col in range(4):
                self.grid_labels[row][col].grid(row=row+1, column=col, padx=5, pady=5)  # Adjusting for time and score row

    def add_random_tile(self):
        # empty_cells: A list comprehension to find all empty cells in the grid (cells that contain a 0).
        # random.choice(): Selects a random empty cell and places either a 2 or a 4 there.
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.game_grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.game_grid[i][j] = random.choice([2, 4])

    def update_grid(self):
        # self.grid_labels[row][col]['text']: Updates each label to display the number from the corresponding game grid cell.
        # self.grid_labels[row][col]['bg']: Sets the background color of each label based on the number (using self.get_color()).
        # self.score_label.config(): Updates the score display after each move.
        for row in range(4):
            for col in range(4):
                number = self.game_grid[row][col]
                self.grid_labels[row][col]['text'] = str(number) if number != 0 else ""
                self.grid_labels[row][col]['bg'] = self.get_color(number)

        # Update score label
        self.score_label.config(text=f"Score: {self.score}")

    def get_color(self, number):
        # get_color(number): Returns a background color for each tile based on its number
        colors = {
            0: 'lightgray', 2: 'lightyellow', 4: 'lightgreen', 8: 'lightblue',
            16: 'lightcoral', 32: 'orange', 64: 'lightpink', 128: 'yellow',
            256: 'green', 512: 'blue', 1024: 'coral', 2048: 'gold'
        }
        return colors.get(number, 'black')

    def move(self, matrix):
        # move(matrix): Handles the logic of moving tiles in one direction. It merges adjacent tiles if they are equal and removes empty spaces.
        new_matrix = np.zeros_like(matrix)
 
        for i in range(4):
            row = matrix[i][matrix[i] != 0]  # Remove zeros
            for j in range(len(row) - 1):
                if row[j] == row[j + 1]:  # Combine tiles
                    row[j] *= 2
                    self.score += row[j]  # Update score
                    row[j + 1] = 0
            row = row[row != 0]  # Remove zero after combining
            new_matrix[i, :len(row)] = row

        return new_matrix

    def rotate_grid(self, grid, k=1):
        # Rotates the grid by 90 degrees clockwise `k` times.
        return np.rot90(grid, k)

    def move_up(self, event):
        # Handles the action for moving tiles up in the grid.
        moved = False
        # Rotate the grid 90 degrees to treat an upward move as a leftward move.
        self.game_grid = self.rotate_grid(self.game_grid, 1)
        for _ in range(3):  # Perform the move 3 times to handle multiple merges.
            new_grid = self.move(self.game_grid)
            # Check if the grid changed, indicating a movement.
            if not np.array_equal(new_grid, self.game_grid):
                moved = True
            self.game_grid = new_grid  # Update the grid after the move.
        # Rotate the grid back to its original orientation.
        self.game_grid = self.rotate_grid(self.game_grid, 3)
        # If any tiles moved, update the game state.
        if moved:
            self.after_move()

    def move_down(self, event):
        # Handles the action for moving tiles down in the grid
        moved = False
        # Rotate the grid 270 degrees to treat a downward move as a leftward move.
        self.game_grid = self.rotate_grid(self.game_grid, 3)
        for _ in range(3):  # Perform the move 3 times for merging.
            new_grid = self.move(self.game_grid)  # Move the tiles.
            if not np.array_equal(new_grid, self.game_grid):
                moved = True
            self.game_grid = new_grid  # Update the grid after moving.
        # Rotate the grid back to its original orientation.
        self.game_grid = self.rotate_grid(self.game_grid, 1)
        if moved:
            self.after_move()

    def move_left(self, event):
        # Handles the action for moving tiles to the left.
        moved = False
        for _ in range(3):  # Perform the move 3 times to handle multiple merges.
            new_grid = self.move(self.game_grid)  # Move the tiles.
            if not np.array_equal(new_grid, self.game_grid):
                moved = True
            self.game_grid = new_grid  # Update the grid after moving.
        if moved:
            self.after_move()

    def move_right(self, event):
        # Handles the action for moving tiles to the right.
        moved = False
        # Flip the grid horizontally to treat a rightward move as a leftward move.
        self.game_grid = np.fliplr(self.game_grid)
        for _ in range(3):
            new_grid = self.move(self.game_grid)
            if not np.array_equal(new_grid, self.game_grid):
                moved = True
            self.game_grid = new_grid  # Update the grid after moving.
        # Flip the grid back to its original orientation.
        self.game_grid = np.fliplr(self.game_grid)
        if moved:
            self.after_move()

    def after_move(self):
        # Executes actions after tiles have been moved.
        self.add_random_tile()  # Adds a new random tile after a move.
        self.update_grid()  # Updates the grid display.
        if not self.can_move():  # Check if the game is over (i.e., no more valid moves are available).
            self.game_over()  # Display game over message if no more moves are possible.

    def can_move(self):
        # Checks if any valid moves are available on the board (i.e., if any tiles can be combined or moved).
        for row in range(4):
            for col in range(4):
                # If the tile is empty or adjacent tiles are the same, return true
                if self.game_grid[row][col] == 0 or (col < 3 and self.game_grid[row][col] == self.game_grid[row][col + 1]) or (row < 3 and self.game_grid[row][col] == self.game_grid[row + 1][col]):
                    return True
        return False

    def game_over(self):
        # Displays a game over message and resets the game state.
        self.running = False  # Stop the timer and movement.
        self.master.unbind("<Up>")  # Unbind the arrow keys to stop movements.
        self.master.unbind("<Down>")
        self.master.unbind("<Left>")
        self.master.unbind("<Right>")
        game_over_label = tk.Label(self.master, text="Game Over!", font=('Helvetica', 32), fg='red')  # Creating a game over label
        game_over_label.grid(row=1, column=0, columnspan=4)  # Position it on the grid.

    def update_timer(self):
        if self.running:  # Continue updating the timer if the game is running.
            self.time_elapsed += 1  # Increment the elapsed time by 1 second.
            self.time_label.config(text=f"Time: {self.time_elapsed} s")  # Update the timer display.
            self.master.after(1000, self.update_timer)  # Call this method again after 1 second.

# Run the game
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    game = Game2048(root)  # Initialize the Game2048 class with the main window as an argument.
    root.mainloop()  # Start the Tkinter event loop.
