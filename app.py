import numpy as np
import pickle
import time
import streamlit as st

# Load the trained model
try:
    loaded_model = pickle.load(open('final_model.sav', 'rb'))
except Exception as e:
    st.error(f"Error loading model: {e}")

# Function for fraud prediction
@st.cache_data
def predict_fraud(TransactionAmt, card1, card2, card3, card5, addr1, addr2):
    try:
        input_data = np.array([[TransactionAmt, card1, card2, card3, card5, addr1, addr2]])
        prediction = loaded_model.predict_proba(input_data)
        pred_score = round(prediction[0][1] * 100, 2)  # Probability of fraud
        return pred_score
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

# Streamlit UI
def main():
    # App Header
    st.markdown(
        """
        <div style="background-color:#000;padding:15px;border-radius:10px;">
        <h1 style="color:white;text-align:center;">💰 Financial Fraud Detection System 🕵️</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar
    st.sidebar.title("Enter Transaction Details")

    # Input Fields
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", 0.0, 20000.0, step=0.01)
    card1 = st.sidebar.number_input("Payment Card 1", 0, 20000, step=1)
    card2 = st.sidebar.number_input("Payment Card 2", 0, 20000, step=1)
    card3 = st.sidebar.number_input("Payment Card 3", 0, 20000, step=1)
    card5 = st.sidebar.number_input("Payment Card 5", 0, 20000, step=1)
    addr1 = st.sidebar.slider("Billing Address 1", 0, 500, step=1)
    addr2 = st.sidebar.slider("Billing Address 2", 0, 100, step=1)

    # Prediction Button
    if st.sidebar.button("🔍 Predict Fraud"):
        fraud_probability = predict_fraud(TransactionAmt, card1, card2, card3, card5, addr1, addr2)

        if fraud_probability is not None:
            st.subheader(f"Fraud Probability: **{fraud_probability}%**")

            if fraud_probability > 75:
                st.error("🚨 **High Risk: Potential Fraud Detected!**")
                st.image("https://media.giphy.com/media/8ymvg6pl1Lzy0/giphy.gif", use_column_width=True)
            else:
                st.success("✅ **Transaction Seems Legitimate**")
                st.balloons()

if __name__ == '__main__':
    main()
