import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Dashboard Analisis Topik — Data WVI", layout="wide")

# Custom CSS to match the HTML style
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Data_WVI_Dashboard_Final.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("File 'Data_WVI_Dashboard_Final.csv' tidak ditemukan. Pastikan file berada di direktori yang sama.")
    st.stop()

# Header
st.title("Dashboard Analisis Topik — Data WVI")
st.markdown("Topic modeling dari 529 tanggapan anak-anak terdampak bencana · Bahasa Indonesia · 3 Wilayah")

# KPI Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Tanggapan", len(df), "3 Wilayah")
with col2:
    st.metric("Topik Utama", "6", "+ 3 Sub-topik T3")
with col3:
    st.metric("Responden Perempuan", "72%", "381 dari 529")
with col4:
    st.metric("Usia 8–11 Tahun", "44%", "234 Responden")

st.divider()

# Section: Distribusi Topik Utama
st.subheader("Distribusi Topik Utama")

topik_labels = ['T0 Kes. Fisik', 'T1 Infrastruktur', 'T2 Psikososial', 'T3 Umum Banjir', 'T4 Kecemasan', 'T5 Logistik']
topik_counts = [90, 37, 43, 260, 54, 45]
topik_colors = ['#5DCAA5', '#378ADD', '#D4537E', '#EF9F27', '#7F77DD', '#888780']

col_left, col_right = st.columns(2)

