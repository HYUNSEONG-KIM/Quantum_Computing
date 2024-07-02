import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import Event
import random

from qiskit.circuit.library import EfficientSU2, ExcitationPreserving

import re

from color import color_function
#-------------------

def extract_numbers(qubit_string):
    pattern = r"Qubit\(QuantumRegister\((\d+), '[a-zA-Z]'\), (\d+)\)"
    match = re.search(pattern, qubit_string)
    if match:
        register_number = int(match.group(1))
        qubit_index = int(match.group(2))
        return register_number, qubit_index
    else:
        raise ValueError("The input string does not match the expected format")

def get_info_node(node):
    name = node.name
    num_qubits = node.op.num_qubits 
    params = [q.name for q in node.op.params]
    qubit_loc = [extract_numbers(str(q))[1] for q in node.qargs]
    return name, num_qubits, params, qubit_loc


# Style 

style_gate = {
    "h":{
        "bg": "salmon",
        "tc": "black",
    },
    "rx":{
        "bg": "pale green",
        "tc": "white"
    },
    "ry":{
        "bg": "CadetBlue1",
        "tc": "white"
    },
    "rz":{
        "bg": "pink",
        "tc": "white"
    },
    "u":{
        "bg": "yellow",
        "tc": "black"
    }
}

class CircuitCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        #self.pack(side=tk.LEFT)
        self.ansatz = None

        self.loc = [100, 90]
        self.d = 40
        self.nodes = []
        self.gates = []
        self.param_index = []
        #self.draw_sample()
        self.configure(scrollregion=self.bbox("all"))

        # Mouse zoom 
        self.bind("<MouseWheel>", self.zoom)
        self.scale_factor = 1.0

    def zoom(self, event: Event):
        scale = 1.0
        if event.delta > 0:
            scale = 1.1
            self.scale_factor *= scale
        elif event.delta < 0:
            scale = 0.9
            self.scale_factor *= scale

        self.scale("all", event.x, event.y, scale, scale)
        self.configure(scrollregion=self.bbox("all"))

    def set_dim(self, x0, y0, dd=30):
        self.loc = [x0, y0]
        self.d = dd

    def cal_loc(self, i, j):
        x0, y0 = self.loc

        x = x0+i*self.d
        y = y0+j*self.d
        return x, y
    def draw_circuit(self, nodes):
        x, y = self.loc
        qubits_num = extract_numbers(str(nodes[0][0].qargs))[0]
        total_len = len(nodes)

        print("Qubits", qubits_num )
        print("totla_len:", total_len)
        # Draw lines
        for i in range(qubits_num):
            dy = i*self.d
            self.create_line(x-2*self.d, y+dy-1   , x+(total_len+1)*self.d, y+dy-1, fill="black")
            self.create_line(x-2*self.d, y+dy     , x+(total_len+1)*self.d, y+dy, fill="black")
            self.create_line(x-2*self.d, y+dy+1   , x+(total_len+1)*self.d, y+dy+1, fill="black")

        self.multi_gate((x-3*self.d, y), qubits_num , "|Ψ>", "gold", 2, 20)

        for i, node in enumerate(nodes):
            for j, n in enumerate(node):
                name, qubits, params, loc = get_info_node(n)
                if name[0] == "c":
                    x0, y0 = self.cal_loc(i, loc[0])
                    x1, y1 = self.cal_loc(i, loc[1])

                    gate_param = (
                        True, 
                        [(x1, y1), 
                        "⊕", "white", 30, 
                        False])
                    self.gates.append(
                        self.cgate((x0, y0), (x1, y1), gate_param, cont_type=0)
                    )

                elif qubits == 1:
                    #print("qubit 1:", name)
                    x0, y0 = self.cal_loc(i, loc[0])
                    custom_style = style_gate[name]
                    #print(custom_style)
                    if len(params) ==0:
                        self.gates.append(
                            self.gate((x0, y0), name, custom_style["bg"])
                        )
                    # if param exists
                    else:
                        self.param_index.append(len(self.gates))
                        self.gates.append(
                            self.param_gate(
                                (x0, y0), 
                                name, 
                                params[0],
                                custom_style["bg"])
                        )
                else:
                    x0, y0 = self.cal_loc(i, loc[0])
                    if len(params) == 0:
                        self.multi_gate((x0, y0), qubits, name, "pink", 1)
                    else:
                        self.param_index.append(len(self.gates))
                        self.gates.append(
                            self.param_multi_gate((x0, y0), qubits, name, params[0], "pink", 1)
                        )
            x += self.d
        # Draw Measurement
        self.multi_gate((x+self.d, y), qubits_num , "     M\n<Ψ|H|Ψ>", "yellow", 2, 30)

    #Basic gates ====
    def gate(self, loc, text, color, font_size=15, bg=True):
        x, y = loc
        dd = self.d / 2
        gate_id = {
            "type": "single",
            "rec": self.create_rectangle(x-dd, y+dd, x+dd, y-dd, fill=color) if bg else None,
            "text": self.create_text(x, y, text=text, font=('Helvetica', font_size), fill='black'),
            "params": (loc, text, color, font_size, bg)
        }
        return gate_id

    def param_gate(self, loc, text, param, color, font_size=15, bg=True):
        x, y = loc
        dd = self.d / 2
        gate_id = {
            "type": "param_single",
            "rec": self.create_rectangle(x-dd, y+dd, x+dd, y-dd, fill=color) if bg else None,
            "text": self.create_text(x, y-dd/4, text=text, font=('Helvetica', int(font_size/1.2)), fill='black'),
            "param": self.create_text(x, y+dd/2, text=param, font=('Helvetica', int(font_size/1.3)), fill='black'),
            "params": (loc, text, param, color, font_size, bg)
        }
        return gate_id

    def multi_gate(self, loc, num, text, color, space=1, font_size=15, bg=True):
        x, y = loc
        dd = self.d / 2
        gate_id = {
            "type": "multi",
            "rec": self.create_rectangle(x-dd, y+dd+(num-1)*self.d, x+space*self.d-dd, y-dd, fill=color),
            "text": self.create_text(x+space*self.d/2 -dd, y+(num-1)*self.d/2, text=text, font=('Helvetica', 15), fill='black'),
            "params": (loc, num, text, color, 1, font_size, bg)
        }
        return gate_id
    def param_multi_gate(self, loc, num, text, param, color, space=1, font_size=15, bg=True):
        x, y = loc
        dd = self.d / 2

        cx, cy = x, y 

        gate_id = {
            "type": "multi",
            "rec": self.create_rectangle(x-dd, y+dd+(num-1)*self.d, x+space*self.d -dd, y-dd, fill=color),
            "text": self.create_text(cx+space*self.d/2 -dd, cy+(num-1)*dd/2, text=text, font=('Helvetica', int(font_size/1.2)), fill='black'),
            "param": self.create_text(cx+space*self.d/2 -dd, cy+(num+1)*dd/2, text=param, font=('Helvetica', int(font_size/1.3)), fill='black'),
            "params": (loc, num, text, color, 1, font_size, bg)
        }
        return gate_id
    def cgate(self, loc, tloc, gate_pack, cont_type=0):
        x, y = loc
        xt, yt = tloc
        dd = self.d / 6
        fill_type = "black" if cont_type == 0 else "white"
        line_id = self.create_line(x, y, xt, yt, fill="black")
        g_type, args = gate_pack
        gate_id = {
            "type": "control",
            "ctrl": self.create_oval(x-dd, y-dd, x+dd, y+dd, fill=fill_type, outline="black"),
            "line": line_id,
            "subgate": self.gate(*args) if g_type else self.multi_gate(*args),
            "params": (loc, tloc, gate_pack, cont_type)
        }
        return gate_id

    def change_random_rectangle_color(self):
        if self.gates:
            idx = random.choice(self.param_index)
            random_gate = self.gates[idx]
            if random_gate["type"] in ["single", "param_single", "multi"]:
                colors = ["red", "blue", "yellow", "green", "purple", "orange", "pink"]
                new_color = random.choice(colors)
                self.itemconfig(random_gate["rec"], fill=new_color)
    def update_color_by_params(self, params):
        if self.gates:
            for pidx, param in zip(self.param_index, params):
                gate = self.gates[pidx]
                name = gate["text"]
                new_color = color_function(param)
                rec_id = gate["rec"] if "rec" in gate.keys() else gate["subgate"]["rec"]
                self.itemconfig(rec_id, fill=new_color)
    # Ansatz
    def apply_ansatz(self, text, qubits):
        self.delete('all')
        if text == "EfficientSU2":
            self.ansatz = EfficientSU2(qubits, reps=3)
        else:
            self.ansatz = ExcitationPreserving(qubits, entanglement='linear')
        nodes = self.ansatz.decompose().draw().nodes
        self.draw_circuit(nodes)

