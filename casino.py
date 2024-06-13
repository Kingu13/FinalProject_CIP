import tkinter as tk
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk

import random

# Canvas size
canvas_width = 1200
canvas_height = 600

symbols = {
    '🍇': 0.5556, # 55.56% chance to get
    '🍌': 0.2778, # 27.78% chance to get
    '🍒': 0.1667  # 16.67% chance to get
    }

balance = 1000
bet_amount = 0

def main():
    casino = tk.Tk()
    casino.title("Casino Royale")

    canvas = tk.Canvas(casino, width=canvas_width, height=canvas_height, bg="black")
    canvas.pack()

    main_menu(canvas, casino)

    # Bind left mouse click to the function on_left_click
    canvas.bind("<Button-1>", lambda event: on_left_click(event, canvas))

    # Window closing protocol, runs the "def window_exit() when clicking the (X) in the corner of the window"
    casino.protocol("WM_DELETE_WINDOW", partial(window_exit, casino))

    casino.mainloop()

def main_menu(canvas, casino):
    clear_canvas(canvas)
    x = canvas_width / 2
    y = canvas_height / 2

    welcome_text = "Welcome To Casino Royale!"
    canvas.create_text(x, y, text=welcome_text, anchor=tk.CENTER, font=("Times New Roman", 42), fill="white")

    # Show Balance
    global balance_text_change
    balance_text = "Balance: $" + str(balance)
    balance_text_change = canvas.create_text(1000, 560, text=balance_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")

    play_text = canvas.create_text(x, y + 90, text="● Press here to play slots", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    canvas.tag_bind(play_text, "<Button-1>", partial(play_slots, canvas=canvas, casino=casino))

    exit_text = canvas.create_text(x, y + 150, text="● Exit", anchor=tk.CENTER, font=("Times New Roman", 16), fill="white")
    canvas.tag_bind(exit_text, "<Button-1>", partial(exit, casino=casino))

def play_slots(event, canvas, casino):
    clear_canvas(canvas)

    display_how_to_win_and_payout(canvas)
    # Showing Balance
    global balance_text_change
    balance_text = "Balance: $" + str(balance)
    balance_text_change = canvas.create_text(1000, 560, text=balance_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    
    global bet_amount_change
    bet_amount_new = "Bet Amount: $" + str(bet_amount)
    bet_amount_change = canvas.create_text(1000, 460, text=bet_amount_new, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")

    # Exit to main menu text
    exit_text = canvas.create_text(180, 560, text="Exit", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    canvas.tag_bind(exit_text, "<Button-1>", partial(exit, casino=casino))

    build_slot_machine(canvas)

    # Entry widget for entering bet amount
    global entry
    entry = tk.Entry(casino, width=15, font=("Times New Roman", 12))
    entry.place(x=915, y=500)

    # Button to submit the bet amount and spin
    submit_button = tk.Button(casino, text="Bet", command=lambda: bet_and_spin(canvas, casino), font=("Times New Roman", 12))
    submit_button.place(x=1040, y=500)
    
    # Button to spin with the same bet amount
    spin_button = tk.Button(casino, text="Spin", command=lambda: spin_same_bet(canvas, casino), font=("Times New Roman", 12))
    spin_button.place(x=800, y=300)

def bet_and_spin(canvas, casino):
    global bet_amount
    global balance

    try:
        bet_amount = float(entry.get())  # Retrieve the input from the entry widget
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid bet amount.")
        return

    if bet_amount <= 0:
        messagebox.showerror("Error", "Bet amount must be greater than zero.")
        return
    elif bet_amount > balance:
        messagebox.showerror("Error", "Insufficient balance.")
        return
    else:
        balance -= bet_amount
        update_balance(canvas)
        update_bet_amount(canvas)
        entry.delete(0, tk.END)  # Clear the entry widget after retrieving the input
        # Spin the slot machine
        winning_symbols = spin(canvas, casino, symbols)
        check_winning(canvas, winning_symbols, bet_amount)

def spin_same_bet(canvas, casino):
    global bet_amount
    global balance

    if bet_amount <= 0:
        messagebox.showerror("Error", "Bet amount must be greater than zero.")
        return
    elif bet_amount > balance:
        messagebox.showerror("Error", "Insufficient balance.")
        return
    else:
        balance -= bet_amount
        update_balance(canvas)
        # Spin the slot machine
        winning_symbols = spin(canvas, casino, symbols)
        check_winning(canvas, winning_symbols, bet_amount)

def build_slot_machine(canvas):
    BOX_ROW = 3
    BOX_SIZE = 50
    BOX_SPACING = 10
    # Calculate the total width of all boxes and spacing
    total_width = BOX_ROW * BOX_SIZE + (BOX_ROW - 1) * BOX_SPACING

    # Calculate the starting x-coordinate for the first box
    start_x = (canvas_width - total_width) / 2

    # Calculate the total height of all boxes and spacing
    total_height = BOX_ROW * BOX_SIZE + (BOX_ROW - 1) * BOX_SPACING

    # Calculate the starting y-coordinate for the first row
    start_y = (canvas_height - total_height) / 2

    
    
    
    
    for i in range(BOX_ROW):
        for j in range(BOX_ROW):
            end_x = start_x + BOX_SIZE
            end_y = start_y + BOX_SIZE

            canvas.create_rectangle(start_x,
                                    start_y,
                                    end_x,
                                    end_y,
                                    outline="white",
                                    fill="black")
            start_x += BOX_SIZE + BOX_SPACING  # Move to the next column
        start_x = (canvas_width - total_width) / 2  # Reset start_x for the next row
        start_y += BOX_SIZE + BOX_SPACING  # Move to the next row    

def spin(canvas, casino, symbols):
    # To remove symbols from spins before, so they don't stack.
    clear_canvas(canvas)

    display_how_to_win_and_payout(canvas)
    
    build_slot_machine(canvas)

    # Showing Balance
    global balance_text_change
    balance_text = "Balance: $" + str(balance)
    balance_text_change = canvas.create_text(1000, 560, text=balance_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    
    global bet_amount_change
    bet_amount_text = "Bet Amount: $" + str(bet_amount)
    bet_amount_change = canvas.create_text(1000, 460, text=bet_amount_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")

    # Exit to main menu text
    exit_text = canvas.create_text(180, 560, text="Exit", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    canvas.tag_bind(exit_text, "<Button-1>", partial(exit, casino=casino))

    BOX_ROW = 3
    BOX_SIZE = 50
    BOX_SPACING = 10
    # Calculate the total width of all boxes and spacing
    total_width = BOX_ROW * BOX_SIZE + (BOX_ROW - 1) * BOX_SPACING

    # Calculate the starting x-coordinate for the first box
    start_x = (canvas_width - total_width) / 2

    # Calculate the total height of all boxes and spacing
    total_height = BOX_ROW * BOX_SIZE + (BOX_ROW - 1) * BOX_SPACING

    # Calculate the starting y-coordinate for the first row
    start_y = (canvas_height - total_height) / 2

    winning_symbols = []

    for i in range(BOX_ROW):
        for j in range(BOX_ROW):
            symbol = random_symbol(symbols)
            winning_symbols.append(symbol)

            canvas.create_text(start_x + BOX_SIZE / 2,
                               start_y + BOX_SIZE / 2,
                               text=symbol,
                               anchor=tk.CENTER,
                               font=("Times New Roman", 24),
                               fill="white")
            start_x += BOX_SIZE + BOX_SPACING  # Move to the next column
        start_x = (canvas_width - total_width) / 2  # Reset start_x for the next row
        start_y += BOX_SIZE + BOX_SPACING  # Move to the next row
    # Returning the list winning_symbols if they match. 
    return winning_symbols

def check_winning(canvas, winning_symbols, bet_amount):
    global balance
    x = canvas_width / 2
    y = canvas_height / 4

    winning_symbols = winning_symbols[3:-3]
    if winning_symbols == ['🍇','🍇','🍇']:
        winnings = bet_amount * 3
        # Contratulate the winner :)
        canvas.create_text(x, y, text="Congratulations! You have won $" + str(winnings) + "!", anchor=tk.CENTER, font=("Times New Roman", 24), fill="white")
        balance += winnings
    elif winning_symbols == ['🍌','🍌','🍌']:
        winnings = bet_amount * 5
        # Contratulate the winner :)
        canvas.create_text(x, y, text="Congratulations! You have won $" + str(winnings) + "!", anchor=tk.CENTER, font=("Times New Roman", 24), fill="white")
        balance += winnings
    elif winning_symbols == ['🍒','🍒','🍒']:
        winnings = bet_amount * 10
        # Contratulate the winner :)
        canvas.create_text(x, y, text="Congratulations! You have won $" + str(winnings) + "!", anchor=tk.CENTER, font=("Times New Roman", 24), fill="white")
        balance += winnings
    else:
        canvas.create_text(x, y, text="You lost, better luck next time -$" + str(bet_amount), anchor=tk.CENTER, font=("Times New Roman", 24), fill="white")
    
    update_balance(canvas)

def random_symbol(choices):
    random_num = random.random()
    probability_symbol = 0
    
    for symbol, probability in choices.items():
        probability_symbol += probability
        if random_num <= probability_symbol:
            return symbol

def exit(event, casino):
    casino.destroy()

def window_exit(casino):
    close = messagebox.askyesno("Leave the Casino?", "Are you sure you want to exit?")
    if close:
        casino.destroy()

def on_left_click(event, canvas):
    x, y = event.x, event.y
    position_text = f"({x}, {y})"
    canvas.create_text(x, y, text=position_text, anchor=tk.NW, font=("Times New Roman", 12), fill="white")

def clear_canvas(canvas):
    canvas.delete("all")

def update_balance(canvas):
    global balance_text_change
    balance_text = "Balance: $" + str(balance)
    canvas.itemconfigure(balance_text_change, text=balance_text)

def update_bet_amount(canvas):
    global bet_amount_change
    bet_amount_text = "Bet Amount: $" + str(bet_amount)
    canvas.itemconfigure(bet_amount_change, text=bet_amount_text)
    
def display_how_to_win_and_payout(canvas):
    canvas.create_text(110, 100, text="How to win ☟", anchor=tk.CENTER, font=("Times New Roman", 15), fill="white")
    canvas.create_text(110, 120, text="3 of a kind in the middle row", anchor=tk.CENTER, font=("Times New Roman", 10), fill="white")
    canvas.create_text(110, 150, text="| 🍇 | 🍇 | 🍇 | = Bet * 3", anchor=tk.CENTER, font=("Times New Roman", 15), fill="white")
    canvas.create_text(110, 180, text="| 🍌 | 🍌 | 🍌 | = Bet * 5", anchor=tk.CENTER, font=("Times New Roman", 15), fill="white")
    canvas.create_text(115, 210, text="| 🍒 | 🍒 | 🍒 | = Bet * 10", anchor=tk.CENTER, font=("Times New Roman", 15), fill="white")   
    
     
if __name__ == "__main__":
    main()
