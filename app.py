import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from PIL import Image

# Load sample dataset (Replace with actual data source)
data = pd.DataFrame({
    'FraudProbability': np.random.uniform(40, 100, 1000),
    'FeatureImportance': np.random.choice(['TransactionAmt', 'Card Type', 'Billing Address', 'Product Code', 'Email Domain', 'Device Type'], 1000)
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
    
    st.markdown("### 📊 Fraud Contribution by Features")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(y=data['FeatureImportance'], order=data['FeatureImportance'].value_counts().index, palette='coolwarm', ax=ax)
    ax.set_title("Fraud Contribution by Feature")
    st.pyplot(fig)
    
    st.markdown("### 📈 Fraud Probability Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data['FraudProbability'], bins=30, kde=True, ax=ax, color='purple')
    ax.set_title("Fraud Probability Distribution")
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
    
    if st.sidebar.button("📄 Generate Fraud Report", key="report_button"):
        generate_report()

if __name__ == '__main__':
    main()
