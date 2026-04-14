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

    # --- LOGIKA DARURAT: CARI MODEL OTOMATIS ---
    if "model_name" not in st.session_state:
        try:
            # Ambil semua model yang bisa generate content
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Prioritaskan model flash, jika tidak ada pakai apa saja yang tersedia
            flash_models = [m for m in available_models if "flash" in m]
            st.session_state.model_name = flash_models[0] if flash_models else available_models[0]
        except:
            st.session_state.model_name = "models/gemini-1.5-flash"

    model = genai.GenerativeModel(st.session_state.model_name)

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
                response = model.generate_content(f"Jawab sebagai asisten Pesisir Barat: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ Kuota penuh. Tunggu sebentar ya!")
                else:
                    st.error(f"Error Model ({st.session_state.model_name}): {str(e)}")

except Exception as e:
    st.error(f"Koneksi Gagal: {str(e)}")
