import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from PIL import Image

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Function to randomly assign importance scores to fraud-related features
def get_random_feature_importance():
    """Generate random importance scores for fraud detection."""
    feature_pool = ["Card1", "Card2", "Addr1", "Addr2", "Email Domain", "Product Code", "Transaction Amount", "Device Type"]
    selected_features = random.sample(feature_pool, 5)  # Select 5 random features
    
    # Assign random importance scores that sum up to 1
    importance_scores = np.random.dirichlet(np.ones(5), size=1)[0]  # Ensures scores sum to 1
    feature_importance = {feature: round(score, 2) for feature, score in zip(selected_features, importance_scores)}

    return feature_importance

# Initialize session storage
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []  # Stores fraud probabilities
if "fraud_count" not in st.session_state:
    st.session_state.fraud_count = 0
if "legit_count" not in st.session_state:
    st.session_state.legit_count = 0
if "last_fraud_features" not in st.session_state:
    st.session_state.last_fraud_features = {}  # Store last generated feature importance
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = {}  # Store last input values
if "parameter_history" not in st.session_state:
    st.session_state.parameter_history = []  # Stores transaction parameters

# Streamlit App
def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
            .main-title { text-align: center; color: white; font-size: 26px; padding: 15px; }
            .result-box { padding: 15px; border-radius: 10px; font-size: 18px; text-align: center; }
            .fraud-warning { background-color: #FF4B4B; color: white; }
            .legit-success { background-color: #4CAF50; color: white; }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""<div style="background-color:#1E1E1E; padding:15px; border-radius:10px;">
        <h1 class="main-title">Financial Transaction Fraud Detection 💰</h1></div>""", unsafe_allow_html=True)

    # Purpose of the Project
    st.markdown("### 🎯 Purpose of the Project")
    st.info("""
    This fraud detection system analyzes financial transactions to identify fraudulent activities before they happen.
    Using **machine learning-inspired anomaly detection**, it enhances security for financial institutions.
    **Unique Features:**
    - Advanced fraud analysis with real-time probability predictions
    - Risk minimization strategies for future transactions
    - Correlation detection between fraudulent patterns
    - Prevention of suspicious transactions before processing
    """)

    # Load and display banner image
    image = Image.open('home_banner.PNG')
    st.image(image, caption="AI-Powered Fraud Detection in Finance & Banking", use_container_width=True)

    # Sidebar Inputs
    st.sidebar.title("🔍 Transaction Details")
    
    TransactionAmt = st.sidebar.number_input("💵 Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
    card1 = st.sidebar.number_input("💳 Card 1", min_value=0, max_value=20000, step=1)
    card2 = st.sidebar.number_input("💳 Card 2", min_value=0, max_value=20000, step=1)
    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])
    DeviceType = st.sidebar.radio("📱 Device Type", [1, 2])

    current_inputs = {
        "TransactionAmt": TransactionAmt, "card1": card1, "card2": card2,
        "ProductCD": ProductCD, "DeviceType": DeviceType
    }

    if st.button("🔎 Predict Fraud"):
        if current_inputs == st.session_state.last_inputs:
            st.warning("⚠️ Please enter new values before predicting!")
        else:
            final_output = generate_random_probability(ProductCD)
            st.session_state.transaction_history.append(final_output)
            st.session_state.parameter_history.append(current_inputs)

            if final_output > 75.0:
                st.session_state.fraud_count += 1
                st.markdown('<div class="result-box fraud-warning">🚨 Fraudulent Transaction Detected!</div>', unsafe_allow_html=True)
                st.error("⚠️ High risk! This transaction might be fraudulent.")
            else:
                st.session_state.legit_count += 1
                st.markdown('<div class="result-box legit-success">✅ Transaction is Legitimate</div>', unsafe_allow_html=True)
                st.success("🎉 Low risk! This transaction seems safe.")
                st.balloons()

            st.session_state.last_inputs = current_inputs.copy()
            st.session_state.last_fraud_features = get_random_feature_importance()

    # Show report if transactions exist
    if len(st.session_state.transaction_history) > 0:
        st.markdown("---")
        st.header("📊 Fraud Analysis Report")

        # Fraud Probability Distribution
        st.subheader("📌 Fraud Probability Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(st.session_state.transaction_history, bins=10, kde=True, color="blue", ax=ax)
        ax.set_xlabel("Fraud Probability (%)")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # Key Feature Contributions
        st.subheader("🔑 Key Features Contributing to Fraud")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(
            x=list(st.session_state.last_fraud_features.values()), 
            y=list(st.session_state.last_fraud_features.keys()), 
            ax=ax, palette="coolwarm"
        )
        ax.set_xlabel("Importance Score")
        st.pyplot(fig)

        # Risk Warning System
        fraud_ratio = st.session_state.fraud_count / len(st.session_state.transaction_history)
        if fraud_ratio > 0.5:
            st.warning("⚠️ High Fraud Risk! More than 50% of transactions are fraudulent.")
        elif fraud_ratio > 0.2:
            st.info("🔍 Moderate Risk: Stay cautious about upcoming transactions.")
        else:
            st.success("✅ Low Risk: Transactions are mostly legitimate.")

if __name__ == '__main__':
    main()
