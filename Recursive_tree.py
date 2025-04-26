import turtle
import time

# Recursive tree drawing function
def draw_tree(t, branch_length, left_angle, right_angle, depth, reduction_factor):
    if depth == 0:
        return

    # Set branch color: brown for trunk, green for branches
    if depth > 2:
        t.pencolor("saddlebrown")  # trunk
    else:
        t.pencolor("forestgreen")  # branches

    # Adjust pensize based on depth
    t.pensize(depth + 1)

    # Draw the branch
    t.forward(branch_length)

    # Save position and heading
    current_pos = t.pos()
    current_heading = t.heading()

    # Left branch
    t.left(left_angle)
    draw_tree(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor)

    # Restore position and heading
    t.penup()
    t.setpos(current_pos)
    t.setheading(current_heading)
    t.pendown()

    # Right branch
    t.right(right_angle)
    draw_tree(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor)

    # Restore again
    t.penup()
    t.setpos(current_pos)
    t.setheading(current_heading)
    t.pendown()

# --- Main Program ---
def main():
    print("🌳 Recursive Tree Drawing with Animation")

    # Get user inputs
    left_angle = float(input("🌿 Enter left branch angle (e.g., 20): "))
    right_angle = float(input("🍃 Enter right branch angle (e.g., 25): "))
    start_length = float(input("🌲 Enter starting branch length (e.g., 100): "))
    max_depth = int(input("📐 Enter recursion depth (e.g., 5): "))
    reduction_factor = float(input("📉 Enter branch length reduction factor (e.g., 0.7): "))

    # Setup turtle screen
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Recursive Tree Drawing")
    t = turtle.Turtle()
    t.speed(0)
    t.left(90)  # Face upward
    t.penup()
    t.goto(0, -screen.window_height() // 2 + 50)
    t.pendown()

    # Use animation: draw step-by-step
    turtle.tracer(1, 20)  # Slow down slightly for animation effect

    # Draw tree
    draw_tree(t, start_length, left_angle, right_angle, max_depth, reduction_factor)

    t.hideturtle()
    turtle.done()

if __name__ == "__main__":
    main()
