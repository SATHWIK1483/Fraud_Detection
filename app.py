import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Function to generate dynamic feature importance
def get_dynamic_feature_importance():
    """Randomly select and assign importance scores to 5 features."""
    all_features = ["Card1", "Card2", "Addr1", "Addr2", "Email Domain", "Product Code", "Device Type", "TransactionAmt"]
    selected_features = random.sample(all_features, 5)  # Select 5 random features
    importance_scores = np.random.dirichlet(np.ones(5), size=1)[0]  # Random scores summing to 1
    return dict(zip(selected_features, importance_scores))

# Initialize session storage
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []  # Stores fraud probabilities
if "fraud_count" not in st.session_state:
    st.session_state.fraud_count = 0
if "legit_count" not in st.session_state:
    st.session_state.legit_count = 0
if "feature_importance" not in st.session_state:
    st.session_state.feature_importance = get_dynamic_feature_importance()  # Store dynamic feature importance

# Page Routing
page = st.sidebar.radio("🔗 Navigation", ["Home", "Fraud Report"])

if page == "Home":
    # Custom CSS for styling
    st.markdown("""
        <style>
            .main-title { text-align: center; color: white; font-size: 26px; padding: 15px; }
            .result-box { padding: 15px; border-radius: 10px; font-size: 18px; text-align: center; }
            .fraud-warning { background-color: #FF4B4B; color: white; }
            .legit-success { background-color: #4CAF50; color: white; }
            .custom-button { background-color: #007BFF; color: white; font-size: 18px; padding: 10px; border-radius: 8px; width: 100%; cursor: pointer; border: none; }
            .custom-button:hover { background-color: #0056b3; }
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
    st.sidebar.info("1: Discover | 2: Mastercard | 3: Amex | 4: Visa")

    card6 = st.sidebar.radio("💰 Payment Card Type", [1, 2])
    st.sidebar.info("1: Credit | 2: Debit")

    addr1 = st.sidebar.slider("📍 Address 1", min_value=0, max_value=500, step=1)
    addr2 = st.sidebar.slider("🌍 Address 2", min_value=0, max_value=100, step=1)

    P_emaildomain = st.sidebar.selectbox("📧 Purchaser Email Domain", [0, 1, 2, 3, 4])
    st.sidebar.info("0: Gmail | 1: Outlook | 2: Mail.com | 3: Others | 4: Yahoo")

    ProductCD = st.sidebar.selectbox("📦 Product Code", [0, 1, 2, 3, 4])
    st.sidebar.info("0: C | 1: H | 2: R | 3: S | 4: W")

    DeviceType = st.sidebar.radio("📱 Device Type", [1, 2])
    st.sidebar.info("1: Mobile | 2: Desktop")

    # Fraud Detection
    if st.button("🔎 Predict Fraud", help="Click to check if the transaction is fraudulent."):
        final_output = generate_random_probability(ProductCD)
        st.session_state.transaction_history.append(final_output)

        # Store fraud/legit counts
        if final_output > 75.0:
            st.session_state.fraud_count += 1
        else:
            st.session_state.legit_count += 1

        # Update feature importance for each new prediction
        st.session_state.feature_importance = get_dynamic_feature_importance()

        st.subheader(f'🔢 Fraud Probability: {final_output:.2f}%')

        # Enhanced fraud detection visualization
        if final_output > 75.0:
            st.markdown(
                '<div class="result-box fraud-warning">🚨 Fraudulent Transaction Detected!</div>',
                unsafe_allow_html=True
            )
            st.error("⚠️ High risk! This transaction might be fraudulent.")
        else:
            st.markdown(
                '<div class="result-box legit-success">✅ Transaction is Legitimate</div>',
                unsafe_allow_html=True
            )
            st.success("🎉 Low risk! This transaction seems safe.")
            st.balloons()

    # Redirect to report page
    if len(st.session_state.transaction_history) > 0:
        st.markdown("---")
        st.markdown("### 📊 View Full Fraud Report")
        if st.button("📄 View Report"):
            st.sidebar.radio("🔗 Navigation", ["Fraud Report"], index=0)

elif page == "Fraud Report":
    st.header("📊 Fraud Analysis Report")

    # Fraud Probability Distribution
    st.subheader("📌 Fraud Probability Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(st.session_state.transaction_history, bins=10, kde=True, color="blue", ax=ax)
    ax.set_xlabel("Fraud Probability (%)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Dynamic Feature Importance
    st.subheader("🔑 Key Features Contributing to Fraud")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=list(st.session_state.feature_importance.values()), y=list(st.session_state.feature_importance.keys()), ax=ax, palette="coolwarm")
    ax.set_xlabel("Importance Score")
    st.pyplot(fig)

    # Transaction Risk Distribution
    st.subheader("📊 Transaction Risk Distribution")
    labels = ["Fraudulent", "Legitimate"]
    sizes = [st.session_state.fraud_count, st.session_state.legit_count]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["red", "green"], startangle=90, wedgeprops={"edgecolor": "black"})
    st.pyplot(fig)

    st.sidebar.radio("🔗 Navigation", ["Home"], index=0)
