import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from PIL import Image
from docx import Document
from io import BytesIO

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Function to randomly assign importance scores to fraud-related features
def get_random_feature_importance():
    feature_pool = ["Card1", "Card2", "Addr1", "Addr2", "Email Domain", "Product Code", "Transaction Amount", "Device Type"]
    selected_features = random.sample(feature_pool, 5)  # Select 5 random features
    importance_scores = np.random.dirichlet(np.ones(5), size=1)[0]
    feature_importance = {feature: round(score, 2) for feature, score in zip(selected_features, importance_scores)}
    return feature_importance

# Function to generate a fraud report
def generate_report(transaction_details, fraud_probability, feature_importance):
    doc = Document()
    doc.add_heading('Fraud Detection Report', level=1)
    
    doc.add_heading('Transaction Details', level=2)
    for key, value in transaction_details.items():
        doc.add_paragraph(f"{key}: {value}")
    
    doc.add_heading('Fraud Analysis', level=2)
    doc.add_paragraph(f"Fraud Probability: {fraud_probability:.2f}%")
    
    doc.add_heading('Key Features Contributing to Fraud', level=2)
    for feature, score in feature_importance.items():
        doc.add_paragraph(f"{feature}: {score}")
    
    report_stream = BytesIO()
    doc.save(report_stream)
    report_stream.seek(0)
    return report_stream

# Initialize session storage
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []
if "fraud_count" not in st.session_state:
    st.session_state.fraud_count = 0
if "legit_count" not in st.session_state:
    st.session_state.legit_count = 0
if "last_fraud_features" not in st.session_state:
    st.session_state.last_fraud_features = {}
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = {}
if "last_fraud_probability" not in st.session_state:
    st.session_state.last_fraud_probability = None

# Streamlit App
def main():
    st.title("Financial Transaction Fraud Detection")
    image = Image.open('home_banner.PNG')
    st.image(image, caption="AI-Powered Fraud Detection", use_container_width=True)
    
    st.sidebar.title("Transaction Details")
    TransactionAmt = st.sidebar.number_input("Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
    card1 = st.sidebar.number_input("Card 1", min_value=0, max_value=20000, step=1)
    card2 = st.sidebar.number_input("Card 2", min_value=0, max_value=20000, step=1)
    ProductCD = st.sidebar.selectbox("Product Code", [0, 1, 2, 3, 4])
    
    current_inputs = {"Transaction Amount": TransactionAmt, "Card1": card1, "Card2": card2, "Product Code": ProductCD}
    
    if st.button("Predict Fraud"):
        if current_inputs == st.session_state.last_inputs:
            st.warning("Please enter new values before predicting!")
        else:
            fraud_probability = generate_random_probability(ProductCD)
            st.session_state.transaction_history.append(fraud_probability)
            st.session_state.last_fraud_probability = fraud_probability
            
            if fraud_probability > 75.0:
                st.session_state.fraud_count += 1
            else:
                st.session_state.legit_count += 1

            st.subheader(f'Fraud Probability: {fraud_probability:.2f}%')
            st.session_state.last_fraud_features = get_random_feature_importance()
            st.session_state.last_inputs = current_inputs.copy()

            if fraud_probability > 75.0:
                st.error("High risk! This transaction might be fraudulent.")
            else:
                st.success("Low risk! This transaction seems safe.")

    if st.session_state.last_fraud_probability is not None:
        st.header("Download Fraud Report")
        report = generate_report(st.session_state.last_inputs, st.session_state.last_fraud_probability, st.session_state.last_fraud_features)
        st.download_button("Download Fraud Report", report, file_name="Fraud_Report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

if __name__ == '__main__':
    main()
