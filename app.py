import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from PIL import Image
import io

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Function to randomly assign importance scores to fraud-related features
def get_random_feature_importance():
    """Generate random importance scores for fraud detection."""
    feature_pool = ["Card1", "Card2", "Addr1", "Addr2", "Email Domain", "Product Code", "Transaction Amount", "Device Type"]
    selected_features = random.sample(feature_pool, 5)  # Select 5 random features
    
    # Assign random importance scores that sum up to 1
    importance_scores = np.random.dirichlet(np.ones(5), size=1)[0]  # Ensures scores sum to 1
    feature_importance = {feature: round(score, 2) for feature, score in zip(selected_features, importance_scores)}

    return feature_importance

# Initialize session storage
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []  # Stores fraud probabilities
if "fraud_count" not in st.session_state:
    st.session_state.fraud_count = 0
if "legit_count" not in st.session_state:
    st.session_state.legit_count = 0
if "last_fraud_features" not in st.session_state:
    st.session_state.last_fraud_features = {}  # Store last generated feature importance
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = {}  # Store last input values
if "graphs" not in st.session_state:
    st.session_state.graphs = []  # Store generated graphs for the report

# Function to generate report text
def generate_report_text():
    report_text = "Fraud Analysis Report\n\n"
    report_text += f"Total Transactions Analyzed: {len(st.session_state.transaction_history)}\n"
    report_text += f"Fraudulent Transactions: {st.session_state.fraud_count}\n"
    report_text += f"Legitimate Transactions: {st.session_state.legit_count}\n\n"
    report_text += "Risk Assessment & Explanation:\n"
    report_text += "- Transactions with a fraud probability above 75% are flagged as high risk.\n"
    report_text += "- Key Features Contributing to Fraud:\n"
    for feature, importance in st.session_state.last_fraud_features.items():
        report_text += f"  - {feature}: {importance * 100:.1f}%\n"
    report_text += "\nSuggested Actions:\n"
    report_text += "- Verify flagged transactions manually.\n"
    report_text += "- Implement stricter fraud detection algorithms.\n"
    return report_text

# Streamlit App
def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
            .main-title { text-align: center; color: white; font-size: 26px; padding: 15px; }
            .result-box { padding: 15px; border-radius: 10px; font-size: 18px; text-align: center; }
            .fraud-warning { background-color: #FF4B4B; color: white; }
            .legit-success { background-color: #4CAF50; color: white; }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div style="background-color:#1E1E1E; padding:15px; border-radius:10px;">
            <h1 class="main-title">Financial Transaction Fraud Detection 💰</h1>
        </div>
    """, unsafe_allow_html=True)

    # Load and display banner image
    image = Image.open('home_banner.PNG')
    st.image(image, caption="AI-Powered Fraud Detection in Finance & Banking", use_container_width=True)

    # Sidebar Inputs
    st.sidebar.title("🔍 Transaction Details")
    
    TransactionAmt = st.sidebar.number_input("💵 Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
    card1 = st.sidebar.number_input("💳 Card 1", min_value=0, max_value=20000, step=1)
    card2 = st.sidebar.number_input("💳 Card 2", min_value=0, max_value=20000, step=1)
    card4 = st.sidebar.radio("🏦 Payment Card Category", [1, 2, 3, 4])
    card6 = st.sidebar.radio("💰 Payment Card Type", [1, 2])
    addr1 = st.sidebar.slider("📍 Address 1", min_value=0, max_value=500, step=1)
    addr2 = st.sidebar.slider("🌍 Address 2", min_value=0, max_value=100, step=1)
    P_emaildomain = st.sidebar.selectbox("📧 Purchaser Email Domain", [0, 1, 2, 3, 4])
    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])
    DeviceType = st.sidebar.radio("📱 Device Type", [1, 2])

    # Generate Fraud Probability
    fraud_prob = generate_random_probability(ProductCD)
    st.session_state.transaction_history.append(fraud_prob)
    
    # Classify transaction
    if fraud_prob > 75:
        st.session_state.fraud_count += 1
    else:
        st.session_state.legit_count += 1
    
    # Generate Fraud Probability Graph
    fig, ax = plt.subplots()
    fraud_probs = [generate_random_probability(i) for i in range(5)]
    sns.barplot(x=[f"Prod {i}" for i in range(5)], y=fraud_probs, ax=ax, palette="coolwarm")
    ax.set_title("Fraud Probability Distribution")
    st.pyplot(fig)
    
    if st.button("📌 Add to Report"):
        st.session_state.graphs.append(fig)
        st.success("Graph added to the report!")
    
    if st.button("📥 Download Report"):
        report_text = generate_report_text()
        report_bytes = io.BytesIO()
        report_bytes.write(report_text.encode())
        report_bytes.seek(0)
        st.download_button("Download Report", report_bytes, file_name="fraud_analysis_report.txt", mime="text/plain")

if __name__ == '__main__':
    main()
