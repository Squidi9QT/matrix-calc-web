import streamlit as st
import numpy as np

# Настройка интерфейса
st.set_page_config(page_title="Pro Math Calculator", layout="wide")

st.title("Универсальный математический калькулятор с пошаговым выводом")

# Инициализация хранилища лога (терминала)
if 'log' not in st.session_state:
    st.session_state.log = ""

def log_step(text):
    """Добавляет строку в терминал решения"""
    st.session_state.log += str(text) + "\n"

def log_matrix(matrix, name=""):
    """Красиво форматирует матрицу для текстового вывода"""
    res = f"Матрица {name}:\n"
    for row in matrix:
        res += "  [" + "  ".join([f"{x:7.2f}" for x in row]) + "]\n"
    return res

def input_matrix(label, rows, cols, key_suffix):
    """Создает сетку ввода для матрицы"""
    matrix_data = []
    for i in range(rows):
        grid_cols = st.columns(cols)
        row_data = []
        for j in range(cols):
            val = grid_cols[j].number_input(
                f"{label}{i}{j}", value=0.0, step=1.0, 
                key=f"{key_suffix}_{i}_{j}", label_visibility="collapsed"
            )
            row_data.append(val)
        matrix_data.append(row_data)
    return np.array(matrix_data)

# --- БОКОВАЯ ПАНЕЛЬ ---
st.sidebar.header("Настройки")
mode = st.sidebar.selectbox("Режим работы:", ["Матрицы", "СЛАУ", "Векторы"])

# --- РЕЖИМ МАТРИЦ ---
if mode == "Матрицы":
    op = st.selectbox("Операция:", ["A + B", "A - B", "A * число", "A * B", "Транспонирование A", "Определитель A", "Ранг A"])
    
    r_a = st.sidebar.number_input("Строк A", 1, 6, 2)
    c_a = st.sidebar.number_input("Столбцов A", 1, 6, 2)
    mat_a = input_matrix("A", r_a, c_a, "ma")
    
    mat_b = None
    scalar = 2.0
    if op in ["A + B", "A - B", "A * B"]:
        r_b = st.sidebar.number_input("Строк B", 1, 6, 2)
        c_b = st.sidebar.number_input("Столбцов B", 1, 6, 2)
        mat_b = input_matrix("B", r_b, c_b, "mb")
    elif op == "A * число":
        scalar = st.number_input("Введите множитель:", value=2.0)

    if st.button("Выполнить вычисление"):
        st.session_state.log = f"--- НАЧАЛО ОПЕРАЦИИ: {op} ---\n"
        try:
            if op in ["A + B", "A - B"]:
                if mat_a.shape != mat_b.shape:
                    log_step("Ошибка: Матрицы должны быть одинакового размера!")
                else:
                    res = np.zeros_like(mat_a)
                    sign = "+" if op == "A + B" else "-"
                    for i in range(r_a):
                        for j in range(c_a):
                            res[i,j] = mat_a[i,j] + mat_b[i,j] if op == "A + B" else mat_a[i,j] - mat_b[i,j]
                            log_step(f"Ячейка [{i+1}][{j+1}]: {mat_a[i,j]} {sign} {mat_b[i,j]} = {res[i,j]}")
                    log_step(log_matrix(res, "Результат"))

            elif op == "A * B":
                if c_a != r_b:
                    log_step(f"Ошибка: Столбцы A ({c_a}) != Строки B ({r_b})")
                else:
                    res = np.zeros((r_a, c_b))
                    for i in range(r_a):
                        for j in range(c_b):
                            parts = []
                            total = 0
                            for k in range(c_a):
                                p = mat_a[i,k] * mat_b[k,j]
                                total += p
                                parts.append(f"({mat_a[i,k]}*{mat_b[k,j]})")
                            res[i,j] = total
                            log_step(f"Элемент [{i+1}][{j+1}]: {' + '.join(parts)} = {total}")
                    log_step(log_matrix(res, "Произведение"))

            elif op == "Транспонирование A":
                log_step("Процесс: замена строк на столбцы (A[i][j] -> A[j][i])")
                log_step(log_matrix(mat_a.T, "A^T"))

            elif op == "Определитель A":
                if r_a != c_a:
                    log_step("Ошибка: Только для квадратных матриц!")
                else:
                    det = np.linalg.det(mat_a)
                    log_step("Алгоритм: Использование LU-разложения для вычисления детерминанта.")
                    log_step(f"ИТОГ: Определитель = {det:.4f}")

            elif op == "Ранг A":
                rank = np.linalg.matrix_rank(mat_a)
                u, s, vh = np.linalg.svd(mat_a)
                log_step(f"Сингулярные числа матрицы: {s}")
                log_step(f"Метод: Ранг равен количеству ненулевых сингулярных чисел.")
                log_step(f"ИТОГ: Ранг матрицы = {rank}")

        except Exception as e:
            log_step(f"Сбой выполнения: {e}")

