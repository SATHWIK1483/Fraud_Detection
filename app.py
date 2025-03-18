import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from PIL import Image

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Load sample dataset (Replace with actual data source)
data = pd.DataFrame({
    'TransactionAmt': np.random.uniform(1, 5000, 1000),
    'FraudProbability': np.random.uniform(40, 100, 1000),
    'PaymentMethod': np.random.choice(['Visa', 'Mastercard', 'Amex', 'Discover'], 1000),
    'Fraudulent': np.random.choice([0, 1], 1000, p=[0.7, 0.3])
})

def generate_report():
    st.title("📊 Fraud Analysis Report")
    
    st.markdown("### 🔍 Feature Importance in Fraud Detection")
    feature_importance = pd.Series({
        'TransactionAmt': 0.35, 'Card Type': 0.25, 'Billing Address': 0.15, 'Product Code': 0.10,
        'Email Domain': 0.08, 'Device Type': 0.07
    }).sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    feature_importance.plot(kind='barh', color='crimson', ax=ax)
    ax.set_title("Feature Importance in Fraud Prediction")
    ax.set_xlabel("Importance Score")
    st.pyplot(fig)
    
    st.markdown("### 📊 Fraud vs. Legitimate Transactions")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data['FraudProbability'], bins=30, kde=True, ax=ax, color='purple')
    ax.set_title("Fraud Probability Distribution")
    st.pyplot(fig)
    
    st.markdown("### 💵 Transaction Amount vs. Fraud Probability")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=data['TransactionAmt'], y=data['FraudProbability'], hue=data['Fraudulent'], palette=['blue', 'red'], ax=ax)
    ax.set_title("Transaction Amount vs. Fraud Probability")
    ax.set_xlabel("Transaction Amount ($)")
    ax.set_ylabel("Fraud Probability (%)")
    st.pyplot(fig)
    
    st.markdown("### 🏦 Payment Method Fraud Analysis")
    fraud_rates = data.groupby('PaymentMethod')['Fraudulent'].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    fraud_rates.plot(kind='bar', color=['green', 'blue', 'orange', 'red'], ax=ax)
    ax.set_title("Fraud Rate by Payment Method")
    ax.set_ylabel("Fraud Percentage")
    st.pyplot(fig)

def main():
    st.markdown("""
        <style>
            .main-title { text-align: center; color: white; font-size: 28px; padding: 15px; font-weight: bold; }
            .custom-sidebar { background-color: #1E1E1E; padding: 20px; border-radius: 10px; }
            .button-style { background-color: #FF4B4B; color: white; font-size: 18px; padding: 12px; border-radius: 8px; width: 100%; cursor: pointer; border: none; text-align: center; }
            .button-style:hover { background-color: #D63E3E; }
        </style>
    
        <div style="background-color:#2E2E2E; padding:15px; border-radius:10px; text-align:center;">
            <h1 class="main-title">Financial Transaction Fraud Detection 💰</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
        <div class="custom-sidebar">
            <h2 style="color:white;">🔍 Transaction Details</h2>
        </div>
    """, unsafe_allow_html=True)
    
    TransactionAmt = st.sidebar.number_input("💵 Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])
    
    if st.sidebar.button("🔎 Predict Fraud", key="predict_button"):
        fraud_probability = generate_random_probability(ProductCD)
        st.subheader(f'🔢 Fraud Probability: {fraud_probability:.2f}%')
        
        if fraud_probability > 75.0:
            st.error("🚨 High Fraud Risk Detected!")
        else:
            st.success("✅ Transaction is Legitimate")
    
    if st.sidebar.button("📄 Generate Fraud Report", key="report_button"):
        generate_report()

if __name__ == '__main__':
    main()
