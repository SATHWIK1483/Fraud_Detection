import streamlit as st
import pickle
import numpy as np

# Load the trained model
model = pickle.load(open('final_model.sav', 'rb'))

st.title("Financial Transaction Fraud Prediction System")

# Sidebar for transaction input details
st.sidebar.header("Enter Transaction Details")

# User input fields
TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", min_value=0.0, step=0.01)
ProductCD = st.sidebar.selectbox("Product Code", ['A', 'B', 'C', 'D', 'E'])
card1 = st.sidebar.number_input("Payment Card 1", min_value=0, step=1)
card2 = st.sidebar.number_input("Payment Card 2", min_value=0, step=1)
card3 = st.sidebar.number_input("Payment Card 3", min_value=0, step=1)
card4 = st.sidebar.selectbox("Payment Card Type", [1, 2, 3, 4])
card5 = st.sidebar.number_input("Payment Card 5", min_value=0, step=1)
card6 = st.sidebar.selectbox("Payment Card Category", [1, 2, 3, 4])
addr1 = st.sidebar.number_input("Billing Address 1", min_value=0, step=1)
addr2 = st.sidebar.number_input("Billing Address 2", min_value=0, step=1)
dist1 = st.sidebar.number_input("Distance 1", min_value=0, step=1)
dist2 = st.sidebar.number_input("Distance 2", min_value=0, step=1)
P_emaildomain = st.sidebar.text_input("Purchaser Email Domain")
R_emaildomain = st.sidebar.text_input("Recipient Email Domain")

# C variables
C_features = [st.sidebar.number_input(f"C{i}", min_value=0, step=1) for i in range(1, 15)]

# D variables
D_features = [st.sidebar.number_input(f"D{i}", min_value=0, step=1) for i in range(1, 15)]

# Feature array creation
features = [
    TransactionAmt, ord(ProductCD), card1, card2, card3, card4, card5, card6,
    addr1, addr2, dist1, dist2, ord(P_emaildomain[0]) if P_emaildomain else 0,
    ord(R_emaildomain[0]) if R_emaildomain else 0
] + C_features + D_features

# Convert to NumPy array and reshape for model prediction
features = np.array(features).reshape(1, -1)

if st.sidebar.button("Predict Fraudulent Transaction"):
    probability = model.predict_proba(features)[0][1] * 100
    
    st.subheader(f"Probability Score of Fraud: {probability:.2f}%")
    
    if probability > 50:
        st.error("🚨 Transaction appears FRAUDULENT!")
    else:
        st.success("✅ Transaction appears LEGITIMATE")
