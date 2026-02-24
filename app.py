import streamlit as st
import numpy as np

st.set_page_config(page_title="Kurban Calc", layout="wide")

st.title("Калькулятор Курбана")


def create_matrix_input(label, rows, cols):
    st.write(f"### {label} ({rows}x{cols})")
    matrix_data = []
    for i in range(rows):
        grid_cols = st.columns(cols)
        row_data = []
        for j in range(cols):
            val = grid_cols[j].number_input(
                f"{label}{i}{j}", 
                value=0.0, step=1.0, key=f"{label}_{i}_{j}", label_visibility="collapsed")
            row_data.append(val)
        matrix_data.append(row_data)
    return np.array(matrix_data)


col_cfg1, col_cfg2 = st.columns(2)

with col_cfg1:
    st.info("Размеры Матрицы A")
    rows_a = st.number_input("Строк A", 1, 10, 2)
    cols_a = st.number_input("Столбцов A", 1, 10, 3)

with col_cfg2:
    st.info("Размеры Матрицы B")
    rows_b = st.number_input("Строк B", 1, 10, 3)
    cols_b = st.number_input("Столбцов B", 1, 10, 2)

st.divider()


c1, c2 = st.columns(2)
with c1:
    mat_a = create_matrix_input("A", rows_a, cols_a)
with c2:
    mat_b = create_matrix_input("B", rows_b, cols_b)

st.divider()


operation = st.selectbox("Что сделать?", ["A + B", "A - B", "A × B", "Определитель A", "Транспонировать A"])

if st.button("Посчитать", use_container_width=True, type="primary"):
    try:
        if operation in ["A + B", "A - B"]:
           
            if mat_a.shape != mat_b.shape:
                st.error(f"Ошибка! Для {operation} матрицы должны быть одинакового размера. У вас {mat_a.shape} и {mat_b.shape}.")
            else:
                res = (mat_a + mat_b) if operation == "A + B" else (mat_a - mat_b)
                st.success("Результат:")
                st.write(res)

        elif operation == "A × B":
       
            if cols_a != rows_b:
                st.error(f"Ошибка умножения! Число столбцов A ({cols_a}) должно быть равно числу строк B ({rows_b}).")
            else:
                res = np.dot(mat_a, mat_b)
                st.success("Результат умножения:")
                st.write(res)

        elif operation == "Определитель A":
      
            if rows_a != cols_a:
                st.error("Ошибка! Определитель можно найти только для квадратной матрицы (например, 2x2 или 3x3).")
            else:
                det = np.linalg.det(mat_a)
                st.metric("Определитель A", f"{det:.2f}")

        elif operation == "Транспонировать A":
            st.write("Результат (строки стали столбцами):")
            st.write(mat_a.T)

    except Exception as e:
        st.error(f"Что-то пошло не так (Курбану не звонить): {e}")
