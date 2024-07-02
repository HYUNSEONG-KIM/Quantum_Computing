import tkinter as tk


class CircleCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(side=tk.LEFT)
        self.bind("<Button-1>", self.create_circle)
        self.bind("<Control-Button-1>", self.delete_circle)
        self.bind("<Shift-Button-1>", self.toggle_select_circle)
        self.bind("<Shift-B1-Motion>", self.move_circle)
        self.bind("<a>", self.toggle_circle_color)

        self.bind("<Enter>", self.on_mouse_enter)

        self.circles = {}  # Store circles and their data
        self.lines = []  # Store lines and their endpoints
        self.selected_circles = []  # Keep track of selected circles
        self.moving_circle = None  # Currently moving circle

        self.marker = None
    def on_mouse_enter(self, event):
        self.focus_set()
    def create_circle(self, event):
        x, y = event.x, event.y
        r = 10  # Radius of the circle
        circle_id = self.create_oval(x-r, y-r, x+r, y+r, fill="blue", outline="black")
        self.circles[circle_id] = {"coords": (x, y), "lines": set(), "fill":"blue"}

    def delete_circle(self, event):
        item = self.find_closest(event.x, event.y)
        if item and item[0] in self.circles:
            for line_id in self.circles[item[0]]["lines"]:
                self.delete(line_id)
                self.lines = [line for line in self.lines if line["line_id"] != line_id]
            del self.circles[item[0]]
            self.delete(item[0])

    def toggle_select_circle(self, event):
        item = self.find_closest(event.x, event.y)
        if item and item[0] in self.circles:
            if item[0] in self.selected_circles:
                # Deselect the circle
                self.selected_circles.remove(item[0])
                self.itemconfig(item[0], outline="black")
            else:
                # Select the circle
                self.selected_circles.append(item[0])
                self.itemconfig(item[0], outline="red")
                if len(self.selected_circles) == 2:
                    self.manage_connection()
    
    def manage_connection(self):
        id1, id2 = self.selected_circles
        if id1 != id2:  # Ensure the ends are different circles
            common_line = self.circles[id1]["lines"] & self.circles[id2]["lines"]
            if common_line:
                line_id = common_line.pop()
                self.delete_line(id1, id2, line_id)
            else:
                self.connect_circles(id1, id2)
        for circle_id in self.selected_circles:
            self.itemconfig(circle_id, outline="black")
        self.selected_circles = []

    def delete_line(self, id1, id2, line_id):
        self.circles[id1]["lines"].remove(line_id)
        self.circles[id2]["lines"].remove(line_id)
        self.delete(line_id)
        self.lines = [line for line in self.lines if line["line_id"] != line_id]

    def connect_circles(self, id1, id2):
        x1, y1 = self.circles[id1]["coords"]
        x2, y2 = self.circles[id2]["coords"]
        line_id = self.create_line(x1, y1, x2, y2, fill="black")
        self.circles[id1]["lines"].add(line_id)
        self.circles[id2]["lines"].add(line_id)
        self.lines.append({"line_id": line_id, "circle1": id1, "circle2": id2})

    def move_circle(self, event):
        if not self.moving_circle:
            item = self.find_closest(event.x, event.y)
            if item and item[0] in self.circles:
                self.moving_circle = item[0]
        if self.moving_circle:
            x, y = event.x, event.y
            r = 10
            self.coords(self.moving_circle, x-r, y-r, x+r, y+r)
            self.circles[self.moving_circle]["coords"] = (x, y)
            self.update_lines(self.moving_circle)
            self.moving_circle=False # test

    def update_lines(self, circle_id):
        for line in self.lines:
            if line["circle1"] == circle_id or line["circle2"] == circle_id:
                x1, y1 = self.circles[line["circle1"]]["coords"]
                x2, y2 = self.circles[line["circle2"]]["coords"]
                self.coords(line["line_id"], x1, y1, x2, y2)

    def release_circle(self, event):
        self.moving_circle = None
        self.unbind("<ButtonRelease-1>")

    def toggle_circle_color(self, event):
        item = self.find_closest(event.x, event.y)
        if item and item[0] in self.circles:
            current_color = self.itemcget(item[0], "fill")
            new_color = "red" if current_color == "blue" else "blue"
            self.itemconfig(item[0], fill=new_color)
            self.circles[item[0]]["fill"] = "red"

    def count_cut(self):
        cut = 0
        for line in self.lines:
            cir_c1 = self.itemcget(line["circle1"], "fill")
            cir_c2 = self.itemcget(line["circle2"], "fill")
            if cir_c1 != cir_c2:
                cut += 1
        return cut
    def draw_id_on_circle(self):
        if self.marker is None:
            self.marker = []
            for c in self.circles:
                x1, y1, x2, y2= self.coords(c)
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                self.marker.append(
                    self.create_text(
                        cx, cy-30, 
                        text=c,
                        font=('Helvetica', 12), fill='black' 
                        )
                    )
                print(c)
        else: #delete markers
            for id in self.marker:
                self.delete(id)
            self.marker = None
    def export_graph(self):
        return self.circles, self.lines

def update_label(canvas, label):
    num_lines = canvas.count_cut()
    label.config(text=f"Number of cut: {num_lines}")



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ising VQA")

    casnvas_frame = tk.LabelFrame(root, text="Graph Canvas", relief="solid", bd=2)
    casnvas_frame.pack(side=tk.LEFT, fill=tk.Y)
    canvas = CircleCanvas(casnvas_frame, width=400, height=400, bg="white")

    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.RIGHT, fill=tk.Y)

    label = tk.Label(control_frame, text="Number of cut: 0")
    label.pack(pady=20)

    button = tk.Button(control_frame, text="Count Cut", command=update_label)
    button.pack(pady=20)

    canvas.focus_set()  # Set focus to the canvas to capture key events
    root.mainloop()
