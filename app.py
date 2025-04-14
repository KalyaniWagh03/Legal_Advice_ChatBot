import os
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
import tempfile

# Streamlit UI configuration
st.set_page_config(page_title="Legal Advice Chatbot", layout="wide")
st.title("📜 Legal Advice Chatbot - India (Contract Clause Assistant)")
st.markdown("""
> 🛑 **Disclaimer:** This chatbot provides general legal information and explanations based on Indian law. It does **NOT** constitute legal advice or replace professional consultation.
""")

# Sidebar for model configuration
with st.sidebar:
    st.header("Model Configuration")
    ollama_model = st.selectbox(
        "Select Ollama Model:",
        options=["llama3.2", "llama3.1", "mistral", "gemma", "phi3"],
        index=0,
        help="Choose the Ollama model to use for embeddings and reasoning"
    )
    
    temperature = st.slider(
        "Temperature:", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.2, 
        step=0.1,
        help="Higher values make output more creative, lower values more deterministic"
    )

# Create tabs for document-specific and general advice
tab1, tab2 = st.tabs(["📄 Document Analysis", "🤔 General Legal Questions"])

with tab1:
    # Upload PDF Legal Document
    uploaded_file = st.file_uploader("Upload a contract or legal document (PDF)", type=["pdf"])
    
    if uploaded_file:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name
        
        try:
            # Process document with progress indicators
            with st.spinner("Processing document..."):
                # Load and split document
                loader = PyPDFLoader(temp_path)
                pages = loader.load()
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                docs = text_splitter.split_documents(pages)
                
                # Create embeddings using Ollama
                embeddings = OllamaEmbeddings(model=ollama_model)
                vectorstore = FAISS.from_documents(docs, embeddings)
                
                # Set up RetrievalQA
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                
                st.success(f"✅ Document processed successfully! ({len(pages)} pages)")
                
                # Document information
                st.subheader("Document Overview")
                st.info(f"📑 Document contains {len(pages)} pages and has been split into {len(docs)} chunks for analysis.")
            
            # Custom prompt for legal analysis
            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""
                You are a helpful legal assistant with expertise in Indian contract law.
                Answer the user's question based on the context below.
                
                If the answer is not in the context, say "I'm not sure based on this document. Please consult a legal expert."
                
                Provide explanations in clear language that non-lawyers can understand.
                If relevant, mention specific clauses or sections from the document.
                
                Context:
                {context}
                
                Question:
                {question}
                
                Answer:
                """
            )
            
            # Initialize Ollama model
            llm = Ollama(model=ollama_model, temperature=temperature)
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt_template}
            )
            
            # Input box
            query = st.text_input("Ask a legal question about the document:", 
                                placeholder="e.g., What does the indemnity clause mean? What are my obligations under this contract?")
            
            if query:
                with st.spinner("Analyzing and generating response..."):
                    result = qa_chain({"query": query})
                    
                    st.subheader("📘 Answer:")
                    st.markdown(result['result'])
                    
                    with st.expander("📄 Context from document"):
                        for i, doc in enumerate(result['source_documents']):
                            st.markdown(f"**Excerpt {i+1} - Page {doc.metadata['page']+1}:**")
                            st.markdown(f"```{doc.page_content[:800]}```")
        
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
            st.info("⚠️ Make sure the Ollama service is running on your machine with the selected model.")
        
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    else:
        st.info("📤 Upload a contract document above to get started.")

with tab2:
    st.subheader("🤔 General Legal Queries")
    st.markdown("Ask questions about Indian law without uploading a document.")
    
    with st.form("general_query_form"):
        general_query = st.text_area("Enter your legal question:", 
        placeholder="e.g., What IPC section applies to fraud? What are my rights as a tenant in Delhi?",
        height=100)
        submit_general = st.form_submit_button("Send")
    
    if general_query:
        with st.spinner("Researching legal information..."):
            # Legal prompt template
            legal_prompt = f"""
            You are a legal assistant knowledgeable in Indian law, especially IPC (Indian Penal Code), civil law, and consumer protection.
            Answer the following question in clear, layman-friendly terms. 
            Include relevant IPC sections or legal statutes if applicable.
            Format your response with clear headings and bullet points where appropriate.
            
            Question: {general_query}
            
            Answer:
            """
            
            try:
                # Use Ollama model
                llm = Ollama(model=ollama_model, temperature=temperature)
                response = llm.invoke(legal_prompt)
                
                st.subheader("📘 Legal Information:")
                st.markdown(response)
                st.warning("🛑 This is informational only and not a substitute for professional legal advice.")
            
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
                st.info("⚠️ Make sure the Ollama service is running on your machine with the selected model.")

# Add a system status indicator
with st.sidebar:
    st.markdown("---")
    st.subheader("System Status")
    try:
        # Simple test to check if Ollama is running
        test_llm = Ollama(model=ollama_model)
        test_response = test_llm.invoke("Hi")
        st.success("✅ Ollama service is running")
    except Exception:
        st.error("❌ Ollama service not detected")
        st.markdown("""
        **Troubleshooting:**
        1. Make sure Ollama is installed
        2. Ensure the Ollama service is running
        3. Check if the selected model is downloaded
        
        To install missing models run:
        ```
        ollama pull llama3.2
        ```
        """)

# Footer
st.markdown("---")
st.markdown("Developed by Akshay Shekade 🤖 | Law-focused NLP Chatbot using Ollama")

# Add helpful instructions
with st.sidebar:
    st.markdown("---")
    st.markdown("""
    ### 🔍 Usage Tips
    
    **For Document Analysis:**
    - Upload PDF contracts or legal documents
    - Ask specific questions about clauses or terms
    - The system will find relevant sections
    
    **For General Questions:**
    - Ask about Indian legal concepts, IPC sections
    - Be specific about jurisdictions (state/city)
    - Specify the legal domain (criminal/civil/etc.)
    """)