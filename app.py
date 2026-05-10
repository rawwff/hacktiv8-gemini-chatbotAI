import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(page_title="Sobat Liburan AI", page_icon="🏖️", layout="centered")

st.title("🏖️ Sobat Liburan: Travel Assistant AI")
st.write("Halo! Aku asisten liburan pribadimu. Mau cari rekomendasi wisata, kuliner, atau bikin itinerary? Tanya aja!")

# ==========================================
# 2. KONFIGURASI API KEY DI SIDEBAR
# ==========================================
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Masukkan Gemini API Key:", type="password")
    st.markdown("[Dapatkan API Key di sini](https://aistudio.google.com/app/apikey)")

# Cek apakah API Key sudah dimasukkan
if api_key:
    # Konfigurasi library Gemini
    genai.configure(api_key=api_key)

    # ==========================================
# 3. KONFIGURASI MODEL & PARAMETER KREATIF
    # ==========================================
    # Mengatur parameter kreativitas (seperti yang dibahas di soal kuis)
    generation_config = {
      "temperature": 0.7, # Sedikit tinggi agar rekomendasi liburan lebih kreatif dan bervariasi
      "top_p": 0.9,
      "max_output_tokens": 1000,
    }

    # Menggunakan System Prompt untuk mengatur Persona/Gaya Bahasa
    system_instruction = """
    Kamu adalah 'Sobat Liburan', asisten travel cerdas yang fokus pada pariwisata di Indonesia. 
    Gaya bahasamu santai, ramah, asyik, dan menggunakan kata ganti 'Aku' dan 'Kamu'. 
    Selalu berikan rekomendasi tempat, kuliner khas, dan tips praktis untuk liburan.
    Jika ditanya di luar topik liburan, arahkan dengan sopan kembali ke topik wisata.
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    # ==========================================
    # 4. INISIALISASI MEMORI (st.session_state)
    # ==========================================
    # Menggunakan st.session_state untuk menyimpan riwayat chat
    if "chat_session" not in st.session_state:
        # Memulai sesi chat baru dengan Gemini yang mendukung history
        st.session_state.chat_session = model.start_chat(history=[])

    # Tampilkan riwayat chat sebelumnya di layar
    for message in st.session_state.chat_session.history:
        # Ubah label 'model' dari Gemini menjadi 'assistant' untuk UI Streamlit
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # ==========================================
    # 5. INPUT PENGGUNA & GENERASI RESPONS
    # ==========================================
    # Menggunakan st.chat_input untuk input text interaktif
    if prompt := st.chat_input("Mau liburan ke mana hari ini? (Misal: Rekomendasi kuliner malam di Bandung)"):
        
        # Tampilkan pesan dari user
        with st.chat_message("user"):
            st.markdown(prompt)

        # Proses pesan ke Gemini API dan tampilkan animasi loading
        with st.chat_message("assistant"):
            with st.spinner("Sedang mencari rekomendasi terbaik..."):
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)

else:
    st.info("Silakan masukkan API Key di sebelah kiri untuk mulai mengobrol.")