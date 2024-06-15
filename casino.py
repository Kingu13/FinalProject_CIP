import tkinter as tk
from tkinter import messagebox
from functools import partial
import random
from playsound import playsound
import threading

# Canvas size
canvas_width = 1200
canvas_height = 600

# Symbols that I included in this program.
symbols = {
    '🍇': 0.5556, # 55.56% chance to get
    '🍌': 0.2778, # 27.78% chance to get
    '🍒': 0.1667  # 16.67% chance to get
    }

# Starting balance and default bet amount.
balance = 1000
bet_amount = 0

def main():
    # Creates the window where the rest of the program will be printed out.
    casino = tk.Tk()
    
    # Top bar will display "Casino Royale"
    casino.title("Casino Royale")

    # Creates the canvas on which the program will be displayed.
    canvas = tk.Canvas(casino, width=canvas_width, height=canvas_height, bg="black")
    canvas.pack()

    # Starts the program by calling the main_menu()
    main_menu(canvas, casino)

    # Bind left mouse click to the function on_left_click to later click around to play some slots!
    canvas.bind("<Button-1>", lambda event: on_left_click(event, canvas))

    # Window closing protocol, runs window_exit() when clicking the (X) in the corner of the window.
    casino.protocol("WM_DELETE_WINDOW", partial(window_exit, casino))

    # Starts the main loop for the program.
    casino.mainloop()

