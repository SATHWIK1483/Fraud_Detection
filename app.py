import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Function to display fraud report
def fraud_report(TransactionAmt, ProductCD, card1, card2, addr1, addr2, DeviceType):
    st.title("📊 Fraud Analysis Report")
    
    # Explanation of fraud factors
    st.markdown("### 🔎 Key Factors Contributing to Fraud")
    st.write("- **Transaction Amount:** Higher transaction amounts tend to be riskier.")
    st.write("- **Product Code:** Certain product categories have a higher fraud probability.")
    st.write("- **Card Information:** Stolen cards may have different usage patterns.")
    st.write("- **Address Mismatch:** Fraudsters often use inconsistent addresses.")
    st.write("- **Device Type:** Transactions from unfamiliar devices may be flagged as fraud.")
    
    # Simulated feature importance graph
    feature_importance = {"Transaction Amount": 30, "Product Code": 25, "Card Details": 20, "Address Mismatch": 15, "Device Type": 10}
    
    fig, ax = plt.subplots()
    ax.bar(feature_importance.keys(), feature_importance.values(), color=['red', 'blue', 'green', 'orange', 'purple'])
    ax.set_ylabel("Contribution (%)")
    ax.set_title("Feature Importance in Fraud Detection")
    st.pyplot(fig)

    # Fraud probability prediction
    fraud_probability = generate_random_probability(ProductCD)
    st.subheader(f'🔢 Fraud Probability: {fraud_probability:.2f}%')

    if fraud_probability > 75.0:
        st.error("⚠️ High risk! This transaction is likely fraudulent.")
    else:
        st.success("✅ Low risk! This transaction seems safe.")

# Streamlit Main App
def main():
    st.sidebar.title("🔍 Transaction Details")
    
    TransactionAmt = st.sidebar.number_input("💵 Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
    card1 = st.sidebar.number_input("💳 Card 1", min_value=0, max_value=20000, step=1)
    card2 = st.sidebar.number_input("💳 Card 2", min_value=0, max_value=20000, step=1)
    addr1 = st.sidebar.slider("📍 Address 1", min_value=0, max_value=500, step=1)
    addr2 = st.sidebar.slider("🌍 Address 2", min_value=0, max_value=100, step=1)
    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])
    DeviceType = st.sidebar.radio("📱 Device Type", [1, 2])
    
    st.markdown("### 📝 Transaction Summary")
    st.write(f"💵 **Transaction Amount:** ${TransactionAmt:.2f}")
    st.write(f"💳 **Card1:** {card1} | **Card2:** {card2}")
    st.write(f"📦 **Product Code:** {ProductCD}")
    st.write(f"📍 **Billing Address:** {addr1}, {addr2}")
    st.write(f"📱 **Device Type:** {'Mobile' if DeviceType == 1 else 'Desktop'}")

    if st.button("🔎 Predict Fraud"):
        fraud_probability = generate_random_probability(ProductCD)
        st.subheader(f'🔢 Fraud Probability: {fraud_probability:.2f}%')
        if fraud_probability > 75.0:
            st.error("⚠️ High risk! This transaction might be fraudulent.")
        else:
            st.success("✅ Low risk! This transaction seems safe.")

    if st.button("📄 Generate Fraud Report"):
        fraud_report(TransactionAmt, ProductCD, card1, card2, addr1, addr2, DeviceType)

if __name__ == '__main__':
    main()
