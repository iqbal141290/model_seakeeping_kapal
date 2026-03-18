import streamlit as st
import joblib
import pandas as pd

# Judul Aplikasi
st.title("🚢 Sistem Monitor Seakeeping")

# Load Model (Pastikan file .sav sudah di-upload ke GitHub juga)
model = joblib.load('model_seakeeping_kapal.sav')

# Input Slider
w = st.slider("Tinggi Gelombang (m)", 0.0, 5.0, 1.5)
s = st.slider("Kecepatan (Knot)", 0, 20, 10)
h = st.slider("Heading (Deg)", 0, 180, 90)

# Prediksi
df_in = pd.DataFrame([[w, s, h]], columns=['Wave_m', 'Speed_Knot', 'Heading_deg'])
res = model.predict(df_in)

# Output
st.metric("Prediksi Roll", f"{res[0][2]:.2f} °")
if res[0][2] > 3.0:
    st.error("🚨 BAHAYA!")
else:
    st.success("✅ AMAN")