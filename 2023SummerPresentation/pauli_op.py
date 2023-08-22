


def Pauli2String(pauli, num_wires=None): 
    # Convert the given Pennylane PauliBasis to Pauli string
    types = "".join(pauli.name).replace("Pauli", "").replace("Identity", "I")
    
    acting_wires = list(pauli.wires)
    if num_wires is None:
        num_wires = pauli.num_wires
        
    pstring = num_wires*["I"]
    for i, p in enumerate(acting_wires):
        pstring[p] = types[i]
    return "".join(pstring)

def PauliDecompose(pauli_string): # Decompose product string into x, z family string 
    # 0: Z family
    # 1: X family
    # 2: product string
    st_type = 2
    st1 = "" # z
    st2 = "" # x
    pro_st = ""
    if "Y" not in pauli_string:
        if "X" in pauli_string and "Z" in pauli_string:
            pro_st = pauli_string
        elif "X" in pauli_string:
            st_type = 1
            st2 = pauli_string
        else:
            st_type = 0
            st1 = pauli_string
    else:
        pro_st = pauli_string
    
    # Decompose pro_st
    if st_type ==2:
        z_st = []
        x_st = []
        for s in pro_st:
            if s =="Y":
                x_st.append("X")
                z_st.append("Z")
            elif s =="X":
                x_st.append("X")
                z_st.append("I")
            elif s =="Z":
                x_st.append("I")
                z_st.append("Z")
            elif s =="I":
                x_st.append("I")
                z_st.append("I")
        st1 = "".join(z_st)
        st2 = "".join(x_st)
    return (st_type, st1, st2)
            