import streamlit as st
import google.generativeai as genai

# Konfigurasi halaman
st.set_page_config(page_title="Chatbot Pesisir Barat", page_icon="🌊")
st.title("🌊 Asisten Digital Pesisir Barat")

# Setup API
API_KEY = "AiZaSyCXEjc-Ca0T_kw4d05vrWMIJdG4JJGE7XI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input pengguna
if prompt := st.chat_input("Tanyakan sesuatu tentang Pesisir Barat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instruksi sederhana
            response = model.generate_content(f"Kamu adalah asisten informasi Pesisir Barat. Jawab pertanyaan ini: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Aduh, ada gangguan koneksi. Coba lagi ya! (Pesan: {e})")
