
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_adaptive_response

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    page_icon="🤖",
    layout="wide"
)

# Initialize RAG pipeline
if "rag" not in st.session_state:
    st.session_state.rag = LocalRAGPipeline()

# Sidebar
with st.sidebar:
    st.header("System Status")

    st.success("Gemini Connected")

    try:
        chunk_count = st.session_state.rag.collection.count()
        st.write(f"Indexed Chunks: {chunk_count}")
    except Exception:
        st.write("Indexed Chunks: 0")

    doc_count = len(list(Path("data").glob("*")))
    st.write(f"Knowledge Base Files: {doc_count}")

    st.divider()

    st.subheader("Technology Stack")
    st.write("• Gemini 2.5 Flash")
    st.write("• Gemini Embedding 001")
    st.write("• ChromaDB")
    st.write("• Streamlit")

# Main UI
st.title("🤖 Persona Adaptive Support Agent")

st.markdown(
    """
    Enter a customer support query below.
    The system will:
    1. Detect customer persona
    2. Retrieve relevant support documents
    3. Generate a persona-adaptive response
    4. Escalate to a human agent if required
    """
)

query = st.text_area(
    "Customer Message",
    height=150,
    placeholder="Describe your issue here..."
)

if st.button("Submit", use_container_width=True):

    if not query.strip():
        st.warning("Please enter a customer message.")
        st.stop()

    with st.spinner("Processing request..."):

        try:
            # Persona Classification
            persona = classify_customer_persona(query)

            # Retrieval
            ctx = st.session_state.rag.retrieve(query)

            # Response Generation
            result = generate_adaptive_response(
                query,
                persona["persona"],
                ctx
            )

            # Persona Section
            st.subheader("Detected Persona")

            persona_name = persona["persona"]

            if persona_name == "Technical Expert":
                st.info(f"👨‍💻 {persona_name}")

            elif persona_name == "Frustrated User":
                st.warning(f"😠 {persona_name}")

            else:
                st.success(f"💼 {persona_name}")

            st.json(persona)

            # Retrieved Sources Section
            st.subheader("Retrieved Sources")

            seen = set()

            for item in ctx:
                if item["source"] in seen:
                    continue

                seen.add(item["source"])

                score = round(item["score"], 3)

                st.write(
                    f"📄 {item['source']} | Similarity Score: {score}"
                )

            # Response Section
            st.subheader("Response")

            st.write(result["response"])

            # Escalation Section
            if result["escalated"]:
                st.error("Escalated to Human Support")

                st.subheader("Handoff Summary")

                st.code(
                    result["handoff_summary"],
                    language="json"
                )

        except Exception as e:
            st.error(f"Application Error: {str(e)}")

