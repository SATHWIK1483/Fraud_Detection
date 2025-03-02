import numpy as np
import pickle
import streamlit as st
from PIL import Image

# Load the trained model
loaded_model = pickle.load(open('final_model.sav', 'rb'))

# Prediction function
@st.cache_data()
def predict_fraud(card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType):
    input_data = np.array([[card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType]])
    prediction = loaded_model.predict_proba(input_data)
    fraud_probability = prediction[0][1]  # Assuming index 1 corresponds to fraud probability
    return float(fraud_probability)

# Main function
def main():
    st.markdown(
        """
        <div style="background-color:#000000; padding:10px">
        <h1 style="color:white; text-align:center;">Financial Transaction Fraud Prediction ML Web App 💰</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    image = Image.open('home_banner.PNG')
    st.image(image, caption='Impacting Finance & Banking with AI')
    
    # Sidebar Inputs
    st.sidebar.title("Financial Transaction Fraud Prediction System 🕵️")
    st.sidebar.subheader("Enter Transaction Details")
    
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=1.0)
    card1 = st.sidebar.number_input("Payment Card 1", min_value=0, max_value=20000, step=1)
    card2 = st.sidebar.number_input("Payment Card 2", min_value=0, max_value=20000, step=1)
    card4 = st.sidebar.radio("Payment Card Category", [1, 2, 3, 4])
    card6 = st.sidebar.radio("Payment Card Type", [1, 2])
    addr1 = st.sidebar.slider("Billing Zip Code", min_value=0, max_value=500, step=1)
    addr2 = st.sidebar.slider("Billing Country Code", min_value=0, max_value=100, step=1)
    P_emaildomain = st.sidebar.selectbox("Purchaser Email Domain", [0, 1, 2, 3, 4])
    ProductCD = st.sidebar.selectbox("Product Code", [0, 1, 2, 3, 4])
    DeviceType = st.sidebar.radio("Device Type", [1, 2])
    
    if st.button("Predict Fraudulent Transaction"):
        fraud_score = predict_fraud(card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType)
        fraud_percentage = fraud_score * 100
        st.subheader(f'Probability Score of Fraud: {fraud_percentage:.2f}%')
        
        if fraud_percentage > 75.0:
            st.error("**Warning! High Probability of Fraudulent Transaction**")
        elif 50.0 <= fraud_percentage <= 75.0:
            st.warning("**Caution! This transaction is suspicious**")
        else:
            st.success("**Transaction appears legitimate**")
    
if __name__ == '__main__':
    main()
