import numpy as np
import pickle
import streamlit as st
from PIL import Image

# Load the saved model
loaded_model = pickle.load(open('final_model.sav', 'rb'))

# Prediction function
@st.cache_data()
def predict_fraud(card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType):
    input_data = np.array([[card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType]])
    prediction = loaded_model.predict_proba(input_data)
    pred = '{0:.{1}f}'.format(prediction[0][0], 2)
    return float(pred)

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
    st.sidebar.subheader("Choose Parameters to Predict a Financial Transaction")
    
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", 0, 20000, step=1)
    card1 = st.sidebar.number_input("Payment Card 1", 0, 20000, step=1)
    card2 = st.sidebar.number_input("Payment Card 2", 0, 20000, step=1)
    card4 = st.sidebar.radio("Payment Card Category", [1, 2, 3, 4])
    card6 = st.sidebar.radio("Payment Card Type", [1, 2])
    addr1 = st.sidebar.slider("Billing Zip Code", 0, 500, step=1)
    addr2 = st.sidebar.slider("Billing Country Code", 0, 100, step=1)
    P_emaildomain = st.sidebar.selectbox("Purchaser Email Domain", [0, 1, 2, 3, 4])
    ProductCD = st.sidebar.selectbox("Product Code", [0, 1, 2, 3, 4])
    DeviceType = st.sidebar.radio("Device Type", [1, 2])
    
    if st.button("Predict Fraudulent Transaction"):
        output = predict_fraud(card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType)
        final_output = output * 100
        st.subheader(f'Probability Score of Fraud: {final_output}%')
        
        if final_output > 75.0:
            st.error("**Warning! Transaction is Fraudulent**")
        else:
            st.success("**Transaction is Legitimate**")
    
if __name__ == '__main__':
    main()
