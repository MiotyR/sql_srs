# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st


if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "groupBy", "dense_rank"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    if theme:
        exercise = (
            con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
            .df()
            .sort_values(by="last_reviewed")
        )
        st.write(exercise)

        exercise_name = exercise.iloc[0]["exercise_name"]
        with open(f"answers/{exercise_name}.sql", "r") as f:
            answer = f.read()

        solution_df = con.execute(answer).df()

st.header("Enter your code:")
query = st.text_area(label="Your SQL code here", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )

    tab2, tab3 = st.tabs(["Tables", "Solution"])

    with tab2:
        exercise_tables = exercise.iloc[0]["tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table)

    with tab3:
        st.write(answer)
