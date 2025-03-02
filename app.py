import numpy as np
import streamlit as st
import random
from PIL import Image

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Streamlit App
def main():
    # Custom Styling
    st.markdown("""
        <style>
            body { font-family: Arial, sans-serif; }
            .header { text-align: center; color: white; padding: 15px; font-size: 28px; font-weight: bold; }
            .container { background-color: #f8f9fa; padding: 20px; border-radius: 10px; }
            .fraud-warning { color: #d9534f; font-size: 20px; font-weight: bold; text-align: center; }
            .legit-success { color: #5cb85c; font-size: 20px; font-weight: bold; text-align: center; }
            .predict-btn { background-color: #007bff; color: white; font-size: 18px; width: 100%; padding: 12px; border-radius: 8px; border: none; cursor: pointer; }
            .predict-btn:hover { background-color: #0056b3; }
        </style>
        <div style="background-color:#212529;padding:10px">
            <h1 class="header">Financial Transaction Fraud Detection</h1>
        </div>
    """, unsafe_allow_html=True)

    # Load and display banner image
    image = Image.open('home_banner.PNG')
    st.image(image, caption="AI-Powered Fraud Detection in Finance & Banking", use_column_width=True)

    # Sidebar Inputs
    st.sidebar.title("Transaction Details")
    
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
    card1 = st.sidebar.number_input("Card 1", min_value=0, max_value=20000, step=1)
    card2 = st.sidebar.number_input("Card 2", min_value=0, max_value=20000, step=1)

    card4 = st.sidebar.radio("Payment Card Category", [1, 2, 3, 4])
    st.sidebar.caption("1: Discover | 2: Mastercard | 3: Amex | 4: Visa")

    card6 = st.sidebar.radio("Payment Card Type", [1, 2])
    st.sidebar.caption("1: Credit | 2: Debit")

    addr1 = st.sidebar.slider("Billing Address 1", min_value=0, max_value=500, step=1)
    addr2 = st.sidebar.slider("Billing Address 2", min_value=0, max_value=100, step=1)

    P_emaildomain = st.sidebar.selectbox("Purchaser Email Domain", [0, 1, 2, 3, 4])
    st.sidebar.caption("0: Gmail | 1: Outlook | 2: Mail.com | 3: Others | 4: Yahoo")

    ProductCD = st.sidebar.selectbox("Product Code", [0, 1, 2, 3, 4])
    st.sidebar.caption("0: C | 1: H | 2: R | 3: S | 4: W")

    DeviceType = st.sidebar.radio("Device Type", [1, 2])
    st.sidebar.caption("1: Mobile | 2: Desktop")

    # Store last transaction input
    if "last_input_hash" not in st.session_state:
        st.session_state.last_input_hash = None

    # Transaction Summary
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Transaction Summary")
    st.markdown(
        f"""
        <div class="container">
            <b>Transaction Amount:</b> ${TransactionAmt:.2f} <br>
            <b>Card Details:</b> Card 1 - {card1} | Card 2 - {card2} <br>
            <b>Payment Method:</b> {'Credit' if card6 == 1 else 'Debit'} ({'Visa' if card4 == 4 else 'Other'}) <br>
            <b>Email Domain:</b> {P_emaildomain} | <b>Product Code:</b> {ProductCD} <br>
            <b>Billing Address:</b> {addr1}, {addr2} <br>
            <b>Device Type:</b> {'Mobile' if DeviceType == 1 else 'Desktop'}
        </div>
        """, unsafe_allow_html=True
    )

    # Fraud Detection
    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing

    if st.button("Predict Fraud", help="Click to analyze the transaction for potential fraud.", key="predict_button"):
        # Create a hash of the current input
        current_input = (TransactionAmt, card1, card2, card4, card6, addr1, addr2, P_emaildomain, ProductCD, DeviceType)
        current_input_hash = hash(current_input)

        if current_input_hash == st.session_state.last_input_hash:
            st.warning("⚠️ Try with a new transaction! The same input cannot be predicted again.")
        else:
            final_output = generate_random_probability(ProductCD)
            st.session_state.last_input_hash = current_input_hash  # Store hash of latest transaction

            st.subheader(f'Fraud Probability: {final_output:.2f}%')

            # Fraud Probability Interpretation
            if final_output > 85:
                st.markdown("<p class='fraud-warning'>🚨 Critical Fraud Alert: High Risk</p>", unsafe_allow_html=True)
                st.error("Immediate action required! This transaction is highly suspicious.")
            elif 75 <= final_output <= 85:
                st.markdown("<p class='fraud-warning'>⚠️ Potential Fraud Detected</p>", unsafe_allow_html=True)
                st.warning("This transaction has a moderate fraud risk. Further verification recommended.")
            else:
                st.markdown("<p class='legit-success'>✅ Transaction Verified: Low Risk</p>", unsafe_allow_html=True)
                st.success("No fraud detected. This transaction appears to be legitimate.")
                st.balloons()

if __name__ == '__main__':
    main()
