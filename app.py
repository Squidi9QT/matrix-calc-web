import streamlit as st
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Math Calc Kurban", layout="wide")

st.title("Калькулятор Курбана")

# Инициализация лога
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
        # Создаем компактные колонки
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

# Боковое меню
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
        scalar = st.number_input("Введите число k:", value=1.0, step=1.0)

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
                            log_step(f"[{i+1},{j+1}]: {mat_a[i,j]} {sign} {mat_b[i,j]} = {res[i,j]}")
                    log_step(log_matrix(res, "ИТОГ"))

            elif op == "A * число":
                res = mat_a * scalar
                for i in range(r_a):
                    for j in range(c_a):
                        log_step(f"[{i+1},{j+1}]: {mat_a[i,j]} * {scalar} = {res[i,j]}")
                log_step(log_matrix(res, "ИТОГ"))

            elif op == "A * B":
                if c_a != mat_b.shape[0]:
                    log_step("Ошибка: столбцы A не равны строкам B")
                else:
                    res = np.dot(mat_a, mat_b)
                    log_step(log_matrix(res, "РЕЗУЛЬТАТ"))

            elif op == "Определитель A":
                if r_a != c_a: log_step("Ошибка: не квадратная")
                else:
                    det = np.linalg.det(mat_a)
                    log_step(f"Определитель = {det:.2f}")

            elif op == "Транспонирование A":
                log_step(log_matrix(mat_a.T, "A^T"))

            elif op == "Ранг A":
                rank = np.linalg.matrix_rank(mat_a)
                log_step(f"Ранг = {rank}")

        except Exception as e:
            log_step(f"Ошибка: {e}")

elif mode == "СЛАУ":
    n = st.sidebar.number_input("Неизвестных:", 2, 5, 3)
    method = st.selectbox("Метод:", ["Метод Гаусса", "Метод Крамера"])
    ma = input_matrix("Матрица A", n, n, "sla")
    mb = input_matrix("Вектор B", n, 1, "slb")

    if st.button("Решить"):
        st.session_state.log = f"--- РЕШЕНИЕ СЛАУ ({method}) ---\n"
        try:
            if method == "Метод Крамера":
                d = np.linalg.det(ma)
                log_step(f"Главный D = {d:.2f}")
                if abs(d) > 1e-9:
                    for i in range(n):
                        t = ma.copy()
                        t[:, i] = mb.flatten()
                        di = np.linalg.det(t)
                        log_step(f"D{i+1} = {di:.2f}, x{i+1} = {di/d:.2f}")
            else:
                sol = np.linalg.solve(ma, mb)
                log_step(f"Ответ: {sol.flatten()}")
        except Exception as e:
            log_step(f"Ошибка: {e}")

elif mode == "Векторы":
    v_op = st.selectbox("Операция:", ["Сложение", "Скалярное", "Векторное"])
    dim = 3 if v_op == "Векторное" else st.sidebar.selectbox("Dim:", [2, 3])
    va = input_matrix("V1", 1, dim, "va").flatten()
    vb = input_matrix("V2", 1, dim, "vb").flatten()
    if st.button("Рассчитать"):
        if v_op == "Сложение": log_step(f"Итог: {va + vb}")
        elif v_op == "Скалярное": log_step(f"Итог: {np.dot(va, vb)}")
        elif v_op == "Векторное": log_step(f"Итог: {np.cross(va, vb)}")

# Терминал
st.divider()
st.subheader("Терминал")
st.text_area("Ход решения:", value=st.session_state.log, height=300)
if st.button("Очистить"):
    st.session_state.log = ""
    st.rerun()
