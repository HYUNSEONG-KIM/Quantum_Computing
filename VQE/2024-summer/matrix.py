import tkinter as tk
from tkinter import Canvas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ShowMatrix(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.fig, self.ax = plt.subplots(figsize=(1.5, 1.5))
        self.ax.axis("off")
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.Y)

    def draw_matrix(self, matrix):
         self.ax.clear()

         self.ax.imshow(matrix, cmap="viridis")
         self.ax.axis("off")
         self.fig_canvas.draw()




if __name__ == "__main__":
    
    # Generate a sample matrix image using numpy
    matrix = np.random.rand(500, 500)
    
    # Create a tkinter window
    root = tk.Tk()
    root.title("Matrix Image on Canvas")
    
    ## Set up the canvas
    #canvas = Canvas(root, width=500, height=500)
    #canvas.pack(side=tk.TOP, fill=tk.Y)
    button = tk.Button(
        root, 
        text="change", 
        command=lambda: show_matrix.draw_matrix(np.random.rand(20, 50)))
    button.pack(pady=20)
    
    # Create a matplotlib figure and axis
    show_matrix = ShowMatrix(master=root, width=300, height=300)
    show_matrix.pack(side=tk.TOP, fill=tk.Y)
    
    show_matrix.draw_matrix(matrix)
    # Start the tkinter main loop
    root.mainloop()
