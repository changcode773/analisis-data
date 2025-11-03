# Setup Environment - Anaconda
conda create --name main-ds python=3.13

conda activate main-ds

pip install -r requirements.txt

# Run steamlit app
Arahkan ke direktori dashboard terlebih dahulu (cd dashboard)
streamlit run dashboard.py