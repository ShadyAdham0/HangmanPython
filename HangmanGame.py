import os
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

HANGMAN_STAGES = [
    '''
       ______
      |      |
             |
             |
             |
             |
    ''',
    '''
       ______
      |      |
      O      |
             |
             |
             |
    ''',
    '''
       ______
      |      |
      O      |
      |      |
             |
             |
    ''',
    '''
       ______
      |      |
      O      |
     /|      |
             |
             |
    ''',
    '''
       ______
      |      |
      O      |
     /|\\    |
             |
             |
    ''',
    '''
       ______
      |      |
      O      |
     /|\\    |
     /       |
             |
    ''',
    '''
       ______
      |      |
      O      |
     /|\\    |
     / \\    |
             |
    '''
]

words = {
    "Animals": ["LION", "TIGER", "ELEPHANT", "MONKEY"],
    "Fruits": ["BANANA", "ORANGE", "MANGO", "LEMON"],
    "Countries": ["GERMANY", "SPAIN", "FRANCE", "ENGLAND"]
}

def get_valid_word(category, words):
    word = random.choice(words[category])
    return word.upper()

def save_game(player_name, word, guesses, wrong_guesses):
    with open(f"{player_name}.txt", "w") as file:
        file.write(f"{word}\n")
        file.write(" ".join(guesses) + "\n")
        file.write(" ".join(wrong_guesses))

