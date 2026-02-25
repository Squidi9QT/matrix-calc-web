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
    if op in ["A + B", "A - B", "A * B"]:
        with col_cfg_b:
            r_b = st.number_input("Строк B", 1, 6, 2)
            c_b = st.number_input("Столбцов B", 1, 6, 2)
        mat_b = input_matrix("Матрица B", r_b, c_b, "mb")
    
    if st.button("Вычислить"):
        st.session_state.log = f"--- ВЫПОЛНЕНИЕ: {op} ---\n"
        try:
            if op in ["A + B", "A - B"]:
                if mat_a.shape != mat_b.shape:
                    log_step("Ошибка: размеры не совпадают")
                else:
                    res = np.zeros_like(mat_a)
                    sign = "+" if op == "A + B" else "-"
                    for i in range(r_a):
                        for j in range(c_a):
                            val = mat_a[i,j] + mat_b[i,j] if op == "A + B" else mat_a[i,j] - mat_b[i,j]
                            res[i,j] = val
                            log_step(f"Элемент [{i+1},{j+1}]: {mat_a[i,j]} {sign} {mat_b[i,j]} = {val}")
                    log_step(log_matrix(res, "ИТОГ"))

            elif op == "A * B":
                if c_a != r_b:
                    log_step("Ошибка: число столбцов A != числу строк B")
                else:
                    res = np.zeros((r_a, c_b))
                    for i in range(r_a):
                        for j in range(c_b):
                            log_step(f"Вычисляем элемент [{i+1},{j+1}]:")
                            sum_val = 0
                            for k in range(c_a):
                                prod = mat_a[i,k] * mat_b[k,j]
                                sum_val += prod
                                log_step(f"  Умножаем {mat_a[i,k]} на {mat_b[k,j]} = {prod}. Текущая сумма: {sum_val}")
                            res[i,j] = sum_val
                            log_step(f"ИТОГО для [{i+1},{j+1}] = {sum_val}\n")
                    log_step(log_matrix(res, "ИТОГ УМНОЖЕНИЯ"))

            elif op == "Транспонирование A":
                log_step("Процесс переноса элементов:")
                for i in range(r_a):
                    for j in range(c_a):
                        log_step(f"Элемент с позиции ({i+1},{j+1}) переходит на ({j+1},{i+1})")
                log_step(log_matrix(mat_a.T, "ИТОГ"))

            elif op == "Определитель A":
                if r_a != c_a: log_step("Матрица не квадратная")
                else:
                    det = np.linalg.det(mat_a)
                    log_step(f"Значение определителя: {det:.2f}")

            elif op == "Ранг A":
                rank = np.linalg.matrix_rank(mat_a)
                log_step(f"Ранг (количество линейно независимых строк): {rank}")

        except Exception as e:
            log_step(f"Ошибка выполнения: {e}")

elif mode == "СЛАУ":
    n = st.sidebar.number_input("Неизвестных:", 2, 5, 3)
    method = st.selectbox("Метод решения:", ["Метод Гаусса", "Метод Крамера"])
    ma = input_matrix("Матрица коэффициентов A", n, n, "sl_a")
    mb = input_matrix("Вектор свободных членов B", n, 1, "sl_b")

    if st.button("Начать решение"):
        st.session_state.log = f"--- РЕШЕНИЕ СЛАУ ({method}) ---\n"
        try:
            if method == "Метод Крамера":
                d_main = np.linalg.det(ma)
                log_step(f"1. Главный определитель D = {d_main:.2f}")
                if abs(d_main) < 1e-9:
                    log_step("D = 0, метод Крамера не применим.")
                else:
                    for i in range(n):
                        temp = ma.copy()
                        temp[:, i] = mb.flatten()
                        d_i = np.linalg.det(temp)
                        log_step(f"2. Определитель D{i+1} = {d_i:.2f}. x{i+1} = {d_i/d_main:.2f}")
            
            elif method == "Метод Гаусса":
                comb = np.hstack((ma.copy(), mb.copy()))
                for i in range(n):
                    for k in range(i+1, n):
                        factor = -comb[k,i] / comb[i,i]
                        comb[k, i:] += factor * comb[i, i:]
                        log_step(f"Обнуление под элементом [{i+1},{i+1}] в строке {k+1}")
                sol = np.linalg.solve(ma, mb)
                log_step(f"Корни системы: {sol.flatten()}")

        except Exception as e:
            log_step(f"Ошибка: {e}")

elif mode == "Векторы":
    v_op = st.selectbox("Операция:", ["Сложение", "Скалярное произведение", "Векторное произведение"])
    dim = 3 if v_op == "Векторное произведение" else st.sidebar.selectbox("Размерность:", [2, 3])
    va = input_matrix("Вектор V_A", 1, dim, "va").flatten()
    vb = input_matrix("Вектор V_B", 1, dim, "vb").flatten()

    if st.button("Посчитать"):
        st.session_state.log = "--- РАЗБОР ВЕКТОРОВ ---\n"
        if v_op == "Сложение":
            res = va + vb
            log_step(f"Результат сложения: {res}")
        elif v_op == "Скалярное произведение":
            res = np.dot(va, vb)
            log_step(f"Результат скалярного произведения: {res}")

st.divider()
st.subheader("Терминал (Пошаговое решение)")
st.text_area("Лог выполнения:", value=st.session_state.log, height=400)
if st.button("Очистить"):
    st.session_state.log = ""
    st.rerun()
