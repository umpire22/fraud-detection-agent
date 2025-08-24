import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import os

# 🎨 Page setup
st.set_page_config(page_title="Fraud Detection Agent", page_icon="🛡️", layout="wide")

# 🌟 App title
st.markdown("<h1 style='color:#4CAF50;text-align:center;'>🛡️ Fraud Detection Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>AI-powered demo for detecting unusual transactions</p>", unsafe_allow_html=True)

# ✅ Always show this
st.success("✅ The app loaded successfully!")

# 📂 Input options
st.sidebar.header("Input Transactions Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
pasted_data = st.sidebar.text_area("Or paste CSV data here", height=200)

# Function to read data from file or pasted text
def load_data(file, text):
    if file is not None:
        return pd.read_csv(file)
    elif text.strip() != "":
        return pd.read_csv(StringIO(text))
    else:
        return None

df = load_data(uploaded_file, pasted_data)

# 📊 If data exists
if df is not None:
    try:
        st.subheader("📋 Preview of Data")
        st.dataframe(df.head())

        # --- Simple Fraud Rule: Flag transactions over threshold
        threshold = 2000
        df["Flagged"] = df["Amount"] > threshold

        # Show flagged transactions
        st.subheader("🚨 Flagged Transactions")
        flagged = df[df["Flagged"] == True]

        if not flagged.empty:
            st.error("⚠️ Suspicious transactions found!")
            st.dataframe(flagged)

            # 📋 Copy suspicious transactions
            flagged_text = flagged.to_csv(index=False)
            st.text_area("📋 Copy Suspicious Transactions (CSV format)", flagged_text, height=200)

            # ⬇️ Download suspicious transactions
            st.download_button(
                label="⬇️ Download Flagged Transactions",
                data=flagged_text,
                file_name="flagged_transactions.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ No suspicious transactions detected.")

        # 📈 Plot transaction amounts
        st.subheader("📊 Transaction Amounts")
        fig, ax = plt.subplots()
        ax.plot(df["Amount"], marker="o", linestyle="-", color="blue", label="Transactions")
        ax.axhline(y=threshold, color="red", linestyle="--", label="Fraud Threshold")
        ax.set_title("Transactions vs Threshold")
        ax.set_xlabel("Transaction #")
        ax.set_ylabel("Amount")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error while processing data: {e}")

else:
    st.info("📂 Please upload a CSV file or paste CSV data in the sidebar to begin analysis.")

# ℹ️ Footer note
st.markdown("<br><hr><p style='text-align:center;color:gray;'>This demo is for educational purposes only. Not for real-world banking use.</p>", unsafe_allow_html=True)
