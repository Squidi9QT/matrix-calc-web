import streamlit as st
import numpy as np

st.set_page_config(page_title="Universal Matrix Calc", page_icon="🔢")

st.title("🔢 Универсальный калькулятор")

# 1. Выбор размерности
size = st.slider("Выберите размер матрицы (N x N):", min_value=2, max_value=10, value=3)

def input_matrix(label, n):
    st.subheader(label)
    matrix_data = []
    # Создаем сетку нужного размера
    for i in range(n):
        cols = st.columns(n)
        row_data = []
        for j in range(n):
            val = cols[j].number_input(f"{i+1}:{j+1}", value=0.0, key=f"{label}_{i}_{j}", label_visibility="collapsed")
            row_data.append(val)
        matrix_data.append(row_data)
    return np.array(matrix_data)

col_a, col_b = st.columns(2)

with col_a:
    mat_a = input_matrix("Матрица A", size)

with col_b:
    mat_b = input_matrix("Матрица B", size)

# 2. Математика остаётся прежней (NumPy сам поймет размер)
operation = st.selectbox("Операция:", [
    "A + B", "A - B", "A × B", "Определитель A", "Транспонировать A"
])

if st.button("Рассчитать", use_container_width=True, type="primary"):
    try:
        if operation == "A + B":
            st.success("Результат:")
            st.write(mat_a + mat_b)
        elif operation == "A × B":
            st.success("Результат:")
            st.write(np.dot(mat_a, mat_b))
        elif operation == "Определитель A":
            det = np.linalg.det(mat_a)
            st.metric("Определитель", f"{det:.2f}")
        # ... и так далее
    except Exception as e:
        st.error(f"Ошибка: {e}")
