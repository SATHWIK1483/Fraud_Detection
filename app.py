import numpy as np
import pickle
import streamlit as st

# Load the saved model
loaded_model = pickle.load(open('final_model.sav', 'rb'))

# Define the prediction function
def predict_fraud(card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType):
    input_data = np.array([[card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType]])
    
    # Ensure input shape matches model expectations
    try:
        prediction = loaded_model.predict_proba(input_data)
        pred = '{0:.{1}f}'.format(prediction[0][1], 2)  # Taking fraud probability
        return float(pred)
    except Exception as e:
        return str(e)  # Error handling for debugging

def main():
    # Streamlit UI
    st.markdown("""
        <div style="background-color:#000000;padding:10px">
        <h1 style="color:white;text-align:center;">Financial Transaction Fraud Detection 💰</h1>
        </div>
    """, unsafe_allow_html=True)

    from PIL import Image
    image = Image.open('home_banner.PNG')  # Ensure the file exists in the working directory
    st.image(image, caption='Impacting Finance & Banking with AI')

    # Sidebar Inputs
    st.sidebar.title("Transaction Details 🕵️")
    
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)

    card1 = st.sidebar.number_input("Card 1", min_value=0, max_value=20000, step=1)
    card2 = st.sidebar.number_input("Card 2", min_value=0, max_value=20000, step=1)

    card4 = st.sidebar.radio("Payment Card Category", [1, 2, 3, 4])
    st.sidebar.info("1: Discover | 2: Mastercard | 3: Amex | 4: Visa")

    card6 = st.sidebar.radio("Payment Card Type", [1, 2])
    st.sidebar.info("1: Credit | 2: Debit")

    addr1 = st.sidebar.slider("Billing Zip Code", min_value=0, max_value=500, step=1)
    addr2 = st.sidebar.slider("Billing Country Code", min_value=0, max_value=100, step=1)

    P_emaildomain = st.sidebar.selectbox("Purchaser Email Domain", [0, 1, 2, 3, 4])
    st.sidebar.info("0: Gmail | 1: Outlook | 2: Mail.com | 3: Others | 4: Yahoo")

    ProductCD = st.sidebar.selectbox("Product Code", [0, 1, 2, 3, 4])
    st.sidebar.info("0: C | 1: H | 2: R | 3: S | 4: W")

    DeviceType = st.sidebar.radio("Device Type", [1, 2])
    st.sidebar.info("1: Mobile | 2: Desktop")

    # Fraud Detection
    if st.button("Predict Fraud"):
        output = predict_fraud(card1, card2, card4, card6, addr1, addr2, TransactionAmt, P_emaildomain, ProductCD, DeviceType)

        try:
            final_output = float(output) * 100
            st.subheader(f'Probability of Fraud: {final_output}%')

            if final_output > 75.0:
                st.error("🚨 Fraudulent Transaction Detected!")
            else:
                st.success("✅ Transaction is Legitimate")
                st.balloons()
        except:
            st.error(f"Error: {output}")  # Display error message if prediction fails

if __name__ == '__main__':
    main()
