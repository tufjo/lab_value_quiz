import tkinter as tk
import csv
import random

# Function to load the CSV file
def load_csv_to_dict(filename):
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]
            if not rows:
                raise ValueError("The CSV file is empty.")
            return rows
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        exit()
    except Exception as e:
        print(f"Error: {e}")
        exit()

# Function to generate a random value using the rand_min and rand_max values
def dynamic_random(rand_min, rand_max):
    # Generate a random value within the provided rand_min and rand_max range
    random_value = round(random.uniform(rand_min, rand_max), 2)
    return max(random_value, 0)  # Ensure it's not below 0

# Function to display a new question
def new_question():
    global current_row, random_value
    current_row = random.choice(data)  # Pick a random row from data
    name_label.config(text=current_row['name'], font=("Arial", 16))

    # Get and validate rand_min and rand_max
    try:
        rand_min = float(current_row['rand_min']) if current_row['rand_min'] else 0
        rand_max = float(current_row['rand_max']) if current_row['rand_max'] else 100
    except ValueError:
        rand_min = 0
        rand_max = 100

    random_value = dynamic_random(rand_min, rand_max)  # Generate the random value
    value_label.config(text=f"{random_value} {current_row['unit']}")

    # Hide feedback section and show question section
    feedback_frame.pack_forget()
    question_frame.pack()

# Function to handle user input for Less Than, Within, Greater Than buttons
def check_answer(answer_type):
    min_val = float(current_row['min'])
    max_val = float(current_row['max'])

    # Check the answer type and compare the random value
    if answer_type == "less_than":
        is_correct = random_value < min_val
    elif answer_type == "within":
        is_correct = min_val <= random_value <= max_val
    else:  # answer_type == "greater_than"
        is_correct = random_value > max_val

    # Hide the question section and show the feedback section
    question_frame.pack_forget()
    feedback_frame.pack()

    # Update feedback message
    if is_correct:
        feedback_label.config(text="Correct!", fg="green", font=("Arial", 16))
    else:
        feedback_label.config(text="Incorrect!", fg="red", font=("Arial", 16))

    # Show the note
    note_label.config(text=current_row['note'], font=("Arial", 12), fg="gray")

# Function to simulate button press effect
def press_button_effect(button):
    button.config(relief="sunken")
    root.update_idletasks()
    root.after(100, lambda: button.config(relief="raised"))

# Load data from CSV before starting the Tkinter GUI loop
filename = "lab_value.csv"  # Make sure the CSV file is in the correct directory
data = load_csv_to_dict(filename)  # Load the CSV data into the `data` variable

# Tkinter GUI setup
root = tk.Tk()
root.title("Lab Value Quiz")

# Widgets for the question and feedback section
name_label = tk.Label(root, text="", font=("Arial", 16), pady=10)
name_label.pack()

# Feedback section for Correct/Incorrect
feedback_frame = tk.Frame(root)
feedback_label = tk.Label(feedback_frame, text="", font=("Arial", 16))
feedback_label.pack(pady=10)

note_label = tk.Label(feedback_frame, text="", font=("Arial", 12), fg="gray")
note_label.pack(pady=5)

continue_button = tk.Button(feedback_frame, text="Continue", command=new_question, bg="lightblue", width=15)
continue_button.pack(pady=10)

# Question section (will be replaced by feedback section when user answers)
value_label = tk.Label(root, text="", font=("Arial", 14))
value_label.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Buttons for Less Than, Within, Greater Than answers
less_than_button = tk.Button(button_frame, text="Lower", command=lambda: check_answer("less_than"), bg="lightgreen", width=10)
less_than_button.grid(row=0, column=0, padx=10)

within_button = tk.Button(button_frame, text="Normal", command=lambda: check_answer("within"), bg="lightblue", width=10)
within_button.grid(row=0, column=1, padx=10)

greater_than_button = tk.Button(button_frame, text="Higher", command=lambda: check_answer("greater_than"), bg="lightcoral", width=10)
greater_than_button.grid(row=0, column=2, padx=10)

# Bind keyboard shortcuts to buttons with press effect
root.bind("j", lambda event: (press_button_effect(less_than_button), check_answer("less_than")))
root.bind("k", lambda event: (press_button_effect(within_button), check_answer("within")))
root.bind("l", lambda event: (press_button_effect(greater_than_button), check_answer("greater_than")))
root.bind("<space>", lambda event: (press_button_effect(continue_button), new_question()))

# Widgets for the question section (hidden initially)
question_frame = tk.Frame(root)

# Start with a question
current_row = {}
random_value = 0
new_question()

# Start the Tkinter event loop
root.mainloop()
