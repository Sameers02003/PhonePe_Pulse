import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json

# MySQL Connection
def get_data(query):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Dijas@19110',
        database='phonepe_insights'
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load Indian map GeoJSON file
with open("india_state.geojson", "r") as file:
    india_geojson = json.load(file)

# Load dataset
aggregated_transaction = pd.read_csv("aggregated_transaction.csv")

# Streamlit App Title
st.title("PhonePe Pulse Insights")

# **Sidebar Navigation**
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Home", "Business Case Study"])

# **Home Page - PhonePe Transaction Visualizations**
if page == "Home":
    st.subheader("📊 PhonePe Transaction Insights")
    option = st.sidebar.selectbox("Select Visualization", ["Transaction Overview", "Category Insights", "State-Wise Trends"])

    # Transaction Overview
    if option == "Transaction Overview":
        query = "SELECT year, quarter, SUM(transaction_amount) AS total_amount FROM aggregated_transaction GROUP BY year, quarter"
        df = get_data(query)

        st.subheader("Total Sum of Transaction Amount per Year and Quarter")
        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="year", y="total_amount", hue="quarter", data=df, ax=ax)
        plt.title("Yearly Transaction Amount (Quarterly Breakdown)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Category Insights
    elif option == "Category Insights":
        query = "SELECT transaction_type, SUM(transaction_amount) AS total_amount FROM aggregated_transaction GROUP BY transaction_type"
        df = get_data(query)

        st.subheader("Transaction Amount by Type")
        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="transaction_type", y="total_amount", data=df, ax=ax)
        plt.title("Transaction Amount by Type")
        plt.xticks(rotation=90)
        st.pyplot(fig)

    # **State-Wise Trends WITH Quarter Selection**
    elif option == "State-Wise Trends":
        selected_quarter = st.sidebar.selectbox("Choose a Quarter:", [1, 2, 3, 4])

        query = f"SELECT state, SUM(transaction_amount) AS total_amount FROM aggregated_transaction WHERE quarter={selected_quarter} GROUP BY state"
        df = get_data(query)

        st.subheader(f"State-Wise Transaction Amount for Quarter {selected_quarter}")
        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="state", y="total_amount", data=df, ax=ax)
        plt.title(f"State-Wise Transaction Amount for Quarter {selected_quarter}")
        plt.xticks(rotation=90)
        st.pyplot(fig)

# Generate Choropleth map for Indian states
        fig_map = px.choropleth(
            aggregated_transaction,
            geojson=india_geojson,
            locations="State",
            featureidkey="properties.NAME_1",
            color="Transaction_amount",
            color_continuous_scale="Reds",
            title=f"Transaction Amount Distribution Across Indian States (Quarter {selected_quarter})"
        )

        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map)

# **Business Case Study Section**
elif page == "Business Case Study":
    st.subheader("📌 Business Case Study Solutions")

    case_option = st.sidebar.selectbox("Select Case Study", ["Case Study 1", "Case Study 2", "Case Study 3", "Case Study 4", "Case Study 5"])

    case_queries = {
        "Case Study 1": """SELECT state, SUM(Transaction_count) AS Total_transaction, SUM(Transaction_amount) AS Total_amount 
                           FROM aggregated_transaction GROUP BY state ORDER BY Total_amount DESC;""",

        "Case Study 2": """SELECT state, SUM(User_count) AS TotalUsers, SUM(User_percentage) AS TotalValue 
                           FROM aggregated_user GROUP BY state ORDER BY TotalValue DESC;""",

        "Case Study 3": """SELECT state, SUM(Insurance_count) AS TotalPolicies, SUM(Insurance_amount) AS TotalValue 
                           FROM aggregated_insurance GROUP BY state ORDER BY TotalValue DESC;""",

        "Case Study 4": """SELECT state, SUM(Transaction_count) AS TotalTransactionValue 
                           FROM map_transaction GROUP BY state ORDER BY TotalTransactionValue DESC;""",

        "Case Study 5": """SELECT state, SUM(Users_registeredUsers) AS TotalUsers, SUM(Users_appOpens) AS TotalAppOpens 
                           FROM map_user GROUP BY state ORDER BY TotalAppOpens DESC;"""
                           
    }

    query_str = case_queries[case_option]
    df_case_study = get_data(query_str)

    st.subheader(f"📍 {case_option}")
    st.dataframe(df_case_study)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=df_case_study.columns[0], y=df_case_study.columns[-1], data=df_case_study, ax=ax)
    plt.title(f"{case_option} - State-wise Breakdown")
    plt.xticks(rotation=90)
    st.pyplot(fig)