# Create the main window
if __name__=="__main__":
    root = tk.Tk()
    root.title("Ising VQA")

    canvas_frame = tk.LabelFrame(root, text="Graph Canvas", relief="solid", bd=2)
    canvas_frame.pack(side=tk.LEFT, fill=tk.Y)
    canvas = CircuitCanvas(canvas_frame, width=800, height=400, bg="white")
    canvas.pack(side=tk.TOP, fill=tk.Y)
    # Adding scrollbars
    canvas_hbar = Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    canvas_hbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(xscrollcommand=canvas_hbar.set)

    canvas_vbar = Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
    canvas_vbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=canvas_vbar.set)



    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.RIGHT, fill=tk.Y)
    change_color_button = tk.Button(button_frame, text="Change Color", command=canvas.change_random_rectangle_color)
    change_color_button.pack(pady=20)

    ansatz_name = tk.StringVar()
    ansatz_combo = ttk.Combobox(button_frame, width=30, textvariable=ansatz_name)
    ansatz_combo["value"] = ["EfficientSU2", "ExcitationPreserving"]
    ansatz_combo.pack()
    apply_ansatz_button = tk.Button(
        button_frame, text="Apply", 
        command=lambda: canvas.apply_ansatz(ansatz_name.get())
        )
    apply_ansatz_button.pack(pady=5)
    #-----------

    root.mainloop()
