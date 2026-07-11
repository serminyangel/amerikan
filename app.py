import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dejenere Amerikan Yazboz", page_icon="🃏", layout="centered")

st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    h1 { text-align: center; color: #E63946; font-size: 22pt !important; }
    h3 { text-align: center; color: #6C757D; font-size: 12pt !important; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

ROUNDS = [
    "1. 4'lü Küt + 3'lü Seri", "2. 3x3'lü Küt", "3. 2x3'lü Seri + 2x3'lü Küt", "4. 3-3'lü Seri",
    "5. 2x3'lü Seri + 1x3'lü Küt", "6. 4'lü Küt", "7. 4'lü Seri", "8. 4'lü Karışık",
    "9. 4'lü Seri + 3'lü Küt", "10. 2x4'lü Seri", "11. 2x4'lü Küt", "12. 5'li Seri",
    "13. 6'lı Seri", "14. 5'li Seri + 3'lü Küt", "15. 4 Çift + 3'lü Seri veya Küt", "16. Elden Bitme"
]

if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'current_round_idx' not in st.session_state:
    st.session_state.current_round_idx = 0

st.title("🃏 Dejenere Amerikan")
st.markdown("### Dijital Skor Tabelası & Yazboz")

if not st.session_state.initialized:
    st.subheader("👥 Oyuncu İsimlerini Girin")
    p1 = st.text_input("1. Oyuncu", "Mecit")
    p2 = st.text_input("2. Oyuncu", "Sermin")
    p3 = st.text_input("3. Oyuncu", "Oyuncu 3")
    p4 = st.text_input("4. Oyuncu", "Oyuncu 4")
    
    players = [p.strip() for p in [p1, p2, p3, p4] if p.strip()]
    if st.button("Oyunu Başlat 🚀"):
        if len(players) < 2:
            st.error("Lütfen en az 2 oyuncu girin!")
        else:
            st.session_state.players = players
            st.session_state.scores_df = pd.DataFrame(0, index=ROUNDS, columns=players)
            st.session_state.initialized = True
            st.rerun()
else:
    players = st.session_state.players
    current_idx = st.session_state.current_round_idx
    
    if current_idx >= len(ROUNDS):
        st.balloons()
        st.success("🎉 OYUN BİTTİ! 🎉")
        totals = st.session_state.scores_df.sum()
        winner = totals.idxmin()
        st.subheader(f"🏆 KAZANAN: {winner} ({totals[winner]} Puan)")
        st.dataframe(st.session_state.scores_df.copy(), use_container_width=True)
        if st.button("Yeni Oyun Başlat 🔄"):
            st.session_state.clear()
            st.rerun()
    else:
        current_round = ROUNDS[current_idx]
        st.info(f"📋 ŞİMDİKİ TUR: {current_round}")
        
        round_inputs = {}
        cols = st.columns(len(players))
        for i, player in enumerate(players):
            with cols[i]:
                score = st.number_input(f"{player}", min_value=0, max_value=500, value=0, step=1, key=f"p_{player}_{current_idx}")
                round_inputs[player] = score
                
        st.write("")
        btn_col1, btn_col2 = st.columns([2, 1])
        with btn_col1:
            if st.button("Skorları Kaydet ve İlerle ➡️"):
                for player, score in round_inputs.items():
                    st.session_state.scores_df.at[current_round, player] = score
                st.session_state.current_round_idx += 1
                st.rerun()
        with btn_col2:
            if current_idx > 0:
                if st.button("Geri Al ↩️"):
                    st.session_state.current_round_idx -= 1
                    st.rerun()
                    
        st.markdown("---")
        st.subheader("📊 Canlı Kümülatif Skorlar")
        cumulative_totals = st.session_state.scores_df.iloc[:current_idx].sum() + pd.Series(round_inputs)
        summary_df = pd.DataFrame({"Bu Tur": [round_inputs[p] for p in players], "Toplam Ceza": [cumulative_totals[p] for p in players]}, index=players)
        st.table(summary_df)