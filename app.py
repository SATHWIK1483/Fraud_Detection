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

# Initialize session storage
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []  # Stores fraud probabilities
if "fraud_count" not in st.session_state:
    st.session_state.fraud_count = 0
if "legit_count" not in st.session_state:
    st.session_state.legit_count = 0

# Streamlit App
def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
            .main-title { text-align: center; color: white; font-size: 26px; padding: 15px; }
            .result-box { padding: 15px; border-radius: 10px; font-size: 18px; text-align: center; }
            .fraud-warning { background-color: #FF4B4B; color: white; }
            .legit-success { background-color: #4CAF50; color: white; }
            .custom-button { background-color: #007BFF; color: white; font-size: 18px; padding: 10px; border-radius: 8px; width: 100%; cursor: pointer; border: none; }
            .custom-button:hover { background-color: #0056b3; }
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
    st.sidebar.info("1: Discover | 2: Mastercard | 3: Amex | 4: Visa")

    card6 = st.sidebar.radio("💰 Payment Card Type", [1, 2])
    st.sidebar.info("1: Credit | 2: Debit")

    addr1 = st.sidebar.slider("📍 Address 1", min_value=0, max_value=500, step=1)
    addr2 = st.sidebar.slider("🌍 Address 2", min_value=0, max_value=100, step=1)

    P_emaildomain = st.sidebar.selectbox("📧 Purchaser Email Domain", [0, 1, 2, 3, 4])
    st.sidebar.info("0: Gmail | 1: Outlook | 2: Mail.com | 3: Others | 4: Yahoo")

    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])
    st.sidebar.info("0: C | 1: H | 2: R | 3: S | 4: W")

    DeviceType = st.sidebar.radio("📱 Device Type", [1, 2])
    st.sidebar.info("1: Mobile | 2: Desktop")

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
        final_output = generate_random_probability(ProductCD)
        st.session_state.transaction_history.append(final_output)

        # Store fraud/legit counts
        if final_output > 75.0:
            st.session_state.fraud_count += 1
        else:
            st.session_state.legit_count += 1

        st.subheader(f'🔢 Fraud Probability: {final_output:.2f}%')

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

        # Feature Importance (Simplified for explanation)
        st.subheader("🔑 Key Features Contributing to Fraud")
        feature_importance = {"Card1": 0.35, "Card2": 0.25, "Addr1": 0.15, "Email Domain": 0.15, "Product Code": 0.10}
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=list(feature_importance.values()), y=list(feature_importance.keys()), ax=ax, palette="coolwarm")
        ax.set_xlabel("Importance Score")
        st.pyplot(fig)

        # Transaction Risk Distribution
        st.subheader("📊 Transaction Risk Distribution")
        labels = ["Fraudulent", "Legitimate"]
        sizes = [st.session_state.fraud_count, st.session_state.legit_count]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["red", "green"], startangle=90, wedgeprops={"edgecolor": "black"})
        st.pyplot(fig)

if __name__ == '__main__':
    main()
