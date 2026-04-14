import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KruiBot - Pesisir Barat", page_icon="🌊")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Logo_Kabupaten_Pesisir_Barat.png/480px-Logo_Kabupaten_Pesisir_Barat.png", width=100)
    st.title("Tentang KruiBot")
    st.info("Asisten digital Pesisir Barat. Tabik Pun!")
    if st.button("Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

st.title("🌊 KruiBot")
st.caption("Negeri Para Sai Batin dan Para Ulama")

try:
    # 1. Pastikan API Key benar
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)

    # 2. PAKSA pakai Gemini 1.5 Flash (Kuota lebih banyak)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input User
    if prompt := st.chat_input("Tanya seputar Pesisir Barat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Tambahkan instruksi agar bot ramah
            instruksi = f"Kamu adalah KruiBot, asisten ramah ahli Pesisir Barat. Jawab dengan sopan: {prompt}"
            response = model.generate_content(instruksi)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    error_msg = str(e)
    if "429" in error_msg:
        st.warning("⚠️ Server Google sedang sibuk (limit tercapai). Tunggu 10 detik lalu coba lagi ya!")
    else:
        st.error(f"Ada kendala: {error_msg}")
