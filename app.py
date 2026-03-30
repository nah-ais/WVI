import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi Halaman
st.set_page_config(page_title="WVI Dashboard - Topic Modeling", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('Data_WVI_Dashboard_Final.csv')
    # Membuat Label Topik berdasarkan ID (Langkah 2 Blueprint)
    topic_map = {
        0: "Keluhan Kesehatan Fisik",
        1: "Kerusakan Infrastruktur (Garoga)",
        2: "Dampak Psikososial & Trauma",
        3: "Dampak Aktivitas Harian",
        4: "Kesehatan & Kecemasan Harian",
        5: "Kebutuhan Logistik & Konsumsi"
    }
    df['Topik Label'] = df['topic_id'].map(topic_map)
    return df

df = load_data()

# --- SIDEBAR FILTER (SLICER) ---
st.sidebar.header("Filter Data")
wilayah_filter = st.sidebar.multiselect("Pilih Wilayah", options=df['Wilayah'].unique(), default=df['Wilayah'].unique())
gender_filter = st.sidebar.multiselect("Jenis Kelamin", options=df['Jenis Kelamin'].unique(), default=df['Jenis Kelamin'].unique())

# Terapkan Filter
df_selection = df[df['Wilayah'].isin(wilayah_filter) & df['Jenis Kelamin'].isin(gender_filter)]

# --- HEADER ---
st.title("📊 Dashboard WVI — Topic Modeling Bencana Banjir")
st.markdown(f"**{len(df_selection)} respons** · {', '.join(wilayah_filter)}")

# --- TABEL NAVIGASI (Sesuai HTML) ---
tab1, tab2, tab3, tab4 = st.tabs(["Ringkasan", "Distribusi Topik", "Demografi", "Wilayah"])

# --- TAB 1: RINGKASAN ---
with tab1:
    # KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Responden", len(df_selection))
    
    top_topic = df_selection['Topik Label'].value_counts().idxmax()
    top_val = df_selection['Topik Label'].value_counts().max()
    c2.metric("Topik Terbesar", top_topic, f"{top_val} respons")
    
    c3.metric("Kelompok Usia", f"{df_selection['Umur'].nunique()} Kelompok", "8-17 Tahun")
    c4.metric("Total Topik Utama", df_selection['topic_id'].nunique())

    st.divider()

    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Distribusi Topik Utama")
        fig_bar = px.bar(
            df_selection['Topik Label'].value_counts().reset_index(),
            x='count', y='Topik Label', orientation='h',
            color='Topik Label', color_discrete_sequence=px.colors.qualitative.Safe,
            labels={'count': 'Jumlah Respons', 'Topik Label': ''}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("Proporsi Topik")
        fig_pie = px.pie(df_selection, names='Topik Label', hole=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 3: DEMOGRAFI ---
with tab3:
    st.subheader("Analisis Berdasarkan Jenis Kelamin & Usia")
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        fig_gender = px.histogram(df_selection, x="Topik Label", color="Jenis Kelamin", barmode="group")
        st.plotly_chart(fig_gender, use_container_width=True)
        
    with col_d2:
        # Mengelompokkan umur (Opsional: sesuaikan dengan kategori di HTML)
        fig_age = px.box(df_selection, x="Topik Label", y="Umur", color="Topik Label")
        st.plotly_chart(fig_age, use_container_width=True)

# --- TAB 4: WILAYAH ---
with tab4:
    st.subheader("Heatmap Intensitas Topik per Wilayah")
    heatmap_data = pd.crosstab(df_selection['Wilayah'], df_selection['Topik Label'])
    fig_heat = px.imshow(heatmap_data, text_auto=True, aspect="auto", color_continuous_scale='GnBu')
    st.plotly_chart(fig_heat, use_container_width=True)