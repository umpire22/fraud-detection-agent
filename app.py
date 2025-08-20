import streamlit as st
import pandas as pd

# --- Title ---
st.title("🔍 Simple Fraud Detection Agent")

st.write("Upload a CSV file with transactions, and the agent will flag suspicious ones.")

# --- Upload file ---
uploaded_file = st.file_uploader("Upload your transactions CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Transactions")
    st.dataframe(df.head())

    # --- Simple Fraud Rules ---
    st.subheader("🔎 Fraud Detection Results")

    def detect_fraud(transaction):
        reasons = []
        if transaction["Amount"] > 10000:  # Example rule
            reasons.append("High transaction amount")
        if transaction["Country"] not in ["Nigeria", "USA", "UK"]:
            reasons.append("Unusual country")
        if transaction["Time"].startswith("2"):  # Example fake rule
            reasons.append("Odd transaction time")
        return ", ".join(reasons) if reasons else "Legit"

    df["Fraud_Check"] = df.apply(detect_fraud, axis=1)
    st.dataframe(df)

    # --- Export results ---
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Results", data=csv, file_name="fraud_results.csv")
