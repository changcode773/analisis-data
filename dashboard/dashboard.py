import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style untuk visualisasi
sns.set_style("whitegrid")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    return df

df = load_data()

# Sidebar
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Dashboard Utama", "Data Overview"])

if page == "Dashboard Utama":
    # Header
    st.title("Dashboard Analisis Kualitas Udara")
    st.markdown("---")
    
    # Pertanyaan 1: Tahun dengan PM10 tertinggi
    st.header("1. Analisis PM10 per Tahun")
    
    # Hitung rata-rata PM10 per tahun
    pm10_per_year = df.groupby('year')['PM10'].mean().reset_index()
    
    # Cari tahun dengan PM10 tertinggi
    max_year = pm10_per_year.loc[pm10_per_year['PM10'].idxmax()]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=pm10_per_year, x='year', y='PM10', palette='viridis', ax=ax)
        ax.set_title('Rata-rata PM10 per Tahun')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Rata-rata PM10')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        st.metric(
            label="Tahun dengan PM10 Tertinggi",
            value=f"{int(max_year['year'])}",
            help=f"Rata-rata PM10: {max_year['PM10']:.2f}"
        )
        st.write(f"**Rata-rata PM10:** {max_year['PM10']:.2f}")
        st.write("**Insight:** Pada tahun 2015, nilai PM10 mencapai puncak tertinggi, menunjukkan kondisi kualitas udara yang paling buruk dalam periode pengamatan.")

    # Pertanyaan 2: Jam dengan PM10 tertinggi di tahun 2015
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
        sns.lineplot(data=pm10_per_hour_2015, x='hour', y='PM10', marker='o', ax=ax2)
        ax2.set_title('Rata-rata PM10 per Jam (Tahun 2015)')
        ax2.set_xlabel('Jam')
        ax2.set_ylabel('Rata-rata PM10')
        ax2.set_xticks(range(0, 24))
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
    
    with col4:
        st.metric(
            label="Jam dengan PM10 Tertinggi (2015)",
            value=f"{int(max_hour['hour'])}:00",
            help=f"Rata-rata PM10: {max_hour['PM10']:.2f}"
        )
        st.write(f"**Rata-rata PM10:** {max_hour['PM10']:.2f}")
        st.write("**Insight:** Polusi PM10 cenderung meningkat di malam hari, dengan puncak terjadi pada jam 11 malam.")

    # Additional insights
    st.markdown("---")
    st.header("Insights Tambahan")
    
    col5, col6 = st.columns(2)
    
    with col5:
        # Tren PM10 bulanan tahun 2015
        st.subheader("Tren PM10 Bulanan 2015")
        pm10_monthly_2015 = df_2015.groupby('month')['PM10'].mean()
        
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        pm10_monthly_2015.plot(kind='line', marker='o', ax=ax3)
        ax3.set_title('Tren PM10 Bulanan 2015')
        ax3.set_xlabel('Bulan')
        ax3.set_ylabel('Rata-rata PM10')
        ax3.set_xticks(range(1, 13))
        ax3.grid(True, alpha=0.3)
        st.pyplot(fig3)
    
    with col6:
        # Perbandingan PM2.5 dan PM10
        st.subheader("Korelasi PM2.5 vs PM10")
        fig4, ax4 = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df.sample(1000), x='PM2.5', y='PM10', alpha=0.6, ax=ax4)
        ax4.set_title('Korelasi PM2.5 dan PM10')
        st.pyplot(fig4)

elif page == "Data Overview":
    st.title("Overview Data")
    
    st.header("Sample Data")
    st.dataframe(df.head(10))
    
    st.header("Statistik Deskriptif")
    st.dataframe(df.describe())
    
    st.header("Informasi Dataset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Jumlah Data")
        st.metric("Total Records", len(df))
        st.metric("Total Kolom", len(df.columns))
    
    with col2:
        st.subheader("Missing Values")
        missing_data = df.isnull().sum()
        st.dataframe(missing_data[missing_data > 0])
    
    st.header("Distribusi Stasiun")
    st.write(f"Stasiun: {df['station'].unique()}")

# Footer
st.markdown("---")
st.markdown(
    "**Dashboard Analisis Kualitas Udara** | "
    "Data: PRSA Guanyuan 2013-2017 | "
    "Dibuat dengan Streamlit"
)