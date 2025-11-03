import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style untuk visualisasi
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    return df

df = load_data()

# Header
st.title("Dashboard Analisis Kualitas Udara")
st.markdown("Dashboard ini menganalisis pola polusi PM10 berdasarkan data kualitas udara historis.")
st.markdown("---")

# Buat tab untuk berbagai analisis PM10
tab1, tab2, tab3 = st.tabs([
    "📊 Analisis PM10 per Tahun", 
    "📈 Analisis PM10 per Bulan", 
    "⏰ Analisis PM10 per Jam"
])

# TAB 1: Analisis PM10 per Tahun
with tab1:
    st.header("Analisis PM10 per Tahun")
    
    # Hitung rata-rata PM10 per tahun
    pm10_per_year = df.groupby('year')['PM10'].mean().reset_index()

    # Cari tahun dengan PM10 tertinggi
    max_year = pm10_per_year.loc[pm10_per_year['PM10'].idxmax()]

    col1, col2 = st.columns([2, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = sns.barplot(data=pm10_per_year, x='year', y='PM10', palette='viridis', ax=ax)
        ax.set_title('Rata-rata PM10 per Tahun', fontsize=14, fontweight='bold')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Rata-rata PM10 (μg/m³)')
        
        #nilai di atas setiap bar
        for i, v in enumerate(pm10_per_year['PM10']):
            ax.text(i, v + 0.5, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.metric(
            label="Tahun dengan PM10 Tertinggi",
            value=f"{int(max_year['year'])}",
        )
        st.write(f"**Rata-rata PM10:** {max_year['PM10']:.2f} μg/m³")
        
        min_year = pm10_per_year.loc[pm10_per_year['PM10'].idxmin()]
        st.metric(
            label="Tahun dengan PM10 Terendah",
            value=f"{int(min_year['year'])}",
        )
        st.write(f"**Rata-rata PM10:** {min_year['PM10']:.2f} μg/m³")

# TAB 2: Analisis PM10 per Bulan (Fitur Interaktif)
with tab2:
    st.header("Analisis PM10 per Bulan")
    st.markdown("Gunakan fitur interaktif di bawah untuk menganalisis pola PM10 berdasarkan bulan pada tahun tertentu.")

    # Untuk memilih tahun
    col_selector1, col_selector2 = st.columns([1, 3])
    
    with col_selector1:
        tahun_terpilih = st.selectbox(
            "Pilih Tahun:",
            options=sorted(df['year'].unique()),
            index=len(df['year'].unique()) - 1  # Default pilih tahun terakhir
        )

    # Filter data berdasarkan tahun yang dipilih
    df_tahun_terpilih = df[df['year'] == tahun_terpilih]

    # Hitung rata-rata PM10 per bulan
    pm10_per_bulan = df_tahun_terpilih.groupby('month')['PM10'].mean().reset_index()

    # Konversi angka bulan ke nama bulan
    nama_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    pm10_per_bulan['nama_bulan'] = pm10_per_bulan['month'].apply(lambda x: nama_bulan[x-1])

    # Cari bulan dengan PM10 tertinggi dan terendah
    max_bulan = pm10_per_bulan.loc[pm10_per_bulan['PM10'].idxmax()]
    min_bulan = pm10_per_bulan.loc[pm10_per_bulan['PM10'].idxmin()]

    col3, col4 = st.columns([2, 1])

    with col3:
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        
        # Grafik batang dengan warna berbeda untuk bulan tertinggi
        colors = ['skyblue' if x != max_bulan['month'] else 'red' for x in pm10_per_bulan['month']]
        bars = ax2.bar(pm10_per_bulan['nama_bulan'], pm10_per_bulan['PM10'], color=colors, alpha=0.7)
        
        ax2.set_title(f'Rata-rata PM10 per Bulan ({tahun_terpilih})', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Bulan')
        ax2.set_ylabel('Rata-rata PM10 (μg/m³)')
        ax2.grid(True, alpha=0.3)
        
        # Tambahkan nilai di atas setiap bar
        for i, v in enumerate(pm10_per_bulan['PM10']):
            ax2.text(i, v + 0.5, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    with col4:
        st.subheader(f"Statistik {tahun_terpilih}")
        
        st.metric(
            label="Bulan dengan PM10 Tertinggi",
            value=max_bulan['nama_bulan'],
            delta=f"{max_bulan['PM10']:.1f} μg/m³"
        )
        
        st.metric(
            label="Bulan dengan PM10 Terendah",
            value=min_bulan['nama_bulan'],
            delta=f"{min_bulan['PM10']:.1f} μg/m³"
        )
        
        # Rata-rata tahunan
        rata_rata_tahunan = pm10_per_bulan['PM10'].mean()
        st.metric(
            label="Rata-rata Tahunan",
            value=f"{rata_rata_tahunan:.1f} μg/m³"
        )
    
# TAB 3: Analisis PM10 per Jam
with tab3:
    st.header("Analisis PM10 per Jam")
    
    # Untuk memilih tahun (bisa dibuat interaktif juga)
    tahun_jam = st.selectbox(
        "Pilih Tahun untuk Analisis per Jam:",
        options=sorted(df['year'].unique()),
        key="tahun_jam_selector"
    )
    
    # Filter data untuk tahun yang dipilih
    df_tahun_jam = df[df['year'] == tahun_jam]

    # Hitung rata-rata PM10 per jam
    pm10_per_hour = df_tahun_jam.groupby('hour')['PM10'].mean().reset_index()

    # Cari jam dengan PM10 tertinggi
    max_hour = pm10_per_hour.loc[pm10_per_hour['PM10'].idxmax()]

    col5, col6 = st.columns([2, 1])

    with col5:
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=pm10_per_hour, x='hour', y='PM10', marker='o', linewidth=2.5, ax=ax3, color='green')
        ax3.set_title(f'Rata-rata PM10 per Jam (Tahun {tahun_jam})', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Jam')
        ax3.set_ylabel('Rata-rata PM10 (μg/m³)')
        ax3.set_xticks(range(0, 24))
        ax3.grid(True, alpha=0.3)
        
        # Highlight titik tertinggi
        ax3.plot(max_hour['hour'], max_hour['PM10'], 'ro', markersize=8, label='Titik Tertinggi')
        ax3.legend()
        
        # Area fill di bawah garis
        ax3.fill_between(pm10_per_hour['hour'], pm10_per_hour['PM10'], alpha=0.3, color='green')
        
        st.pyplot(fig3)

    with col6:
        st.metric(
            label=f"Jam dengan PM10 Tertinggi ({tahun_jam})",
            value=f"{int(max_hour['hour'])}:00",
            help=f"Rata-rata PM10: {max_hour['PM10']:.2f} μg/m³"
        )
        st.write(f"**Rata-rata PM10:** {max_hour['PM10']:.2f} μg/m³")
        
        # Jam dengan PM10 terendah
        min_hour = pm10_per_hour.loc[pm10_per_hour['PM10'].idxmin()]
        st.metric(
            label=f"Jam dengan PM10 Terendah ({tahun_jam})",
            value=f"{int(min_hour['hour'])}:00",
            help=f"Rata-rata PM10: {min_hour['PM10']:.2f} μg/m³"
        )

# Footer
st.markdown("---")