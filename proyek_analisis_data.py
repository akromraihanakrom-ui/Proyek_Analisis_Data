
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Bike Sharing – Dashboard", layout="wide")

# ---------- Data loader (shared with Colab) ----------
BASE_DIR = Path(__file__).resolve().parent
DAY_CSV  = BASE_DIR / "dataset" / "day.csv"
HOUR_CSV = BASE_DIR / "dataset" / "hour.csv"

@st.cache_data(show_spinner=False)
def load_data():
    day  = pd.read_csv(DAY_CSV)
    hour = pd.read_csv(HOUR_CSV)
    # basic fixes
    day['dteday']  = pd.to_datetime(day['dteday'])
    hour['dteday'] = pd.to_datetime(hour['dteday'])
    return day, hour

try:
    day, hour = load_data()
except FileNotFoundError as e:
    st.error(f"{e}. Pastikan folder 'dataset' berisi day.csv & hour.csv ada di sebelah file .py.")
    st.stop()

# ---------- Header ----------
st.title("Proyek Analisis Data: Bike Sharing")
st.caption("Nama: **Muhamad Akrom Raihan** · Email: **akromraihanakrom@gmail.com** · ID Dicoding: **b25b9d035**")

# ---------- Sidebar Filters ----------
min_date, max_date = day['dteday'].min(), day['dteday'].max()
with st.sidebar:
    st.header("Filter")
    dr = st.date_input("Rentang tanggal (day.csv)",
                       value=(min_date, max_date),
                       min_value=min_date, max_value=max_date)
    if isinstance(dr, tuple) and len(dr)==2:
        day_f = day[(day['dteday']>=pd.to_datetime(dr[0])) & (day['dteday']<=pd.to_datetime(dr[1]))]
    else:
        day_f = day.copy()

# ---------- KPIs ----------
total_cnt = int(day_f['cnt'].sum())
avg_day   = float(day_f['cnt'].mean())
reg_share = (day_f['registered'].sum() / max(1, day_f['cnt'].sum())) * 100
c1, c2, c3 = st.columns(3)
c1.metric("Total Sewa (rentang terpilih)", f"{total_cnt:,}")
c2.metric("Rata-rata / Hari", f"{avg_day:,.0f}")
c3.metric("Proporsi Registered", f"{reg_share:,.1f}%")

# ---------- Charts ----------
st.subheader("Tren Harian (cnt)")
day_plot = day_f[['dteday','cnt']].set_index('dteday').sort_index()
st.line_chart(day_plot, height=260)

st.subheader("Rata-rata Sewa per Jam (hour.csv)")
hour_avg = hour.groupby('hr', as_index=False)['cnt'].mean()
hour_avg = hour_avg.sort_values('hr')
st.bar_chart(hour_avg.set_index('hr'), height=260)

with st.expander("Informasi Data & Korelasi Singkat"):
    st.write("Ukuran data: day =", day.shape, "| hour =", hour.shape)
    st.write("Missing values (day):", dict(day.isna().sum()))
    st.write("Missing values (hour):", dict(hour.isna().sum()))
    corr_day = day.select_dtypes(include=[np.number]).corr()['cnt'].sort_values(ascending=False).head(8)
    corr_hour = hour.select_dtypes(include=[np.number]).corr()['cnt'].sort_values(ascending=False).head(8)
    st.write("Top korelasi (day → cnt):")
    st.dataframe(corr_day.to_frame())
    st.write("Top korelasi (hour → cnt):")
    st.dataframe(corr_hour.to_frame())

st.success("Dashboard siap. Gunakan sidebar untuk filter tanggal. Pastikan struktur folder sesuai ketentuan submission.")
