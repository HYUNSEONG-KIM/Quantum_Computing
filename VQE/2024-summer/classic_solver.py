import tkinter as tk
import networkx as nx
import numpy as np
from networkx.algorithms.approximation import randomized_partitioning


class ClassicSolver(tk.LabelFrame):
    def __init__(self, master= None, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = tk.Canvas(master=self, width=500, height=500, bg="white")
        self.canvas.pack(side=tk.BOTTOM, fill=tk.X)
        self.c_label_cut = tk.Label(self, text="Max_cut = 0", font=("Arial", 15))
        self.c_label_cut.pack(pady=20)

        self.max_cut = 0
        self.partition = None
    def draw_graph(self, circles, lines):
        self.canvas.delete("all")
        r= 10
        for line in lines:
            c1_idx = line["circle1"]
            c2_idx = line["circle2"]

            c1_x, c1_y = circles[c1_idx]["coords"]
            c2_x, c2_y = circles[c2_idx]["coords"] 
            self.canvas.create_line(c1_x, c1_y, c2_x, c2_y, fill="black")
        for circle in circles.keys():
            x, y = circles[circle]["coords"]
            color = circles[circle]["fill"]
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="black")
    def solve_cut(self, graph:nx.Graph, circles, lines):
        p = 0.1
        dp = 0.1
        max_cut_size = 0
        max_partition = None
        for i in range(0, 10):
            pi = p + i*dp

            cut_size, partition = randomized_partitioning(graph, p=pi)

            if max_cut_size < cut_size:
                max_cut_size = cut_size
                max_partition = partition

        if max_cut_size < self.max_cut:
            pass
        else:
            self.c_label_cut.config(text=f"Max_cut={max_cut_size}")

            red_list = list(list(max_partition)[0])
            blue_list = list(list(max_partition)[1])
            for cidx in red_list:
                circles[cidx]["fill"] = "red"
            for cidx in blue_list:
                circles[cidx]["fill"] = "blue"
            self.draw_graph(circles, lines)

            self.max_cut = max_cut_size
            self.partition = max_partition





