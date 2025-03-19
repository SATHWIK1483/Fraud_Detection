import streamlit as st
import app  # Main page
import report  # Report page

# Get query params
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["main"])[0]

# Navigate based on query param
if page == "report":
    report.report()
else:
    app.main()

