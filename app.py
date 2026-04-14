import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan Utama
st.set_page_config(page_title="KruiBot - Pesisir Barat", page_icon="🌊", layout="wide")

# --- SIDEBAR (Menu Samping) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Logo_Kabupaten_Pesisir_Barat.png/480px-Logo_Kabupaten_Pesisir_Barat.png", width=100)
    st.title("Tentang KruiBot")
    st.info("""
    KruiBot adalah asisten digital pintar untuk wilayah Kabupaten Pesisir Barat. 
    Dapatkan informasi tentang:
    * 🏄‍♂️ Destinasi Wisata & Surfing
    * 🍲 Kuliner Khas (Gulai Taboh, Pandap)
    * 🏺 Budaya & Adat Sai Batin
    * 🏢 Layanan Publik
    """)
    if st.button("Bersihkan Chat"):
        st.session_state.messages = []
        st.rerun()

# --- HEADER UTAMA ---
st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", use_column_width=True)
st.title("🌊 KruiBot: Asisten Digital Pesisir Barat")
st.caption("Negeri Para Sai Batin dan Para Ulama")

# --- SETUP AI ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Menampilkan riwayat chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input User
    if prompt := st.chat_input("Tanya seputar Pesisir Barat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Memberikan instruksi kepribadian (Prompt Engineering)
            instruksi = (
                "Kamu adalah KruiBot, asisten ramah yang ahli tentang Kabupaten Pesisir Barat, Lampung. "
                "Gunakan gaya bahasa sopan dan sesekali gunakan istilah lokal seperti 'Tabik Pun'. "
                "Berikan jawaban yang informatif tentang wisata, budaya, dan sejarah Krui. "
                f"Pertanyaan: {prompt}"
            )
            response = model.generate_content(instruksi)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Koneksi terputus: {e}")
