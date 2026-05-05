import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("Dashboard Analisis Data Laptops - E-Commerce")

# Load data
df = pd.read_csv("laptops.csv")

# Preprocessing
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['no_of_ratings'] = pd.to_numeric(df['no_of_ratings'], errors='coerce')
df['no_of_reviews'] = pd.to_numeric(df['no_of_reviews'], errors='coerce')
df['price(in Rs.)'] = pd.to_numeric(df['price(in Rs.)'], errors='coerce')
df['display(in inch)'] = pd.to_numeric(df['display(in inch)'], errors='coerce')

df['rating'] = df['rating'].fillna(df['rating'].median())
df['no_of_ratings'] = df['no_of_ratings'].fillna(0)
df['no_of_reviews'] = df['no_of_reviews'].fillna(0)

df['processor_brand'] = df['processor'].str.split().str[0]
df['ram_gb'] = df['ram'].str.extract(r'(\d+)').astype(float)
df['storage_type'] = df['storage'].str.extract(r'(SSD|HDD)')
df['storage_gb'] = df['storage'].str.extract(r'(\d+)').astype(float)

# Sidebar untuk filtering
st.sidebar.header("Filter Data")

processor_brands = st.sidebar.multiselect("Pilih Processor Brand", df['processor_brand'].dropna().unique())

operating_systems = st.sidebar.multiselect("Pilih Sistem Operasi", df['os'].dropna().unique())

st.sidebar.subheader("Filter Rentang Harga")
min_price, max_price = int(df['price(in Rs.)'].min()), int(df['price(in Rs.)'].max())
price_range = st.sidebar.slider("Harga (Rp):", min_value=min_price, max_value=max_price, value=(min_price, max_price))

st.sidebar.subheader("Filter Rentang Rating")
min_rating, max_rating = 0.0, 5.0
rating_range = st.sidebar.slider("Rating:", min_value=min_rating, max_value=max_rating, value=(min_rating, max_rating))

# Apply filters
filtered_df = df[
    (df["processor_brand"].isin(processor_brands) if processor_brands else True) &
    (df["os"].isin(operating_systems) if operating_systems else True) &
    (df["price(in Rs.)"].between(price_range[0], price_range[1])) &
    (df["rating"].between(rating_range[0], rating_range[1]))
]

st.sidebar.write(f"Jumlah produk setelah filter: {len(filtered_df)}")

# 1. Dataset
st.header("1. Dataset yang digunakan")
st.write("Dataset ini berisi informasi tentang laptop yang dijual di platform E-Commerce, termasuk spesifikasi teknis, harga, dan ulasan pelanggan.")
st.write(f"Jumlah baris: {filtered_df.shape[0]}")
st.write(f"Jumlah kolom: {filtered_df.shape[1]}")

st.subheader("Informasi Variabel:")
st.write("- img_link: Link gambar produk")
st.write("- name: Nama laptop")
st.write("- price(in Rs.): Harga dalam Rupiah")
st.write("- processor: Tipe processor")
st.write("- ram: Kapasitas RAM")
st.write("- os: Sistem operasi")
st.write("- storage: Kapasitas penyimpanan")
st.write("- display(in inch): Ukuran layar dalam inch")
st.write("- rating: Rating rata-rata")
st.write("- no_of_ratings: Jumlah rating")
st.write("- no_of_reviews: Jumlah ulasan")

st.subheader("Preview Data:")
st.dataframe(filtered_df.head(10))

st.subheader("Tipe Data :")
st.write(filtered_df.dtypes)


# 2. Preprocessing Data
st.header("2. Preprocessing Data")
st.write("Preprocessing telah dilakukan: handling missing values, ekstraksi fitur processor_brand, ram_gb, storage_type, storage_gb.")

st.subheader("Data Setelah Preprocessing:")
st.dataframe(df.head(10))

# 3. Exploratory Data Analysis (EDA)
st.header("3. Exploratory Data Analysis")

st.subheader("Statistik Deskriptif:")
st.write(filtered_df.describe())

st.subheader("Insight Awal:")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rata-rata Harga", f"Rp {filtered_df['price(in Rs.)'].mean():,.0f}")
with col2:
    st.metric("Rata-rata Rating", f"{filtered_df['rating'].mean():.1f}")
with col3:
    st.metric("Total Produk", len(filtered_df))

# Distribusi OS
st.subheader("Distribusi Sistem Operasi:")
os_counts = filtered_df['os'].value_counts()
st.bar_chart(os_counts)

