# -*- coding: utf-8 -*-
"""
Hangman GUI Game

"""

from guizero import App, Text, PushButton, MenuBar, Picture, TextBox, Box, Window, ButtonGroup, Combo
import random
from string import ascii_lowercase
from tkinter import Canvas


# TODO
# Stats window
    # Graph(s)
    # Combo box that changes graph
# Database implementation
# Colors


def submit_guess():
    global guesses_left
    global status_of_game
    global letters_guessed
    global chosen_word
    global chosen_word_letters
    global chosen_word_underscores
    global game_mode
    
    # Eventually save wins and losses information to an SQLite database
    # Implement this in the if clauses for wins and losses

    
    if user_guess.value not in ascii_lowercase or user_guess.value in ["", " "]:
        app.error("Invalid character", "You tried to submit an invalid character as a guess. \
                  Please only enter the letters a-z.")
        user_guess.value = ""
        return
    if user_guess.value in letters_guessed:
        app.error("Letter already guessed", "You already guessed this letter. Enter in another letter that you have not guessed yet")
        user_guess.value = ""
        return
    if user_guess.value not in letters_guessed:
        letters_guessed.append(user_guess.value)
        letters_guessed_text.value = letters_guessed_text.value + user_guess.value
        if user_guess.value not in chosen_word and guesses_left > 0:
            guesses_left -= 1
            guesses_left_text.value = "Guesses Left: {}".format(guesses_left)
            user_guess.value = ""
            try:
                if game_mode == "Easy":
                    hangman_image.image = img_paths_easy[guesses_left]
                elif game_mode == "Medium":
                    hangman_image.image = img_paths_medium[guesses_left]
                elif game_mode == "Hard":
                    hangman_image.image = img_paths_hard[guesses_left]
            except:
                pass
    if user_guess.value in chosen_word:
        for letter in range(len(chosen_word_letters)):
            if chosen_word_letters[letter] == user_guess.value:
                chosen_word_underscores[letter] = user_guess.value
        secret_word.value = "Secret word to guess: {}".format(" ".join(chosen_word_underscores))
        user_guess.value = ""   
    # If user guessed letters equals the secret word, the user wins and certain
    # widgets are changed or disabled in order to reflect this
    if chosen_word_underscores == chosen_word_letters:
        app.info("Game Win", "You won the game!!!")
        status_of_game = "Win"
        if game_mode == "Easy":
            hangman_image.image = img_paths_easy["win"]
        if game_mode == "Medium":
            hangman_image.image = img_paths_medium["win"]
        if game_mode == "Hard":
            hangman_image.image = img_paths_hard["win"]
        game_status_text.value = "Status of Game: {}".format(status_of_game)
        game_status_text.bg = "green"
        secret_word.value = "Secret word to guess: {}".format("".join(chosen_word_underscores))
        user_guess.disable()
        submit_letter.disable()
    # If guesses left equals zero, player loses
    if guesses_left == 0:
        app.info("Game Loss", "Sorry, you lost! You ran out of guesses.")
        status_of_game = "Loss"
        if game_mode == "Easy":
            hangman_image.image = img_paths_easy["loss"]
        if game_mode == "Medium":
            hangman_image.image = img_paths_medium["loss"]
        if game_mode == "Hard":
            hangman_image.image = img_paths_hard["loss"]
        game_status_text.value = "Status of Game: {}".format(status_of_game)
        game_status_text.bg = "red"
        secret_word.value = "Secret word to guess: {}".format(chosen_word)
        user_guess.disable()
        submit_letter.disable()
        
    
def exit_function():
    app.destroy() # Quits out of the program
    
def new_game_function():
    # New window pops up that lets user start a new game and select the mode
    new_game_window.show(wait=True)
    
def hide_new_game_window():
    new_game_window.hide()

def start_new_game():
    global letters_guessed
    global guesses_left    
    global game_mode
    global status_of_game
    global chosen_word
    global chosen_word_letters
    global chosen_word_underscores

    if button_group_modes.value == "easy":
        game_mode = "Easy"
        guesses_left = 10
    elif button_group_modes.value == "medium":
        game_mode = "Medium"
        guesses_left = 8
    elif button_group_modes.value == "hard":
        game_mode = "Hard"
        guesses_left = 6
    # Start a new game
    chosen_word, chosen_word_letters, chosen_word_underscores = pick_random_word()
    status_of_game = "In Progress"
    letters_guessed = []
    new_game_window.hide()
    
    # Update main window widgets
    user_guess.enable()
    submit_letter.enable()
    hangman_image.image = r"C:\Users\akladke\Desktop\Other\Hangman_Game\Images\Hangman_Stages\1.png"
    game_mode_text.value = "Game Mode: {}".format(game_mode)
    guesses_left_text.value = "Guesses Left: {}".format(guesses_left)
    game_status_text.value = "Status of Game: {}".format(status_of_game)
    game_status_text.bg= "#093145"
    secret_word.value = "Secret word to guess: {}".format(" ".join(chosen_word_underscores))
    letters_guessed_text.value = "Letters already guessed: "
    user_guess.value = ""
    

def stats_function():
    print("Stats")
    #statistics_window.show(wait=True)
    
def graph_selector():
    print("Graph selected")
    
def pick_random_word():
    # Pick random word from text file
    word_lst = []
    with open("words.txt") as file:
        for word in file:
            word_lst.append(word)
    # Randomly choose secret word from list of words
    chosen_word = random.choice(word_lst).strip()

    # Both of these lists should be the same length
    # Used to keep track of letters in chosen word and for replacing underscores
    # in chosen word print out when player guesses a word correctly
    chosen_word_letters = []
    chosen_word_underscores = []
    for letter in chosen_word:
        chosen_word_letters.append(letter)
        chosen_word_underscores.append("_")
    
    # Return the chosen word, list of letters and list of underscores
    return chosen_word, chosen_word_letters, chosen_word_underscores
    
