import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="Asisten Digital Pesisir Barat", page_icon="🌊")
st.title("🌊 Asisten Digital Pesisir Barat")
st.markdown("---")

# 2. Setup API dengan Key Terbaru Kamu
API_KEY = "AIzaSyAY7qrjbmWmjAVghjWX97ApgsvM4ncNZIw" 
genai.configure(api_key=API_KEY)

# 3. Inisialisasi Riwayat Chat agar tidak hilang saat refresh
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan percakapan sebelumnya
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input Pertanyaan dari Pengguna
if prompt := st.chat_input("Tanya seputar Pesisir Barat (Krui)..."):
    # Simpan chat user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Proses Jawaban dari AI
    with st.chat_message("assistant"):
        try:
            # Gunakan instruksi khusus agar AI tahu dia adalah asisten Pesisir Barat
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            context = (
                "Kamu adalah asisten informasi resmi Kabupaten Pesisir Barat, Lampung. "
                "Berikan informasi tentang pariwisata (Tanjung Setia, Pulau Pisang), "
                "budaya, dan layanan publik dengan ramah. Slogan: Negeri Para Sai Batin dan Para Ulama. "
                f"Pertanyaan user: {prompt}"
            )
            
            response = model.generate_content(context)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
        except Exception as e:
            # Jika masih error, ini akan membantu kita mendeteksi masalahnya
            st.error(f"Aplikasi sedang sinkronisasi. Pesan: {str(e)}")
