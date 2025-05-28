import os
import requests
import streamlit as st

# Environment detection
IS_CLOUD = os.environ.get("STREAMLIT_ENV") == "cloud"

# Backend URL
if IS_CLOUD:
    BACKEND_URL = "https://ai-knowledge-backend.onrender.com"
else:
    BACKEND_URL = "http://localhost:8000"

# App title and instructions
st.title("AI Knowledge Assistant")
st.markdown(
    "Important: Avoid uploading documents with sensitive information. This is for experimental purposes only."
)

st.header("📤 Upload a Document")
uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])

if uploaded_file is not None:
    with st.spinner("Uploading..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)

    if response.status_code == 200:
        st.success("File uploaded and processed!")
    else:
        st.error(f"Upload failed: {response.text}")

st.header("💬 Ask a Question")
question = st.text_input("Enter your question:")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        response = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
        if response.status_code == 200:
            st.write("**Answer:**", response.json().get("answer", "No answer returned."))
        else:
            st.error(f"Question failed: {response.text}")