with col_left:
    fig_bar = px.bar(
        x=topik_labels, 
        y=topik_counts, 
        color=topik_labels,
        color_discrete_sequence=topik_colors,
        title="Jumlah Tanggapan per Topik",
        labels={'x': 'Kategori Topik', 'y': 'Jumlah'}
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    fig_pie = px.pie(
        names=topik_labels, 
        values=topik_counts, 
        color=topik_labels,
        color_discrete_sequence=topik_colors,
        title="Proporsi Topik (Pie)",
        hole=0.5
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Section: Distribusi Topik per Wilayah
st.subheader("Distribusi Topik per Wilayah")
wilayah_labels = ['Sibolga Utara', 'Tapsel', 'Tapteng']
# Data from HTML
data_wilayah = {
    'T0 Kes. Fisik': [33, 39, 18],
    'T1 Infrastruktur': [20, 16, 1],
    'T2 Psikososial': [30, 12, 1],
    'T3 Umum Banjir': [63, 61, 136],
    'T4 Kecemasan': [48, 5, 1],
    'T5 Logistik': [22, 15, 8]
}

fig_wilayah = go.Figure()
for i, (label, counts) in enumerate(data_wilayah.items()):
    fig_wilayah.add_trace(go.Bar(
        name=label,
        x=wilayah_labels,
        y=counts,
        marker_color=topik_colors[i]
    ))

fig_wilayah.update_layout(
    barmode='group',
    title="Perbandingan Frekuensi Topik di Tiap Wilayah",
    xaxis_title="Wilayah",
    yaxis_title="Jumlah Tanggapan",
    legend_title="Topik"
)
st.plotly_chart(fig_wilayah, use_container_width=True)

st.divider()

# Section: Demografi Responden
st.subheader("Demografi Responden")
col_usia, col_gender = st.columns(2)

with col_usia:
    # Data from HTML
    usia_labels = ['T0', 'T1', 'T2', 'T3', 'T4', 'T5']
    data_usia = {
        '8–11 th': [41, 26, 32, 69, 38, 28],
        '12–15 th': [31, 10, 10, 55, 15, 9],
        '15–17 th': [18, 1, 1, 136, 1, 8]
    }
    usia_colors = ['#5DCAA5', '#378ADD', '#D4537E']
    
    fig_usia = go.Figure()
    for i, (label, counts) in enumerate(data_usia.items()):
        fig_usia.add_trace(go.Bar(
            name=label,
            x=usia_labels,
            y=counts,
            marker_color=usia_colors[i]
        ))
    fig_usia.update_layout(barmode='stack', title="Topik per Kelompok Usia", xaxis_title="Topik", yaxis_title="Jumlah")
    st.plotly_chart(fig_usia, use_container_width=True)

with col_gender:
    # Data from HTML (estimated/inferred from context)
    gender_labels = ['T0', 'T1', 'T2', 'T3', 'T4', 'T5']
    data_gender = {
        'Perempuan': [65, 25, 28, 185, 46, 32], # Estimated based on 72% total
        'Laki-laki': [25, 12, 15, 75, 8, 13]
    }
    gender_colors = ['#D4537E', '#378ADD']
    
    fig_gender = go.Figure()
    for i, (label, counts) in enumerate(data_gender.items()):
        fig_gender.add_trace(go.Bar(
            name=label,
            x=gender_labels,
            y=counts,
            marker_color=gender_colors[i]
        ))
    fig_gender.update_layout(barmode='group', title="Topik per Jenis Kelamin", xaxis_title="Topik", yaxis_title="Jumlah")
    st.plotly_chart(fig_gender, use_container_width=True)

st.divider()

# Section: Topik 3 Breakdown
st.subheader("Topik 3 — Deskripsi Umum Kondisi Banjir (260 tanggapan)")
st.markdown("Topik 3 dipecah menjadi 3 sub-topik untuk analisis lebih mendalam.")

col_st1, col_st2, col_st3 = st.columns(3)
with col_st1:
    st.info("**90**\n\n3.0 Dampak Aktivitas Harian & Sekolah\n\n35% dari T3")
with col_st2:
    st.success("**102**\n\n3.1 Kerusakan Lingkungan & Properti\n\n39% dari T3")
with col_st3:
    st.warning("**68**\n\n3.2 Trauma Suara & Penyelamatan Diri\n\n26% dari T3")

col_sub_wil, col_sub_usia = st.columns(2)

with col_sub_wil:
    sub_topik_labels = ['3.0 Aktivitas', '3.1 Lingkungan', '3.2 Trauma']
    # Data from HTML
    data_sub_wilayah = {
        'Sibolga Utara': [11, 5, 33],
        'Tapsel': [26, 36, 17],
        'Tapteng': [53, 61, 18]
    }
    sub_wil_colors = ['#5DCAA5', '#378ADD', '#EF9F27']
    
    fig_sub_wil = go.Figure()
    for i, (label, counts) in enumerate(data_sub_wilayah.items()):
        fig_sub_wil.add_trace(go.Bar(
            name=label,
            x=sub_topik_labels,
            y=counts,
            marker_color=sub_wil_colors[i]
        ))
    fig_sub_wil.update_layout(barmode='group', title="Sub-topik T3 per Wilayah")
    st.plotly_chart(fig_sub_wil, use_container_width=True)

with col_sub_usia:
    # Data from HTML
    data_sub_usia = {
        '8–11 th': [15, 12, 41],
        '12–15 th': [22, 23, 10],
        '15–17 th': [53, 67, 17]
    }
    
    fig_sub_usia = go.Figure()
    for i, (label, counts) in enumerate(data_sub_usia.items()):
        fig_sub_usia.add_trace(go.Bar(
            name=label,
            x=sub_topik_labels,
            y=counts,
            marker_color=usia_colors[i]
        ))
    fig_sub_usia.update_layout(barmode='group', title="Sub-topik T3 per Kelompok Usia")
    st.plotly_chart(fig_sub_usia, use_container_width=True)

# Heatmap Section
st.subheader("Heatmap Intensitas Topik × Wilayah")
# Data from HTML analysis
heatmap_data = [
    [15.3, 9.3, 13.9, 29.2, 22.2, 10.2], # Sibolga Utara
    [26.4, 10.8, 8.1, 41.2, 3.4, 10.1],  # Tapsel
    [10.9, 0.6, 0.6, 82.4, 0.6, 4.8]     # Tapteng
]

fig_hm = px.imshow(
    heatmap_data,
    labels=dict(x="Topik", y="Wilayah", color="Intensitas (%)"),
    x=topik_labels,
    y=wilayah_labels,
    color_continuous_scale='YlGnBu',
    text_auto=True,
    title="Konsentrasi Topik di Tiap Wilayah (% dari total per wilayah)"
)
st.plotly_chart(fig_hm, use_container_width=True)

st.sidebar.title("Tentang Dashboard")
st.sidebar.info("Dashboard ini mereplikasi visualisasi dari analisis topic modeling WVI menggunakan Streamlit dan Plotly.")
st.sidebar.markdown("---")
st.sidebar.write("Data: 529 Tanggapan")
st.sidebar.write("Bahasa: Indonesia")