# --- РЕЖИМ СЛАУ ---
elif mode == "СЛАУ":
    n = st.sidebar.number_input("Количество переменных:", 2, 5, 3)
    method = st.selectbox("Выберите метод решения:", ["Метод Гаусса", "Метод Крамера", "Матричный метод"])
    
    st.write("Введите систему Ax = B")
    col1, col2 = st.columns([3, 1])
    with col1: ma = input_matrix("A", n, n, "sa")
    with col2: mb = input_matrix("B", n, 1, "sb")

    if st.button("Найти решение"):
        st.session_state.log = f"--- РЕШЕНИЕ СЛАУ: {method} ---\n"
        try:
            if method == "Метод Крамера":
                det_main = np.linalg.det(ma)
                log_step(f"1. Находим главный определитель D: {det_main:.2f}")
                if abs(det_main) < 1e-9:
                    log_step("Результат: Система не имеет единственного решения (D=0)")
                else:
                    xs = []
                    for i in range(n):
                        temp = ma.copy()
                        temp[:, i] = mb.flatten()
                        det_i = np.linalg.det(temp)
                        log_step(f"2. Заменяем столбец {i+1} на вектор B. Получаем D_{i+1} = {det_i:.2f}")
                        xs.append(det_i / det_main)
                    log_step(f"3. Вычисляем x_i = D_i / D\nИТОГ: {xs}")

            elif method == "Метод Гаусса":
                combined = np.hstack((ma.copy(), mb.copy()))
                log_step("1. Формируем расширенную матрицу [A|B]:")
                log_step(log_matrix(combined))
                for i in range(n):
                    for k in range(i+1, n):
                        factor = -combined[k,i] / combined[i,i]
                        combined[k, i:] += factor * combined[i, i:]
                        log_step(f"Обнуляем элемент [{k+1}][{i+1}] (множитель {factor:.2f})")
                log_step("2. Матрица после прямого хода:")
                log_step(log_matrix(combined))
                res_x = np.linalg.solve(ma, mb)
                log_step(f"3. Выполнен обратный ход. ИТОГ: {res_x.flatten()}")

        except Exception as e:
            log_step(f"Математическая невозможность: {e}")

# --- РЕЖИМ ВЕКТОРОВ ---
elif mode == "Векторы":
    v_op = st.selectbox("Операция:", ["Сложение", "Скалярное произведение", "Векторное произведение", "Смешанное произведение"])
    dim = 3 if v_op in ["Векторное произведение", "Смешанное произведение"] else st.sidebar.selectbox("Размерность:", [2, 3])
    
    va = input_matrix("V_A", 1, dim, "va").flatten()
    vb = input_matrix("V_B", 1, dim, "vb").flatten()
    vc = np.zeros(3)
    if v_op == "Смешанное произведение":
        st.write("Третий вектор для смешанного произведения:")
        vc = input_matrix("V_C", 1, 3, "vc").flatten()

    if st.button("Вычислить вектор"):
        st.session_state.log = f"--- ВЕКТОРНАЯ ОПЕРАЦИЯ: {v_op} ---\n"
        if v_op == "Сложение":
            log_step(f"Результат (сложение координат): {va + vb}")
        elif v_op == "Скалярное произведение":
            res = np.dot(va, vb)
            log_step(f"Сумма произведений (x1*x2 + y1*y2...): {res}")
        elif v_op == "Векторное произведение":
            res = np.cross(va, vb)
            log_step(f"Результат (вектор, перпендикулярный двум данным): {res}")
        elif v_op == "Смешанное произведение":
            res = np.dot(np.cross(va, vb), vc)
            log_step(f"Результат (объем параллелепипеда): {res}")

# --- ТЕРМИНАЛ (ВЫВОД ХОДА РЕШЕНИЯ) ---
st.divider()
st.subheader("Ход решения (Терминал)")
st.text_area("Промежуточные шаги и результат:", value=st.session_state.log, height=450)

if st.button("Очистить терминал"):
    st.session_state.log = ""
    st.rerun()
