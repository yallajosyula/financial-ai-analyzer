import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

from dotenv import load_dotenv


# ===============================
# LOAD API KEY
# ===============================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("API Key not found! Check .env file")
    st.stop()

genai.configure(api_key=API_KEY)


# ===============================
# INITIALIZE MODEL (LATEST)
# ===============================

MODEL_NAME = "models/gemini-1.0-pro"

model = genai.GenerativeModel(MODEL_NAME)


# ===============================
# FILE LOADER
# ===============================

def load_file(file):

    if file is None:
        return None

    try:

        if file.name.endswith(".csv"):
            return pd.read_csv(file)

        elif file.name.endswith(".xlsx"):
            return pd.read_excel(file)

        else:
            return None

    except:
        return None


# ===============================
# AI SUMMARY GENERATOR
# ===============================

def generate_summary(data, doc_type):

    if data is None:
        return "No data found."

    data_dict = data.to_dict()

    prompt = f"""
You are a professional financial analyst.

Document Type: {doc_type}

Analyze the following data:

{data_dict}

Provide:
- Key Metrics
- Trends
- Risks
- Financial Health
- Recommendations

Give a clear summary.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI Error: {e}"


# ===============================
# VISUALIZATION
# ===============================

def visualize(title, data):

    st.subheader(title)

    if data is not None:

        st.dataframe(data, use_container_width=True)

        numeric = data.select_dtypes(include="number")

        if not numeric.empty:
            st.line_chart(numeric)
        else:
            st.info("No numeric data available")

    else:
        st.warning("No data uploaded")


# ===============================
# STREAMLIT UI
# ===============================

st.set_page_config(
    page_title="AI Financial Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Financial Document Analyzer")

st.markdown("""
Upload your financial files and get **AI-powered insights**.
""")


# ===============================
# FILE UPLOAD
# ===============================

st.header("📂 Upload Files")

col1, col2, col3 = st.columns(3)

with col1:
    balance_file = st.file_uploader(
        "Balance Sheet",
        ["csv", "xlsx"]
    )

with col2:
    profit_file = st.file_uploader(
        "Profit & Loss",
        ["csv", "xlsx"]
    )

with col3:
    cash_file = st.file_uploader(
        "Cash Flow",
        ["csv", "xlsx"]
    )


# ===============================
# GENERATE BUTTON
# ===============================

st.markdown("---")

if st.button("🚀 Generate Report", use_container_width=True):

    with st.spinner("Analyzing financial data..."):

        # Load Data
        balance_data = load_file(balance_file)
        profit_data = load_file(profit_file)
        cash_data = load_file(cash_file)

        # Generate AI Summaries
        balance_summary = generate_summary(
            balance_data, "Balance Sheet"
        )

        profit_summary = generate_summary(
            profit_data, "Profit and Loss"
        )

        cash_summary = generate_summary(
            cash_data, "Cash Flow"
        )


        # ===============================
        # DISPLAY RESULTS
        # ===============================

        st.success("Analysis Completed ✅")

        st.header("📝 AI Summaries")

        tab1, tab2, tab3 = st.tabs([
            "Balance Sheet",
            "Profit & Loss",
            "Cash Flow"
        ])

        with tab1:
            st.write(balance_summary)

        with tab2:
            st.write(profit_summary)

        with tab3:
            st.write(cash_summary)


        st.header("📈 Visualizations")

        visualize("Balance Sheet Data", balance_data)

        visualize("Profit & Loss Data", profit_data)

        visualize("Cash Flow Data", cash_data)


# ===============================
# FOOTER
# ===============================

st.markdown("---")

st.markdown("""
<center>
Developed by Appu using Streamlit & Gemini AI ❤️
</center>
""", unsafe_allow_html=True)
