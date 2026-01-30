import streamlit as st
import pandas as pd
import os
import plotly.express as px
from chatbot.financial_chatbot import chatbot

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Financial Analysis & Chatbot",
    layout="wide"
)

# ================= LOAD DATA =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_financials.csv")

df = pd.read_csv(DATA_PATH)
df = df.sort_values(["Company", "Year"])

# ================= DERIVED METRICS =================
df["Profit_Margin"] = (df["NetIncome"] / df["Revenue"]) * 100
df["Debt_Ratio"] = (df["Liabilities"] / df["Assets"]) * 100

# ================= SIDEBAR NAV =================
page = st.sidebar.radio(
    "Navigation",
    ["Home", "About"]
)

company = st.sidebar.selectbox(
    "Select Company",
    sorted(df["Company"].unique())
)

# ================= HOME PAGE =================
if page == "Home":

    st.title("Financial Analysis & Chatbot")

    # -------- KPIs --------
    latest = df[df["Company"] == company].iloc[-1]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue", f"${latest['Revenue']:,.0f} M")
    col2.metric("Net Income", f"${latest['NetIncome']:,.0f} M")
    col3.metric("Profit Margin", f"{latest['Profit_Margin']:.2f}%")
    col4.metric("Debt Ratio", f"{latest['Debt_Ratio']:.2f}%")

    st.divider()

    # -------- Revenue Trend --------
    st.subheader(f"Revenue Trend – {company}")

    revenue_df = (
        df[df["Company"] == company]
        .groupby("Year", as_index=False)["Revenue"]
        .mean()
    )

    st.plotly_chart(
        px.line(
            revenue_df,
            x="Year",
            y="Revenue",
            markers=True,
            title="Revenue Over Time (Yearly Average)"
        ),
        use_container_width=True
    )

    # -------- Profit Trend --------
    st.subheader(f"Net Income Trend – {company}")

    profit_df = (
        df[df["Company"] == company]
        .groupby("Year", as_index=False)["NetIncome"]
        .mean()
    )

    st.plotly_chart(
        px.line(
            profit_df,
            x="Year",
            y="NetIncome",
            markers=True,
            title="Net Income Over Time (Yearly Average)"
        ),
        use_container_width=True
    )

    st.divider()

    # -------- Profit Margin --------
    st.subheader("Average Profit Margin by Company")

    margin_df = (
        df.groupby("Company")["Profit_Margin"]
        .mean()
        .reset_index()
        .sort_values("Profit_Margin", ascending=False)
    )

    st.plotly_chart(
        px.bar(
            margin_df,
            x="Company",
            y="Profit_Margin",
            text_auto=".2f",
            title="Average Profit Margin (%)"
        ),
        use_container_width=True
    )

    # -------- Debt Ratio --------
    st.subheader("Average Debt Ratio by Company")

    debt_df = (
        df.groupby("Company")["Debt_Ratio"]
        .mean()
        .reset_index()
        .sort_values("Debt_Ratio")
    )

    st.plotly_chart(
        px.bar(
            debt_df,
            x="Company",
            y="Debt_Ratio",
            text_auto=".2f",
            title="Average Debt Ratio (%)"
        ),
        use_container_width=True
    )

    st.divider()

    # ================= CHATBOT =================
    st.subheader("🤖 AI Financial Chatbot")
    st.caption("Select a predefined question or type your own")

    question_templates = [
        "",
        "revenue apple",
        "net income microsoft",
        "profit margin google",
        "debt ratio amazon",
        "revenue growth apple",
        "profit growth microsoft",
        "compare companies",
        "compare revenue",
        "compare profit margin",
        "compare apple vs microsoft",
        "top 3 companies",
        "best company to invest",
        "should i invest in apple"
    ]

    selected_question = st.selectbox(
        "Choose a question",
        question_templates
    )

    user_query = st.text_input(
        "Or type your own financial question",
        value=selected_question
    )

    if st.button("Ask"):
        if user_query.strip():
            st.success(chatbot(user_query))
        else:
            st.warning("Please select or type a question.")

# ================= ABOUT PAGE =================
elif page == "About":

    st.title(" About This Application")

    st.markdown("""
    ##  Financial Analysis & Chatbot

    This application is an **end-to-end financial analytics dashboard**
    built using **Python, Pandas, Streamlit, and Plotly**.

    ###  Purpose
    - Analyze structured financial data
    - Visualize trends and performance
    - Compare companies across metrics
    - Answer finance-related questions using an AI-style chatbot

    ###  Visualizations
    - Line graphs for revenue & profit trends
    - Bar charts for profit margin & debt comparison

    ###  Chatbot Capabilities
    - Revenue & profit analysis
    - Growth & risk evaluation
    - Company comparison & ranking
    - Investment-style insights

   
    """)
