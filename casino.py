import tkinter as tk
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk

import random

# Canvas size
canvas_width = 1200
canvas_height = 600

symbols = ['🍇', '🍌', '🍒']

balance = 1000
bet_amount = 0

def main():
    casino = tk.Tk()
    casino.title("Casino Royale")

    canvas = tk.Canvas(casino, width=canvas_width, height=canvas_height, bg="black")
    canvas.pack()
    
    # Load the background image
    original_image = Image.open(r"C:\Users\jespe\codeInPlaceFinalProject\slotsMachine.png")
    
    # Resize the image to fit the canvas
    resized_image = original_image.resize((canvas_width, canvas_height))

    # Convert the resized image to a PhotoImage object
    background_image = ImageTk.PhotoImage(resized_image)
    
    # Create the background image on the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image, tags="background")
    canvas.background_image = background_image
    
    main_menu(canvas, casino, background_image)

    # Bind left mouse click to the function on_left_click
    canvas.bind("<Button-1>", lambda event: on_left_click(event, canvas))

    # Window closing protocol, runs the "def window_exit() when clicking the (X) in the corner of the window"
    casino.protocol("WM_DELETE_WINDOW", partial(window_exit, casino))

    casino.mainloop()

def main_menu(canvas, casino, background_image):
    clear_canvas(canvas, background_image)
    x = canvas_width / 2
    y = canvas_height / 2

    welcome_text = "Welcome To Casino Royale!"
    canvas.create_text(x, y, text=welcome_text, anchor=tk.CENTER, font=("Times New Roman", 42), fill="white")

    # Show Balance
    balance_text = "Balance: $" + str(balance)
    canvas.create_text(1000, 560, text=balance_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")

    play_text = canvas.create_text(x, y + 90, text="● Press here to play slots", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    canvas.tag_bind(play_text, "<Button-1>", partial(play_slots, canvas=canvas, casino=casino, background_image=background_image))

    exit_text = canvas.create_text(x, y + 150, text="● Exit", anchor=tk.CENTER, font=("Times New Roman", 16), fill="white")
    canvas.tag_bind(exit_text, "<Button-1>", partial(exit, casino=casino))

def play_slots(event, canvas, casino, background_image):
    clear_canvas(canvas, background_image)

    # Showing Balance
    balance_text = "Balance: $" + str(balance)
    canvas.create_text(1000, 560, text=balance_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")

    # Exit to main menu text
    exit_text = canvas.create_text(180, 560, text="Exit", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
    canvas.tag_bind(exit_text, "<Button-1>", partial(exit, casino=casino))

    build_slot_machine(canvas)

    # Entry widget for entering bet amount
    global entry
    entry = tk.Entry(casino, width=15, font=("Times New Roman", 12))
    entry.place(x=915, y=500)

    # Button to submit the bet amount and spin
    submit_button = tk.Button(casino, text="Bet", command=lambda: bet_and_spin(canvas, casino, background_image), font=("Times New Roman", 12))
    submit_button.place(x=1040, y=500)
    
    # Button to spin with the same bet amount
    spin_button = tk.Button(casino, text="Spin", command=lambda: spin_same_bet(canvas, casino, background_image), font=("Times New Roman", 12))
    spin_button.place(x=800, y=300)

def bet_and_spin(canvas, casino, background_image):
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
        entry.delete(0, tk.END)  # Clear the entry widget after retrieving the input
        # Spin the slot machine
        winning_symbols = spin(canvas, casino, symbols, background_image)
        check_winning(canvas, winning_symbols, bet_amount)

def spin_same_bet(canvas, casino, background_image):
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
        # Spin the slot machine
        winning_symbols = spin(canvas, casino, symbols, background_image)
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

def spin(canvas, casino, symbols, background_image):
    # To remove symbols from spins before, so they don't stack.
    clear_canvas(canvas, background_image)

    build_slot_machine(canvas)

    # Showing Balance
    balance_text = "Balance: $" + str(balance)
    canvas.create_text(1000, 560, text=balance_text, anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")

    # Exit to main menu text
    exit_text = canvas.create_text(200 , canvas_height / 2 + 280 , text="Exit", anchor=tk.CENTER, font=("Times New Roman", 20), fill="white")
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
            end_x = start_x + BOX_SIZE
            end_y = start_y + BOX_SIZE
            symbol = random.choice(symbols)
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
    if winning_symbols == ['🍇','🍇','🍇'] or winning_symbols == ['🍒','🍒','🍒'] or winning_symbols == ['🍌','🍌','🍌']:
        canvas.create_text(x, y, text="Congratulations! You have won!", anchor=tk.CENTER, font=("Times New Roman", 24), fill="white")
        balance += bet_amount * 2
    else:
        canvas.create_text(x, y, text="You lost, better luck next time!", anchor=tk.CENTER, font=("Times New Roman", 24), fill="white")

def exit(event, casino):
    casino.destroy()

def window_exit(casino):
    close = messagebox.askyesno("Leave the Casino?", "Are you sure you want to exit?")
    if close:
        casino.destroy()

def on_left_click(event, canvas):
    x, y = event.x, event.y
    #position_text = f"({x}, {y})"
    #canvas.create_text(x, y, text=position_text, anchor=tk.NW, font=("Times New Roman", 12), fill="white")

def clear_canvas(canvas, background_image):
    canvas.delete(tk.ALL)
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image, tags="background")

if __name__ == "__main__":
    main()
