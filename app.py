import streamlit as st
import streamlit.components.v1 as components

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Dejenere Amerikan Yazboz",
    page_icon="🃏",
    layout="centered"
)

# Stil Özelleştirmeleri
st.markdown("""
    <style>
    .main .block-container { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

# Sunucu uyku moduna karşı %100 bağışık, gücünü yerel hafızadan ve canlı tarayıcı senkronizasyonundan alan HTML5 Motoru
HTML_ENGINE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #ffffff; color: #31333F; margin: 0; padding: 10px;
        }
        .header { text-align: center; margin-bottom: 15px; }
        .title { color: #E63946; font-size: 24px; font-weight: bold; margin: 0; }
        .subtitle { color: #6C757D; font-size: 13px; margin: 5px 0 0 0; font-weight: 500; }
        .card {
            background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 12px; padding: 16px; margin-bottom: 15px;
        }
        h2 { font-size: 17px; margin-top: 0; color: #495057; border-bottom: 2px solid #e9ecef; padding-bottom: 8px; }
        .form-group { margin-bottom: 12px; }
        label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 13px; color: #495057; }
        input[type="text"], input[type="number"], select {
            width: 100%; padding: 10px; border: 1px solid #ced4da; border-radius: 8px;
            box-sizing: border-box; font-size: 15px; background: #fff;
        }
        .grid-inputs {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(70px, 1fr)); gap: 10px; margin-bottom: 15px;
        }
        .score-box { text-align: center; }
        .score-box label { font-size: 12px; margin-bottom: 4px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }
        .score-box input { width: 100%; padding: 10px 2px; text-align: center; font-size: 16px; font-weight: bold; }
        button {
            width: 100%; background-color: #E63946; color: white; border: none; padding: 12px;
            font-size: 15px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-bottom: 10px;
        }
        button:hover { background-color: #cb323f; }
        .btn-secondary { background-color: #6C757D; }
        .btn-secondary:hover { background-color: #5a6268; }
        .btn-outline { background-color: transparent; color: #6C757D; border: 1px solid #ced4da; }
        .mode-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }
        .mode-btn { padding: 15px 10px; font-size: 14px; border: 2px solid #dee2e6; border-radius: 8px; text-align: center; cursor: pointer; font-weight: bold; background: #fff; }
        .mode-btn.active { border-color: #E63946; color: #E63946; background: #fff5f5; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
        th, td { border: 1px solid #dee2e6; padding: 8px; text-align: center; }
        th { background-color: #f1f3f5; font-weight: 600; }
        .total-row { font-weight: bold; background-color: #e9ecef; }
        .history-wrapper { overflow-x: auto; margin-top: 10px; }
        .badge { background: #E63946; color: #fff; padding: 1px 5px; border-radius: 4px; font-size: 10px; vertical-align: middle; }
        .live-badge { background: #2b9348; color: white; animation: blink 1.5s infinite; float: right; font-size: 10px; padding: 2px 6px; border-radius: 20px; font-weight: bold; margin-top: -3px; }
        @keyframes blink { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }
        .info-text { font-size: 12px; color: #6c757d; margin-bottom: 10px; background: #e8f4fd; padding: 8px; border-radius: 6px; }
    </style>
</head>
<body>

    <div class="header">
        <p class="title">🃏 Dejenere Amerikan ⭐</p>
        <p class="subtitle">📡 Canlı Oda Paylaşımlı Canlı Yazboz</p>
    </div>

    <!-- AŞAMA 1: GİRİŞ VE MOD SEÇİM EKRANI -->
    <div id="setup-screen" class="card">
        <h2>⚡ Oyun Modunu Seçin</h2>
        <div class="mode-container">
            <div id="btn-mode-writer" class="mode-btn active" onclick="setMode('writer')">✍️ Skor Yazıcı<br><small style="font-weight:normal;font-size:10px;color:#6c757d;">Skorları ben gireceğim</small></div>
            <div id="btn-mode-viewer" class="mode-btn" onclick="setMode('viewer')">👀 Sadece İzleyici<br><small style="font-weight:normal;font-size:10px;color:#6c757d;">Masadan takip edeceğim</small></div>
        </div>

        <div class="form-group">
            <label>🔑 Oda Kodu (Masadaki Herkes Aynı Kodu Girmeli)</label>
            <input type="text" id="room-code" placeholder="Örn: masa5" style="font-weight:bold; text-transform:uppercase;">
        </div>

        <div id="writer-inputs">
            <h2>👥 Oyuncu İsimlerini Girin</h2>
            <div class="form-group"><input type="text" id="p1" placeholder="1. Oyuncu"></div>
            <div class="form-group"><input type="text" id="p2" placeholder="2. Oyuncu"></div>
            <div class="form-group"><input type="text" id="p3" placeholder="3. Oyuncu"></div>
            <div class="form-group"><input type="text" id="p4" placeholder="4. Oyuncu"></div>
            <div class="form-group"><input type="text" id="p5" placeholder="5. Oyuncu"></div>
        </div>

        <button onclick="initAction()" style="margin-top:10px;">Bağlan ve Oyunu Başlat 🚀</button>
    </div>

    <!-- AŞAMA 2: OYUN PANELI (SADECE YAZICILAR GÖRÜR) -->
    <div id="game-screen" class="card" style="display:none;">
        <h2>🎯 Tur Detayları <span class="live-badge" id="sync-status">BULUT AKTİF</span></h2>
        <div class="form-group">
            <label>Oynanan Tur</label>
            <select id="current-round-select"></select>
        </div>
        <div class="form-group" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div>
                <label>Kağıt Dağıtan 🃏</label>
                <select id="dealer-select"></select>
            </div>
            <div>
                <label>Oyunu Biten 🗣️</label>
                <select id="announcer-select"></select>
            </div>
        </div>

        <h2 style="margin-top: 15px;">✍️ Cezaları Girin</h2>
        <div id="dynamic-inputs" class="grid-inputs"></div>
        
        <button onclick="saveRound()">➡️ Tur Skorlarını Kaydet</button>
        <button class="button btn-secondary" id="undo-btn" onclick="undoLastRound()" style="display:none; font-size:13px; padding:8px;">⚠️ Son Turu Geri Al</button>
    </div>

    <!-- AŞAMA 3: PUAN TABLOLARI (HERKES GÖRÜR) -->
    <div id="table-screen" class="card" style="display:none;">
        <h2>📊 Canlı Ceza Puanları (Kümülatif) <span class="live-badge" id="viewer-sync-status" style="display:none;">CANLI TAKİP</span></h2>
        <table id="summary-table"><thead><tr><th>Oyuncu</th><th>Bu Tur</th><th>Toplam Ceza</th></tr></thead><tbody id="summary-body"></tbody></table>

        <h2 style="margin-top:25px;">📄 Yazboz Sayfasının Tamamı</h2>
        <div class="history-wrapper">
            <table id="history-table"><thead><tr id="history-headers"></tr></thead><tbody id="history-body"></tbody></table>
        </div>
        
        <div id="writer-reset-area" style="display:none;">
            <button class="button btn-secondary" style="background-color:#6c757d; margin-top:25px; font-size:13px; padding:10px;" onclick="resetGame()">🔄 Oyunu Tamamen Sıfırla / Yeni Oyun</button>
        </div>
        <div id="viewer-exit-area" style="display:none;">
            <button class="button btn-outline" style="margin-top:25px; font-size:13px; padding:10px;" onclick="exitViewer()">🚶 İzleme Modundan Çık</button>
        </div>
    </div>

    <script>
        const ROUNDS = [
            "1. 4'lü Küt + 3'lü Seri", "2. 3x3'lü Küt", "3. 2x3'lü Seri + 2x3'lü Küt", "4. 3-3'lü Seri",
            "5. 2x3'lü Seri + 1x3'lü Küt", "6. 4'lü Küt", "7. 4'lü Seri", "8. 4'lü Karışık",
            "9. 4'lü Seri + 3'lü Küt", "10. 2x4'lü Seri", "11. 2x4'lü Küt", "12. 5'li Seri",
            "13. 6'lı Seri", "14. 5'li Seri + 3'lü Küt", "15. 4 Çift + 3'lü Seri veya Küt", "16. Elden Bitme"
        ];

        let selectedMode = 'writer';
        let currentRoomCode = '';

        let state = {
            initialized: false,
            mode: 'writer',
            roomCode: '',
            players: [],
            completedRounds: [],
            roundDetails: {},
            scores: {}
        };

        function setMode(mode) {
            selectedMode = mode;
            document.getElementById("btn-mode-writer").className = "mode-btn" + (mode === 'writer' ? ' active' : '');
            document.getElementById("btn-mode-viewer").className = "mode-btn" + (mode === 'viewer' ? ' active' : '');
            document.getElementById("writer-inputs").style.display = mode === 'writer' ? 'block' : 'none';
        }

        // BULUT BULUŞMA KANALI (Doğrudan tarayıcıdan tarayıcıya çok hızlı bağlantı)
        function getCloudUrl() {
            return "https://kvdb.io/K38qgX6T57g8uX6fG68p8T/deg_room_" + currentRoomCode.trim().toUpperCase();
        }

        async function pushToCloud() {
            if (!currentRoomCode) return;
            try {
                await fetch(getCloudUrl(), {
                    method: 'POST',
                    body: JSON.stringify(state),
                    headers: {'Content-Type': 'application/json'}
                });
                document.getElementById("sync-status").innerText = "BULUT SENKRON";
                document.getElementById("sync-status").style.backgroundColor = "#2b9348";
            } catch(e) {
                document.getElementById("sync-status").innerText = "YEREL KAYIT";
                document.getElementById("sync-status").style.backgroundColor = "#f39c12";
            }
        }

        async function pullFromCloud() {
            if (!currentRoomCode) return;
            try {
                let res = await fetch(getCloudUrl());
                if (res.status === 200) {
                    let cloudState = await res.json();
                    if (cloudState && cloudState.initialized) {
                        state = cloudState;
                        renderTables();
                    }
                }
            } catch(e) {}
        }

        function loadFromLocalStorage() {
            const saved = localStorage.getItem("dejenere_yazboz_v5");
            if (saved) {
                try {
                    let localState = JSON.parse(saved);
                    if (localState.initialized && localState.mode === 'writer') {
                        state = localState;
                        currentRoomCode = state.roomCode;
                        renderGame();
                        // Arka planda buluta da tazeleyin
                        pushToCloud();
                    }
                } catch(e) {}
            }
        }

        function saveToLocalStorage() {
            localStorage.setItem("dejenere_yazboz_v5", JSON.stringify(state));
        }

        function initAction() {
            currentRoomCode = document.getElementById("room-code").value.trim();
            if (!currentRoomCode) {
                alert("Lütfen masadaki diğer oyuncularla paylaşacağınız bir Oda Kodu belirleyin!");
                return;
            }

            if (selectedMode === 'writer') {
                let names = [
                    document.getElementById("p1").value.trim(),
                    document.getElementById("p2").value.trim(),
                    document.getElementById("p3").value.trim(),
                    document.getElementById("p4").value.trim(),
                    document.getElementById("p5").value.trim()
                ].filter(n => n !== "");

                if (names.length < 2) {
                    alert("Lütfen en az 2 oyuncu ismi girin!");
                    return;
                }

                state.initialized = true;
                state.mode = 'writer';
                state.roomCode = currentRoomCode;
                state.players = names;
                state.completedRounds = [];
                state.roundDetails = {};
                state.scores = {};
                
                ROUNDS.forEach(r => {
                    state.scores[r] = {};
                    state.players.forEach(p => { state.scores[r][p] = 0; });
                });

                saveToLocalStorage();
                pushToCloud();
                renderGame();
            } else {
                // İzleyici Modu Girişi
                state.initialized = true;
                state.mode = 'viewer';
                state.roomCode = currentRoomCode;
                
                document.getElementById("setup-screen").style.display = "none";
                document.getElementById("table-screen").style.display = "block";
                document.getElementById("viewer-sync-status").style.display = "inline-block";
                document.getElementById("viewer-exit-area").style.display = "block";
                
                pullFromCloud();
                // Her 5 saniyede bir skor yazanın ekranından verileri canlı çek
                setInterval(pullFromCloud, 5000);
            }
        }

        function renderGame() {
            document.getElementById("setup-screen").style.display = "none";
            document.getElementById("game-screen").style.display = "block";
            document.getElementById("table-screen").style.display = "block";
            document.getElementById("writer-reset-area").style.display = "block";

            const selectRound = document.getElementById("current-round-select");
            selectRound.innerHTML = "";
            let available = ROUNDS.filter(r => !state.completedRounds.includes(r));
            
            if (available.length === 0) {
                document.getElementById("game-screen").innerHTML = "<h2>🎉 OYUN BİTTİ! 🎉</h2><p style='text-align:center; font-weight:bold; font-size:15px;'>Tüm turlar oynandı. Şampiyonu tebrik edin!</p>";
            } else {
                available.forEach(r => {
                    let opt = document.createElement("option");
                    opt.value = r; opt.innerText = r;
                    selectRound.appendChild(opt);
                });
            }

            const dSelect = document.getElementById("dealer-select");
            const aSelect = document.getElementById("announcer-select");
            dSelect.innerHTML = ""; aSelect.innerHTML = "";
            state.players.forEach(p => {
                let o1 = document.createElement("option"); o1.value = p; o1.innerText = p;
                let o2 = document.createElement("option"); o2.value = p; o2.innerText = p;
                dSelect.appendChild(o1); aSelect.appendChild(o2);
            });

            const inputContainer = document.getElementById("dynamic-inputs");
            inputContainer.innerHTML = "";
            state.players.forEach(p => {
                let div = document.createElement("div");
                div.className = "score-box";
                div.innerHTML = `<label><strong>${p}</strong></label><input type="number" id="input_${p}" placeholder="0">`;
                inputContainer.appendChild(div);
            });

            document.getElementById("undo-btn").style.display = state.completedRounds.length > 0 ? "block" : "none";
            renderTables();
        }

        function saveRound() {
            const currentRound = document.getElementById("current-round-select").value;
            if (!currentRound) return;

            const dealer = document.getElementById("dealer-select").value;
            const announcer = document.getElementById("announcer-select").value;

            state.roundDetails[currentRound] = { dealer: dealer, announcer: announcer };
            
            state.players.forEach(p => {
                let val = parseInt(document.getElementById(`input_${p}`).value);
                state.scores[currentRound][p] = isNaN(val) ? 0 : val;
            });

            state.completedRounds.push(currentRound);
            saveToLocalStorage();
            pushToCloud();
            renderGame();
        }

        function undoLastRound() {
            if (state.completedRounds.length === 0) return;
            if (confirm("En son girilen turu iptal etmek istediğinize emin misiniz?")) {
                let last = state.completedRounds.pop();
                delete state.roundDetails[last];
                state.players.forEach(p => { state.scores[last][p] = 0; });
                saveToLocalStorage();
                pushToCloud();
                window.location.reload();
            }
        }

        function renderTables() {
            if (!state.players || state.players.length === 0) return;

            let totals = {};
            state.players.forEach(p => totals[p] = 0);
            
            state.completedRounds.forEach(r => {
                state.players.forEach(p => {
                    totals[p] += (state.scores[r][p] || 0);
                });
            });

            let lastRound = state.completedRounds[state.completedRounds.length - 1] || null;

            // Özet Tablo Üretimi
            const summaryBody = document.getElementById("summary-body");
            summaryBody.innerHTML = "";
            let minScore = Math.min(...state.players.map(p => totals[p]));

            state.players.forEach(p => {
                let thisRoundScore = lastRound ? (state.scores[lastRound][p] || 0) : 0;
                let tr = document.createElement("tr");
                let isWinnerBadge = (totals[p] === minScore && state.completedRounds.length > 0) ? " <span class='badge'>1.</span>" : "";
                tr.innerHTML = `<td><strong>${p}</strong>${isWinnerBadge}</td><td>${thisRoundScore}</td><td style='font-weight:bold;'>${totals[p]}</td>`;
                summaryBody.appendChild(tr);
            });

            // Büyük Yazboz Başlıkları
            const hHeaders = document.getElementById("history-headers");
            hHeaders.innerHTML = "<th>Yazboz Turları</th><th>Dağıtan</th><th>Biten</th>";
            state.players.forEach(p => {
                let th = document.createElement("th"); th.innerText = p;
                hHeaders.appendChild(th);
            });

            // Büyük Yazboz Satırları
            const historyBody = document.getElementById("history-body");
            historyBody.innerHTML = "";
            
            ROUNDS.forEach(r => {
                let tr = document.createElement("tr");
                let isDone = state.completedRounds.includes(r);
                let dText = isDone ? state.roundDetails[r].dealer : "-";
                let aText = isDone ? state.roundDetails[r].announcer : "-";
                
                let html = `<td style="text-align:left; ${isDone ? 'font-weight:bold; color:#2b9348;' : ''}">${r}</td><td>${dText}</td><td>${aText}</td>`;
                state.players.forEach(p => {
                    let scoreText = isDone ? state.scores[r][p] : "-";
                    html += `<td>${scoreText}</td>`;
                });
                tr.innerHTML = html;
                historyBody.appendChild(tr);
            });

            // Toplam Alt Satırı
            let totalTr = document.createElement("tr");
            totalTr.className = "total-row";
            let fHtml = `<td colspan="3" style="text-align:right;">GENEL TOPLAM:</td>`;
            state.players.forEach(p => { fHtml += `<td>${totals[p]}</td>`; });
            totalTr.innerHTML = fHtml;
            historyBody.appendChild(totalTr);
        }

        function resetGame() {
            if (confirm("Tüm skorları silip tamamen YENİ OYUN başlatmak istediğinize emin misiniz?")) {
                localStorage.removeItem("dejenere_yazboz_v5");
                state.initialized = false;
                pushToCloud(); // Bulutu da sıfırla
                window.location.reload();
            }
        }

        function exitViewer() {
            window.location.reload();
        }

        window.onload = loadFromLocalStorage;
    </script>
</body>
</html>
"""

# HTML uygulamasını telefona tam ekran ve kaydırma destekli olarak basıyoruz.
components.html(HTML_ENGINE, height=1100, scrolling=True)
