import streamlit as st
import random
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Set Page Configuration
st.set_page_config(page_title="Fraud Detection System", layout="wide")

# Custom CSS for Background & Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #121212;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #222222 !important;
            color: white;
        }
        h1, h2, h3, h4 {
            color: #1DB954 !important; /* Spotify Green for Highlights */
        }
        .css-1v0mbdj {
            color: white !important;
        }
        .stButton>button {
            background-color: #1DB954 !important;
            color: white !important;
            border-radius: 5px;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit App Title
st.markdown("<h1 style='text-align: center;'>🛡️ Fraud Detection System</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Transaction Details")

# Input Fields
TransactionAmt = st.sidebar.number_input("💵 Transaction Amount (USD)", min_value=0.0, max_value=20000.0, step=0.01)
card1 = st.sidebar.number_input("💳 Card 1", min_value=0, max_value=20000, step=1)

# Function to generate a random fraud probability
def generate_random_probability(ProductCD):
    """Generate a random fraud probability based on ProductCD parity."""
    if ProductCD % 2 == 0:
        return random.uniform(40, 75)  # Legitimate
    else:
        return random.uniform(75, 100)  # Fraudulent

# Fraud Prediction Button
prediction_made = False  # Flag to track if prediction has been made
if st.button("🔎 Predict Fraud"):
    final_output = generate_random_probability(card1)
    st.success(f"🔢 Fraud Probability: {final_output:.2f}%")
    prediction_made = True

# Show Graphs & Buttons After Prediction
if prediction_made:
    st.markdown("<h2 style='text-align: center;'>📊 Fraud Analysis Reports</h2>", unsafe_allow_html=True)

    # Create a button for Feature Importance Graph
    if st.button("📈 Show Feature Importance"):
        fig, ax = plt.subplots(figsize=(8, 5))
        features = ['TransactionAmt', 'Card1', 'Card2', 'Merchant']
        importance = np.random.rand(4)  # Random values for demo purposes

        ax.barh(features, importance, color="#1DB954")
        ax.set_xlabel("Importance")
        ax.set_title("Feature Importance in Fraud Detection")

        # Show Graph
        st.pyplot(fig)

    # Create a button for Fraud Distribution Graph
    if st.button("📊 Show Fraud Distribution"):
        fig, ax = plt.subplots(figsize=(8, 5))
        labels = ['Legitimate', 'Fraudulent']
        sizes = [random.randint(60, 80), random.randint(20, 40)]  # Random distribution

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["#1DB954", "#FF5733"])
        ax.set_title("Fraud Transaction Distribution")

        # Show Graph
        st.pyplot(fig)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>© 2025 Fraud Detection System</p>", unsafe_allow_html=True)
