import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Amerikan 5", page_icon="🃏", layout="centered")

# Google'dan aldığımız o asıl canlı URL
API_URL = "https://script.google.com/macros/s/AKfycbxZp2bpoN25mqjukeUehUcovMbeBi9nfEK2z4AsrqusFNOXsdWbRt1xkbG8V5zBZjBv/exec"
ADMIN_PIN = "1905"

st.title("🃏 Amerikan 5 Canlı Skor")
st.caption("Veriler canlı olarak Google Sheets'ten çekilmektedir.")

# 1. BÖLÜM: SKORLARI GETİRME VE GÖSTERME
def skorlari_getir():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

skorlar = skorlari_getir()

st.subheader("📊 Güncel Puan Durumu")

# Ekranı çirkinleştiren st.table yerine mobil uyumlu temiz kolon düzeni
if skorlar:
    for satir in skorlar:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"👤 **{satir.get('oyuncu', '---')}**")
        with col2:
            st.markdown(f"🔴 `{satir.get('skor', 0)} Puan`")
        st.write('<div style="margin: -5px 0;"></div>', unsafe_allow_html=True) # Hafif boşluk
else:
    st.info("Tablo boş veya skorlar şu an çekilemedi.")

# Yenile butonu
if st.button("🔄 Skorları Yenile", use_container_width=True):
    st.rerun()

st.divider()

# 2. BÖLÜM: ŞİFRELİ SKOR GİRİŞİ (Yöntem 2)
st.subheader("🔐 Yönetici Paneli")
sifre = st.text_input("Skor eklemek için PIN kodunu girin:", type="password")

if sifre == ADMIN_PIN:
    st.success("🔓 Yetki doğrulandı. Skor giriş formu aktif.")
    
    with st.form("skor_formu", clear_on_submit=True):
        oyuncu_adi = st.text_input("Oyuncu Adı:")
        ceza_puani = st.number_input("Eklenecek Ceza Puanı:", min_value=0, step=1, value=0)
        form_butonu = st.form_submit_button("Skoru Gönder", use_container_width=True)
        
        if form_butonu and oyuncu_adi:
            veri = {"oyuncu": oyuncu_adi, "skor": int(ceza_puani)}
            try:
                requests.post(API_URL, json=veri, timeout=5)
                st.success(f"✅ {oyuncu_adi} için skor başarıyla yazıldı!")
                st.rerun()
            except:
                st.error("Skor gönderilirken bir hata oluştu, interneti kontrol edin.")
