import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="Asisten Digital Pesisir Barat", page_icon="🌊")
st.title("🌊 Asisten Digital Pesisir Barat")
st.markdown("---")

# 2. Setup API
API_KEY = "AiZaSyCXEjc-Ca0T_kw4d05vrWMIJdG4JJGE7XI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Bank Data (Context) - Di sinilah "Otak" chatbot kamu berada
context = """
Kamu adalah 'KruiBot', asisten digital resmi Kabupaten Pesisir Barat, Lampung. 
Tugasmu adalah memberikan informasi yang akurat, ramah, dan mempromosikan pariwisata serta layanan publik.

DATA PENTING PESISIR BARAT:
- Ibu Kota: Pasar Krui.
- Wisata Pantai: Pantai Tanjung Setia (Terkenal untuk Surfing dunia), Pantai Labuhan Jukung (Sunset), Pantai Mandiri.
- Wisata Alam: Pulau Pisang (Lumba-lumba & Kain Tapis), Gua Matu (Wisata Religi/Mistik), TNBBS (Taman Nasional).
- Budaya & Oleh-oleh: Kain Tapis, Kerajinan Damar, Ikan Blue Marlin (Tuhuk).
- Makanan Khas: Taboh Ikan, Pandap, Sambol Seruit.
- Event Utama: WSL World Surf League (Krui Pro) yang biasanya diadakan setiap pertengahan tahun.
- Kantor Penting: Komplek Perkantoran Padang Haluan (Pusat Pemerintahan).

ATURAN MENJAWAB:
- Gunakan bahasa Indonesia yang sopan dan sedikit santai (seperti warga lokal yang ramah).
- Jika ada pertanyaan yang tidak kamu ketahui datanya, arahkan warga untuk datang ke kantor dinas terkait di Komplek Perkantoran Padang Haluan.
- Selalu promosikan slogan 'Pesisir Barat, Negeri Para Sai Batin dan Para Ulama'.
"""

# 4. Logika Chat
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
            # Menggabungkan Context dan Pertanyaan User
            full_prompt = f"{context}\n\nPertanyaan Pengguna: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Waduh, koneksi ke server pusat sedang sibuk. Coba sebentar lagi ya!")
