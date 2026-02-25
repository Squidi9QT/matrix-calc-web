import streamlit as st
import numpy as np

st.set_page_config(page_title="Matrix and Vector Calculator", layout="wide")

st.title("Универсальный математический калькулятор")

# Функция для вывода в "терминал"
def log_step(text):
    if 'log' not in st.session_state:
        st.session_state.log = ""
    st.session_state.log += text + "\n"

# Инициализация лога
if 'log' not in st.session_state:
    st.session_state.log = ""

# --- БЛОК 1: ВЫБОР РЕЖИМА ---
mode = st.sidebar.selectbox("Выберите режим работы:", 
    ["Матричные операции", "Решение СЛАУ", "Векторные операции"])

# Функция создания ввода матрицы
def input_matrix(label, rows, cols, key_suffix):
    matrix_data = []
    for i in range(rows):
        grid_cols = st.columns(cols)
        row_data = []
        for j in range(cols):
            val = grid_cols[j].number_input(f"{label}{i}{j}", value=0.0, step=1.0, 
                                          key=f"{key_suffix}_{i}_{j}", label_visibility="collapsed")
            row_data.append(val)
        matrix_data.append(row_data)
    return np.array(matrix_data)

# --- ЛОГИКА РЕЖИМОВ ---

if mode == "Матричные операции":
    op = st.selectbox("Операция:", ["A + B", "A - B", "A * число", "A * B", "Транспонирование A", "Определитель A", "Ранг A"])
    
    r_a = st.sidebar.number_input("Строк A", 1, 10, 2)
    c_a = st.sidebar.number_input("Столбцов A", 1, 10, 2)
    
    mat_a = input_matrix("A", r_a, c_a, "mat_a")
    
    mat_b = None
    scalar = 1.0
    
    if op in ["A + B", "A - B", "A * B"]:
        r_b = st.sidebar.number_input("Строк B", 1, 10, 2)
        c_b = st.sidebar.number_input("Столбцов B", 1, 10, 2)
        mat_b = input_matrix("B", r_b, c_b, "mat_b")
    elif op == "A * число":
        scalar = st.number_input("Введите число:", value=1.0)

    if st.button("Выполнить"):
        st.session_state.log = "--- Начало операции ---\n"
        try:
            if op == "A + B":
                if mat_a.shape != mat_b.shape:
                    log_step("Ошибка: размеры матриц не совпадают.")
                else:
                    res = mat_a + mat_b
                    log_step(f"Сложение матриц размера {mat_a.shape}")
                    log_step(f"Результат:\n{res}")
            
            elif op == "A * B":
                if mat_a.shape[1] != mat_b.shape[0]:
                    log_step(f"Ошибка: число столбцов A ({mat_a.shape[1]}) не равно числу строк B ({mat_b.shape[0]})")
                else:
                    res = np.dot(mat_a, mat_b)
                    log_step("Выполнение матричного умножения (строка на столбец)")
                    log_step(f"Результат:\n{res}")

            elif op == "Определитель A":
                if mat_a.shape[0] != mat_a.shape[1]:
                    log_step("Ошибка: матрица должна быть квадратной")
                else:
                    det = np.linalg.det(mat_a)
                    log_step(f"Нахождение определителя для матрицы {mat_a.shape}")
                    log_step(f"Значение: {det}")

            elif op == "Ранг A":
                rank = np.linalg.matrix_rank(mat_a)
                log_step(f"Используется метод SVD для вычисления ранга")
                log_step(f"Ранг матрицы: {rank}")

            elif op == "Транспонирование A":
                res = mat_a.T
                log_step("Строки и столбцы поменялись местами")
                log_step(f"Результат:\n{res}")

        except Exception as e:
            log_step(f"Сбой выполнения: {str(e)}")

elif mode == "Решение СЛАУ":
    n = st.sidebar.number_input("Количество неизвестных", 2, 10, 3)
    method = st.selectbox("Метод решения:", ["Матричный метод", "Метод Крамера", "Метод Гаусса"])
    
    st.write("Введите коэффициенты (матрица A) и свободные члены (вектор B):")
    col_left, col_right = st.columns([3, 1])
    with col_left:
        mat_a = input_matrix("A", n, n, "slau_a")
    with col_right:
        mat_b = input_matrix("B", n, 1, "slau_b")

    if st.button("Решить СЛАУ"):
        st.session_state.log = f"--- Решение СЛАУ методом: {method} ---\n"
        try:
            det_a = np.linalg.det(mat_a)
            log_step(f"Шаг 1: Определитель основной матрицы = {det_a:.2f}")
            
            if method == "Матричный метод":
                if det_a == 0:
                    log_step("Система не имеет однозначного решения (det=0)")
                else:
                    inv_a = np.linalg.inv(mat_a)
                    log_step("Шаг 2: Найдена обратная матрица A^-1")
                    res = np.dot(inv_a, mat_b)
                    log_step(f"Шаг 3: X = A^-1 * B\nРезультат:\n{res}")

            elif method == "Метод Гаусса":
                res = np.linalg.solve(mat_a, mat_b)
                log_step("Выполнено приведение к ступенчатому виду и обратный ход")
                log_step(f"Результат:\n{res}")

        except Exception as e:
            log_step(f"Ошибка при вычислении: {str(e)}")

elif mode == "Векторные операции":
    v_op = st.selectbox("Операция над векторами:", ["Сложение", "Скалярное произведение", "Векторное произведение"])
    dim = st.sidebar.selectbox("Размерность:", [2, 3])
    
    vec_a = input_matrix("V_A", 1, dim, "v_a")
    vec_b = input_matrix("V_B", 1, dim, "v_b")

    if st.button("Вычислить"):
        st.session_state.log = "--- Операции над векторами ---\n"
        v1 = vec_a.flatten()
        v2 = vec_b.flatten()
        
        if v_op == "Скалярное произведение":
            res = np.dot(v1, v2)
            log_step(f"Формула: x1*x2 + y1*y2 + ...\nРезультат: {res}")
        elif v_op == "Векторное произведение":
            if dim != 3:
                log_step("Ошибка: Векторное произведение определено только для 3D")
            else:
                res = np.cross(v1, v2)
                log_step(f"Результат (новый вектор): {res}")

# --- ТЕРМИНАЛ ВЫВОДА ---
st.divider()
st.subheader("Терминал (Ход решения)")
st.text_area(label="Вывод команд:", value=st.session_state.log, height=300)

if st.button("Очистить терминал"):
    st.session_state.log = ""
    st.rerun()
