import streamlit as st
import pickle
import numpy as np

# Load trained model
with open('final_model.sav', 'rb') as model_file:
    model = pickle.load(model_file)

# Streamlit UI
st.title("Financial Transaction Fraud Prediction System")
st.subheader("Enter Transaction Details")

# User inputs
TransactionAmt = st.number_input("Transaction Amount (USD)", min_value=0.0, step=0.01)
ProductCD = st.text_input("Product Code")
card1 = st.number_input("Payment Card 1", min_value=0, step=1)
card2 = st.number_input("Payment Card 2", min_value=0, step=1)
card3 = st.number_input("Payment Card 3", min_value=0, step=1)
card4 = st.selectbox("Payment Card Type", ["Credit", "Debit", "Other"])
card5 = st.number_input("Payment Card 5", min_value=0, step=1)
card6 = st.selectbox("Payment Card Category", ["1", "2", "3", "4"])
addr1 = st.number_input("Billing Address 1", min_value=0, step=1)
addr2 = st.number_input("Billing Address 2", min_value=0, step=1)
P_emaildomain = st.text_input("Primary Email Domain")
R_emaildomain = st.text_input("Recipient Email Domain")

# Prepare input data
input_data = np.array([[TransactionAmt, card1, card2, card3, card5, addr1, addr2]])

# Make prediction
if st.button("Predict Fraudulent Transaction"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0, 1] * 100
    
    if prediction == 1:
        st.error(f"⚠️ Fraudulent Transaction Detected! (Probability: {probability:.2f}%)")
    else:
        st.success(f"✅ Transaction appears legitimate (Probability: {probability:.2f}%)")
