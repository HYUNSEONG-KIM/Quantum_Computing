def get_state_strings(n):
    total_n = 2**n
    
    st = []
    for i in range(0, total_n):
        str_num = format(i, 'b')
        st.append((n-len(str_num))*"0" + str_num)
    return st