import streamlit as st
from response_generate_paris_curated import qa_chain

# --------------------------
# 🌍 Page Configuration
# --------------------------
st.set_page_config(
    page_title="TravelMate ✈️ | Your Smart Travel Companion",
    page_icon="🌍",
    layout="centered",
)

# --------------------------
# ✨ Custom Styling
# --------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #1e3c72, #2a5298);
    font-family: 'Poppins', sans-serif;
    color: white;
}
.chat-box {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    margin-top: 10px;
}
input, textarea {
    border-radius: 10px !important;
}
.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.15);
    color: white;
}
.stTextArea > div > div > textarea {
    background-color: rgba(255,255,255,0.15);
    color: rgb(97 77 243);
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------------
# 🧭 Header Section
# --------------------------
st.markdown("<h1 style='text-align:center;'>🌍 TravelMate</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Your personal travel assistant — Ask anything about destinations, attractions, or plans!</p>", unsafe_allow_html=True)
st.divider()

# --------------------------
# 🧳 Chat Interface
# --------------------------
query = st.text_input("✈️ Where do you want to explore today?", placeholder="e.g., What are the best places to visit in Paris?")

if st.button("Ask TravelMate 🚀", use_container_width=True):
    if query.strip() == "":
        st.warning("Please enter a question before asking!")
    else:
        with st.spinner("Thinking... exploring the world for you 🌏"):
            result = qa_chain.invoke({"query": query})

        st.success("Here's what I found!")
        st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
        st.markdown(f"**🧭 Query:** {query}")
        st.markdown(f"**💬 Answer:** {result['result']}")
        st.markdown("</div>", unsafe_allow_html=True)

        # --------------------------
        # 📚 Sources Section
        # --------------------------
        with st.expander("📖 Sources Used"):
            for doc in result.get('source_documents', []):
                source_file = doc.metadata.get('source', 'Unknown').split('/')[-1]
                st.markdown(f"**File:** `{source_file}`")
                st.markdown(f"📝 **Excerpt:** {doc.page_content[:250]}...\n")

# --------------------------
# 🏝️ Footer
# --------------------------
st.divider()
st.markdown("""
<p style='text-align:center; color: rgb(97 77 243); font-size: 14px;'>
Made with ❤️ for explorers by <b>Rahul Dewani</b> <br>
<small>Embrace the journey. Discover more.</small>
</p>
""", unsafe_allow_html=True)
