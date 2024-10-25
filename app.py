# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st
from datetime import date, timedelta

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Checks that user sql query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct !")
            st.balloons()
        else:
            st.write("Unexpected values in result dataframe")
            st.dataframe(result.compare(solution_df))
    except KeyError:
        st.write("Some columns are missing")
        n_lines_difference = result.shape[0] - solution_df.shape[0]
        if n_lines_difference != 0:
            st.write(
                f"Result has a {n_lines_difference} lines different from the solution"
            )


# theme selection
with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )
    if theme:
        st.write("You selected:", theme)
        selected_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
        exercise = (
            con.execute(selected_exercise_query).df().sort_values(by="last_reviewed")
        )
        st.write(exercise)
        exercise_name = exercise.iloc[0]["exercise_name"]
        with open(f"answers/{exercise_name}.sql", "r") as f:
            answer = f.read()

        solution_df = con.execute(answer).df()

# st header config
st.header("SQL SRS")
query = st.text_area(label="Your SQL code here", key="user_input")

# compare query result with expected result
if query:
    check_users_solution(query)

# srs mechanism
st_columns = st.columns([1, 1, 1, 1])
for col, n_days in zip(st_columns[:3], [2, 7, 21]):
    with col:
        if st.button(f"Revisit in {n_days} days"):
            next_review = date.today() + timedelta(days=n_days)
            con.execute(
                f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
            )
            st.rerun()

with st_columns[-1]:
    if st.button("Reset"):
        con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
        st.rerun()

# show tables and solution only if a theme was selected
if theme:
    tab2, tab3 = st.tabs(["Tables", "Solution"])

    with tab2:
        exercise_tables = exercise.iloc[0]["tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table)

    with tab3:
        st.markdown(answer.replace("\n", "<br />"), unsafe_allow_html=True)
