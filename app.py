import streamlit as st
import pandas as pd

# Sayfa Konfigürasyonu (Mobil Uyumlu)
st.set_page_config(
    page_title="Dejenere Amerikan Yazboz",
    page_icon="🃏",
    layout="centered"
)

# Stil Özelleştirmeleri
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    h1 { text-align: center; color: #E63946; font-size: 22pt !important; margin-bottom: 5px; }
    h3 { text-align: center; color: #6C757D; font-size: 12pt !important; margin-bottom: 25px; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 16 Turun Listesi
ROUNDS = [
    "1. 4'lü Küt + 3'lü Seri", "2. 3x3'lü Küt", "3. 2x3'lü Seri + 2x3'lü Küt", "4. 3-3'lü Seri",
    "5. 2x3'lü Seri + 1x3'lü Küt", "6. 4'lü Küt", "7. 4'lü Seri", "8. 4'lü Karışık",
    "9. 4'lü Seri + 3'lü Küt", "10. 2x4'lü Seri", "11. 2x4'lü Küt", "12. 5'li Seri",
    "13. 6'lı Seri", "14. 5'li Seri + 3'lü Küt", "15. 4 Çift + 3'lü Seri veya Küt", "16. Elden Bitme"
]

if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'completed_rounds' not in st.session_state:
    st.session_state.completed_rounds = [] 
if 'round_details' not in st.session_state:
    st.session_state.round_details = {} # Tur detaylarını (dağıtan/söyleyen) tutacak

st.title("🃏 Dejenere Amerikan")
st.markdown("### Akıllı Gelişmiş Skor Tabelası")

# --- AŞAMA 1: 5 OYUNCULU GİRİŞ EKRANI ---
if not st.session_state.initialized:
    st.subheader("👥 Oyuncu İsimlerini Girin")
    
    p1 = st.text_input("1. Oyuncu", "Mecit")
    p2 = st.text_input("2. Oyuncu", "Sermin")
    p3 = st.text_input("3. Oyuncu", "Oyuncu 3")
    p4 = st.text_input("4. Oyuncu", "Oyuncu 4")
    p5 = st.text_input("5. Oyuncu", "Oyuncu 5")
    
    players = [p.strip() for p in [p1, p2, p3, p4, p5] if p.strip()]
    
    if st.button("Oyunu Başlat 🚀"):
        if len(players) < 2:
            st.error("Lütfen en az 2 oyuncu girin!")
        else:
            st.session_state.players = players
            st.session_state.scores_df = pd.DataFrame(0, index=ROUNDS, columns=players)
            st.session_state.initialized = True
            st.rerun()

# --- AŞAMA 2: SKOR GİRİŞ VE CANLI TABLO ---
else:
    players = st.session_state.players
    
    # Tüm turlar oynandıysa oyunu bitir
    if len(st.session_state.completed_rounds) >= len(ROUNDS):
        st.balloons()
        st.success("🎉 TÜM TURLAR TAMAMLANDI! 🎉")
        totals = st.session_state.scores_df.sum()
        winner = totals.idxmin()
        st.subheader(f"🏆 KAZANAN: {winner} ({totals[winner]} Puan)")
        st.dataframe(st.session_state.scores_df, use_container_width=True)
        if st.button("Yeni Oyun Başlat 🔄"):
            st.session_state.clear()
            st.rerun()
            
    else:
        # Üst Panel: Tur Seçimi ve Sorumlular
        st.subheader("🎯 Tur Detayları")
        available_rounds = [r for r in ROUNDS if r not in st.session_state.completed_rounds]
        
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            selected_round = st.selectbox("Oynanan Tur", available_rounds)
        with col_r2:
            dealer = st.selectbox("Kağıdı Dağıtan 🃏", players, key=f"dealer_{selected_round}")
        with col_r3:
            announcer = st.selectbox("Oyunu Biten/Söyleyen 🗣️", players, key=f"announcer_{selected_round}")
        
        st.markdown("---")
        st.subheader("✍️ Cezaları Girin")
        st.info("🎙️ Skor kutularına tıklayıp telefon klavyenizdeki mikrofonla sayıları sesli söyleyebilirsiniz.")
        
        # Seçilen tur için skor giriş alanları
        round_inputs = {}
        cols = st.columns(len(players))
        
        for i, player in enumerate(players):
            with cols[i]:
                # Oyunu söyleyen kişinin kutusunu varsayılan olarak 0 yapalım (kolaylık olsun diye)
                default_val = 0 if player == announcer else 0
                score = st.number_input(f"{player}", min_value=0, max_value=500, value=default_val, step=1, key=f"score_{player}_{selected_round}")
                round_inputs[player] = score
                
        # Skor Kaydetme Butonu
        st.write("")
        if st.button(f"➡️ {selected_round} Skorlarını Kaydet"):
            for player, score in round_inputs.items():
                st.session_state.scores_df.at[selected_round, player] = score
            
            # Detayları kaydet
            st.session_state.round_details[selected_round] = {
                "Dağıtan": dealer,
                "Söyleyen": announcer
            }
            
            st.session_state.completed_rounds.append(selected_round)
            st.success(f"Kaydedildi! Dağıtan: {dealer} | Söyleyen: {announcer}")
            st.rerun()
            
        # --- CANLI HESAP TABLOSU ---
        st.markdown("---")
        st.subheader("📊 Genel Ceza Puanları (Kümülatif)")
        
        current_totals = st.session_state.scores_df.sum()
        summary_df = pd.DataFrame({
            "Bu Tur": [round_inputs.get(p, 0) for p in players],
            "Toplam Ceza": [current_totals[p] for p in players]
        }, index=players)
        
        st.table(summary_df)
        
        # Tüm tabloyu gösteren detay alanı
        with st.expander("📄 Yazboz Sayfasının Tamamını Gör (Oynanan ve Kalan Turlar)"):
            # Detaylı tablo için ekstra kolonlar eklenmiş bir kopya oluşturalım
            display_df = st.session_state.scores_df.copy()
            
            # Dağıtan ve Söyleyen bilgilerini tabloya ekle
            dealers_col = []
            announcers_col = []
            for r in ROUNDS:
                if r in st.session_state.round_details:
                    dealers_col.append(st.session_state.round_details[r]["Dağıtan"])
                    announcers_col.append(st.session_state.round_details[r]["Söyleyen"])
                else:
                    dealers_col.append("-")
                    announcers_col.append("-")
                    
            display_df.insert(0, "Oyunu Biten", announcers_col)
            display_df.insert(0, "Kağıt Dağıtan", dealers_col)
            
            st.dataframe(display_df, use_container_width=True)
            
            if st.session_state.completed_rounds:
                if st.button("⚠️ En Son Girilen Turu İptal Et / Geri Al"):
                    last_round = st.session_state.completed_rounds.pop()
                    st.session_state.scores_df.loc[last_round] = 0
                    if last_round in st.session_state.round_details:
                        del st.session_state.round_details[last_round]
                    st.rerun()
