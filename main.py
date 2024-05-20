import tkinter.messagebox
from tkinter import *
import random
from data import quotes, highscore

time = 0
quote_text = ""
game_continue = True


def start_game():
    window.bind("<Return>", end_game)
    global time
    global quote_text
    time = 0
    timer.config(text="0.00s")
    quote_text = random.choice(quotes).lower()
    quote.config(text=quote_text)
    typing_input.delete(0, END)
    typing_input.focus()
    start_button["state"] = "disabled"

    start_timer()


def start_timer():
    global time
    global quote_text
    global game_continue
    if game_continue:
        time = round(time + 0.01, 2)
        if time % 0.1 == 0:
            timer.config(text=f"{time}0s")
        else:
            timer.config(text=f"{time}s")
        window.after(10, start_timer)
    else:
        accuracy_percentage = check_accuracy(quote_text, typing_input.get())
        type_speed = round(len(typing_input.get()) / time, 2)
        message = ""
        if accuracy_percentage == 100:
            message = "Perfect!"
            if type_speed > highscore:
                new_highscore = type_speed
                message = "Perfect! You got a new highscore!"
                with open("score.txt", "w") as file:
                    file.write(str(type_speed))
                highscore_text.config(text=f"Highscore = {new_highscore} letters per second")

        start_button.config(text="Restart Game")
        tkinter.messagebox.showinfo("Results:", f"Your time: {time}s\n"
                                                f"Letters per second: {type_speed}\n"
                                                f"Accuracy: {accuracy_percentage}%\n"
                                                f"{message}")
        start_button["state"] = "active"
        window.unbind("<Return>")
        game_continue = True


def end_game(event):
    global game_continue
    game_continue = False


def check_accuracy(sentence, user_sentence):
    words = sentence.split(" ")
    user_words = user_sentence.split(" ")[:len(words)]
    count = 0
    correct_words = 0
    for word in words:
        if count < len(user_words):
            if word == user_words[count]:
                correct_words += 1
            count += 1
    return round((correct_words / len(words) * 100))


window = Tk()
window.title("How fast can you type?")
window.config(pady=20, padx=20, bg="black")

title = Label(text="SPEED TYPER", font=("Arial", 80, "bold"), fg="white", bg="black", pady=20)
title.pack()

quote = Label(text="(Quote appears here)", font=("Arial", 30, "normal"), fg="white", bg="black", pady=20)
quote.pack()

typing_input = Entry(width=50, font=("Arial", 20, "normal"), bg="black", fg="white", borderwidth=2)
typing_input.pack()

start_button = Button(command=start_game, text="Start Game", font=("Arial", 30, "bold"), fg="black", bg="white")
start_button.pack(pady=20)

timer = Label(text="0.00s", font=("Arial", 40, "bold"), fg="white", bg="black")
timer.pack()

highscore_text = Label(text=f"Highscore = {highscore} letters per second",
                       font=("Arial", 20, "normal"), fg="white", bg="black", pady=20)
highscore_text.pack()

window.mainloop()
