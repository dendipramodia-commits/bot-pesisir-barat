import streamlit as st
import google.generativeai as genai

st.title("🌊 KruiBot")

# Ambil API Key (Pastikan sudah terisi di menu Secrets!)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # KITA PAKAI MODEL 'gemini-pro' KARENA PALING STABIL DI SEMUA VERSI
    model = genai.GenerativeModel('gemini-pro')

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for content in st.session_state.chat_history:
        with st.chat_message(content["role"]):
            st.markdown(content["text"])

    if prompt := st.chat_input("Tanya apa saja..."):
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "text": response.text})

except Exception as e:
    st.error(f"Pesan sistem: {str(e)}")
    st.info("Tips: Pastikan GOOGLE_API_KEY sudah benar di menu Settings > Secrets.")
