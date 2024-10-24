import io

import pandas as pd
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
    "theme": ["cross_joins", "cross_joins", "dense_rank", "groupBy"],
    "exercise_name": [
        "beverages_and_food",
        "sizes_and_trademarks",
        "wages_rank",
        "wages_group",
    ],
    "tables": [
        ["beverages", "food_items"],
        ["sizes", "trademarks"],
        ["wages"],
        ["wages"],
    ],
    "last_reviewed": ["1980-01-01", "1970-01-01", "1990-01-01", "1980-01-01"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df")

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE OR REPLACE TABLE beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE OR REPLACE TABLE food_items AS SELECT * FROM food_items")

SIZES = """
size
XS
M
L
XL
"""
sizes = pd.read_csv(io.StringIO(SIZES))
con.execute("CREATE OR REPLACE TABLE sizes AS SELECT * FROM sizes")

TRADEMARKS = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademarks = pd.read_csv(io.StringIO(TRADEMARKS))
con.execute("CREATE OR REPLACE TABLE trademarks AS SELECT * FROM trademarks")

WAGES = {
    "name": [
        "Toufik",
        "Jean-Nicolas",
        "Daniel",
        "Kaouter",
        "Sylvie",
        "Sebastien",
        "Diane",
        "Romain",
        "François",
        "Anna",
        "Zeinaba",
        "Gregory",
        "Karima",
        "Arthur",
        "Benjamin",
    ],
    "wage": [
        60000,
        75000,
        55000,
        100000,
        70000,
        90000,
        65000,
        100000,
        68000,
        85000,
        100000,
        120000,
        95000,
        83000,
        110000,
    ],
    "department": [
        "IT",
        "HR",
        "SALES",
        "IT",
        "IT",
        "HR",
        "SALES",
        "IT",
        "HR",
        "SALES",
        "IT",
        "IT",
        "HR",
        "SALES",
        "CEO",
    ],
    "sex": [
        "H",
        "H",
        "H",
        "F",
        "F",
        "H",
        "F",
        "H",
        "H",
        "F",
        "F",
        "H",
        "F",
        "H",
        "H",
    ],
}
wages = pd.DataFrame(WAGES)
con.execute("CREATE OR REPLACE TABLE wages AS SELECT * FROM wages")
