import numpy as np
import pickle
import time
import streamlit as st

# loading the saved model
loaded_model = pickle.load(open('final_model.sav', 'rb'))

# creating a function for Prediction
@st.cache(persist=True)
def predict_fraud(TransactionAmt, card1, card2, card3, card5, addr1, addr2, P_emaildomain, R_emaildomain):
    input = np.array([[TransactionAmt, card1, card2, card3, card5, addr1, addr2]])
    prediction = loaded_model.predict_proba(input)
    pred = '{0:.{1}f}'.format(prediction[0][0], 2)
    return float(pred)


def main():
    html_temp = """
        <div style="background-color:#000000 ;padding:10px">
        <h1 style="color:white;text-align:center;">Financial Transaction Fraud Prediction ML Web App 💰 </h1>
        </div>
     """
    st.markdown(html_temp, unsafe_allow_html=True)
    
    # getting the input data from the user
    st.sidebar.title("Financial Transaction Fraud Prediction System 🕵️")
    st.sidebar.subheader("Enter Transaction Details")

    # TransactionAmt
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", 0.0, 20000.0, step=0.01)
    
    # card1
    card1 = st.sidebar.number_input("Payment Card 1", 0, 20000, step=1)

    # card2
    card2 = st.sidebar.number_input("Payment Card 2", 0, 20000, step=1)

    # card3
    card3 = st.sidebar.number_input("Payment Card 3", 0, 20000, step=1)

    # card5
    card5 = st.sidebar.number_input("Payment Card 5", 0, 20000, step=1)
    
    # addr1
    addr1 = st.sidebar.slider("Billing Address 1", 0, 500, step=1)

    # addr2
    addr2 = st.sidebar.slider("Billing Address 2", 0, 100, step=1)
    
    # P_emaildomain
    P_emaildomain = st.sidebar.text_input("Primary Email Domain")
    
    # R_emaildomain
    R_emaildomain = st.sidebar.text_input("Recipient Email Domain")
    
    safe_html = """ 
    <img src="https://media.giphy.com/media/g9582DNuQppxC/giphy.gif" alt="confirmed" style="width:698px;height:350px;"> 
    """
    
    danger_html = """  
    <img src="https://media.giphy.com/media/8ymvg6pl1Lzy0/giphy.gif" alt="cancel" style="width:698px;height:350px;">
    """
    
    # creating a button for Prediction
    if st.button("Click Here To Predict"):
        output = predict_fraud(TransactionAmt, card1, card2, card3, card5, addr1, addr2, P_emaildomain, R_emaildomain)
        final_output = output * 100
        st.subheader('Probability Score of Financial Transaction is {}% '.format(final_output))

        if final_output > 75.0:
            st.markdown(danger_html, unsafe_allow_html=True)
            st.error("**OMG! Financial Transaction is Fraud**")
        else:
            st.balloons()
            time.sleep(5)
            st.balloons()
            time.sleep(5)
            st.balloons()
            st.markdown(safe_html, unsafe_allow_html=True)
            st.success("**Hurray! Transaction is Legitimate**")
    
if __name__ == '__main__':
    main()
