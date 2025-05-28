import os
import requests
import streamlit as st

# Detect environment
IS_CLOUD = os.environ.get("STREAMLIT_ENV") == "cloud"

# Set backend URL
if IS_CLOUD:
    BACKEND_URL = "https://ai-knowledge-backend.onrender.com"
else:
    BACKEND_URL = "http://localhost:8000"

# App intro and instructions
st.title("🧠 AI Knowledge Assistant")

st.markdown("""
Welcome to the **AI Knowledge Assistant**, a simple prototype built by [Adam Mattis](https://www.adammattis.com), a hillbilly by roots, tech exec by trade, doing his best to stay sharp in the ever-evolving world of technology.

This tool is a lightweight demonstration of how enterprise-grade AI architecture can be implemented locally and in the cloud.

---

### 🤖 What This Is
This project is a composable, full-stack AI system that uses OpenAI for embeddings and language generation, Pinecone for high-performance vector search, FastAPI for backend services, Streamlit for a real-time user interface, and GitHub for version control.

---

### 🚀 How to Use It

1. **Upload a File**  
   Upload a `.txt` document containing your reference material. The system will break it into chunks and store it in a vector database.

2. **Ask a Question**  
   Enter a natural-language question based on the content of your document. The system will search for relevant context and return a GPT-4-powered response.

3. **Learn by Doing**  
   This isn't a polished product, it's an experiment. Use it to understand how generative AI systems work.

---

**Disclaimer:** This is for educational and experimental purposes only. Do not upload sensitive or confidential data.
""", unsafe_allow_html=True)

# Upload section
st.header("📤 Upload a Document")
uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])

if uploaded_file is not None:
    with st.spinner("Uploading..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{BACKEND_URL}/upload", files=files)

            if response.status_code == 200:
                st.success("File uploaded and processed!")
            else:
                st.error(f"Upload failed: {response.text}")
        except Exception as e:
            st.error(f"Upload error: {e}")

# Question section
st.header("💬 Ask a Question")
question = st.text_input("Enter your question:")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(f"{BACKEND_URL}/ask", json={"question": question})
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                st.markdown(f"**Answer:** {answer}")
            else:
                st.error(f"Question failed: {response.text}")
        except Exception as e:
            st.error(f"Request error: {e}")

