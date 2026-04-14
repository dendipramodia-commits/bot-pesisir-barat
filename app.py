import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

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
    # 1. Ambil API Key
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    
    # 2. PAKSA MENGGUNAKAN API VERSION V1 (Menghindari 404 v1beta)
    options = client_options.ClientOptions(api_endpoint="generativelanguage.googleapis.com")
    genai.configure(api_key=API_KEY, client_options=options)

    # 3. Pakai model 1.5 Flash
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input User
    if prompt := st.chat_input("Tanya seputar Pesisir Barat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Tambahkan instruksi kepribadian
            instruksi = f"Kamu adalah KruiBot, asisten ramah ahli Pesisir Barat. Jawab dengan sopan: {prompt}"
            
            # Eksekusi dengan penanganan error quota (429)
            try:
                response = model.generate_content(instruksi)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ Antrean penuh. Tunggu 10 detik dan coba lagi ya!")
                else:
                    st.error(f"Terjadi kesalahan saat menjawab: {str(e)}")

except Exception as e:
    st.error(f"Gagal menghubungkan ke server Google: {str(e)}")
