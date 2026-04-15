import streamlit as st
import google.generativeai as genai

# 1. Judul dan Tampilan Browser
st.set_page_config(page_title="KruiBot - Pesisir Barat Lampung", page_icon="🌊")

# --- SIDEBAR (Menu Samping) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Logo_Kabupaten_Pesisir_Barat.png/480px-Logo_Kabupaten_Pesisir_Barat.png", width=100)
    st.title("Tentang KruiBot")
    st.info("Asisten digital khusus Kabupaten Pesisir Barat, Lampung. Tabik Pun!")
    if st.button("Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

# --- TAMPILAN UTAMA ---
st.title("🌊 KruiBot")
st.caption("Pusat Informasi Wisata & Budaya Pesisir Barat, Lampung")

try:
    # Mengambil API KEY dari Secrets
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Pilih model yang paling stabil
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Menampilkan sejarah percakapan
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input dari User
    if prompt := st.chat_input("Tanya apa saja tentang Krui/Pesisir Barat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # --- INI ADALAH 'OTAK' KRUIBOT (PROMPT ENGINEERING) ---
            instruksi_ketat = (
                f"Sapa dengan 'Tabik Pun'. Kamu adalah KruiBot, ahli informasi Kabupaten Pesisir Barat, Lampung, Indonesia. "
                f"INGAT: Pesisir Barat yang dimaksud adalah di Lampung, bukan di Amerika Serikat. "
                f"Fokus pada info: Pantai Tanjung Setia, Labuhan Jukung, Pulau Pisang, surfing, "
                f"adat Sai Batin, kuliner Gulai Taboh, dan wilayah Krui sekitarnya. "
                f"Jika ditanya pantai, jangan sebut pantai di Amerika. "
                f"Pertanyaan User: {prompt}"
            )
            
            try:
                response = model.generate_content(instruksi_ketat)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ Google lagi ramai antrean. Tunggu 10 detik lalu coba lagi ya!")
                else:
                    st.error(f"Ada kendala: {str(e)}")

except Exception as e:
    st.error(f"Aplikasi belum siap: {str(e)}")
