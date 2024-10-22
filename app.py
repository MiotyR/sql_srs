import streamlit as st
import pandas as pd
import duckdb

st.write("""
SQL SRS
Spaced Repetition System SQL Practice
""")

with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme ..."
    )

    st.write("You selected:", option)


data = {"a": [0, 1, 2], "b": [3, 4, 5]}
df = pd.DataFrame(data)

query = st.text_area(label="Input your SQL query")
if query:
    st.dataframe(duckdb.sql(query).df())