def load_game(player_name):
    if not os.path.exists(f"{player_name}.txt"):
        return None, None, None
    with open(f"{player_name}.txt", "r") as file:
        word = file.readline().strip()
        guesses = file.readline().strip().split()
        wrong_guesses = file.readline().strip().split()
        return word, guesses, wrong_guesses

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman")
        self.guesses = []
        self.wrong_guesses = []
        self.word = ""
        self.category = ""
        self.player_name = ""
        self.center_frame = tk.Frame(master)
        self.center_frame.pack(expand=True)
        self.menu_frame = tk.Frame(self.center_frame)
        tk.Button(self.menu_frame, text="Start New Game", font=('Helvetica', 20), command=self.show_name_entry, height=2, width=16, padx=5, pady=5).pack(pady=25)
        tk.Button(self.menu_frame, text="Load Game",  font=('Helvetica', 20), command=self.load_game, height=2, width=16, padx=5, pady=5).pack(pady=25)
        tk.Button(self.menu_frame, text="Exit",  font=('Helvetica', 20), command=self.exit_game, height=2, width=16, padx=5, pady=5).pack(pady=25)
        self.menu_frame.pack()
        self.name_frame = tk.Frame(self.center_frame)
        tk.Label(self.name_frame, text="Enter your name:", font=('Helvetica', 20)).pack(pady=25)
        self.name_entry = tk.Entry(self.name_frame, font=('Helvetica', 32))
        self.name_entry.pack(pady=10)
        tk.Button(self.name_frame, text="Submit", font=('Helvetica', 16), command=self.category_selection, height=2, width=39, padx=5, pady=5).pack(pady=10)
        self.category_frame = tk.Frame(self.center_frame)
        for category in words.keys():
            tk.Button(self.category_frame, text=category, font=('Helvetica', 20), command=lambda c=category: self.new_game(c), height=2, width=90, padx=5, pady=5).pack(pady=25)
        tk.Button(self.category_frame, text="Random", font=('Helvetica', 20), command=self.random_category, height=2, width=90, padx=5, pady=5).pack(pady=25)
        self.game_frame = tk.Frame(self.center_frame)
        self.lbl_word = tk.Label(self.game_frame, font=('Helvetica', 70))
        self.lbl_word.pack(pady=5)
        self.lbl_hangman = tk.Label(self.game_frame, font=('Helvetica', 40))
        self.lbl_hangman.pack(pady=7)
        self.entry_guess = tk.Entry(self.game_frame, font=('Helvetica', 30))
        self.entry_guess.pack(pady=10)
        self.entry_guess.bind("<Return>", self.process_guess)
        self.btn_guess = tk.Button(self.game_frame, text="Guess", font=('Helvetica', 16), command=self.process_guess, height=2, width=16, padx=5, pady=5)
        self.btn_guess.pack(pady=20)
        self.btn_save = tk.Button(self.game_frame, text="Save Game", font=('Helvetica', 16), command=self.save_game_wrapper, height=2, width=16, padx=5, pady=5)
        self.btn_save.pack(pady=20)
        self.lbl_incorrect_guesses = tk.Label(self.game_frame, font=('Helvetica', 16), fg='red')
        self.lbl_incorrect_guesses.pack(anchor='nw')
        self.master.bind('<Escape>', self.on_esc_pressed)

    def show_name_entry(self):
        self.menu_frame.pack_forget()
        self.name_frame.pack()

    def category_selection(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            self.name_frame.pack_forget()
            self.menu_frame.pack()
            return
        self.name_frame.pack_forget()
        self.category_frame.pack()

    def random_category(self):
        category = random.choice(list(words.keys()))
        self.new_game(category)

    def new_game(self, category):
        self.category = category
        self.word = get_valid_word(self.category, words)
        self.guesses = []
        self.wrong_guesses = []
        self.category_frame.pack_forget()
        self.switch_to_game_frame()
        self.update_display()

    def load_game(self):
        self.player_name = simpledialog.askstring("Name", "Enter your name:", parent=self.master)
        if not self.player_name:
            return
        self.word, self.guesses, self.wrong_guesses = load_game(self.player_name)
        if self.word:
            self.clear_frames_except_game()
            self.switch_to_game_frame()
            self.update_display()
        else:
            messagebox.showinfo("Info", "No saved game found.")

    def clear_frames_except_game(self):
        self.menu_frame.pack_forget()
        self.name_frame.pack_forget()
        self.category_frame.pack_forget()

    def save_game_wrapper(self):
        if not self.player_name:
            self.player_name = simpledialog.askstring("Name", "Enter your name:", parent=self.master)
            if not self.player_name:
                return
        save_game(self.player_name, self.word, self.guesses, self.wrong_guesses)
        messagebox.showinfo("Info", "Game saved.")
        self.switch_to_menu_frame()

    def switch_to_game_frame(self):
        self.game_frame.pack()

    def switch_to_menu_frame(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack()

    def update_display(self):
        display_word = "".join([letter if letter in self.guesses else "_ " for letter in self.word])
        self.lbl_word.config(text=display_word)
        stage = HANGMAN_STAGES[len(self.wrong_guesses)]
        self.lbl_hangman.config(text=stage)
        self.lbl_incorrect_guesses.config(text="Incorrect: " + ", ".join(self.wrong_guesses))

    def process_guess(self, event=None):
        guess = self.entry_guess.get().upper()
        self.entry_guess.delete(0, tk.END)
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Warning", "Please enter a single valid letter.")
            return
        if guess in self.guesses or guess in self.wrong_guesses:
            messagebox.showinfo("Info", "You have already guessed that letter.")
            return
        if guess in self.word:
            self.guesses.append(guess)
            if all(letter in self.guesses for letter in self.word):
                messagebox.showinfo("Congratulations!", "You found the word! You win!")
                self.switch_to_menu_frame()
        else:
            self.wrong_guesses.append(guess)
            if len(self.wrong_guesses) == len(HANGMAN_STAGES) - 1:
                messagebox.showinfo("Game Over", "You lost! The word was " + self.word)
                self.switch_to_menu_frame()
        self.update_display()

    def on_esc_pressed(self, event):
        choice = messagebox.askyesnocancel("Pause", "Do you want to pause and save the game?")
        if choice is True:
            self.save_game_wrapper()
            self.master.destroy()
        elif choice is False:
            self.master.destroy()

    def exit_game(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()