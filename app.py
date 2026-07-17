import streamlit as st
import streamlit.components.v1 as components

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Dejenere Amerikan Yazboz",
    page_icon="🃏",
    layout="centered"
)

# Sunucu uyku moduna karşı tamamen bağışık, gücünü doğrudan telefonun tarayıcı hafızasından alan HTML5 Motoru
HTML_ENGINE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #ffffff;
            color: #31333F;
            margin: 0;
            padding: 10px;
        }
        .header { text-align: center; margin-bottom: 20px; }
        .title { color: #E63946; font-size: 24px; font-weight: bold; margin: 0; }
        .subtitle { color: #6C757D; font-size: 14px; margin: 5px 0 0 0; font-weight: 500; }
        .card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
        }
        h2 { font-size: 18px; margin-top: 0; color: #495057; border-bottom: 2px solid #e9ecef; padding-bottom: 8px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 14px; color: #495057; }
        input[type="text"], input[type="password"], select {
            width: 100%; padding: 10px; border: 1px solid #ced4da; border-radius: 8px;
            box-sizing: border-box; font-size: 15px; background: #fff;
        }
        .grid-inputs {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(70px, 1fr)); gap: 10px; margin-bottom: 15px;
        }
        .score-box { text-align: center; }
        .score-box label { font-size: 13px; margin-bottom: 4px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }
        .score-box input {
            width: 100%; padding: 10px 5px; border: 1px solid #ced4da; border-radius: 8px;
            text-align: center; font-size: 16px; font-weight: bold; box-sizing: border-box;
        }
        button {
            width: 100%; background-color: #E63946; color: white; border: none; padding: 12px;
            font-size: 15px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: background 0.2s;
        }
        button:hover { background-color: #cb323f; }
        .btn-secondary { background-color: #6C757D; margin-top: 10px; }
        .btn-secondary:hover { background-color: #5a6268; }
        .btn-danger { background-color: #6c757d; font-size: 12px; padding: 6px; width: auto; float: right; margin-top: -32px; border-radius: 4px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }
        th, td { border: 1px solid #dee2e6; padding: 10px; text-align: center; }
        th { background-color: #f1f3f5; font-weight: 600; }
        .total-row { font-weight: bold; background-color: #e9ecef; }
        .history-wrapper { overflow-x: auto; margin-top: 10px; }
        .badge { background: #E63946; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
        .info-text { font-size: 12px; color: #6c757d; margin-bottom: 10px; background: #e8f4fd; padding: 8px; border-radius: 6px; }
    </style>
</head>
<body>

    <div class="header">
        <p class="title">🃏 Dejenere Amerikan ⭐</p>
        <p class="subtitle">📱 Kesintisiz Cihaz Hafızalı Canlı Yazboz</p>
    </div>

    <!-- 1. AŞAMA: GİRİŞ EKRANI -->
    <div id="setup-screen" class="card">
        <h2>👥 Oyuncu İsimlerini Girin</h2>
        <div class="form-group"><input type="text" id="p1" placeholder="1. Oyuncu"></div>
        <div class="form-group"><input type="text" id="p2" placeholder="2. Oyuncu"></div>
        <div class="form-group"><input type="text" id="p3" placeholder="3. Oyuncu"></div>
        <div class="form-group"><input type="text" id="p4" placeholder="4. Oyuncu"></div>
        <div class="form-group"><input type="text" id="p5" placeholder="5. Oyuncu"></div>
        <button onclick="startGame()">Oyunu Başlat 🚀</button>
    </div>

    <!-- 2. AŞAMA: OYUN EKRANI -->
    <div id="game-screen" class="card" style="display:none;">
        <h2>🎯 Tur Detayları</h2>
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

        <h2 style="margin-top: 20px;">✍️ Cezaları Girin</h2>
        <div class="info-text">💡 Kutular boş gelir. Biten kişiye eksi ceza girmek için başına eksi koyun (Örn: -50).</div>
        <div id="dynamic-inputs" class="grid-inputs"></div>
        
        <button onclick="saveRound()">➡️ Tur Skorlarını Kaydet</button>
        <button class="button btn-secondary" id="undo-btn" onclick="undoLastRound()" style="display:none;">⚠️ Son Turu İptal Et / Geri Al</button>
    </div>

    <!-- YÖNTEM 2: İZLEYİCİLER İÇİN GİZLİ YÖNETİCİ GİRİŞİ -->
    <div id="admin-login-screen" class="card" style="display:none;">
        <h2>🔐 Skor Giriş Yetkisi</h2>
        <div class="info-text">💡 Masada sadece yönetici skor girebilir. Diğer cihazlar tabloyu canlı izler.</div>
        <div class="form-group">
            <input type="password" id="admin-pin" placeholder="Yönetici PIN Kodu Girin">
        </div>
        <button onclick="checkAdminPIN()">Paneli Aç 🔓</button>
    </div>

    <!-- 3. AŞAMA: PUAN TABLOLARI -->
    <div id="table-screen" class="card" style="display:none;">
        <h2>📊 Genel Ceza Puanları (Kümülatif)</h2>
        <table id="summary-table"><thead><tr><th>Oyuncu</th><th>Bu Tur</th><th>Toplam Ceza</th></tr></thead><tbody id="summary-body"></tbody></table>

        <h2 style="margin-top:30px;">📄 Yazboz Sayfasının Tamamı</h2>
        <div class="history-wrapper">
            <table id="history-table"><thead><tr id="history-headers"></tr></thead><tbody id="history-body"></tbody></table>
        </div>
        
        <button class="button btn-secondary" style="background-color:#6c757d; margin-top:30px;" onclick="resetGame()">🔄 Oyunu Tamamen Sıfırla / Yeni Oyun</button>
    </div>

    <script>
        // Söküp aldığımız o asıl canlı Google Sheets bağlantısı
        const API_URL = "https://script.google.com/macros/s/AKfycbxZp2bpoN25mqjukeUehUcovMbeBi9nfEK2z4AsrqusFNOXsdWbRt1xkbG8V5zBZjBv/exec";
        const ADMIN_PIN = "1905";
        let isAdmin = localStorage.getItem("is_admin") === "true";

        const ROUNDS = [
            "1. 4'lü Küt + 3'lü Seri", "2. 3x3'lü Küt", "3. 2x3'lü Seri + 2x3'lü Küt", "4. 3-3'lü Seri",
            "5. 2x3'lü Seri + 1x3'lü Küt", "6. 4'lü Küt", "7. 4'lü Seri", "8. 4'lü Karışık",
            "9. 4'lü Seri + 3'lü Küt", "10. 2x4'lü Seri", "11. 2x4'lü Küt", "12. 5'li Seri",
            "13. 6'lı Seri", "14. 5'li Seri + 3'lü Küt", "15. 4 Çift + 3'lü Seri veya Küt", "16. Elden Bitme"
        ];

        let state = {
            initialized: false,
            players: [],
            completedRounds: [],
            roundDetails: {}, // round -> {dealer, announcer}
            scores: {} // round -> {player: score}
        };

        // GOOGLE SHEETS BULUT ENTEGRASYONU (Arka planda çalışır, yereli engellemez)
        function pushToCloud() {
            fetch(API_URL, {
                method: "POST",
                mode: "no-cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(state)
            }).catch(e => console.log("Bulut eşitleme hatası"));
        }

        function fetchFromCloud() {
            fetch(API_URL)
                .then(res => res.json())
                .then(cloudState => {
                    if (cloudState && typeof cloudState === 'object') {
                        // Eğer bulutta aktif bir oyun varsa yerel durumu onunla güncelle (İzleyiciler için)
                        state = cloudState;
                        if (state.initialized) {
                            renderGame();
                        } else {
                            // Bulut sıfırlanmışsa herkesi ilk ekrana at
                            document.getElementById("setup-screen").style.style.display = "block";
                            document.getElementById("game-screen").style.display = "none";
                            document.getElementById("admin-login-screen").style.display = "none";
                            document.getElementById("table-screen").style.display = "none";
                        }
                    }
                }).catch(e => console.log("Canlı yayın çekilemedi"));
        }

        function checkAdminPIN() {
            const pinInput = document.getElementById("admin-pin").value;
            if (pinInput === ADMIN_PIN) {
                isAdmin = true;
                localStorage.setItem("is_admin", "true");
                renderGame();
            } else {
                alert("Hatalı PIN Kodu! Masada sadece yönetici skor girebilir.");
            }
        }

        // TELEFONUN KENDİ HAFIZASINDAN VERİ ÇEKME (ASLA ÇÖKMEZ)
        function loadFromLocalStorage() {
            const saved = localStorage.getItem("dejenere_yazboz_v4");
            if (saved) {
                try {
                    state = JSON.parse(saved);
                    if (state.initialized) {
                        renderGame();
                    }
                } catch(e) {
                    localStorage.removeItem("dejenere_yazboz_v4");
                }
            }
            // Sayfa açıldığında hemen buluttaki en taze veriyi de kontrol et
            fetchFromCloud();
        }

        function saveToLocalStorage() {
            localStorage.setItem("dejenere_yazboz_v4", JSON.stringify(state));
        }

        function startGame() {
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
            isAdmin = true; // Oyunu kuran cihaz otomatik yöneticidir
            localStorage.setItem("is_admin", "true");

            state.players = names;
            state.completedRounds = [];
            state.roundDetails = {};
            state.scores = {};
            
            ROUNDS.forEach(r => {
                state.scores[r] = {};
                state.players.forEach(p => { state.scores[r][p] = 0; });
            });

            saveToLocalStorage();
            pushToCloud(); // Buluta gönder
            renderGame();
        }

        function renderGame() {
            document.getElementById("setup-screen").style.display = "none";
            
            // YÖNTEM 2 KONTROLÜ: Yönetici mi izleyici mi?
            if (isAdmin) {
                document.getElementById("game-screen").style.display = "block";
                document.getElementById("admin-login-screen").style.display = "none";
            } else {
                document.getElementById("game-screen").style.display = "none";
                document.getElementById("admin-login-screen").style.display = "block";
            }
            
            document.getElementById("table-screen").style.display = "block";

            // Kalan turları listele
            const selectRound = document.getElementById("current-round-select");
            selectRound.innerHTML = "";
            let available = ROUNDS.filter(r => !state.completedRounds.includes(r));
            
            if (available.length === 0) {
                document.getElementById("game-screen").innerHTML = "<h2>🎉 OYUN BİTTİ! 🎉</h2><p style='text-align:center; font-weight:bold; font-size:18px;'>Tüm turlar tamamlandı. Aşağıdaki tablodan kazananı görebilirsiniz.</p>";
            } else {
                available.forEach(r => {
                    let opt = document.createElement("option");
                    opt.value = r; opt.innerText = r;
                    selectRound.appendChild(opt);
                });
            }

            // Dağıtan ve Söyleyen listesi
            const dSelect = document.getElementById("dealer-select");
            const aSelect = document.getElementById("announcer-select");
            dSelect.innerHTML = ""; aSelect.innerHTML = "";
            state.players.forEach(p => {
                let o1 = document.createElement("option"); o1.value = p; o1.innerText = p;
                let o2 = document.createElement("option"); o2.value = p; o2.innerText = p;
                dSelect.appendChild(o1); aSelect.appendChild(o2);
            });

            // Ceza giriş kutuları
            const inputContainer = document.getElementById("dynamic-inputs");
            inputContainer.innerHTML = "";
            state.players.forEach(p => {
                let div = document.createElement("div");
                div.className = "score-box";
                div.innerHTML = `<label>${p}</label><input type="number" id="input_${p}" placeholder="0">`;
                inputContainer.appendChild(div);
            });

            // Geri al butonu görünürlüğü
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
            pushToCloud(); // Buluta gönder
            renderGame();
        }

        function undoLastRound() {
            if (state.completedRounds.length === 0) return;
            if (confirm("En son girilen turun skorlarını silip geri almak istediğinize emin misiniz?")) {
                let last = state.completedRounds.pop();
                delete state.roundDetails[last];
                state.players.forEach(p => { state.scores[last][p] = 0; });
                saveToLocalStorage();
                pushToCloud(); // Buluttan da geri al
                window.location.reload();
            }
        }

        function renderTables() {
            // Kümülatif Hesaplama
            let totals = {};
            state.players.forEach(p => totals[p] = 0);
            
            state.completedRounds.forEach(r => {
                state.players.forEach(p => {
                    totals[p] += (state.scores[r][p] || 0);
                });
            });

            // Son el girenleri yakala
            let lastRound = state.completedRounds[state.completedRounds.length - 1] || null;

            // Özet Tablo
            const summaryBody = document.getElementById("summary-body");
            summaryBody.innerHTML = "";
            
            // En düşük puanı bul (Kazananı belirlemek için)
            let minScore = Math.min(...state.players.map(p => totals[p]));

            state.players.forEach(p => {
                let thisRoundScore = lastRound ? (state.scores[lastRound][p] || 0) : 0;
                let tr = document.createElement("tr");
                let isWinnerBadge = (totals[p] === minScore && state.completedRounds.length > 0) ? " <span class='badge'>1.</span>" : "";
                tr.innerHTML = `<td><strong>${p}</strong>${isWinnerBadge}</td><td>${thisRoundScore}</td><td style="font-weight:bold; color:${totals[p] > 150 ? '#E63946' : '#31333F'}">${totals[p]}</td>`;
                summaryBody.appendChild(tr);
            });

            // Büyük Yazboz Tablosu Başlıkları
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
                
                let html = `<td style="text-align:left; ${isDone ? 'font-weight:600; color:#2b9348;' : ''}">${r}</td><td>${dText}</td><td>${aText}</td>`;
                
                state.players.forEach(p => {
                    let scoreText = isDone ? state.scores[r][p] : "-";
                    html += `<td>${scoreText}</td>`;
                });
                
                tr.innerHTML = html;
                historyBody.appendChild(tr);
            });

            // Genel Toplam Alt Satırı
            let totalTr = document.createElement("tr");
            totalTr.className = "total-row";
            let fHtml = `<td colspan="3" style="text-align:right;">GENEL TOPLAM:</td>`;
            state.players.forEach(p => {
                fHtml += `<td>${totals[p]}</td>`;
            });
            totalTr.innerHTML = fHtml;
            historyBody.appendChild(totalTr);
        }

        function resetGame() {
            if (confirm("Tüm skorları silip tamamen YENİ OYUN başlatmak istediğinize emin misiniz? Bu işlem geri alınamaz!")) {
                localStorage.removeItem("dejenere_yazboz_v4");
                // Bulutu da temizle
                fetch(API_URL, {
                    method: "POST",
                    mode: "no-cors",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ initialized: false })
                }).then(() => {
                    window.location.reload();
                });
            }
        }

        // Sayfa açıldığında hafızayı yokla
        window.onload = loadFromLocalStorage;

        // İzleyen diğer oyuncuların ekranı her 7 saniyede bir otomatik canlansın
        setInterval(fetchFromCloud, 7000);
    </script>
</body>
</html>
"""

# HTML Motorunu Streamlit ekranına tam sayfa, dokunmatik uyumlu olarak gömüyoruz.
components.html(HTML_ENGINE, height=1000, scrolling=True)
