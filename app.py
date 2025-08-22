import streamlit as st
import pandas as pd
import io

def run():
    st.title("💳 Fraud Detection Agent")
    st.markdown(
        "Upload a **CSV file** of transactions and get instant fraud risk analysis. "
        "This tool is for **educational and demo purposes only**, not production banking use."
    )

    uploaded_file = st.file_uploader("📂 Upload Transactions CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Show uploaded data
        st.subheader("📊 Uploaded Transactions")
        st.dataframe(df.head())

        # Simple fraud rules
        df["Risk_Score"] = df["Amount"].apply(
            lambda x: "🚨 High" if x > 5000 else "✅ Low"
        )

        # Show analyzed data
        st.subheader("🔎 Analyzed Transactions")
        st.dataframe(df)

        # Summary stats
        high_risk = df[df["Risk_Score"] == "🚨 High"]
        st.warning(f"⚠️ {len(high_risk)} High-Risk Transactions Detected")

        # ✅ Download analyzed CSV
        st.subheader("⬇️ Download Results")
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            label="📥 Download Analyzed CSV",
            data=buffer,
            file_name="fraud_analysis_results.csv",
            mime="text/csv"
        )

        st.success("✅ Analysis Complete. Results ready for download.")
