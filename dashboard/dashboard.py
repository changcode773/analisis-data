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

# Analisis PM10 per Tahun
st.header("1. Analisis PM10 per Tahun")

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
        help=f"Rata-rata PM10: {max_year['PM10']:.2f} μg/m³"
    )
    st.write(f"**Rata-rata PM10:** {max_year['PM10']:.2f} μg/m³")

# Analisis PM10 per Jam
st.header("2. Analisis PM10 per Jam (Tahun 2015)")

# Filter data untuk tahun 2015
df_2015 = df[df['year'] == 2015]

# Hitung rata-rata PM10 per jam
pm10_per_hour_2015 = df_2015.groupby('hour')['PM10'].mean().reset_index()

# Cari jam dengan PM10 tertinggi
max_hour = pm10_per_hour_2015.loc[pm10_per_hour_2015['PM10'].idxmax()]

col3, col4 = st.columns([2, 1])

with col3:
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=pm10_per_hour_2015, x='hour', y='PM10', marker='o', linewidth=2.5, ax=ax2)
    ax2.set_title('Rata-rata PM10 per Jam (Tahun 2015)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Jam')
    ax2.set_ylabel('Rata-rata PM10 (μg/m³)')
    ax2.set_xticks(range(0, 24))
    ax2.grid(True, alpha=0.3)
    
    # Highlight titik tertinggi
    ax2.plot(max_hour['hour'], max_hour['PM10'], 'ro', markersize=8, label='Titik Tertinggi')
    ax2.legend()
    
    st.pyplot(fig2)

with col4:
    st.metric(
        label="Jam dengan PM10 Tertinggi (2015)",
        value=f"{int(max_hour['hour'])}:00",
        help=f"Rata-rata PM10: {max_hour['PM10']:.2f} μg/m³"
    )
    st.write(f"**Rata-rata PM10:** {max_hour['PM10']:.2f} μg/m³")

# Footer
st.markdown("---")