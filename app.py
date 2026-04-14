import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KruiBot", page_icon="🌊")
st.title("🌊 KruiBot")

# Ambil API Key dari Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # JURUS PAMUNGKAS: Cari model yang support secara otomatis
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Ambil yang terbaru (biasanya gemini-1.5-flash)
    target_model = available_models[0] if available_models else "models/gemini-pro"
    
    model = genai.GenerativeModel(target_model)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Tanya Pesisir Barat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Paksa instruksi di sini
            full_prompt = f"Kamu asisten Pesisir Barat. Jawab singkat: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Sistem sedang sinkronisasi. Detail: {str(e)}")
