import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from docx import Document

# Load pre-trained model for embeddings
MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)

# Title and description
st.title("Document Similarity Checker")
st.write("Upload two documents to compare their vector embeddings and compute their similarity.")

# File uploaders
doc1 = st.file_uploader("Upload the first document", type=["txt", "pdf", "docx"])
doc2 = st.file_uploader("Upload the second document", type=["txt", "pdf", "docx"])

# Helper function to read text from uploaded files
def extract_text(file):
    if file is not None:
        if file.type == "application/pdf":
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(file)
                return "\n".join([page.extract_text() for page in reader.pages])
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                return None
        elif file.type == "text/plain":
            return file.read().decode("utf-8")
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            try:
                doc = Document(file)
                return "\n".join([paragraph.text for paragraph in doc.paragraphs])
            except Exception as e:
                st.error(f"Error reading Word document: {e}")
                return None
        else:
            st.error("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
            return None

# Process the uploaded documents
if doc1 and doc2:
    text1 = extract_text(doc1)
    text2 = extract_text(doc2)

    if text1 and text2:
        # Display the documents
        st.subheader("Document 1 Preview:")
        st.text_area("", text1[:500] + ("..." if len(text1) > 500 else ""), height=200, disabled=True)

        st.subheader("Document 2 Preview:")
        st.text_area("", text2[:500] + ("..." if len(text2) > 500 else ""), height=200, disabled=True)

        # Compute embeddings
        st.write("Computing vector embeddings...")
        embeddings1 = model.encode([text1])[0]
        embeddings2 = model.encode([text2])[0]

        # Compute cosine similarity
        similarity = cosine_similarity([embeddings1], [embeddings2])[0][0]

        # Display similarity score
        st.subheader("Similarity Score")
        st.metric(label="Cosine Similarity", value=f"{similarity:.4f}")

    else:
        st.warning("Please ensure both documents are valid and not empty.")
else:
    st.info("Please upload both documents to proceed.")
