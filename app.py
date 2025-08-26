import streamlit as st
from pathlib import Path
import base64
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Ortec Solar Sürücü Hesaplama Modülü", page_icon="🌞", layout="centered")

# ========================
# LOGO (en üstte, ortalı)
# ========================
local_logo = Path("logo.png")

def show_centered_image(img_path: Path, width: int = 250):
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image(str(img_path), use_container_width=False, width=width)

if local_logo.exists():
    show_centered_image(local_logo, width=250)
else:
    st.warning("Logo bulunamadı. 'logo.png' dosyasını app.py ile aynı klasöre kopyalayabilirsin.")

st.title("🌞 Ortec Solar Sürücü Hesaplama Modülü")
st.markdown("VOC, Pm, K ve Pp değerlerini girin. Aşağıdaki **Sistem 1–5** blokları Excel’deki hesaplara göre çalışır.")

# ========================
# GİRİŞLER (varsayılanlar)
# ========================
with st.form("inputs"):
    col1, col2 = st.columns(2)
    with col1:
        voc = st.number_input("Voc (Panel Açık Devre Voltajı)", min_value=0.0, step=0.1, format="%.2f", value=49.6)
        k   = st.number_input("K (Güvenlik Katsayısı)", min_value=0.0, step=0.1, format="%.2f", value=1.5)
    with col2:
        pm  = st.number_input("Pm (Panel Watt)", min_value=0.0, step=0.1, format="%.2f", value=550.0)
        pp  = st.number_input("Pp (Pompa Gücü)", min_value=0.0, step=0.1, format="%.2f", value=0.0)

    submitted = st.form_submit_button("Hesapla")

# ========================
# HESAP FONKSİYONU
# ========================
def hesapla_sistem(voc, pm, k, pp, taban):
    N = round(taban / voc) if voc > 0 else 0
    S = round(((k * pp) / (pm * N)) + 0.4) if (pm > 0 and N > 0) else 0
    Pf = voc * N
    Vtoc = N * S * pm
    Kf = round(Vtoc / pp, 2) if pp > 0 else 0
    return {"N": N, "S": S, "Pf": Pf, "Vtoc": Vtoc, "Kf": Kf}

# ========================
# SİSTEMLER
# ========================
sistemler = [
    ("220V Pompa", 420),
    ("380V - 1. Seçenek", 662),
    ("380V - 2. Seçenek", 700),
    ("380V - 3. Seçenek", 720),
    ("440V Pompa", 720),
]

# ========================
# HESAPLA ve GÖRÜNTÜLE
# ========================
if submitted:
    results = []
    for ad, taban in sistemler:
        r = hesapla_sistem(voc, pm, k, pp, taban)
        results.append((ad, taban, r))

    tabs = st.tabs([ad for ad, _ in sistemler])
    for tab, (ad, taban, r) in zip(tabs, results):
        with tab:
            if voc <= 0 or pm <= 0:
                st.warning("Lütfen **Voc** ve **Pm** için 0'dan büyük değerler girin.")
            else:
                st.subheader(f"{ad} – Hesap Sonuçları (Taban: {taban})")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("N (Bir stringdeki panel sayısı)", value=r["N"])
                    st.metric("Pf (Toplam kurulu panel gücü)", value=f"{r['Pf']:.2f}")
                    st.metric("Kf (Kurulu güç katsayısı)", value=f"{r['Kf']:.2f}")
                with c2:
                    st.metric("S (String sayısı)", value=r["S"])
                    st.metric("Vtoc (Her string için toplam)", value=f"{r['Vtoc']:.2f}")

    # Toplu tablo + EXCEL indir (sekmelerin dışında)
    rows = []
    for ad, taban, r in results:
        rows.append({
            "Sistem": ad, "Taban": taban, "Voc": voc, "Pm": pm, "K": k, "Pp": pp,
            "N": r["N"], "S": r["S"], "Pf": r["Pf"], "Vtoc": r["Vtoc"], "Kf": r["Kf"],
        })

    df = pd.DataFrame(rows, columns=["Sistem","Taban","Voc","Pm","K","Pp","N","S","Pf","Vtoc","Kf"])
    st.markdown("### Tüm Sistemler Özeti")
    st.dataframe(df, use_container_width=True)

    buffer = BytesIO()
    try:
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Hesap Özeti")
            worksheet = writer.sheets["Hesap Özeti"]
            for i, col in enumerate(df.columns):
                width = max(12, min(40, int(df[col].astype(str).map(len).max() if not df.empty else 12) + 2))
                worksheet.set_column(i, i, width)
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    except Exception:
        # xlsxwriter yoksa openpyxl ile deneyelim
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Hesap Özeti")
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    st.download_button(
        label="Excel indir",
        data=buffer.getvalue(),
        file_name="ortec_solar_hesap_ozet.xlsx",
        mime=mime,
        key="download_xlsx",
    )
else:
    tabs = st.tabs([ad for ad, _ in sistemler])
    for (ad, taban), tab in zip(sistemler, tabs):
        with tab:
            st.info(f"{ad} için taban: **{taban}**. Üstteki formdan değerleri girip **Hesapla**'ya basın.")

# ========================
# ALT BAŞLIK
# ========================
# ========================
# ALT BAŞLIK
# ========================
st.markdown("---")
st.markdown("<h6 style='text-align:center;'>Ortec Solar</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align:center;'>www.enerjitoptan.com</h6>", unsafe_allow_html=True)
