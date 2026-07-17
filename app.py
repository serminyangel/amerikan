import streamlit as st
import streamlit.components.v1 as components

# Sayfa başlığı ve ikon ayarları
st.set_page_config(page_title="Amerikan 5", page_icon="🃏", layout="centered")

# CSS ile Streamlit'in kendi boşluklarını sıfırlayalım ki arayüz tam otursun
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 0rem; }
        iframe { background-color: transparent; }
    </style>
""", unsafe_allow_html=True)

# Hazırladığımız HTML ve JavaScript arayüzünü Python metni olarak buraya gömüyoruz
html_content = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amerikan 5 - Canlı Skor Tahtası</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style>
        body { font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen flex flex-col items-center p-2">

    <!-- Üst Başlık -->
    <div class="w-full max-w-md text-center my-4">
        <h1 class="text-3xl font-extrabold text-emerald-400 tracking-wide uppercase">Amerikan 5</h1>
        <p class="text-xs text-slate-400 mt-1">Canlı Skor Takip Sistemi</p>
    </div>

    <!-- Canlı Skor Tablosu -->
    <div class="w-full max-w-md bg-slate-800 rounded-2xl shadow-xl border border-slate-700/50 p-5 mb-5">
        <div class="flex justify-between items-center mb-4 border-b border-slate-700 pb-3">
            <h2 class="text-lg font-bold text-slate-200 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Anlık Durum
            </h2>
            <button onclick="skorlariGetir()" class="text-xs bg-slate-700 hover:bg-slate-600 px-3 py-1.5 rounded-lg font-medium transition active:scale-95">
                Yenile ↻
            </button>
        </div>

        <div id="loading" class="text-center py-8 text-slate-400 text-sm">
            Skorlar Google Sheets'ten çekiliyor...
        </div>

        <div id="tableContainer" class="hidden overflow-hidden rounded-xl border border-slate-750">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-750 text-slate-300 text-xs font-bold uppercase tracking-wider">
                        <th class="p-3">Oyuncu</th>
                        <th class="p-3 text-right">Toplam Skor</th>
                    </tr>
                </thead>
                <tbody id="skorGövdesi" class="divide-y divide-slate-700/50 text-sm">
                    <!-- Google Sheets verileri buraya dolacak -->
                </tbody>
            </table>
        </div>
    </div>

    <!-- Şifreli Yönetici Giriş Paneli -->
    <div class="w-full max-w-md bg-slate-800 rounded-2xl shadow-xl border border-slate-700/50 p-5">
        <div id="adminGirisAlani">
            <h3 class="text-sm font-semibold text-slate-400 mb-3">Skor Girişi Yap (Sadece Yönetici)</h3>
            <div class="flex gap-2">
                <input type="password" id="pinKodu" placeholder="PIN Kodu Girin" class="bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm w-full focus:outline-none focus:border-emerald-500 transition text-white">
                <button onclick="adminDogrula()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 rounded-xl font-bold text-sm transition active:scale-95 whitespace-nowrap">
                    Paneli Aç
                </button>
            </div>
        </div>

        <!-- Şifre Doğruysa Açılacak Gizli Skor Ekleme Formu -->
        <div id="skorEklemeAlani" class="hidden">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-sm font-bold text-emerald-400">Yönetici Paneli Aktif</h3>
                <button onclick="paneliKapat()" class="text-xs text-rose-400 hover:underline">Paneli Kilitle</button>
            </div>
            <div class="space-y-3">
                <div>
                    <label class="block text-xs text-slate-400 mb-1">Oyuncu İsmi</label>
                    <input type="text" id="oyuncuAd" placeholder="Örn: Mecit" class="bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm w-full focus:outline-none focus:border-emerald-500 text-white">
                </div>
                <div>
                    <label class="block text-xs text-slate-400 mb-1">Eklenecek Skor (Ceza Puanı)</label>
                    <input type="number" id="oyuncuSkor" placeholder="Örn: 45" class="bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm w-full focus:outline-none focus:border-emerald-500 text-white">
                </div>
                <button onclick="skorGonder()" id="gonderBtn" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white py-3 rounded-xl font-bold text-sm transition active:scale-95 shadow-lg shadow-emerald-900/20 mt-2">
                    Skoru Tabloya İşle
                </button>
            </div>
        </div>
    </div>

    <!-- Haberleşme Scriptleri -->
    <script>
        const API_URL = "https://script.google.com/macros/s/AKfycbxZp2bpoN25mqjukeUehUcovMbeBi9nfEK2z4AsrqusFNOXsdWbRt1xkbG8V5zBZjBv/exec";
        const ADMIN_PIN = "1905"; 

        window.onload = function() {
            skorlariGetir();
        };

        function skorlariGetir() {
            const loadingDiv = document.getElementById("loading");
            const tableContainer = document.getElementById("tableContainer");
            const skorGövdesi = document.getElementById("skorGövdesi");

            loadingDiv.classList.remove("hidden");
            tableContainer.classList.add("hidden");

            fetch(API_URL)
                .then(response => response.json())
                .then(data => {
                    skorGövdesi.innerHTML = "";
                    if(data && data.length > 0) {
                        data.forEach(satir => {
                            const tr = document.createElement("tr");
                            tr.className = "hover:bg-slate-750/50 transition";
                            tr.innerHTML = `
                                <td class="p-3 font-medium text-slate-200">${satir.oyuncu}</td>
                                <td class="p-3 text-right font-bold ${satir.skor > 100 ? 'text-rose-400' : 'text-emerald-400'}">${satir.skor}</td>
                            `;
                            skorGövdesi.appendChild(tr);
                        });
                        loadingDiv.classList.add("hidden");
                        tableContainer.classList.remove("hidden");
                    } else {
                        loadingDiv.innerText = "Tabloda henüz kayıtlı skor bulunamadı.";
                    }
                })
                .catch(error => {
                    console.error("Hata:", error);
                    loadingDiv.innerText = "Skorlar çekilemedi! İnterneti veya Google dağıtım ayarını kontrol edin.";
                });
        }

        function adminDogrula() {
            const pinInput = document.getElementById("pinKodu").value;
            if(pinInput === ADMIN_PIN) {
                document.getElementById("adminGirisAlani").classList.add("hidden");
                document.getElementById("skorEklemeAlani").classList.remove("hidden");
                document.getElementById("pinKodu").value = "";
            } else {
                alert("Hatalı PIN Kodu! Masada sadece yönetici skor girebilir.");
            }
        }

        function paneliKapat() {
            document.getElementById("adminGirisAlani").classList.remove("hidden");
            document.getElementById("skorEklemeAlani").classList.add("hidden");
        }

        function skorGonder() {
            const isim = document.getElementById("oyuncuAd").value.trim();
            const skor = document.getElementById("oyuncuSkor").value.trim();
            const btn = document.getElementById("gonderBtn");

            if(!isim || !skor) {
                alert("Lütfen isim ve skor alanlarını boş bırakmayın!");
                return;
            }

            btn.disabled = true;
            btn.innerText = "Veri Tabloya Yazılıyor...";
            btn.className = "w-full bg-slate-600 text-slate-400 py-3 rounded-xl font-bold text-sm cursor-not-allowed mt-2";

            const veriPaketi = {
                oyuncu: isim,
                skor: parseInt(skor)
            };

            fetch(API_URL, {
                method: "POST",
                mode: "no-cors",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(veriPaketi)
            })
            .then(() => {
                alert(isim + " için " + skor + " puan başarıyla gönderildi!");
                document.getElementById("oyuncuAd").value = "";
                document.getElementById("oyuncuSkor").value = "";
                
                btn.disabled = false;
                btn.innerText = "Skoru Tabloya İşle";
                btn.className = "w-full bg-emerald-600 hover:bg-emerald-500 text-white py-3 rounded-xl font-bold text-sm transition active:scale-95 shadow-lg shadow-emerald-900/20 mt-2";
                
                setTimeout(skorlariGetir, 1500);
            })
            .catch(error => {
                console.error("Gönderim Hatası:", error);
                alert("Skor gönderilemedi, bir hata oluştu.");
                btn.disabled = false;
                btn.innerText = "Skoru Tabloya İşle";
                btn.className = "w-full bg-emerald-600 hover:bg-emerald-500 text-white py-3 rounded-xl font-bold text-sm transition active:scale-95 mt-2";
            });
        }
    </script>
</body>
</html>
"""

# Streamlit üzerinden paketimizi ekrana basıyoruz
components.html(html_content, height=800, scrolling=True)
