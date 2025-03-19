import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def report():
    st.title("📊 Fraud Analysis Report")

    # Check if transactions exist
    if len(st.session_state.transaction_history) == 0:
        st.warning("⚠️ No transaction history found! Please predict a transaction first.")
        return

    # Fraud Probability Distribution
    st.subheader("📌 Fraud Probability Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(st.session_state.transaction_history, bins=10, kde=True, color="blue", ax=ax)
    ax.set_xlabel("Fraud Probability (%)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Transaction Risk Distribution
    st.subheader("📊 Transaction Risk Distribution")
    labels = ["Fraudulent", "Legitimate"]
    sizes = [st.session_state.fraud_count, st.session_state.legit_count]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["red", "green"], startangle=90, wedgeprops={"edgecolor": "black"})
    st.pyplot(fig)

    # Back Button
    if st.button("⬅️ Back to Main Page"):
        st.experimental_set_query_params(page="main")

if __name__ == '__main__':
    report()
