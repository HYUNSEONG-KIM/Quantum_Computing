import numpy as np
import tkinter as tk
from scipy.optimize import minimize

# Create a Tkinter window
root = tk.Tk()
root.title("Optimization Visualization")

# Create a canvas
canvas = tk.Canvas(root, width=400, height=400, bg='white')
canvas.pack()

# Define a function to update the canvas
def update_canvas(params):
    canvas.delete("all")
    x, y = params
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='blue')
    canvas.update()

# Define an objective function to minimize (e.g., a simple quadratic function)
def objective(params):
    x, y = params
    return (x - 200)**2 + (y - 200)**2

# Define a callback function to update the canvas during optimization
def callback(params):
    update_canvas(params)
    root.update_idletasks()

# Initial guess for the parameters
initial_guess = [50, 50]

# Perform the optimization
result = minimize(objective, initial_guess, callback=callback)

# Print the result
print("Optimization Result:", result)

# Start the Tkinter main loop
root.mainloop()
