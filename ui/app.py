import streamlit as st
import requests

st.title("AI Knowledge Assistant")

uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
if uploaded_file:
    response = requests.post("http://localhost:8000/upload", files={"file": uploaded_file})
    st.write(response.json())

question = st.text_input("Ask a question:")
if question:
    response = requests.post("http://localhost:8000/ask", params={"query": question})
    st.write(response.json().get("answer", "No response"))
