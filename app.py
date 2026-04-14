import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="Asisten Digital Pesisir Barat", page_icon="🌊")
st.title("🌊 Asisten Digital Pesisir Barat")
st.markdown("---")

# 2. Setup API
API_KEY = "AiZaSyCXEjc-Ca0T_kw4d05vrWMIJdG4JJGE7XI"
genai.configure(api_key=API_KEY)

# 3. Inisialisasi Model & Riwayat Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input User
if prompt := st.chat_input("Tanya seputar Pesisir Barat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Kita pakai cara yang lebih stabil
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Gabungkan instruksi langsung di sini
            instruksi_lengkap = (
                "Kamu adalah asisten resmi Kabupaten Pesisir Barat, Lampung. "
                "Berikan informasi tentang wisata seperti Pantai Tanjung Setia, Pulau Pisang, "
                "dan budaya lokal dengan ramah. Slogan: Negeri Para Sai Batin dan Para Ulama. "
                f"Pertanyaan user: {prompt}"
            )
            
            response = model.generate_content(instruksi_lengkap)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("AI tidak memberikan jawaban, coba tanya lagi ya.")
                
        except Exception as e:
            # Menampilkan error asli supaya kita tahu masalahnya apa
            st.error(f"Maaf, ada gangguan teknis kecil: {str(e)}")
