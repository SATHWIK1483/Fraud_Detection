import streamlit as st
import random
import numpy as np

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Initialize session storage
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []  # Stores fraud probabilities
if "fraud_count" not in st.session_state:
    st.session_state.fraud_count = 0
if "legit_count" not in st.session_state:
    st.session_state.legit_count = 0
if "last_transaction" not in st.session_state:
    st.session_state.last_transaction = None  # Stores the last transaction input

# Streamlit App
def main():
    st.title("💰 Financial Transaction Fraud Detection")

    # Sidebar Inputs
    st.sidebar.title("🔍 Transaction Details")
    TransactionAmt = st.sidebar.number_input("💵 Transaction Amount", min_value=0.0, max_value=20000.0, step=0.01)
    card1 = st.sidebar.number_input("💳 Card 1", min_value=0, max_value=20000, step=1)
    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])

    # Fraud Detection Button
    if st.button("🔎 Predict Fraud"):
        current_transaction = (TransactionAmt, card1, ProductCD)

        if current_transaction == st.session_state.last_transaction:
            st.warning("⚠️ Please change the transaction details before predicting again!")
        else:
            # Store transaction
            st.session_state.last_transaction = current_transaction
            final_output = generate_random_probability(ProductCD)
            st.session_state.transaction_history.append(final_output)

            # Count frauds and legits
            if final_output > 75.0:
                st.session_state.fraud_count += 1
            else:
                st.session_state.legit_count += 1

            st.subheader(f'🔢 Fraud Probability: {final_output:.2f}%')
            if final_output > 75.0:
                st.error("🚨 High risk! This transaction might be fraudulent.")
            else:
                st.success("✅ Low risk! This transaction seems safe.")

    # Show Report Button
    if len(st.session_state.transaction_history) > 0:
        st.markdown("---")
        if st.button("📊 View Fraud Report"):
            st.experimental_set_query_params(page="report")

if __name__ == '__main__':
    main()
