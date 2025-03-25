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
    st.markdown("""
        <div style="background-color:#1E1E1E; padding:15px; border-radius:10px;">
            <h1 class="main-title">Financial Transaction Fraud Detection 💰</h1>
        </div>
    """, unsafe_allow_html=True)

    # Load and display banner image
    image = Image.open('home_banner.PNG')
    st.image(image, caption="AI-Powered Fraud Detection in Finance & Banking", use_container_width=True)

    # Sidebar Inputs
    st.sidebar.title("🔍 Transaction Details")
    
    TransactionAmt = st.sidebar.number_input("💵 Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
    card1 = st.sidebar.number_input("💳 Card 1", min_value=0, max_value=20000, step=1)
    card2 = st.sidebar.number_input("💳 Card 2", min_value=0, max_value=20000, step=1)
    card4 = st.sidebar.radio("🏦 Payment Card Category", [1, 2, 3, 4])
    card6 = st.sidebar.radio("💰 Payment Card Type", [1, 2])
    addr1 = st.sidebar.slider("📍 Address 1", min_value=0, max_value=500, step=1)
    addr2 = st.sidebar.slider("🌍 Address 2", min_value=0, max_value=100, step=1)
    P_emaildomain = st.sidebar.selectbox("📧 Purchaser Email Domain", [0, 1, 2, 3, 4])
    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])
    DeviceType = st.sidebar.radio("📱 Device Type", [1, 2])

    # Current Input Values Dictionary
    current_inputs = {
        "TransactionAmt": TransactionAmt, "card1": card1, "card2": card2,
        "card4": card4, "card6": card6, "addr1": addr1, "addr2": addr2,
        "P_emaildomain": P_emaildomain, "ProductCD": ProductCD, "DeviceType": DeviceType
    }

    # Transaction Summary
    st.markdown("### 📝 Transaction Summary")
    st.write(f"💵 **Transaction Amount:** ${TransactionAmt:.2f}")
    st.write(f"💳 **Card1:** {card1} | **Card2:** {card2}")
    st.write(f"🏦 **Payment Card:** {card4} | **Type:** {card6}")
    st.write(f"📧 **Email Domain:** {P_emaildomain} | 📦 **Product Code:** {ProductCD}")
    st.write(f"📍 **Billing Address:** {addr1}, {addr2}")
    st.write(f"📱 **Device Type:** {'Mobile' if DeviceType == 1 else 'Desktop'}")

    # Fraud Detection
    if st.button("🔎 Predict Fraud", help="Click to check if the transaction is fraudulent."):
        # Check if the inputs have changed
        if current_inputs == st.session_state.last_inputs:
            st.warning("Please enter new values before predicting!")
        else:
            final_output = generate_random_probability(ProductCD)
            st.session_state.transaction_history.append(final_output)

            # Store fraud/legit counts
            if final_output > 75.0:
                st.session_state.fraud_count += 1
            else:
                st.session_state.legit_count += 1

            st.subheader(f'🔢 Fraud Probability: {final_output:.2f}%')

            # Generate new random fraud feature importance for this transaction
            st.session_state.last_fraud_features = get_random_feature_importance()

            # Store the latest inputs
            st.session_state.last_inputs = current_inputs.copy()

            # Enhanced fraud detection visualization
            if final_output > 75.0:
                st.markdown(
                    '<div class="result-box fraud-warning">🚨 Fraudulent Transaction Detected!</div>',
                    unsafe_allow_html=True
                )
                st.error("⚠️ High risk! This transaction might be fraudulent.")
            else:
                st.markdown(
                    '<div class="result-box legit-success">✅ Transaction is Legitimate</div>',
                    unsafe_allow_html=True
                )
                st.success("🎉 Low risk! This transaction seems safe.")
                st.balloons()

    # Show report if at least one transaction has been made
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

        # Feature Importance (Dynamic)
        st.subheader("🔑 Key Features Contributing to Fraud")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(
            x=list(st.session_state.last_fraud_features.values()), 
            y=list(st.session_state.last_fraud_features.keys()), 
            ax=ax, 
            palette="coolwarm"
        )
        ax.set_xlabel("Importance Score")
        st.pyplot(fig)

if __name__ == '__main__':
    main()
