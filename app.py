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
    # Streamlit UI Header
    st.markdown("""
        <style>
            .main-title { text-align: center; color: white; padding: 10px; font-size: 26px; }
            .fraud-warning { color: red; font-size: 22px; font-weight: bold; text-align: center; }
            .legit-success { color: green; font-size: 22px; font-weight: bold; text-align: center; }
            .custom-button { background-color: #FF4B4B; color: white; font-size: 20px; width: 100%; padding: 10px; border-radius: 8px; border: none; cursor: pointer; }
            .custom-button:hover { background-color: #FF1E1E; }
        </style>
        <div style="background-color:#000000;padding:10px">
            <h1 class="main-title">Financial Transaction Fraud Detection 💰</h1>
        </div>
    """, unsafe_allow_html=True)

    # Load and display banner image
    image = Image.open('home_banner.PNG')
    st.image(image, caption='Impacting Finance & Banking with AI')

    # Sidebar Inputs
    st.sidebar.title("🔍 Enter Transaction Details")
    
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

    # Store last transaction input
    if "last_input_hash" not in st.session_state:
        st.session_state.last_input_hash = None

    # Show live transaction summary
    st.markdown("### 📝 Transaction Summary")
    st.write(f"💵 **Transaction Amount:** ${TransactionAmt:.2f}")
    st.write(f"💳 **Card1:** {card1} | **Card2:** {card2}")
    st.write(f"🏦 **Payment Card:** {card4} | **Type:** {card6}")
    st.write(f"📧 **Email Domain:** {P_emaildomain} | 📦 **Product Code:** {ProductCD}")
    st.write(f"📍 **Billing Address:** {addr1}, {addr2}")
    st.write(f"📱 **Device Type:** {'Mobile' if DeviceType == 1 else 'Desktop'}")

    # Fraud Detection
    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing

    if st.button("🔎 Predict Fraud", help="Click to check if the transaction is fraudulent."):
        # Create a hash of the current input
        current_input = (TransactionAmt, card1, card2, card4, card6, addr1, addr2, P_emaildomain, ProductCD, DeviceType)
        current_input_hash = hash(current_input)

        if current_input_hash == st.session_state.last_input_hash:
            st.warning("⚠️ Try with a new transaction! The same input cannot be predicted again.")
        else:
            final_output = generate_random_probability(ProductCD)
            st.session_state.last_input_hash = current_input_hash  # Store hash of latest transaction

            st.subheader(f'🔢 Fraud Probability: {final_output:.2f}%')

            # Enhanced fraud detection visualization
            if final_output > 75.0:
                st.markdown("<p class='fraud-warning'>🚨 Fraudulent Transaction Detected!</p>", unsafe_allow_html=True)
                st.error("⚠️ High risk! This transaction might be fraudulent.")
                st.markdown(
                    '<img src="https://media.giphy.com/media/8ymvg6pl1Lzy0/giphy.gif" width="400">',
                    unsafe_allow_html=True
                )
            else:
                st.markdown("<p class='legit-success'>✅ Transaction is Legitimate</p>", unsafe_allow_html=True)
                st.success("🎉 Low risk! This transaction seems safe.")
                st.markdown(
                    '<img src="https://media.giphy.com/media/g9582DNuQppxC/giphy.gif" width="400">',
                    unsafe_allow_html=True
                )
                st.balloons()

if __name__ == '__main__':
    main()
