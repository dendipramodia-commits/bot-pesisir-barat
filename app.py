import streamlit as st
import google.generativeai as genai

# Judul Aplikasi
st.set_page_config(page_title="Chatbot Pesisir Barat", page_icon="🌊")
st.title("🌊 Asisten Digital Pesisir Barat")

# API Key Kamu
API_KEY = "AiZaSyCXEjc-Ca0T_kw4d05vrWMIJdG4JJGE7XI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanyakan sesuatu tentang Pesisir Barat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        context = "Kamu adalah asisten resmi Pemkab Pesisir Barat. Jawablah dengan sangat sopan."
        response = model.generate_content(context + " Pertanyaan: " + prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
