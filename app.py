import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Asisten Digital Pesisir Barat", page_icon="🌊")
st.title("🌊 Asisten Digital Pesisir Barat")

# Ambil API Key dari Secrets (Saran saya tetap pakai Secrets agar aman)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Paksa konfigurasi menggunakan API version 'v1'
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("API Key belum terpasang di Secrets!")

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
        try:
            # Gunakan penamaan model yang paling lengkap
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
            
            response = model.generate_content(f"Kamu asisten Pesisir Barat. Jawab: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Masih ada kendala teknis: {str(e)}")
