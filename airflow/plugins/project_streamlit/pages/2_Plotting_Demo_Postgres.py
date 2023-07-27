import streamlit as st
import psycopg2
from psycopg2 import Error
import pandas as pd
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plotting Demo Postgres", page_icon="📈")
st.sidebar.header("📈 Plotting Demo Postgres")

# Database connection settings
DB_HOST = "<YOUR-IP-ADDRESS>"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "secret"
DB_PORT = 5433


# Function to establish a database connection
def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        st.success("Connected to the database!")
    except psycopg2.DatabaseError as e:
        st.error(f"Error connecting to the database: {e}")
    return conn


# Function to execute a SQL query and retrieve data
def execute_query(conn, query):
    data = None
    column_names = None
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()
        data = pd.DataFrame(data)
        data.columns = column_names
    except (Exception, Error) as e:
        st.error(f"Error executing the query: {e}")
    return data


# Streamlit app
def main():
    # Create a connection to the database
    conn = create_connection()

    # Streamlit layout
    st.title("Real-time Data from PostgreSQL")

    ######################################################

    query = """ 
            SELECT 
                t.transaction_date,
                t.transaction_amount,
                tp.transaction_type_description
            FROM transactions t
            LEFT JOIN "Transaction Type" tp
            ON t.transaction_type_id = tp.transaction_type_id
            """

    data = execute_query(conn, query)

    # Side Bar
    min_date, max_date = data["transaction_date"].min(), data["transaction_date"].max()

    start_date, end_date = st.sidebar.date_input(
        label="Date Range",
        min_value=min_date,
        max_value=max_date,
        value=[data["transaction_date"].min(), data["transaction_date"].max()],
    )

    data = data[
        (data["transaction_date"] >= start_date)
        & (data["transaction_date"] <= end_date)
    ]

    transaction_types = ["All"] + list(data["transaction_type_description"].unique())
    transaction_types_select = st.sidebar.selectbox(
        label="Transaction Type", options=transaction_types
    )

    if transaction_types_select != "All":
        data = data[data["transaction_type_description"] == transaction_types_select]

    # Line Chart
    st.subheader("Time Series Plot")

    data_line = data[["transaction_date", "transaction_amount"]]
    data_line = data_line.set_index("transaction_date")

    st.line_chart(data_line)

    # Bar Chart
    st.subheader("Transaction Type Plot")

    data_bar = data.groupby(["transaction_type_description"]).count()
    st.bar_chart(data=data_bar)

    # External Chart
    st.subheader("External Plot")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="lightgray")

    ax.plot(data["transaction_date"], data["transaction_amount"], color="goldenrod")

    ax.set_facecolor("lightcyan")
    ax.yaxis.grid(color="gray", linestyle="dashed")

    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("External Line Plot of Time Series")

    st.pyplot(fig)

    ######################################################

    # Input query
    query = st.text_input("Enter a SQL query:")

    # Execute the query and display results
    if st.button("Execute"):
        data = execute_query(conn, query)

        col1, col2 = st.columns(2)
        col1.dataframe(data)
        col2.table(data)
        st.success("Query executed successfully!")


def streaming_data(text_placeholder):
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )

    query = """SELECT sum(transaction_amount) FROM transactions"""

    temp_df = pd.read_sql_query(query, conn)

    text_placeholder.text(f"""Total Transaction Amount: {temp_df['sum'][0]}""")

    time.sleep(1)

def main_local():

    data = pd.read_csv('/mount/src/data_engineer_streamlit_airflow/airflow/plugins/project_streamlit/pages/data_postgres_local.csv')
    data['transaction_date'] = pd.to_datetime(data['transaction_date']).dt.date

    min_date, max_date = data["transaction_date"].min(), data["transaction_date"].max()

    start_date, end_date = st.sidebar.date_input(
        label="Date Range",
        min_value=min_date,
        max_value=max_date,
        value=[data["transaction_date"].min(), data["transaction_date"].max()],
    )

    data = data[
        (data["transaction_date"] >= start_date)
        & (data["transaction_date"] <= end_date)
    ]

    transaction_types = ["All"] + list(data["transaction_type_description"].unique())
    transaction_types_select = st.sidebar.selectbox(
        label="Transaction Type", options=transaction_types
    )

    if transaction_types_select != "All":
        data = data[data["transaction_type_description"] == transaction_types_select]

    # Line Chart
    st.subheader("Time Series Plot")

    data_line = data[["transaction_date", "transaction_amount"]]
    data_line = data_line.set_index("transaction_date")

    st.line_chart(data_line)

    # Bar Chart
    st.subheader("Transaction Type Plot")

    data_bar = data.groupby(["transaction_type_description"]).count()
    st.bar_chart(data=data_bar)

    # External Chart
    st.subheader("External Plot")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="lightgray")

    ax.plot(data["transaction_date"], data["transaction_amount"], color="goldenrod")

    ax.set_facecolor("lightcyan")
    ax.yaxis.grid(color="gray", linestyle="dashed")

    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("External Line Plot of Time Series")

    st.pyplot(fig)

# Run the app
if __name__ == "__main__":
    #importing the os module
    import os
    
    #to get the current working directory
    directory = os.getcwd()
    
    st.text(directory)
    # main()
    main_local()
    # text_placeholder = st.empty()

    # while True:
    #     streaming_data(text_placeholder)
