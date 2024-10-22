import streamlit as st
import pandas as pd
import duckdb

data = {"a": [0, 1, 2], "b": [3, 4, 5]}
df = pd.DataFrame(data)

query = st.text_area(label="Input your SQL query")
if query:
    st.dataframe(duckdb.sql(query).df())
