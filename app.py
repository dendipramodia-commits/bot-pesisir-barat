import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asisten Digital Pesisir Barat", page_icon="🌊")
st.title("🌊 Asisten Digital Pesisir Barat")

# Masukkan API KEY baru kamu di sini
API_KEY = "AIzaSyD7utq2kgVR2yZioUm0RVC0ZBjvNsj5yLE" 
genai.configure(api_key=API_KEY)

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
            # Gunakan nama model tanpa awalan 'models/'
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Kamu adalah asisten Pesisir Barat. Jawab: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {str(e)}")
