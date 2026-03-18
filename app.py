import streamlit as st
import joblib
import pandas as pd
import numpy as np

# 1. Judul Aplikasi
st.set_page_config(page_title="Seakeeping Monitor Iqbal", layout="wide")
st.title("🚢 Sistem Monitor Seakeeping Kapal")

# 2. Fungsi Load Model agar tidak berat saat dijalankan
@st.cache_resource
def load_model():
    return joblib.load('model_seakeeping_kapal.sav')

try:
    model = load_model()

    # 3. Input Sidebar
    st.sidebar.header("Input Data Kondisi")
    w = st.sidebar.slider("Tinggi Gelombang (m)", 0.5, 5.0, 1.5)
    s = st.sidebar.slider("Kecepatan Kapal (Knot)", 0, 20, 10)
    h = st.sidebar.slider("Heading (Derajat)", 0, 180, 90)

    # 4. Proses Prediksi
    # Pastikan nama kolom SAMA PERSIS dengan saat training
    df_in = pd.DataFrame([[w, s, h]], 
                        columns=['Wave_m', 'Speed_Knot', 'Heading_deg'])
    
    pred = model.predict(df_in)
    
    # Karena model kita multi-output (H, P, R)
    p_h, p_p, p_r = pred[0][0], pred[0][1], pred[0][2]

    # 5. Tampilan Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("Heave", f"{p_h:.2f} m")
    col2.metric("Pitch", f"{p_p:.2f} °")
    col3.metric("Roll", f"{p_r:.2f} °")

    # 6. Indikator Keselamatan
    if p_r > 3.0:
        st.error(f"🚨 STATUS: BAHAYA! Oleng ({p_r:.2f}°) melebihi batas 3°.")
    else:
        st.success(f"✅ STATUS: AMAN. Operasi dapat dilanjutkan.")

except Exception as e:
    st.error(f"Gagal memuat model atau data: {e}")
    st.info("Pastikan file 'model_seakeeping_kapal.sav' sudah ada di folder yang sama di GitHub.")
