import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Dasar
st.set_page_config(page_title="KruiBot - Pesisir Barat Lampung", page_icon="🌊")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Logo_Kabupaten_Pesisir_Barat.png/480px-Logo_Kabupaten_Pesisir_Barat.png", width=100)
    st.title("Tentang KruiBot")
    st.info("Asisten digital khusus Kabupaten Pesisir Barat, Lampung. Tabik Pun!")
    if st.button("Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

st.title("🌊 KruiBot")
st.caption("Pusat Informasi Wisata & Budaya Pesisir Barat, Lampung")

try:
    # Koneksi API
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # --- JURUS ANTI 404: CARI MODEL OTOMATIS ---
    if "model_aktif" not in st.session_state:
        # Mencari model yang tersedia di API Key kamu secara otomatis
        list_model = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Pilih yang paling baru (biasanya flash atau pro)
        st.session_state.model_aktif = list_model[0] if list_model else "models/gemini-pro"

    model = genai.GenerativeModel(st.session_state.model_aktif)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Tanya seputar Krui..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # INSTRUKSI AGAR TIDAK NYASAR KE AMERIKA
            konteks = (
                f"Sapa dengan 'Tabik Pun'. Kamu adalah KruiBot, asisten lokal Pesisir Barat, Lampung, Indonesia. "
                f"Fokus pada info Krui, Tanjung Setia, Pulau Pisang, dan budaya Lampung. "
                f"Jangan bahas Amerika. Pertanyaan: {prompt}"
            )
            
            try:
                response = model.generate_content(konteks)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ Kuota penuh, tunggu 10 detik ya!")
                else:
                    st.error(f"Maaf, ada kendala: {str(e)}")

except Exception as e:
    st.error(f"Sistem sedang sinkronisasi. Silakan refresh halaman dalam 10 detik. (Detail: {str(e)})")
