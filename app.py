import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt

# Custom styling
def add_styles():
    st.markdown("""
        <style>
        .reportview-container {
            background: linear-gradient(to bottom right, #e6f0ff, #ffffff);
        }
        .stButton>button {
            background-color: #0047AB;
            color: white;
            border-radius: 10px;
            padding: 0.5em 1em;
        }
        .stButton>button:hover {
            background-color: #0066FF;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def highlight_risk(val):
    """Color cells based on fraud risk."""
    color = "red" if "High" in val else "green"
    return f"color: {color}; font-weight: bold"

def run():
    add_styles()
    st.title("💳 Fraud Detection Agent")
    st.markdown(
        "An **AI-powered fraud detection demo** that analyzes transaction data, "
        "flags risky activities, and provides instant insights. <br>"
        "**Note**: This is for *educational and demonstration* purposes only.",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("📂 Upload Transactions CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Show uploaded data
        st.subheader("📊 Uploaded Transactions")
        st.dataframe(df.head())

        # Simple fraud rules
        df["Risk_Score"] = df["Amount"].apply(
            lambda x: "🚨 High Risk" if x > 5000 else "✅ Low Risk"
        )

        # Show analyzed data with color styling
        st.subheader("🔎 Analyzed Transactions")
        styled_df = df.style.applymap(highlight_risk, subset=["Risk_Score"])
        st.dataframe(styled_df)

        # Summary stats
        high_risk = df[df["Risk_Score"].str.contains("High")]
        st.warning(f"⚠️ {len(high_risk)} High-Risk Transactions Detected")
        st.info(f"✅ {len(df) - len(high_risk)} Safe Transactions Found")

        # 📊 Visualization - Pie Chart
        st.subheader("📊 Fraud Risk Distribution")
        risk_counts = df["Risk_Score"].value_counts()

        fig, ax = plt.subplots()
        ax.pie(
            risk_counts, 
            labels=risk_counts.index, 
            autopct='%1.1f%%',
            startangle=90,
            colors=["red", "green"]
        )
        ax.axis("equal")
        st.pyplot(fig)

        # 📊 Visualization - Bar Chart
        st.subheader("📊 Transaction Amounts by Risk Category")
        fig2, ax2 = plt.subplots()
        df.groupby("Risk_Score")["Amount"].sum().plot(kind="bar", ax2=ax2, color=["red", "green"])
        ax2.set_ylabel("Total Transaction Amount")
        ax2.set_xlabel("Risk Category")
        ax2.set_title("Total Transaction Value by Fraud Risk")
        st.pyplot(fig2)

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
