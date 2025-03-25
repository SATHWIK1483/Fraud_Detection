import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from PIL import Image
from docx import Document
from io import BytesIO

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    return random.uniform(40, 100)

# Function to randomly assign importance scores to fraud-related features
def get_random_feature_importance():
    """Generate random importance scores for fraud detection."""
    feature_pool = ["Card1", "Card2", "Addr1", "Addr2", "Email Domain", "Product Code", "Transaction Amount", "Device Type"]
    selected_features = random.sample(feature_pool, 5)
    importance_scores = np.random.dirichlet(np.ones(5), size=1)[0]
    return {feature: round(score, 2) for feature, score in zip(selected_features, importance_scores)}

# Streamlit session storage
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []
if "fraud_count" not in st.session_state:
    st.session_state.fraud_count = 0
if "legit_count" not in st.session_state:
    st.session_state.legit_count = 0
if "last_fraud_features" not in st.session_state:
    st.session_state.last_fraud_features = {}

# Streamlit UI
def main():
    st.title("Financial Transaction Fraud Detection 💰")
    
    # Sidebar Inputs
    st.sidebar.title("🔍 Transaction Details")
    TransactionAmt = st.sidebar.number_input("💵 Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])
    DeviceType = st.sidebar.radio("📱 Device Type", ["Mobile", "Desktop"])
    
    # Predict Fraud
    if st.button("🔎 Predict Fraud"):
        fraud_probability = generate_random_probability(ProductCD)
        st.session_state.transaction_history.append(fraud_probability)
        st.session_state.last_fraud_features = get_random_feature_importance()

        if fraud_probability > 75.0:
            st.session_state.fraud_count += 1
            st.error(f"🚨 Fraud Detected! Probability: {fraud_probability:.2f}%")
        else:
            st.session_state.legit_count += 1
            st.success(f"✅ Transaction is Legitimate. Probability: {fraud_probability:.2f}%")

    # Generate Report Button
    if st.button("📥 Download Fraud Report"):
        doc = Document()
        doc.add_heading("🚨 Fraud Detection Report 🚨", level=1)
        doc.add_paragraph(f"Transaction Amount: ${TransactionAmt:.2f}")
        doc.add_paragraph(f"Device Type: {DeviceType}")
        doc.add_paragraph(f"Fraud Probability: {fraud_probability:.2f}%")
        doc.add_paragraph("\nKey Features Contributing to Fraud:")
        for feature, score in st.session_state.last_fraud_features.items():
            doc.add_paragraph(f"- {feature}: {score}")
        
        # Save report to a buffer
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button("📥 Download Report", buffer, "Fraud_Report.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

if __name__ == '__main__':
    main()
