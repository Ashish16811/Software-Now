import turtle
import tkinter as tk
from tkinter import messagebox

# Function to draw the tree recursively
def draw_tree(t, branch_length, left_angle, right_angle, depth, reduction_factor, is_stem=True):
    if depth == 0:
        return

    # Set color and thickness
    if is_stem:
        t.pencolor("saddlebrown")  # Trunk color
        t.pensize(12)
    else:
        t.pencolor("forestgreen")  # Branch color
        t.pensize(max(depth, 1))

    t.forward(branch_length)  # Draw current branch

    # Save current position and angle
    current_position = t.pos()
    current_heading = t.heading()

    # Draw left branch
    t.left(left_angle)
    draw_tree(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor, is_stem=False)

    # Go back to original position and heading
    t.penup()
    t.setpos(current_position)
    t.setheading(current_heading)
    t.pendown()

    # Draw right branch
    t.right(right_angle)
    draw_tree(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor, is_stem=False)

    # Go back again to original position and heading
    t.penup()
    t.setpos(current_position)
    t.setheading(current_heading)
    t.pendown()

# Function that starts the drawing when button clicked
def start_drawing():
    try:
        # Get user inputs
        left_angle = float(left_angle_entry.get())
        right_angle = float(right_angle_entry.get())
        start_length = float(start_length_entry.get())
        max_depth = int(max_depth_entry.get())
        reduction_factor = float(reduction_factor_entry.get())

        # Close GUI window
        window.destroy()

        # Setup Turtle window
        screen = turtle.Screen()
        screen.bgcolor("white")
        screen.title("🌳 Your Recursive Tree")

        t = turtle.Turtle()
        t.speed(0)
        t.left(90)  # Point turtle upwards
        t.penup()
        t.goto(0, -screen.window_height() // 2 + 50)
        t.pendown()

        turtle.tracer(1, 20)  # Add slight delay for animation effect

        draw_tree(t, start_length, left_angle, right_angle, max_depth, reduction_factor)

        t.hideturtle()
        turtle.done()

    except Exception as e:
        error_label.config(text=f"Error: {e}", fg="red")

# Function to show info popups
def show_info(parameter):
    messages = {
        "left_angle": "Left Branch Angle: How much the left branch tilts. Larger = more spread out.",
        "right_angle": "Right Branch Angle: How much the right branch tilts.",
        "start_length": "Starting Length: The size of the first trunk.",
        "max_depth": "Depth: How many layers of branches.",
        "reduction_factor": "Reduction Factor: How much smaller each new branch becomes."
    }
    messagebox.showinfo("Info", messages.get(parameter, "No info available."))

# --- GUI Setup ---

# Create main window
window = tk.Tk()
window.title("🌳 Easy Recursive Tree Generator")
window.geometry("600x700")
window.configure(bg="lightblue")

# Title label
title_label = tk.Label(window, text="Enter Values Below", font=("Arial", 20, "bold"), bg="lightblue")
title_label.pack(pady=20)

# Frame to hold all input fields
input_frame = tk.Frame(window, bg="lightblue")
input_frame.pack()

# Function to create label, entry box and info button
def create_input_row(label_text, variable_name):
    frame = tk.Frame(input_frame, bg="lightblue")
    frame.pack(pady=10, padx=20, fill="x")

    # Label + Info Button
    label_frame = tk.Frame(frame, bg="lightblue")
    label_frame.pack(anchor="w")
    label = tk.Label(label_frame, text=label_text, font=("Arial", 14), bg="lightblue")
    label.pack(side="left")
    info_button = tk.Button(label_frame, text="i", command=lambda: show_info(variable_name), bg="white", fg="blue", font=("Arial", 12, "bold"), width=2)
    info_button.pack(side="left", padx=5)

    # Entry Box
    entry = tk.Entry(frame, font=("Arial", 14))
    entry.pack(fill="x", pady=5)

    return entry

# Create input fields
left_angle_entry = create_input_row("Left Branch Angle (e.g., 20°):", "left_angle")
right_angle_entry = create_input_row("Right Branch Angle (e.g., 25°):", "right_angle")
start_length_entry = create_input_row("Starting Branch Length (e.g., 100):", "start_length")
max_depth_entry = create_input_row("Recursion Depth (e.g., 5):", "max_depth")
reduction_factor_entry = create_input_row("Reduction Factor (e.g., 0.7):", "reduction_factor")

# Create Tree Button
create_tree_button = tk.Button(window, text="🌳 Create Tree 🌳", command=start_drawing, bg="green", fg="white", font=("Arial", 16, "bold"), width=20)
create_tree_button.pack(pady=40)

# Error label
error_label = tk.Label(window, text="", font=("Arial", 12), bg="lightblue")
error_label.pack()

# Start the GUI loop
window.mainloop()
