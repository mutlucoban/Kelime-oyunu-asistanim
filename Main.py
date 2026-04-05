import streamlit as st
import pandas as pd
from collections import Counter

# --- HARF PUANLARI ---
PUANLAR = {'A':1,'B':3,'C':4,'Ç':4,'D':3,'E':1,'F':7,'G':5,'Ğ':8,'H':3,'I':2,'İ':1,'J':10,'K':1,'L':1,'M':2,'N':1,'O':2,'Ö':7,'P':5,'R':1,'S':2,'Ş':4,'T':1,'U':2,'Ü':3,'V':7,'Y':3,'Z':4,'?':0}

# --- KODUN İÇİNE GÖMÜLÜ SÖZLÜK (Özet Liste) ---
# Buraya en popüler kelimeleri ekledim, böylece dış dosyaya gerek kalmaz.
SABIT_SOZLUK = [
    "ABİDE", "ADALET", "ADRES", "AKŞAM", "ALTYAPI", "ANNE", "ARABA", "ASİSTAN", "AYNA",
    "BABA", "BAHÇE", "BALIK", "BARIŞ", "BAŞARI", "BAYRAM", "BEBEK", "BİLGİ", "BİSİKLET",
    "CAMİ", "CANLI", "CEVAP", "CÜMLE", "ÇALIŞKAN", "ÇAYIR", "ÇEVRE", "ÇİÇEK", "ÇOCUK",
    "DAĞLAR", "DENİZ", "DEFTER", "DEĞER", "DERECE", "DİKKAT", "DÜNYA", "DÜZEN",
    "EKMEK", "ELBİSE", "ELMA", "EMEK", "ENERJİ", "ERDEM", "ESNEK", "EŞYA",
    "FABRİKA", "FAALİYET", "FARK", "FATURA", "FAYDA", "FENER", "FIRÇA", "FİKİR",
    "GAZETE", "GECE", "GELENEK", "GELİŞİM", "GERÇEK", "GÖRÜŞ", "GÜNEŞ", "GÜVEN",
    "HABER", "HAFIZA", "HAKİKAT", "HALK", "HAREKET", "HAYAT", "HEDEF", "HUZUR",
    "IŞIK", "IRMAK", "ISPANAK", "ISSIZ", "İBADET", "İLAÇ", "İLETİŞİM", "İNSAN", "İSİM",
    "JALE", "JETON", "JİLET", "JOKER", "JURNAL", "JÜPİTER", "JÜRİ",
    "KADER", "KAĞIT", "KALEM", "KAPI", "KARAR", "KİTAP", "KONU", "KORKU", "KÜLTÜR",
    "LAMBA", "LEZZET", "LİMAN", "LİSTE", "LOKUM", "LÜTFEN", "LÜKS",
    "MACERA", "MAKİNE", "MANZARA", "MASA", "MEYVE", "MİLLET", "MÜZİK",
    "NEFES", "NESİL", "NEZAKET", "NİMET", "NOKTA", "NORMAL", "NUMARA",
    "OKUL", "ORMAN", "ORTAK", "OYUN", "ÖĞRENCİ", "ÖNEM", "ÖRNEK", "ÖZGÜR",
    "PARA", "PARK", "PAZAR", "PEYNİR", "PLAN", "PROJE", "PUSULA",
    "RADYO", "RAHAT", "REHBER", "RESİM", "ROBOT", "ROMAN", "RÜZGAR",
    "SABAH", "SAĞLIK", "SANAT", "SAYGI", "SEVGİ", "SİSTEM", "SOKAK", "SÖZLÜK",
    "ŞEHİR", "ŞEKER", "ŞİİR", "ŞİRKET", "ŞOFÖR", "ŞUBAT", "ŞÜPHE",
    "TABAK", "TAKIM", "TARİH", "TATİL", "TEKNİK", "TEMİZ", "TOPLUM", "TÜRKİYE",
    "UYGULAMA", "UZMAN", "ÜCRETSİZ", "ÜLKE", "ÜNİVERSİTE", "ÜRETİM", "ÜYELİK",
    "VAKİT", "VATAN", "VİCDAN", "VİDEO", "VİTRİN", "VÜCUT",
    "YAĞMUR", "YARDIM", "YAŞAM", "YAZAR", "YEMEK", "YENİ", "YILDIZ", "YOLCULUK",
    "ZAMAN", "ZEKA", "ZENGİN", "ZEYTİN", "ZİHNİYET", "ZİNCİR", "ZİYARET"
    # Buraya binlerce kelime daha eklenebilir...
]

st.set_page_config(page_title="Scrabble Asistanım", layout="wide")

# --- MANTIK ---
def can_word_be_formed(word, rack):
    word_count = Counter(word)
    rack_count = Counter(rack)
    jokers = rack_count.get('?', 0)
    missing = 0
    for char, count in word_count.items():
        if rack_count[char] < count:
            missing += (count - rack_count[char])
    return missing <= jokers

# --- ARAYÜZ ---
st.title("🧩 Scrabble Strateji Paneli")
eldeki_harfler = st.sidebar.text_input("Eldeki Harfler:", "").upper()
is_first_move = st.sidebar.checkbox("İlk Hamle (Merkez Yıldız)", value=True)

if st.button("🚀 Hesapla"):
    if not eldeki_harfler:
        st.warning("Harfleri girin.")
    else:
        sonuclar = []
        for kelime in SABIT_SOZLUK:
            if can_word_be_formed(kelime, eldeki_harfler):
                p = sum(PUANLAR.get(h,0) for h in kelime)
                if is_first_move: p *= 2 # Merkez kuralı
                if len(kelime) == 7: p += 30 # Bingo kuralı
                sonuclar.append({"Kelime": kelime, "Puan": p})
        
        if sonuclar:
            st.table(pd.DataFrame(sonuclar).sort_values("Puan", ascending=False).head(10))
        else:
            st.error("Kelime bulunamadı.")