img_paths_easy = {
    10: "1.png", 
    9: "2.png",
    8: "3.png",
    7: "4.png",
    6: "5.png",
    5: "6.png",
    4: "7.png",
    3: "8.png",
    2: "9.png",
    1: "10.png",
    "win": "win.png",
    "loss": "loss.png"
}

img_paths_medium = {
    8: "1.png",
    7: "2.png", 
    6: "3.png",
    5: "4.png",
    4: "5.png",
    3: "7.png",
    2: "8.png",
    1: "9.png",
    "win": "win.png",
    "loss": "loss.png"
}

img_paths_hard = {
    7: "1.png",
    6: "2.png", 
    5: "3.png",
    4: "5.png",
    3: "7.png",
    2: "8.png",
    1: "9.png", 
    "win": "win.png",
    "loss": "loss.png"
}
    
image_path = "1.png"



# Pick random word and create underscores so user
# can see how many characters the word has
#######################################################

chosen_word, chosen_word_letters, chosen_word_underscores = pick_random_word()

#######################################################

# Game mode
game_mode = "Medium" # Medium is the default

# Status of game
status_of_game = "In Progress"

# Default to Medium difficulty, otherwise change to another difficulty when
# user selects certain mode from menu
guesses_left = 8

# Letters that have been guessed already
letters_guessed = []


###########################
# Main window
###########################
app = App(title="Hangman v1.0", width=500, height=475)
app.bg = "#093145"
app.text_color = "white"

menubar = MenuBar(app, 
                  toplevel=["File"],
                  options = [
                      [["New Game", new_game_function],  ["Statistics", stats_function], ["Exit", exit_function]],
                      ])

image_box = Box(app, width="fill")
image_box.bg = "#093145"
hangman_image = Picture(image_box, image=image_path, width=160, height=190) # width=160, height=190

overall_statuses_box = Box(app, border=True, layout="grid")
status_box1 = Box(overall_statuses_box, border=True, grid=[0, 0], align="left")
status_box1.tk.config(padx=2, highlightbackground="yellow")
game_mode_text = Text(status_box1, text="Game Mode: {}".format(game_mode))
status_box2 = Box(overall_statuses_box, border=True, grid=[1, 0], width="fill")
status_box2.tk.config(padx=2, highlightbackground="yellow")
guesses_left_text = Text(status_box2, text="Guesses Left: {}".format(guesses_left))
status_box3 = Box(overall_statuses_box, border=True, grid=[3, 0], width="fill", align="right")
status_box3.tk.config(padx=1, highlightbackground="yellow")
game_status_text = Text(status_box3, text="Status of Game: {}".format(status_of_game)) # In Progress, Win, Loss

empty_box = Box(app, border=True)
empty_message = Text(app, text="")

secret_word_box = Box(app)
secret_word = Text(app, text="Secret word to guess: {}".format(" ".join(chosen_word_underscores)))

empty_box = Box(app, border=True)
empty_message = Text(app, text="")

letters_guessed_box = Box(app)
letters_guessed_text = Text(app, text="Letters already guessed: ")

empty_box = Box(app, border=True)
empty_message = Text(app, text="")

user_guess_box = Box(app, layout="grid")
user_guess_text = Text(user_guess_box, "Guess a letter: ", grid=[0,0])
user_guess = TextBox(user_guess_box, grid=[1,0])
user_guess.bg = "white"
user_guess.text_color = "black"

empty_box = Box(app)
empty_message = Text(app, text="")

submit_letter_box = Box(app, border=True)
submit_letter = PushButton(app, text="Submit guess", command=submit_guess)
submit_letter.bg = "#efd469"
submit_letter.text_color = "#093145"


###########################
# Start a new game window
###########################
new_game_window = Window(app, title="Start a New Game", width=300, height=230)
new_game_window.bg = "#093145"
new_game_window.hide()
empty_box = Box(new_game_window)
empty_message = Text(new_game_window, text="")
new_game_text = Text(new_game_window, text="Choose a game mode:")
empty_box = Box(new_game_window)
empty_message = Text(new_game_window, text="")
choices_box = Box(new_game_window, border=True)
choices_box.bg = "white"
choices_box.text_color = "black"
button_group_modes = ButtonGroup(choices_box, options=[
    ["Easy (10 guesses)", "easy"], ["Medium (8 guesses)", "medium"], ["Hard (6 guesses)", "hard"]])
empty_box = Box(new_game_window)
empty_message = Text(new_game_window, text="")
buttons_box = Box(new_game_window, width="fill", align="bottom")
cancel_button = PushButton(new_game_window, text="Cancel", align="right", command=hide_new_game_window)
cancel_button.bg = "#efd469"
cancel_button.text_color = "#093145"
start_new_game_button = PushButton(new_game_window, text="Ok", command=start_new_game, align="right")
start_new_game_button.bg = "#efd469"
start_new_game_button.text_color = "#093145"

###########################
# Statistics window
###########################
statistics_window = Window(app, title="Statistics", width = 400, height=350)
statistics_window.bg = "#093145"
stats_box = Box(statistics_window, border=True)
stats_box.bg = "white"
canvas = Canvas(stats_box.tk)
stats_box.add_tk_widget(canvas)
empty_box = Box(stats_box)
empty_message = Text(stats_box, text="")
graph_combo = Combo(statistics_window, options=["Test1", "Test2", "Test3"], command=graph_selector)
statistics_window.hide()

app.display()

