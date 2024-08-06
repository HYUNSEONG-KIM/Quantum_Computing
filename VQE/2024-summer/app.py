import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import Event
import random

from qiskit.circuit.library import EfficientSU2, ExcitationPreserving
from qiskit.quantum_info import SparsePauliOp

import numpy as np
import networkx as nx

import re

import time
#-------------------
from Ising_vqe import CircleCanvas, update_label
from matrix import ShowMatrix
from qiskit_draw import extract_numbers, get_info_node, CircuitCanvas

from mat_cal import zizj

from classic_solver import ClassicSolver
from qiskit_VQE import VQEFrame


if __name__=="__main__":
    hamiltonain = None
    graph = None
    net_graph = None

    qiskit_hamiltonian = None
    # Create the main window
    root = tk.Tk()
    root.title("Ising VQA")

    #Graph canvas==============\\
    graph_casnvas_frame = tk.LabelFrame(root, text="Graph Canvas", relief="solid", bd=2)
    graph_casnvas_frame.grid(row=0, column=0, rowspan=2)

    control_frame = tk.Frame(graph_casnvas_frame)
    control_frame.pack(side=tk.TOP, fill=tk.X)
    label = tk.Label(control_frame, text="Number of cut: 0", font=("Arial", 15))
    label.pack(pady=10)
    button = tk.Button(control_frame, text="Count Cut", command=lambda:update_label(graph_canvas, label))
    button.pack(pady=5)
    button2 = tk.Button(control_frame, text="Mark Circle")
    button2.pack(pady=1)

    graph_canvas = CircleCanvas(graph_casnvas_frame, width=600, height=600, bg="white")
    graph_canvas.pack(side=tk.BOTTOM, fill=tk.Y)

    button2.config(command=lambda: graph_canvas.draw_id_on_circle())

    #=================
    classic_frame = ClassicSolver(root,  text="Classic", width=300, height=450)
    classic_frame.grid(row=0, column=1, rowspan=2)
    classic_solve_button = tk.Button(classic_frame, text="Solve")

    def solve_classic():
        if net_graph is None:
            print("Graph has not been maken.")
            return None
        circles, lines = graph_canvas.export_graph()
        classic_frame.solve_cut(net_graph, circles, lines)

    classic_solve_button.config(command=solve_classic)
    classic_solve_button.pack()

    #Matrix==================
    m_frame = tk.LabelFrame(master=root, text="Hamiltonian")
    m_frame.grid(row=2, column=0)
    # image_frame, 
    show_matrix_frame = ShowMatrix(master=m_frame , width=350, height=350)
    show_matrix_frame.grid(row=1, column=0)

    def get_h_matrix(canvas):
        global hamiltonain, graph, net_graph, qiskit_hamiltonian
        nodes = set()
        edge = set()
        for c in canvas.circles:
            nodes.add(c)
        for line in canvas.lines:
            edge.add(frozenset([line["circle1"], line["circle2"]]))
        
        node_list= list(nodes)
        edge_list = list(edge)
        graph = [node_list, edge_list]
        net_graph = nx.Graph()
        net_graph.add_nodes_from(node_list)
        net_graph.add_edges_from(edge_list)

        n = len(nodes)
        _2n = int(2**n)

        hamiltonain = len(edge_list) * np.eye(_2n, dtype=complex)
        p_strs = []
        for edge in edge_list:
            c1, c2 = edge

            i1 = node_list.index(c1)
            i2 = node_list.index(c2)

            ZiZj = zizj(n, i1,i2)
            hamiltonain -= ZiZj

            l = n*["I"]
            l[i1] = "Z"
            l[i2] = "Z"
            p_strs.append("".join(l))
        
        qiskit_hamiltonian= SparsePauliOp.from_list(
            [(n*"I", -n/2)]+[(p, 0.5) for p in p_strs]
        )

        hamiltonain *= -0.5
        show_matrix_frame.draw_matrix(hamiltonain.real)
    mat_button = tk.Button(
        m_frame , 
        text="Get Hamiltonain", 
        command= lambda: get_h_matrix(graph_canvas)
        #lambda: show_matrix_frame.draw_matrix(np.random.rand(20, 50))
        )
    mat_button.grid(row=0, column=0)

    #=====================
    ansatz_frame = tk.Frame(root)
    ansatz_frame.grid(row=2, column=1, columnspan=3)
    canvas_frame = tk.LabelFrame(ansatz_frame, text="Circuit ansatz", relief="solid", bd=2)
    canvas_frame.grid(row=0, column=0)
    canvas = CircuitCanvas(canvas_frame, width=500, height=250, bg="white")
    canvas.pack(side=tk.TOP, fill=tk.Y)
    # Adding scrollbars
    canvas_hbar = Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    canvas_hbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(xscrollcommand=canvas_hbar.set)

    canvas_vbar = Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
    canvas_vbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=canvas_vbar.set)


    def set_params(circuit_canvas):
         p_index = circuit_canvas.param_index
         params = 1/2 * np.ones(len(p_index))

         circuit_canvas.update_color_by_params(params)

    button_frame = tk.Frame(ansatz_frame)
    button_frame.grid(row=0, column=1)
    change_color_button = tk.Button(
        button_frame, text="Set Params", 
        command=lambda: set_params(canvas))
    change_color_button.pack(pady=20)

    ansatz_name = tk.StringVar(value="EfficientSU2")
    ansatz_combo = ttk.Combobox(button_frame, width=30, textvariable=ansatz_name, state='readonly')
    ansatz_combo["value"] = ["EfficientSU2", "ExcitationPreserving"]
    ansatz_combo.pack()
    apply_ansatz_button = tk.Button(
        button_frame, text="Apply", 
        command=lambda: canvas.apply_ansatz(ansatz_name.get(), len(graph_canvas.circles))
        )
    apply_ansatz_button.pack(pady=5)

    #--------------------------------------------------
    #-----------
      # Set focus to the canvas to capture key events

    graph_canvas.focus_set()

    # VQE frame---------------
 

    vqe_frame = VQEFrame(root, text="VQE", width=250, height=250)
    vqe_frame.grid(row=0, column=2, rowspan=2)

    vqe_button = tk.Button(master=vqe_frame, text="run")
    vqe_button.pack(side=tk.TOP)
    vqe_state_button = tk.Button(master=vqe_frame, text="State")
    vqe_state_button.pack(side=tk.TOP)

    vqe_params = None
    run_time = 10
    cost_history_dict = {
            "prev_vector": None,
            "iters": 0,
            "cost_history": [],
            "params":[]
        }
    def run_param_update():
        from qiskit_aer.primitives import EstimatorV2 as Estimator

        import time 
        
        from qiskit_symb.quantum_info import Statevector
        # SciPy minimizer routine
        from scipy.optimize import minimize
        global vqe_params, canvas, run_time, cost_history_dict
        
        estimator = Estimator()
        n_p = canvas.ansatz.num_parameters
        x0 = 2*np.pi * np.random.random(n_p)

        time.sleep(10/1000)

        def cost_func(params, ansatz, hamiltonian, estimator):
            global cost_history_dict
            time.sleep(10/1000)

            pub = (ansatz, [hamiltonian], [params])
            result = estimator.run(pubs=[pub]).result()
            energy = result[0].data.evs[0]

            cost_history_dict["iters"] += 1
            cost_history_dict["prev_vector"] = params
            cost_history_dict["cost_history"].append(energy)

            print(f"Iters. done: {cost_history_dict['iters']} [Current cost: {energy}]")
            return energy
        def callback_work(params):
            print("callback call")
            global cost_history_dict, root
            i = cost_history_dict["iters"]
            e = cost_history_dict["cost_history"][-1]
            vqe_frame.canvas.delete("all")
            vqe_frame.canvas.create_text(100, 100, 
                                    text=f"Iters:{i}/1500",
                                    font=('Helvetica', 15), 
                                    fill="black")
            vqe_frame.canvas.create_text(100, 125, 
                                    text=f"Energy:{e:.4}",
                                    font=('Helvetica', 15), 
                                    fill="black")
            canvas.update_color_by_params(params - 2*np.round(params/(2*np.pi)) *np.pi)
            
            root.update()
            root.update_idletasks()
        
        res = minimize(cost_func,
            x0,
            args =  (canvas.ansatz.decompose(), qiskit_hamiltonian, estimator),
            method="cobyqa", # Cobyla method,
            callback=callback_work,
            options={"maxiter":1000}
        )
        cost_history_dict["iters"] = 0

        vqe_frame.opt_param = res.x
        vqe_frame.ansatz = canvas.ansatz
        #vqe_frame.cal_st_vector()
    def state_cal():
        vqe_frame.cal_st_vector()
        state_vec = vqe_frame.state_vector

        vqe_frame.canvas.create_text(125, 175, 
                                    text=str(state_vec),
                                    font=('Helvetica', 20), 
                                    fill="black")
    vqe_button.config(command=run_param_update)
    vqe_state_button.config(command=state_cal)
    ## Ansatz color _update

    #----------
    # Function to properly close the application
    def on_closing():
        root.quit()  # Stop the main loop
        root.destroy()  # Destroy the window

    # Handle the window close event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the tkinter main loop
    root.mainloop()
