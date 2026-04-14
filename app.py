import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="Asisten Digital Pesisir Barat", page_icon="🌊")
st.title("🌊 Asisten Digital Pesisir Barat")
st.markdown("---")

# 2. Setup API - Pastikan API KEY baru kamu sudah benar di sini
API_KEY = "AIzaSyD7utq2kgVR2yZioUm0RVC0ZBjvNsj5yLE"
genai.configure(api_key=API_KEY)

# 3. Inisialisasi Riwayat Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input User
if prompt := st.chat_input("Tanya seputar Pesisir Barat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # MENGGUNAKAN NAMA MODEL VERSI LENGKAP AGAR TIDAK 404
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
            
            instruksi = (
                "Kamu adalah asisten resmi Kabupaten Pesisir Barat, Lampung. "
                "Jawablah dengan ramah dan informatif. "
                f"Pertanyaan: {prompt}"
            )
            
            response = model.generate_content(instruksi)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
        except Exception as e:
            # Jika masih error, kita tampilkan detailnya untuk analisa
            st.error(f"Catatan sistem: {str(e)}")
