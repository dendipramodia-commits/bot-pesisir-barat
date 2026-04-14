import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="KruiBot - Pesisir Barat", page_icon="🌊")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Logo_Kabupaten_Pesisir_Barat.png/480px-Logo_Kabupaten_Pesisir_Barat.png", width=100)
    st.title("Tentang KruiBot")
    st.info("Asisten digital cerdas Kabupaten Pesisir Barat. Tabik Pun!")
    if st.button("Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

# --- HEADER ---
st.title("🌊 KruiBot")
st.caption("Negeri Para Sai Batin dan Para Ulama")

# --- PROSES AI ---
try:
    # Mengambil API KEY dari Secrets
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # KITA PAKAI GEMINI-PRO KARENA PALING STABIL DAN JARANG ERROR 404
    model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Tanya seputar Pesisir Barat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Tambahkan instruksi lokal
            full_prompt = f"Kamu adalah KruiBot, asisten Pesisir Barat yang ramah. Jawablah dengan sopan: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Maaf, ada kendala teknis: {str(e)}")
