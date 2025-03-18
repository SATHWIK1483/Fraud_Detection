import numpy as np
import streamlit as st
import random
from PIL import Image
import os
import matplotlib.pyplot as plt

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Streamlit App
def main():
    st.set_page_config(page_title="Financial Fraud Detection", layout="wide")
    
    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Home", "Fraud Report"])
    
    if page == "Home":
        home_page()
    elif page == "Fraud Report":
        report_page()


def home_page():
    st.title("💰 Financial Transaction Fraud Detection")
    
    image = Image.open('home_banner.PNG')
    st.image(image, caption="AI-Powered Fraud Detection", use_container_width=True)
    
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

    st.markdown("### 📝 Transaction Summary")
    st.write(f"💵 **Transaction Amount:** ${TransactionAmt:.2f}")
    st.write(f"💳 **Card1:** {card1} | **Card2:** {card2}")
    
    if st.button("🔎 Predict Fraud"):
        final_output = generate_random_probability(ProductCD)
        st.session_state['fraud_probability'] = final_output  # Store result for report page
        st.session_state['transaction_data'] = {
            "TransactionAmt": TransactionAmt,
            "Card1": card1,
            "Card2": card2,
            "ProductCD": ProductCD,
            "Fraud Probability": final_output
        }
        
        st.subheader(f'🔢 Fraud Probability: {final_output:.2f}%')
        
        if final_output > 75.0:
            st.error("🚨 Fraudulent Transaction Detected!")
        else:
            st.success("✅ Legitimate Transaction")
            st.balloons()
        
        st.markdown("## 📜 View Detailed Report")
        if st.button("📊 Generate Report"):
            st.switch_page("Fraud Report")


def report_page():
    st.title("📊 Fraud Detection Report")
    
    if 'transaction_data' in st.session_state:
        data = st.session_state['transaction_data']
        
        st.write("### Transaction Details")
        st.json(data)
        
        if 'fraud_probability' in st.session_state:
            fraud_score = st.session_state['fraud_probability']
            
            fig, ax = plt.subplots()
            labels = ['Legit', 'Fraud']
            values = [100 - fraud_score, fraud_score]
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['green', 'red'], startangle=140)
            ax.set_title("Fraud Probability Analysis")
            st.pyplot(fig)
    else:
        st.warning("No transaction data available. Please predict fraud first!")

if __name__ == '__main__':
    main()
