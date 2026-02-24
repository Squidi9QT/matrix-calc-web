import streamlit as st
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Pro Matrix Calc", page_icon="🔢")

st.title("🔢 Продвинутый матричный калькулятор")
st.write("Введите данные для матриц 3x3:")

# Функция для создания ввода матрицы
def input_matrix(label):
    st.subheader(label)
    cols = st.columns(3)
    matrix_data = []
    for i in range(3):
        row_data = []
        for j in range(3):
            # Создаем уникальный ключ для каждого поля ввода
            val = cols[j].number_input(f"{label} {i+1}:{j+1}", value=0.0, key=f"{label}_{i}_{j}")
            row_data.append(val)
        matrix_data.append(row_data)
    return np.array(matrix_data)

# Создаем две колонки для матриц А и Б, чтобы на ПК было красиво, а на телефоне в столбик
col_a, col_b = st.columns([1, 1])

with col_a:
    mat_a = input_matrix("Матрица A")

with col_b:
    mat_b = input_matrix("Матрица B")

st.divider()

# Выбор операций
st.subheader("Что нужно найти?")
operation = st.selectbox("Выберите действие:", [
    "Сложить (A + B)", 
    "Вычесть (A - B)",
    "Умножить (A × B)", 
    "Определитель матрицы A", 
    "Транспонировать A",
    "Обратная матрица A"
])

if st.button("Рассчитать результат", use_container_width=True, type="primary"):
    try:
        if operation == "Сложить (A + B)":
            res = mat_a + mat_b
            st.success("Результат сложения:")
            st.dataframe(res)

        elif operation == "Вычесть (A - B)":
            res = mat_a - mat_b
            st.success("Результат вычитания:")
            st.dataframe(res)

        elif operation == "Умножить (A × B)":
            res = np.dot(mat_a, mat_b)
            st.success("Результат умножения (строка на столбец):")
            st.dataframe(res)

        elif operation == "Определитель матрицы A":
            det = np.linalg.det(mat_a)
            st.info(f"Определитель (детерминант) матрицы A равен:")
            st.title(f"{det:.4f}")

        elif operation == "Транспонировать A":
            res = mat_a.T
            st.success("Транспонированная матрица A:")
            st.dataframe(res)

        elif operation == "Обратная матрица A":
            if np.linalg.det(mat_a) == 0:
                st.error("Ошибка: Определитель равен 0, обратной матрицы не существует!")
            else:
                res = np.linalg.inv(mat_a)
                st.success("Обратная матрица A:")
                st.dataframe(res)
                
    except Exception as e:
        st.error(f"Произошла ошибка при расчетах: {e}")

st.caption("Сделано на Python с помощью Streamlit и NumPy")
