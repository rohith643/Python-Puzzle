import tkinter as tk
from tkinter import messagebox
import random

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle Game")
        self.moves = 0
        self.size = 3  # 3x3 grid
        self.buttons = []
        self.current_state = []
        
        # Create game frame
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(padx=10, pady=10)
        
        # Create moves label
        self.moves_label = tk.Label(self.root, text="Moves: 0")
        self.moves_label.pack(pady=5)
        
        # Create buttons for the grid
        self.create_board()
        
        # Create new game button
        self.new_game_btn = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_btn.pack(pady=5)
        
        # Initialize the game
        self.new_game()

    def create_board(self):
        # Create buttons for the grid
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(self.game_frame, width=10, height=5, 
                                command=lambda x=i, y=j: self.button_click(x, y))
                button.grid(row=i, column=j, padx=2, pady=2)
                row.append(button)
            self.buttons.append(row)

    def new_game(self):
        # Reset moves counter
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        
        # Create solved state
        numbers = list(range(1, self.size * self.size))
        numbers.append(None)  # Empty space
        
        # Shuffle numbers
        while True:
            random.shuffle(numbers)
            # Make sure puzzle is solvable
            if self.is_solvable(numbers):
                break
        
        # Update current state
        self.current_state = []
        for i in range(self.size):
            self.current_state.append(numbers[i * self.size:(i + 1) * self.size])
        
        # Update button texts
        self.update_buttons()

    def is_solvable(self, numbers):
        # Count inversions
        inversions = 0
        for i in range(len(numbers) - 1):
            if numbers[i] is None:
                continue
            for j in range(i + 1, len(numbers)):
                if numbers[j] is None:
                    continue
                if numbers[i] > numbers[j]:
                    inversions += 1
        
        # For 3x3 puzzle, if inversion count is even, puzzle is solvable
        return inversions % 2 == 0

    def button_click(self, i, j):
        # Check adjacent cells for empty space
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for move in moves:
            new_i, new_j = i + move[0], j + move[1]
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                if self.current_state[new_i][new_j] is None:
                    # Swap values
                    self.current_state[new_i][new_j] = self.current_state[i][j]
                    self.current_state[i][j] = None
                    self.moves += 1
                    self.moves_label.config(text=f"Moves: {self.moves}")
                    self.update_buttons()
                    
                    # Check if puzzle is solved
                    if self.check_win():
                        messagebox.showinfo("Congratulations!", 
                            f"You solved the puzzle in {self.moves} moves!")
                    break

    def update_buttons(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.current_state[i][j]
                self.buttons[i][j].config(text="" if value is None else str(value))

    def check_win(self):
        # Check if numbers are in order
        numbers = []
        for row in self.current_state:
            numbers.extend(row)
        
        # Remove None and check if remaining numbers are in order
        numbers = [x for x in numbers if x is not None]
        return numbers == list(range(1, self.size * self.size))

if __name__ == "__main__":
    root = tk.Tk()
    game = SlidingPuzzle(root)
    root.mainloop()