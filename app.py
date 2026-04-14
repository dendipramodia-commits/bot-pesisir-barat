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
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)

    # --- JURUS DETEKSI OTOMATIS ---
    if "active_model" not in st.session_state:
        # Mencari model yang tersedia di API Key kamu
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Pilih yang paling canggih (biasanya urutan pertama atau kedua)
        if models:
            st.session_state.active_model = models[0]
        else:
            st.session_state.active_model = "models/gemini-1.5-flash"

    model = genai.GenerativeModel(st.session_state.active_model)

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
            instruksi = f"Kamu adalah KruiBot, asisten Pesisir Barat yang ramah. Jawab dengan sopan: {prompt}"
            response = model.generate_content(instruksi)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Koneksi sedang disesuaikan. Silakan refresh halaman. (Detail: {str(e)})")
