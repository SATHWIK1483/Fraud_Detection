import numpy as np
import pickle
import streamlit as st

# loading the saved model
loaded_model = pickle.load(open('final_model.sav', 'rb'))

# creating a function for Prediction
@st.cache(persist=True)
def predict_fraud(TransactionAmt, ProductCD, card1, card2, card3, card4, card5, card6, addr1, addr2, dist1, P_emaildomain, R_emaildomain, C1, C2, C3, C4):
    input = np.array([[TransactionAmt, ProductCD, card1, card2, card3, card4, card5, card6, addr1, addr2, dist1, P_emaildomain, R_emaildomain, C1, C2, C3, C4]])
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
    
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", 0.0, 20000.0, step=0.01)
    ProductCD = st.sidebar.number_input("Product Code", 0, 10, step=1)
    card1 = st.sidebar.number_input("Payment Card 1", 0, 20000, step=1)
    card2 = st.sidebar.number_input("Payment Card 2", 0, 20000, step=1)
    card3 = st.sidebar.number_input("Payment Card 3", 0, 20000, step=1)
    card4 = st.sidebar.number_input("Payment Card 4", 0, 20000, step=1)
    card5 = st.sidebar.number_input("Payment Card 5", 0, 20000, step=1)
    card6 = st.sidebar.number_input("Payment Card 6", 0, 20000, step=1)
    addr1 = st.sidebar.number_input("Billing Address 1", 0, 500, step=1)
    addr2 = st.sidebar.number_input("Billing Address 2", 0, 100, step=1)
    dist1 = st.sidebar.number_input("Distance from Home", 0, 10000, step=1)
    P_emaildomain = st.sidebar.number_input("Primary Email Domain", 0, 100, step=1)
    R_emaildomain = st.sidebar.number_input("Recipient Email Domain", 0, 100, step=1)
    C1 = st.sidebar.number_input("C1", 0, 100, step=1)
    C2 = st.sidebar.number_input("C2", 0, 100, step=1)
    C3 = st.sidebar.number_input("C3", 0, 100, step=1)
    C4 = st.sidebar.number_input("C4", 0, 100, step=1)
    
    if st.button("Predict Fraud"):
        output = predict_fraud(TransactionAmt, ProductCD, card1, card2, card3, card4, card5, card6, addr1, addr2, dist1, P_emaildomain, R_emaildomain, C1, C2, C3, C4)
        final_output = output * 100
        st.subheader(f'Probability Score of Financial Transaction is {final_output}%')
        
        if final_output > 75.0:
            st.error("🚨 OMG! Financial Transaction is Fraudulent!")
        else:
            st.success("✅ Hurray! Transaction is Legitimate")
            st.balloons()
    
if __name__ == '__main__':
    main()

