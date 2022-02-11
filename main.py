from tkinter import *
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"

# Attempt to open words_to_learn file, if it can't be found then use the full list of French words.
# to_learn will be a dict of French/English words
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
current_card = {}


# After flip_timer flips card once, stop the cycle. Set current_card dict to a random choice from to_learn.
# Configure canvas attributes to the front of card French side. Then set the flip_timer.
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_background, image=card_front_img)
    flip_timer = window.after(3000, func=card_flip)


# Method to flip card and configure canvas attributes to the back of card English side.
def card_flip():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_background, image=card_back_img)


# When right_button is pressed remove current_card from to_learn dict. Then create a DataFrame from to_learn and turn
# it into a csv file named words_to_learn located inside the data folder and do not allow indexes, so it looks nice.
def known_card():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    # Call next_card to run through process of displaying the next French word.
    next_card()


# Create window.
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# flip_timer is initialized here so when the first card appears it will know to flip over after 3 seconds.
flip_timer = window.after(3000, func=card_flip)

# Create canvas.
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
# Two different photos are used to represent the front and back of the card. We set the background to the card_front_img
# first because that is the French side the user is guessing.
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Create two buttons with associated images.
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=known_card)
right_button.grid(column=1, row=1)

# Call next_card() so current_card dict is filled with a new card to start the FlashCard process.
next_card()

# mainloop() to keep window on screen.
window.mainloop()
