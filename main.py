import tkinter as tk
import csv
import random

# func load csv
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

# func to gen random value
def dynamic_random(rand_min, rand_max):
    random_value = round(random.uniform(rand_min, rand_max), 2)
    return max(random_value, 0)  # clamp

# func 4 display new question
def new_question():
    global current_row, random_value
    current_row = random.choice(data)  # pick a random row from data
    name_label.config(text=current_row['name'])

    # get and validate rand_min and rand_max
    try:
        rand_min = float(current_row['rand_min']) if current_row['rand_min'] else 0
        rand_max = float(current_row['rand_max']) if current_row['rand_max'] else 100
    except ValueError:
        rand_min = 0
        rand_max = 100

    random_value = dynamic_random(rand_min, rand_max)  # generate random value
    value_label.config(text=f"{random_value} {current_row['unit']}")

    # hide feedback section & show question section
    feedback_frame.pack_forget()
    question_frame.pack()

# func user input buttons
def check_answer(answer_type):
    min_val = float(current_row['min'])
    max_val = float(current_row['max'])

    # check the answer type and compare the random value
    if answer_type == "less_than":
        is_correct = random_value < min_val
    elif answer_type == "within":
        is_correct = min_val <= random_value <= max_val
    else:  # answer_type == "greater_than"
        is_correct = random_value > max_val

    # hide the question section and show the feedback section
    question_frame.pack_forget()
    feedback_frame.pack()

    # update feedback message
    if is_correct:
        feedback_label.config(text="Correct!", fg="green")
    else:
        feedback_label.config(text="Incorrect!", fg="red")

    # show note
    note_label.config(text=current_row['note'], fg="gray")

# func adjust font size
def adjust_font_size(delta):
    global font_size
    font_size += delta
    font_size = max(8, font_size)  # clamp at 8

    update_font_size()

# func update font size and input box value
def update_font_size():
    name_label.config(font=("Arial", font_size))
    value_label.config(font=("Arial", font_size))
    feedback_label.config(font=("Arial", font_size))
    note_label.config(font=("Arial", font_size - 4))
    font_size_entry.delete(0, tk.END)
    font_size_entry.insert(0, str(font_size))

# func set font size from input box
def set_font_size(event=None):
    global font_size
    try:
        new_size = int(font_size_entry.get())
        font_size = max(8, new_size)  # clamp at 8
        update_font_size()
    except ValueError:
        font_size_entry.delete(0, tk.END)
        font_size_entry.insert(0, str(font_size))

# func button sunken
def press_button_effect(button):
    button.config(relief="sunken")
    root.update_idletasks()
    root.after(100, lambda: button.config(relief="raised"))

# load data from CSV before starting the Tkinter GUI loop
filename = "lab_value.csv"  # make sure the CSV file is in the correct directory
data = load_csv_to_dict(filename)  # load the CSV data into the `data` variable

# Tkinter GUI setup
root = tk.Tk()
root.title("Lab Value Quiz")
font_size = 16  # default font size

# top-right control buttons
control_frame = tk.Frame(root)
control_frame.pack(anchor="ne", padx=10, pady=5)

increase_font_button = tk.Button(control_frame, text="+", command=lambda: adjust_font_size(1))
increase_font_button.grid(row=0, column=2, padx=5)

font_size_entry = tk.Entry(control_frame, width=5, justify="center")
font_size_entry.grid(row=0, column=1, padx=5)
font_size_entry.insert(0, str(font_size))
font_size_entry.bind("<Return>", set_font_size)


decrease_font_button = tk.Button(control_frame, text="-", command=lambda: adjust_font_size(-1))
decrease_font_button.grid(row=0, column=0, padx=5)

# question and feedback section
name_label = tk.Label(root, text="", font=("Arial", font_size), pady=10)
name_label.pack()

# feedback section
feedback_frame = tk.Frame(root)
feedback_label = tk.Label(feedback_frame, text="", font=("Arial", font_size))
feedback_label.pack(pady=10)

note_label = tk.Label(feedback_frame, text="", font=("Arial", font_size - 4), fg="gray")
note_label.pack(pady=5)

continue_button = tk.Button(feedback_frame, text="Continue", command=new_question, bg="lightblue", width=15)
continue_button.pack(pady=10)

# question section
value_label = tk.Label(root, text="", font=("Arial", font_size - 2))
value_label.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# too low, normal, too high buttons
less_than_button = tk.Button(button_frame, text="Too Low", command=lambda: check_answer("less_than"), bg="lightgreen", width=10)
less_than_button.grid(row=0, column=0, padx=10)

within_button = tk.Button(button_frame, text="Normal", command=lambda: check_answer("within"), bg="lightblue", width=10)
within_button.grid(row=0, column=1, padx=10)

greater_than_button = tk.Button(button_frame, text="Too High", command=lambda: check_answer("greater_than"), bg="lightcoral", width=10)
greater_than_button.grid(row=0, column=2, padx=10)

# keyboard shortcuts
root.bind("j", lambda event: (press_button_effect(less_than_button), check_answer("less_than")))
root.bind("k", lambda event: (press_button_effect(within_button), check_answer("within")))
root.bind("l", lambda event: (press_button_effect(greater_than_button), check_answer("greater_than")))
root.bind("<space>", lambda event: (press_button_effect(continue_button), new_question()))

# question section
question_frame = tk.Frame(root)

# start with a question
current_row = {}
random_value = 0
new_question()

# start the Tkinter event loop
root.mainloop()
