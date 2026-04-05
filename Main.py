import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scrabble Strateji Pro", layout="wide")

# --- STANDART TÜRKÇE HARF SETİ ---
if 'harfler' not in st.session_state:
    st.session_state.harfler = {
        'A': [12, 1], 'B': [2, 3], 'C': [2, 4], 'Ç': [2, 4], 'D': [2, 3],
        'E': [8, 1], 'F': [1, 7], 'G': [1, 5], 'Ğ': [1, 8], 'H': [3, 3],
        'I': [4, 2], 'İ': [7, 1], 'J': [1, 10], 'K': [7, 1], 'L': [7, 1],
        'M': [4, 2], 'N': [5, 1], 'O': [3, 2], 'Ö': [1, 7], 'P': [1, 5],
        'R': [6, 1], 'S': [3, 2], 'Ş': [2, 4], 'T': [5, 1], 'U': [3, 2],
        'Ü': [2, 3], 'V': [1, 7], 'Y': [2, 3], 'Z': [1, 4], 'Joker': [2, 0]
    }

# --- YAN PANEL: AYARLAR ---
st.sidebar.header("⚙️ Oyun Ayarları")
st.sidebar.subheader("Özel Bonuslar")
ozel_yildiz_konum = st.sidebar.text_input("25 Puanlık Yıldız (Örn: A5)", "C10").upper()
bingo_bonusu = st.sidebar.number_input("7 Harf (Bingo) Bonusu", value=30)
merkez_yildiz_carpan = st.sidebar.number_input("Merkez Yıldız Çarpanı", value=2)

st.sidebar.subheader("Harf Düzenle (Adet/Puan)")
for h, deger in st.session_state.harfler.items():
    col1, col2 = st.sidebar.columns(2)
    st.session_state.harfler[h][0] = col1.number_input(f"{h} Adet", value=deger[0], key=f"a_{h}")
    st.session_state.harfler[h][1] = col2.number_input(f"{h} Puan", value=deger[1], key=f"p_{h}")

# --- ANA EKRAN: TAHTA VE GİRİŞ ---
st.title("🧩 Scrabble Master: Strateji Paneli")

# 15x15 Tahta Verisi
if 'board' not in st.session_state:
    st.session_state.board = pd.DataFrame("", index=range(1, 16), columns=[chr(i) for i in range(65, 80)])

st.subheader("Tahta Durumu")
st.info("Tahtadaki harfleri ilgili hücrelere yazın. Boş bırakılan yerler oyun alanıdır.")
edited_board = st.data_editor(st.session_state.board, use_container_width=True)

st.divider()

col_el1, col_el2 = st.columns([2, 1])
with col_el1:
    eldeki_harfler = st.text_input("Elinizdeki 7 Harfi Girin (Joker için ? kullanın):", "").upper()
with col_el2:
    if st.button("🚀 EN İYİ HAMLEYİ HESAPLA", use_container_width=True):
        # HESAPLAMA MANTIĞI (Simülasyon)
        st.subheader("🔍 Önerilen Hamleler")
        # Burada senin kuralın: (Puan * Çarpan) + 25 uygulanacak
        st.write(f"1. **{ozel_yildiz_konum}** bölgesini kullanarak 'ZEYTİN' yaz: **84 Puan**")
        st.caption(f"Hesaplama: (Kelime x {merkez_yildiz_carpan}) + 25 Özel Yıldız + {bingo_bonusu} Bingo")
        
        st.warning("⚠️ RAKİP ANALİZİ: Bu hamle sonrası rakibin 'J' harfi ile 3W karesine ulaşma ihtimali %15.")

# --- TORBA TAKİBİ ---
st.subheader("📦 Torbada Kalan Harfler (Tahmini)")
# Tahtadaki ve eldeki harfleri toplam setten çıkarıp buraya listeleyeceğiz.
st.write("Oyun ilerledikçe burası rakibinizin elinde olabilecek harfleri gösterecek.")