def main_menu(canvas, casino):
    x = canvas_width / 2
    y = canvas_height / 2

    # Welcome screen!
    welcome_text = "Welcome To Casino Royale!"
    canvas.create_text(x, y, text=welcome_text, anchor=tk.CENTER, font=("Times New Roman", 42), fill="white")

    # Show Balance
    global balance_text_change
    balance_text = "Balance: $" + str(balance)
    balance_text_change = canvas.create_text(1080, 560, text=balance_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")

    # Text with a button on it to call the play_slots()
    play_text = canvas.create_text(x, y + 90, text="● Press here to play slots", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    canvas.tag_bind(play_text, "<Button-1>", partial(play_slots, canvas=canvas, casino=casino))

    # Exit button to exit close down the program.
    exit_text = canvas.create_text(x, y + 150, text="● Exit", anchor=tk.CENTER, font=("Times New Roman", 16), fill="white")
    canvas.tag_bind(exit_text, "<Button-1>", partial(exit, casino=casino))

def play_slots(event, canvas, casino):
    clear_canvas(canvas)

    # Shows winning conditions
    display_how_to_win_and_payout(canvas)
    
    # Showing balance.
    update_balance(canvas)
    
    # Showing bet amount.
    global bet_amount_change
    bet_amount_new = "Bet Amount: $" + str(bet_amount)
    bet_amount_change = canvas.create_text(1080, 460, text=bet_amount_new, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")

    # Exit the program button
    exit_text = canvas.create_text(60, 560, text="Exit", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    canvas.tag_bind(exit_text, "<Button-1>", partial(exit, casino=casino))

    # Builds the boxes after clearing the canvas earlier in the function.
    build_slot_machine(canvas)

    # Box to type in for entering bet amount.
    global entry
    entry = tk.Entry(casino, width=20, font=("Times New Roman", 12))
    entry.place(x=995, y=500)

    # Button to submit the bet amount and spin.
    submit_button = tk.Button(casino, text="Bet", command=lambda: bet_and_spin(canvas, casino), font=("Times New Roman", 12))
    submit_button.place(x=1130, y=500)
    
    # Button to spin with the same bet amount.
    spin_button = tk.Button(casino, text="Spin", command=lambda: spin_same_bet(canvas, casino), font=("Times New Roman", 12))
    spin_button.place(x=580, y=400)

def bet_and_spin(canvas, casino):
    global bet_amount
    global balance
    # Checks a valid bet, no letters and if the bet is bigger than 0 and smaller or the same as balance.
    try:
        bet_amount = float(entry.get())  # Take the input from the entry box.
    except ValueError: # If there is an error it asks again for a valid bet.
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
        entry.delete(0, tk.END)  # Clear the entry box after receiving the input.
        # Spin the slot machine
        winning_symbols = spin(canvas, casino, symbols)
        check_winning(canvas, casino, winning_symbols, bet_amount)

def spin_same_bet(canvas, casino):
    global bet_amount
    global balance
    # Check so that bet_amount is bigger than 0 and not bigger than the balance. This is if you use the spin button after entering a valid amount, and not letters before.
    if bet_amount <= 0:
        messagebox.showerror("Error", "Bet amount must be greater than zero.")
        return
    elif bet_amount > balance:
        messagebox.showerror("Error", "Insufficient balance.")
        return
    else:
        balance -= bet_amount
        update_balance(canvas)
        # Spin the slot machine to get the symbols printed out.
        winning_symbols = spin(canvas, casino, symbols)
        # To later check the symbols for the winning row or losing. :D
        check_winning(canvas, casino, winning_symbols, bet_amount)

def build_slot_machine(canvas):
    BOX_ROW = 3
    BOX_SIZE = 50
    BOX_SPACING = 10
    # Calculate the total width of all boxes and spacing between them
    total_width = BOX_ROW * BOX_SIZE + (BOX_ROW - 1) * BOX_SPACING

    # Calculate the starting x value for the first box
    start_x = (canvas_width - total_width) / 2

    # Calculate the total height of all boxes and spacing between them
    total_height = BOX_ROW * BOX_SIZE + (BOX_ROW - 1) * BOX_SPACING

    # Calculate the starting y value for the first row
    start_y = (canvas_height - total_height) / 2

    # Creates a white L shape in the lower left corner
    canvas.create_line(15, canvas_height - 150, 15, canvas_height - 7, fill="white", width=5)
    canvas.create_line(15, canvas_height - 10, 158, canvas_height - 10, fill="white", width=5)
    # Mirrors the white L shape to the lower right corner
    canvas.create_line(canvas_width - 15, canvas_height - 150, canvas_width - 15, canvas_height - 7, fill="white", width=5)
    canvas.create_line(canvas_width - 158, canvas_height - 10, canvas_width - 15, canvas_height - 10, fill="white", width=5)
    
    # Creates a white L shape in the upper left corner
    canvas.create_line(15, 150, 15, 8, fill="white", width=5)
    canvas.create_line(15, 10, 158, 10, fill="white", width=5)    
    # Mirrors the white L shape to the upper right corner
    canvas.create_line(canvas_width - 15, 150, canvas_width - 15, 8, fill="white", width=5)
    canvas.create_line(canvas_width - 158, 10, canvas_width - 15, 10, fill="white", width=5) 

    # Create arrows pointing at the row which you win in.
    canvas.create_text(504, 305, text="⇨", anchor=tk.CENTER, font=("Oswald", 40), fill="white")
    canvas.create_text(697, 305, text="⇦", anchor=tk.CENTER, font=("Oswald", 40), fill="white")
    
    for i in range(BOX_ROW): # Prints out the 9 boxes forming the "slots machine" 
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
    clear_canvas(canvas) # To remove symbols from spins before, so they don't stack.

    display_how_to_win_and_payout(canvas) # Calls the function that displays the winnings and how in the left corner.
    
    build_slot_machine(canvas) # Rebuilds the canvas after clearing it, so things dont stack.

    # Showing Balance, calling the function and changing the balance so its the right amount.
    update_balance(canvas)
    
    # Showing Bet Amount, calling the function to change to new amount.
    update_bet_amount(canvas)

    # Exit the program button in left corner
    exit_text = canvas.create_text(60, 560, text="Exit", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    canvas.tag_bind(exit_text, "<Button-1>", partial(exit, casino=casino))

    BOX_ROW = 3
    BOX_SIZE = 50
    BOX_SPACING = 10
    # Calculate the total width of all boxes and spacing
    total_width = BOX_ROW * BOX_SIZE + (BOX_ROW - 1) * BOX_SPACING

    # Calculate the starting x value for the first box
    start_x = (canvas_width - total_width) / 2

    # Calculate the total height of all boxes and spacing
    total_height = BOX_ROW * BOX_SIZE + (BOX_ROW - 1) * BOX_SPACING

    # Calculate the starting y value for the first row
    start_y = (canvas_height - total_height) / 2

    winning_symbols = []   # creates a list that saves all the symbols printed out on the canvas, to later check for winnings.

    for i in range(BOX_ROW): # Prints out the symbols on the screen.
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

def check_winning(canvas, casino, winning_symbols, bet_amount): # Checks the winning_symbols which has 9 symbols,
    global balance
    x = canvas_width / 2
    y = canvas_height / 4

    winning_symbols = winning_symbols[3:-3]             # slice it up into the middle 3 and 
    if winning_symbols == ['🍇','🍇','🍇']:           # check for winnings.
        winnings = bet_amount * 3
        # Contratulate the winner :)
        message = f"Congratulations! You have won ${winnings}!"
        threading.Thread(target=winning_sound).start()
        balance += winnings
    elif winning_symbols == ['🍌','🍌','🍌']:
        winnings = bet_amount * 5
        # Contratulate the winner :)
        message = f"Congratulations! You have won ${winnings}!"
        threading.Thread(target=winning_sound).start()
        balance += winnings
    elif winning_symbols == ['🍒','🍒','🍒']:
        winnings = bet_amount * 10
        # Contratulate the winner :)
        message = f"Congratulations! You have won ${winnings}!"
        threading.Thread(target=winning_sound).start()
        balance += winnings
    else:
        if balance == 0:
            message = "Truth is... the game was rigged from the start. :D" # No money, no more fun :(
        else:
            message = f"You lost, better luck next time -${bet_amount}" # Best wishes!
            threading.Thread(target=losing_sound).start()
             
    canvas.create_text(x, y, text=message, anchor=tk.CENTER, font=("Times New Roman", 24), fill="white") # Print the outcome.
    
    if "rigged" in message: # Checks if rigged is in the message, which only is in balance == 0 message
        threading.Thread(target=rigged_exit).start()
        canvas.after(7000, exit, None, casino) # so if balance == 0 get thrown out :D
    else:
        update_balance(canvas) # Updates the balance if its a winning row, or it stays the same if losing. (Already takes away the bet amount from balance.)

def random_symbol(choices): 
    random_num = random.random() # Randomize a number between 0 and 1
    probability_symbol = 0
    
    for symbol, probability in choices.items(): # Goes through every symbol and their probability if random number is 0.4 its = 🍇 which has a 55.56% probability (0.5556) so between 0 and 0.5556 its 🍇
        probability_symbol += probability       # or random number is 0.6 its = 🍌 which has a 27.78% probability (0.2778) so between 0.5556 and 0.8334 its 🍌
        if random_num <= probability_symbol:    # and if random number is above 0.8334 its 🍒 which has the last remaining 16.67% probability (0.1667) so between 0.8334 and 1 its 🍒
            return symbol                       # then it returns that symbol that matches probability with the random number.

def exit(event, casino):
    casino.destroy()

def window_exit(casino):
    close = messagebox.askyesno("Leave the Casino?", "Are you sure you want to exit?") # Pop up window asking if you really want to quit :)
    if close:
        casino.destroy()                                                               # if so it exits the program.

def on_left_click(event, canvas): # Uses the left click to click on buttons so the program can do its thing and spin! :)
    x, y = event.x, event.y       # These 2 rows commented I used to find the position so I can put out everything where I want it. It helped alot :D
    #position_text = f"({x}, {y})"                    
    #canvas.create_text(x, y, text=position_text, anchor=tk.NW, font=("Times New Roman", 12), fill="white")

def clear_canvas(canvas): # Looks cleaner to have a function clean the canvas :D
    canvas.delete("all")

def update_balance(canvas): # Updates the balance displayed when this function is called.
    global balance_text_change
    balance_text = "Balance: $" + str(balance)
    canvas.itemconfigure(balance_text_change, text=balance_text)
    balance_text_change = canvas.create_text(1080, 560, text=balance_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    
def update_bet_amount(canvas): # Updates the bet amount displayed when this function is called.
    global bet_amount_change
    bet_amount_text = "Bet Amount: $" + str(bet_amount)
    canvas.itemconfigure(bet_amount_change, text=bet_amount_text)
    bet_amount_change = canvas.create_text(1080, 460, text=bet_amount_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    
def winning_sound():
    playsound(r'C:\PATH\kaching.mp3') # Change PATH, right click "kaching.mp3" and COPY PATH and paste here    Kachiiiing

def losing_sound():
    playsound(r'C:\PATH\lose.mp3')   # Change PATH, right click "kaching.mp3" and COPY PATH and paste here     OOF

def rigged_exit():
    playsound(r'C:\PATH\rigged.mp3') # Change PATH, right click "rigged.mp3" and COPY PATH and paste here    Warning for this one, might end with a bang :D
  
def display_how_to_win_and_payout(canvas): # Left corner displays how to win and payout.
    canvas.create_text(120, 30, text="How to win ☟", anchor=tk.CENTER, font=("Times New Roman", 15), fill="white")
    canvas.create_text(120, 60, text="3 of a kind in the middle row", anchor=tk.CENTER, font=("Times New Roman", 12), fill="white")
    canvas.create_text(120, 90, text="| 🍇 | 🍇 | 🍇 | = Bet * 3", anchor=tk.CENTER, font=("Times New Roman", 15), fill="white")
    canvas.create_text(120, 120, text="| 🍌 | 🍌 | 🍌 | = Bet * 5", anchor=tk.CENTER, font=("Times New Roman", 15), fill="white")
    canvas.create_text(125, 150, text="| 🍒 | 🍒 | 🍒 | = Bet * 10", anchor=tk.CENTER, font=("Times New Roman", 15), fill="white")   
    
if __name__ == "__main__":
    main()
