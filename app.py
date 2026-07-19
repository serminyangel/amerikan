import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import base64
import time

# Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Dejenere Amerikan Yazboz",
    page_icon="🃏",
    layout="centered"
)

# Yeni gönderdiğin taze ve "Herkes" erişimli Google Web App URL'si
API_URL = "https://script.google.com/macros/s/AKfycbyxmpjUVXvqMtF_qzqntxOasqZWQNcvrXC-PW8WYW-EwqS2ZexDzwiLfcLMl8hX-th1/exec"

# SUNUCU SEVİYESİNDE ÖN-YÜKLEME
cloud_state_data = {"initialized": False}
try:
    res = requests.get(f"{API_URL}?t={int(time.time())}", timeout=4)
    if res.status_code == 200:
        cloud_state_data = res.json()
except:
    pass

# Veriyi güvenli Base64 zırhına alıyoruz
cloud_b64 = base64.b64encode(json.dumps(cloud_state_data).encode('utf-8')).decode('utf-8')

# HTML5 Motoru
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
        .spectator-card {
            background: #e8f5e9;
            border: 1px solid #c8e6c9;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
            text-align: center;
        }
        .spectator-badge {
            background: #2e7d32;
            color: white;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 8px;
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
        .btn-success { background-color: #2b9348; }
        .btn-success:hover { background-color: #217338; }
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

    <!-- 2. AŞAMA: YÖNETİCİ OYUN EKRANI -->
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
        <button class="button btn-secondary" onclick="logoutAdmin()" style="background-color:#495057; margin-top:10px;">🔒 Bu Cihazda İzleyici Moduna Geç</button>

        <!-- GEÇMİŞ TUR SKORUNU DÜZELTME ALANI -->
        <div id="edit-round-area" style="margin-top:25px; border-top: 2px dashed #ced4da; padding-top: 15px; display:none;">
            <h2 style="font-size:16px; color:#2b9348;">✏️ Geçmiş Tur Skorunu Düzelt</h2>
            <div class="form-group">
                <label>Düzeltmek İstediğiniz Turu Seçin</label>
                <select id="edit-round-select" onchange="loadRoundForEditing()"></select>
            </div>
            <div id="edit-form-fields" style="display:none;">
                <div class="form-group" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div><label>Dağıtan 🃏</label><select id="edit-dealer-select"></select></div>
                    <div><label>Biten 🗣️</label><select id="edit-announcer-select"></select></div>
                </div>
                <div id="edit-dynamic-inputs" class="grid-inputs"></div>
                <button class="button btn-success" onclick="saveEditedRound()">💾 Düzeltmeyi Kaydet</button>
            </div>
        </div>
    </div>

    <!-- 3. AŞAMA: İZLEYİCİ BİLDİRİMİ -->
    <div id="admin-login-screen" class="spectator-card" style="display:none;">
        <span class="spectator-badge">🟢 CANLI İZLEYİCİ MODU</span>
        <h3 style="margin: 5px 0 10px 0; color:#1b5e20; font-size:16px;">👁️ Masa Skorları Canlı Yayınlanıyor</h3>
        <p style="font-size:13px; color:#2e7d32; margin: 0 0 15px 0;">
            Masayı canlı izliyorsunuz. Skor girişini masa yöneticisi yapar, puanlar ekranınıza otomatik düşer.
        </p>

        <button onclick="toggleAdminForm()" style="background-color:#5c6bc0; font-size:13px; padding:8px;">🔑 Masa Yöneticisi misiniz? (PIN Girin)</button>
        
        <div id="admin-form-box" style="display:none; margin-top:15px; text-align:left; background:white; padding:12px; border-radius:8px; border:1px solid #ced4da;">
            <div class="form-group" style="margin-bottom:8px;">
                <label style="font-size:12px;">Yönetici PIN Kodu</label>
                <input type="password" id="admin-pin" placeholder="PIN Kodu">
            </div>
            <button onclick="checkAdminPIN()" style="font-size:13px; padding:8px;">Paneli Aç 🔓</button>
        </div>
    </div>

    <!-- 4. AŞAMA: PUAN TABLOLARI -->
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
        const API_URL = "https://script.google.com/macros/s/AKfycbyxmpjUVXvqMtF_qzqntxOasqZWQNcvrXC-PW8WYW-EwqS2ZexDzwiLfcLMl8hX-th1/exec";
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
            roundDetails: {},
            scores: {}
        };

        function toggleAdminForm() {
            const box = document.getElementById("admin-form-box");
            box.style.display = box.style.display === "none" ? "block" : "none";
        }

        function pushToCloud() {
            fetch(API_URL + "?puanla=" + encodeURIComponent(JSON.stringify(state)) + "&t=" + new Date().getTime())
            .catch(e => console.log("Bulut eşitleme hatası"));
        }

        function fetchFromCloud() {
            fetch(API_URL + "?t=" + new Date().getTime())
                .then(res => res.json())
                .then(cloudState => {
                    if (cloudState && typeof cloudState === 'object') {
                        if (cloudState.initialized) {
                            const cloudCount = cloudState.completedRounds ? cloudState.completedRounds.length : 0;
                            const localCount = state.completedRounds ? state.completedRounds.length : 0;
                            
                            if (!state.initialized || !isAdmin || cloudCount !== localCount) {
                                state = cloudState;
                                saveToLocalStorage();
                                renderGame(true);
                            }
                        } else if (state.initialized) {
                            localStorage.removeItem("dejenere_yazboz_v4");
                            location.reload();
                        }
                    }
                }).catch(e => console.log("Yenileme hatası"));
        }

        function checkAdminPIN() {
            const pinInput = document.getElementById("admin-pin").value;
            if (pinInput === ADMIN_PIN) {
                isAdmin = true;
                localStorage.setItem("is_admin", "true");
                renderGame();
            } else {
                alert("Hatalı PIN Kodu!");
            }
        }

        function logoutAdmin() {
            isAdmin = false;
            localStorage.removeItem("is_admin");
            renderGame();
        }

        function loadFromLocalStorage() {
            const saved = localStorage.getItem("dejenere_yazboz_v4");
            
            if (saved) {
                try { 
                    const parsed = JSON.parse(saved);
                    if (parsed && parsed.initialized) {
                        state = parsed;
                    }
                } catch(e) {}
            }
            
            if (!state.initialized) {
                try {
                    let cloudStateRaw = decodeURIComponent(escape(window.atob("/*CLOUD_STATE_B64*/")));
                    let parsedCloud = JSON.parse(cloudStateRaw);
                    if (parsedCloud && parsedCloud.initialized) {
                        state = parsedCloud;
                    }
                } catch(e) {}
            }
            
            if (state.initialized) {
                renderGame();
            } else {
                document.getElementById("setup-screen").style.display = "block";
                document.getElementById("game-screen").style.display = "none";
                document.getElementById("admin-login-screen").style.display = "none";
                document.getElementById("table-screen").style.display = "none";
            }
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
            isAdmin = true; 
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
            pushToCloud();
            renderGame(true);
        }

        function renderGame(clearInputs = false) {
            document.getElementById("setup-screen").style.display = "none";
            
            if (isAdmin) {
                document.getElementById("game-screen").style.display = "block";
                document.getElementById("admin-login-screen").style.display = "none";
            } else {
                document.getElementById("game-screen").style.display = "none";
                document.getElementById("admin-login-screen").style.display = "block";
            }
            
            document.getElementById("table-screen").style.display = "block";

            let available = ROUNDS.filter(r => !state.completedRounds.includes(r));
            
            if (available.length === 0) {
                document.getElementById("game-screen").innerHTML = `
                    <h2>🎉 OYUN BİTTİ! 🎉</h2>
                    <p style='text-align:center; font-weight:bold; font-size:16px; margin: 15px 0;'>16 turun tamamı oynandı. Kazananı aşağıdaki kümülatif tablodan görebilirsiniz.</p>
                    <button class="button btn-secondary" id="undo-btn" onclick="undoLastRound()">⚠️ Son Turu (16. Tur) İptal Et / Geri Al</button>
                    <button class="button btn-secondary" onclick="logoutAdmin()" style="background-color:#495057; margin-top:10px;">🔒 Bu Cihazda İzleyici Moduna Geç</button>
                    
                    <div id="edit-round-area" style="margin-top:25px; border-top: 2px dashed #ced4da; padding-top: 15px;">
                        <h2 style="font-size:16px; color:#2b9348;">✏️ Geçmiş Tur Skorunu Düzelt</h2>
                        <div class="form-group">
                            <label>Düzeltmek İstediğiniz Turu Seçin</label>
                            <select id="edit-round-select" onchange="loadRoundForEditing()"></select>
                        </div>
                        <div id="edit-form-fields" style="display:none;">
                            <div class="form-group" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                <div><label>Dağıtan 🃏</label><select id="edit-dealer-select"></select></div>
                                <div><label>Biten 🗣️</label><select id="edit-announcer-select"></select></div>
                            </div>
                            <div id="edit-dynamic-inputs" class="grid-inputs"></div>
                            <button class="button btn-success" onclick="saveEditedRound()">💾 Düzeltmeyi Kaydet</button>
                        </div>
                    </div>
                `;
            } else {
                const selectRound = document.getElementById("current-round-select");
                if (selectRound) {
                    const oldRoundVal = selectRound.value;
                    selectRound.innerHTML = "";
                    available.forEach(r => {
                        let opt = document.createElement("option");
                        opt.value = r; opt.innerText = r;
                        selectRound.appendChild(opt);
                    });
                    if(oldRoundVal && available.includes(oldRoundVal)) {
                        selectRound.value = oldRoundVal;
                    }
                }

                const dSelect = document.getElementById("dealer-select");
                const aSelect = document.getElementById("announcer-select");
                if (dSelect && aSelect) {
                    const oldD = dSelect.value; const oldA = aSelect.value;
                    dSelect.innerHTML = ""; aSelect.innerHTML = "";
                    state.players.forEach(p => {
                        let o1 = document.createElement("option"); o1.value = p; o1.innerText = p;
                        let o2 = document.createElement("option"); o2.value = p; o2.innerText = p;
                        dSelect.appendChild(o1); aSelect.appendChild(o2);
                    });
                    if(oldD) dSelect.value = oldD;
                    if(oldA) aSelect.value = oldA;
                }

                const inputContainer = document.getElementById("dynamic-inputs");
                if (inputContainer) {
                    const currentInputs = {};
                    if (!clearInputs) {
                        state.players.forEach(p => {
                            const el = document.getElementById(`input_${p}`);
                            if(el) currentInputs[p] = el.value;
                        });
                    }

                    inputContainer.innerHTML = "";
                    state.players.forEach(p => {
                        let div = document.createElement("div");
                        div.className = "score-box";
                        let savedVal = (currentInputs[p] !== undefined && !clearInputs) ? currentInputs[p] : "";
                        div.innerHTML = `<label>${p}</label><input type="number" id="input_${p}" placeholder="0" value="${savedVal}">`;
                        inputContainer.appendChild(div);
                    });
                }

                const undoBtn = document.getElementById("undo-btn");
                if (undoBtn) {
                    undoBtn.style.display = state.completedRounds.length > 0 ? "block" : "none";
                }
            }

            const editArea = document.getElementById("edit-round-area");
            const editSelect = document.getElementById("edit-round-select");
            if (editArea && editSelect) {
                if (state.completedRounds.length > 0) {
                    editArea.style.display = "block";
                    const currentVal = editSelect.value;
                    editSelect.innerHTML = '<option value="">-- Tur Seçin --</option>';
                    state.completedRounds.forEach(r => {
                        let opt = document.createElement("option");
                        opt.value = r; opt.innerText = r;
                        editSelect.appendChild(opt);
                    });
                    if (currentVal && state.completedRounds.includes(currentVal)) {
                        editSelect.value = currentVal;
                        loadRoundForEditing();
                    } else {
                        document.getElementById("edit-form-fields").style.display = "none";
                    }
                } else {
                    editArea.style.display = "none";
                }
            }

            renderTables();
        }

        function loadRoundForEditing() {
            const r = document.getElementById("edit-round-select").value;
            const editFields = document.getElementById("edit-form-fields");
            if (!r) {
                editFields.style.display = "none";
                return;
            }
            editFields.style.display = "block";

            const dSelect = document.getElementById("edit-dealer-select");
            const aSelect = document.getElementById("edit-announcer-select");
            dSelect.innerHTML = ""; aSelect.innerHTML = "";
            
            const currentDetails = state.roundDetails[r] || {};
            state.players.forEach(p => {
                let o1 = document.createElement("option"); o1.value = p; o1.innerText = p;
                let o2 = document.createElement("option"); o2.value = p; o2.innerText = p;
                if(currentDetails.dealer === p) o1.selected = true;
                if(currentDetails.announcer === p) o2.selected = true;
                dSelect.appendChild(o1); aSelect.appendChild(o2);
            });

            const inputContainer = document.getElementById("edit-dynamic-inputs");
            inputContainer.innerHTML = "";
            const roundScores = state.scores[r] || {};
            state.players.forEach(p => {
                let div = document.createElement("div");
                div.className = "score-box";
                let val = roundScores[p] !== undefined ? roundScores[p] : 0;
                div.innerHTML = `<label>${p}</label><input type="number" id="edit_input_${p}" value="${val}">`;
                inputContainer.appendChild(div);
            });
        }

        function saveEditedRound() {
            const r = document.getElementById("edit-round-select").value;
            if (!r) return;

            const dealer = document.getElementById("edit-dealer-select").value;
            const announcer = document.getElementById("edit-announcer-select").value;

            state.roundDetails[r] = { dealer: dealer, announcer: announcer };

            state.players.forEach(p => {
                let val = parseInt(document.getElementById(`edit_input_${p}`).value);
                state.scores[r][p] = isNaN(val) ? 0 : val;
            });

            saveToLocalStorage();
            pushToCloud();
            alert(r + " skorları başarıyla güncellendi!");
            renderGame();
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
            renderGame(true);
        }

        function undoLastRound() {
            if (state.completedRounds.length === 0) return;
            if (confirm("En son girilen turun skorlarını silip geri almak istediğinize emin misiniz?")) {
                let last = state.completedRounds.pop();
                delete state.roundDetails[last];
                state.players.forEach(p => { state.scores[last][p] = 0; });
                saveToLocalStorage();
                pushToCloud();
                window.location.reload();
            }
        }

        function renderTables() {
            let totals = {};
            state.players.forEach(p => totals[p] = 0);
            
            state.completedRounds.forEach(r => {
                state.players.forEach(p => {
                    totals[p] += (state.scores[r][p] || 0);
                });
            });

            let lastRound = state.completedRounds[state.completedRounds.length - 1] || null;

            const summaryBody = document.getElementById("summary-body");
            summaryBody.innerHTML = "";
            
            let minScore = Math.min(...state.players.map(p => totals[p]));

            state.players.forEach(p => {
                let thisRoundScore = lastRound ? (state.scores[lastRound][p] || 0) : 0;
                let tr = document.createElement("tr");
                let isWinnerBadge = (totals[p] === minScore && state.completedRounds.length > 0) ? " <span class='badge'>1.</span>" : "";
                tr.innerHTML = `<td><strong>${p}</strong>${isWinnerBadge}</td><td>${thisRoundScore}</td><td style="font-weight:bold; color:${totals[p] > 150 ? '#E63946' : '#31333F'}">${totals[p]}</td>`;
                summaryBody.appendChild(tr);
            });

            const hHeaders = document.getElementById("history-headers");
            hHeaders.innerHTML = "<th>Yazboz Turları</th><th>Dağıtan</th><th>Biten</th>";
            state.players.forEach(p => {
                let th = document.createElement("th"); th.innerText = p;
                hHeaders.appendChild(th);
            });

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
                localStorage.clear();
                sessionStorage.clear();

                state = {
                    initialized: false,
                    players: [],
                    completedRounds: [],
                    roundDetails: {},
                    scores: {}
                };

                fetch(API_URL + "?puanla=" + encodeURIComponent(JSON.stringify({ initialized: false })) + "&t=" + new Date().getTime())
                .then(() => {
                    setTimeout(() => {
                        window.location.reload();
                    }, 500);
                })
                .catch(() => {
                    window.location.reload();
                });
            }
        }

        window.onload = loadFromLocalStorage;
        setInterval(fetchFromCloud, 7000);
    </script>
</body>
</html>
""".replace("/*CLOUD_STATE_B64*/", cloud_b64)

# HTML Motorunu ekrana gömüyoruz
components.html(HTML_ENGINE, height=1000, scrolling=True)
