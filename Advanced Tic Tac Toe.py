import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [' ' for _ in range(9)]
        self.turn = 'X'
        self.difficulty = None
        self.setup_gui()

    def setup_gui(self):
        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.master, text=' ', font=('Arial', 30), width=5, height=2,
                                command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

        player_choice = tk.StringVar()
        tk.Label(self.master, text="Choose X or O:").grid(row=3, column=0, padx=5, pady=5)
        tk.Radiobutton(self.master, text="X", variable=player_choice, value="X").grid(row=3, column=1, padx=5, pady=5)
        tk.Radiobutton(self.master, text="O", variable=player_choice, value="O").grid(row=3, column=2, padx=5, pady=5)

        tk.Label(self.master, text="Choose Difficulty Level:").grid(row=4, column=0, padx=5, pady=5)
        difficulty_menu = tk.StringVar()
        difficulty_menu.set("Easy")
        tk.OptionMenu(self.master, difficulty_menu, "Easy", "Medium", "Hard").grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        tk.Button(self.master, text="Start", command=lambda: self.start_game(player_choice.get(), difficulty_menu.get())).grid(row=5, column=1, columnspan=2, padx=5, pady=5)

    def start_game(self, player_choice, difficulty):
        if player_choice == 'X':
            self.computer_choice = 'O'
        else:
            self.computer_choice = 'X'
        self.difficulty = difficulty
        if self.computer_choice == 'X':
            self.computer_move()

    def on_click(self, row, col):
        index = 3 * row + col
        if self.board[index] == ' ':
            self.board[index] = self.turn
            self.buttons[index].config(text=self.turn, state='disabled', disabledforeground='black')
            if self.check_winner(self.turn):
                messagebox.showinfo("Winner", f"{self.turn} wins!")
                self.reset_board()
                return
            elif ' ' not in self.board:
                messagebox.showinfo("Draw", "It's a draw!")
                self.reset_board()
                return
            self.turn = 'O' if self.turn == 'X' else 'X'
            if self.turn == self.computer_choice:
                self.computer_move()

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        for button in self.buttons:
            button.config(text=' ', state='normal')

    def check_winner(self, player):
        winning_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for condition in winning_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def computer_move(self):
        if self.difficulty == "Easy":
            while True:
                index = random.randint(0, 8)
                if self.board[index] == ' ':
                    break
        elif self.difficulty == "Medium":
            index = self.medium_ai_move()
        else:
            index = self.hard_ai_move()

        self.board[index] = self.computer_choice
        self.buttons[index].config(text=self.computer_choice, state='disabled', disabledforeground='black')
        if self.check_winner(self.computer_choice):
            messagebox.showinfo("Winner", f"{self.computer_choice} wins!")
            self.reset_board()
            return
        elif ' ' not in self.board:
            messagebox.showinfo("Draw", "It's a draw!")
            self.reset_board()
            return
        self.turn = 'O' if self.turn == 'X' else 'X'

    def medium_ai_move(self):
        # Medium difficulty: Random move
        while True:
            index = random.randint(0, 8)
            if self.board[index] == ' ':
                break
        return index

    def hard_ai_move(self):
        # Hard difficulty: Find winning move or block opponent's winning move
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.computer_choice
                if self.check_winner(self.computer_choice):
                    return i
                else:
                    self.board[i] = ' '

        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.turn
                if self.check_winner(self.turn):
                    self.board[i] = self.computer_choice
                    return i
                else:
                    self.board[i] = ' '

        return self.medium_ai_move()

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
