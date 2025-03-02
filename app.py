import numpy as np
import pickle
import time
import streamlit as st

# loading the saved model
loaded_model = pickle.load(open('final_model.sav', 'rb'))

# creating a function for Prediction
@st.cache(persist=True)
def predict_fraud(TransactionAmt, card1, addr1, card2, P_emaildomain, card4, DeviceType, ProductCD, card6, addr2):
    input = np.array([[TransactionAmt, card1, addr1, card2, P_emaildomain, card4, DeviceType, ProductCD, card6, addr2]])
    prediction = loaded_model.predict_proba(input)
    pred = '{0:.{1}f}'.format(prediction[0][0], 2)
    return float(pred)

def main():
    html_temp = """
        <div style="background-color:#000000 ;padding:10px">
        <h1 style="color:white;text-align:center;">Financial Fraud Detection System 💰🕵️</h1>
        </div>
     """
    st.markdown(html_temp, unsafe_allow_html=True)
    
    # Sidebar Inputs
    st.sidebar.title("Enter Transaction Details")
    
    # TransactionAmt
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", 0.0, 20000.0, step=0.01)
    
    # card1
    card1 = st.sidebar.number_input("Payment Card 1", 0, 20000, step=1)
    
    # addr1
    addr1 = st.sidebar.number_input("Billing Address 1", 0, 500, step=1)
    
    # card2
    card2 = st.sidebar.number_input("Payment Card 2", 0, 20000, step=1)
    
    # P_emaildomain
    P_emaildomain = st.sidebar.text_input("Primary Email Domain")
    
    # card4 (Newly Added)
    card4 = st.sidebar.number_input("Payment Card 4", 0, 20000, step=1)
    
    # DeviceType (Newly Added)
    DeviceType = st.sidebar.selectbox("Device Type", ["Mobile", "Desktop", "Other"])
    
    # ProductCD (Newly Added)
    ProductCD = st.sidebar.selectbox("Product Code", ["A", "B", "C", "D", "E"])
    
    # card6
    card6 = st.sidebar.number_input("Payment Card 6", 0, 20000, step=1)
    
    # addr2
    addr2 = st.sidebar.number_input("Billing Address 2", 0, 100, step=1)
    
    # Prediction Logic
    if st.button("Predict Fraud"):
        output = predict_fraud(TransactionAmt, card1, addr1, card2, P_emaildomain, card4, DeviceType, ProductCD, card6, addr2)
        final_output = output * 100
        st.subheader(f'Probability Score of Financial Transaction is {final_output}%')
        
        if final_output > 75.0:
            st.error("🚨 OMG! Financial Transaction is Fraudulent!")
        else:
            st.success("✅ Hurray! Transaction is Legitimate")
            st.balloons()
    
if __name__ == '__main__':
    main()
