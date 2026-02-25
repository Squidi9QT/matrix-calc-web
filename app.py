import streamlit as st
import numpy as np

st.set_page_config(page_title="Step-by-Step Math Calc", layout="wide")

st.title("Калькулятор Курбана")

if 'log' not in st.session_state:
    st.session_state.log = ""

def log_step(text):
    st.session_state.log += str(text) + "\n"

def log_matrix(matrix, name=""):
    res = f"Матрица {name}:\n"
    for row in matrix:
        res += "  [" + "  ".join([f"{x:7.2f}" for x in row]) + "]\n"
    return res

def input_matrix(label, rows, cols, key_suffix):
    st.write(f"**{label}**")
    matrix_data = []
    for i in range(rows):
   
        grid_cols = st.columns([1] * cols + [10 - cols]) 
        row_data = []
        for j in range(cols):
            val = grid_cols[j].number_input(
                f"{label}{i}{j}", value=0.0, step=1.0, 
                key=f"{key_suffix}_{i}_{j}", label_visibility="collapsed"
            )
            row_data.append(val)
        matrix_data.append(row_data)
    return np.array(matrix_data)

st.sidebar.header("Меню")
mode = st.sidebar.selectbox("Режим:", ["Матрицы", "СЛАУ", "Векторы"])

if mode == "Матрицы":
    op = st.selectbox("Операция:", ["A + B", "A - B", "A * число", "A * B", "Транспонирование A", "Определитель A", "Ранг A"])
    
    col_cfg_a, col_cfg_b = st.columns(2)
    with col_cfg_a:
        r_a = st.number_input("Строк A", 1, 6, 2)
        c_a = st.number_input("Столбцов A", 1, 6, 2)
    
    mat_a = input_matrix("Матрица A", r_a, c_a, "ma")
    
    mat_b = None
    scalar = 1.0
    
  
    if op in ["A + B", "A - B", "A * B"]:
        with col_cfg_b:
            r_b = st.number_input("Строк B", 1, 6, 2)
            c_b = st.number_input("Столбцов B", 1, 6, 2)
        mat_b = input_matrix("Матрица B", r_b, c_b, "mb")
    
    elif op == "A * число":
        scalar = st.number_input("Введите число для умножения:", value=1.0, step=1.0)

    if st.button("Вычислить"):
        st.session_state.log = f"--- ВЫПОЛНЕНИЕ: {op} ---\n"
        try:
            if op in ["A + B", "A - B"]:
                if mat_a.shape != mat_b.shape:
                    log_step("Ошибка: размеры не совпадают")
                else:
                    res = mat_a + mat_b if op == "A + B" else mat_a - mat_b
                    sign = "+" if op == "A + B" else "-"
                    for i in range(r_a):
                        for j in range(c_a):
                            log_step(f"Элемент [{i