# Distribusi harga
st.subheader("Distribusi Processor Brand:")
processor_counts = filtered_df['processor_brand'].value_counts()
st.bar_chart(processor_counts)

# 4. Visualisasi Data
st.header("4. Visualisasi Data")

# Histogram Harga
st.subheader("Histogram Harga Laptop")
fig_hist_price = px.histogram(filtered_df, x='price(in Rs.)', nbins=20, title="Distribusi Harga Laptop")
st.plotly_chart(fig_hist_price)

# Scatter Plot: Harga vs Rating
st.subheader("Scatter Plot: Harga vs Rating")
fig_scatter = px.scatter(filtered_df, x='price(in Rs.)', y='rating', color='processor_brand', 
                        title="Hubungan Harga dan Rating Berdasarkan Processor")
st.plotly_chart(fig_scatter)

# Box Plot: Harga berdasarkan Processor Brand
st.subheader("Box Plot: Harga berdasarkan Processor Brand")
fig_box = px.box(filtered_df, x='processor_brand', y='price(in Rs.)', title="Distribusi Harga per Processor Brand")
st.plotly_chart(fig_box)

# Scatter Plot: RAM vs Harga
st.subheader("Scatter Plot: RAM vs Harga")
fig_scatter_ram = px.scatter(filtered_df, x='ram_gb', y='price(in Rs.)', color='rating', 
                            title="Hubungan RAM dan Harga dengan Rating")
st.plotly_chart(fig_scatter_ram)

# Bar Chart: Rata-rata Rating per OS
st.subheader("Rata-rata Rating per Sistem Operasi")
avg_rating_os = filtered_df.groupby('os')['rating'].mean().reset_index()
fig_bar_rating = px.bar(avg_rating_os, x='os', y='rating', title="Rata-rata Rating per OS")
st.plotly_chart(fig_bar_rating)

# 5. Temuan dan Interpretasi
st.header("5. Temuan dan Interpretasi")

st.subheader("Insight Utama:")
st.write("1. Harga dan Processor: Laptop dengan processor Intel Core i5 dan i7 cenderung memiliki harga lebih tinggi, menunjukkan segmentasi pasar premium.")
st.write("2. Rating dan Popularitas: Produk dengan rating tinggi (>4.0) memiliki lebih banyak ulasan, menunjukkan korelasi antara kualitas dan engagement pelanggan.")
st.write("3. RAM dan Harga: Laptop dengan RAM lebih besar (16GB+) memiliki harga yang signifikan lebih tinggi, sesuai dengan kebutuhan gaming/profesional.")
st.write("4. Sistem Operasi: Windows 11 mendominasi pasar, diikuti oleh Mac OS untuk segmen premium.")
st.write("5. Storage: SSD menjadi standar, dengan kapasitas 512GB sebagai sweet spot untuk keseimbangan harga-performa.")

st.subheader("Interpretasi dalam Konteks E-Commerce:")
st.write("- Segmentasi Pelanggan: Platform dapat merekomendasikan produk berdasarkan budget dan kebutuhan spesifik.")
st.write("- Strategi Harga: Harga kompetitif untuk entry-level, premium untuk high-end.")
st.write("- Fokus pada Rating: Tingkatkan kualitas produk untuk meningkatkan ulasan positif dan konversi penjualan.")

# 6. Kesimpulan dan Rekomendasi
st.header("6. Kesimpulan dan Rekomendasi")

st.subheader("Kesimpulan:")
st.write("Dataset laptop menunjukkan pasar yang kompetitif dengan fokus pada spesifikasi teknis dan harga. Intel mendominasi processor, Windows 11 sebagai OS utama, dan SSD sebagai storage standar. Rating tinggi berkorelasi dengan engagement pelanggan yang lebih baik.")

st.subheader("Rekomendasi:")
st.write("1. Untuk Platform E-Commerce: Implementasikan filter canggih berdasarkan spesifikasi untuk meningkatkan user experience.")
st.write("2. Strategi Pemasaran: Promosikan laptop entry-level (AMD/Ryzen) untuk menjangkau pelanggan budget-conscious.")
st.write("3. Pengembangan Produk: Fokus pada laptop dengan RAM 16GB+ dan SSD 512GB untuk segmen premium.")
st.write("4. Analisis Lanjutan: Lakukan A/B testing untuk rekomendasi produk berdasarkan perilaku pembelian.")
st.write("5. Monitoring: Track rating dan ulasan secara real-time untuk identifikasi produk bermasalah.")

