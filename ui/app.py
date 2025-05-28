# ui/app.py

import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Knowledge Assistant", layout="wide")
st.title("📚 AI Knowledge Assistant")

st.markdown("""
Upload a `.txt` file containing your reference material. Here's how it works:

1. Files should be plain text (`.txt`) format.
2. The content will be split into 500-character chunks.
3. Each chunk is embedded and stored securely in Pinecone.
4. Once uploaded, you can ask natural language questions about the content.

**Important:** Avoid uploading documents with sensitive information. This is for experimental purposes only.
""")

# Upload section
st.header("📤 Upload a Document")

uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])
if uploaded_file is not None:
    files = {'file': uploaded_file.getvalue()}
    response = requests.post(f"{API_URL}/upload", files={"file": (uploaded_file.name, uploaded_file)})
    if response.status_code == 200:
        st.success("File uploaded and processed successfully.")
    else:
        st.error("There was an error processing the file.")

# Question asking section
st.header("❓ Ask a Question")
user_question = st.text_input("What would you like to know?")
if user_question:
    with st.spinner("Thinking..."):
        res = requests.post(f"{API_URL}/ask", json={"question": user_question})
        if res.status_code == 200:
            st.markdown("#### 💬 Answer")
            st.write(res.json()["answer"])
        else:
            st.error("Something went wrong. Try again.")

# Health check (optional)
try:
    health = requests.get(f"{API_URL}/health")
    if health.status_code == 200:
        st.sidebar.success("Backend is running ✅")
    else:
        st.sidebar.warning("Backend issue")
except Exception:
    st.sidebar.error("Cannot reach backend")
