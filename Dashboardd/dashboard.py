import pandas as pd
import streamlit as st
import urllib
import matplotlib.image as mpimg
import plotly.express as px
from function import AnalyticsTool, BrazilGeospatial

# Atur konfigurasi halaman Streamlit
st.set_page_config(layout="wide")

# Memuat dataset pesanan dan data geolokasi
orders_df = pd.read_csv("https://raw.githubusercontent.com/Wakbarr/Proyek-Analisis-Data/refs/heads/main/Dashboardd/all_df.csv")
orders_df.sort_values(by="order_purchase_timestamp", inplace=True)
orders_df.reset_index(drop=True, inplace=True)

geo_df = pd.read_csv("https://raw.githubusercontent.com/Wakbarr/Proyek-Analisis-Data/refs/heads/main/Dashboardd/geolocation.csv")
geo_data = geo_df.drop_duplicates(subset='customer_unique_id')

# Konversi kolom waktu menjadi format datetime
datetime_columns = [
    "order_approved_at", 
    "order_delivered_carrier_date", 
    "order_delivered_customer_date", 
    "order_estimated_delivery_date", 
    "order_purchase_timestamp", 
    "shipping_limit_date"
]
for col in datetime_columns:
    orders_df[col] = pd.to_datetime(orders_df[col])

# Tentukan rentang tanggal minimum dan maksimum
min_date = orders_df["order_purchase_timestamp"].min()
max_date = orders_df["order_purchase_timestamp"].max()

# Sidebar Streamlit untuk input interaktif
with st.sidebar:
    col_left, col_center, col_right = st.columns(3)
    with col_left:
        st.write(' ')
    with col_center:
        st.image(
            "https://raw.githubusercontent.com/nurhadimeilana05/Proyek-Analisis-Data-Dicoding/main/dashboard/images.jpeg",
            width=100
        )
    with col_right:
        st.write(' ')
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_orders = orders_df[
    (orders_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
    (orders_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

# Inisialisasi modul analisis dan peta geospasial
analytics = AnalyticsTool(filtered_orders)
geo_plotter = BrazilGeospatial(geo_data, st)

# Buat data ringkasan dari berbagai fungsi analitik
order_items_summary = analytics.create_sum_order_items_df()
monthly_perf = analytics.create_monthly_performance_df()
daily_orders = analytics.create_daily_order_df()
customer_spending = analytics.create_sum_spend_df()
city_stats, top_city = analytics.create_city_df()
rfm_metrics = analytics.create_rfm_df()

# Tampilan judul dan pesan sambutan
st.title("E-Commerce Public Dataset")
st.write("**Hi Everyone! Welcome to the E-Commerce Public Dataset Dashboard.**")

# ==================== Pertanyaan 1: Performa Penjualan Produk ====================
st.subheader("Pertanyaan 1: Performa Penjualan Produk")

# Misalnya, order_items_summary memiliki kolom "product_category_name_english" dan "order_item_count"
sum_order_items_df = order_items_summary.copy()
st.write("Data Order Items Summary:", sum_order_items_df.head())

# Best Performing Product (Top 5)
best_df = sum_order_items_df.head(5)
fig_best = px.bar(
    best_df, 
    x="order_item_count", 
    y="product_category_name_english", 
    orientation="h",
    title="Best Performing Product",
    labels={"order_item_count": "Number of Sales (Order Item)", "product_category_name_english": "Product Category"},
    color="order_item_count",
    color_continuous_scale=["#72BF78", "#72BF78"]  # Pastikan ada dua warna
)
fig_best.update_layout(yaxis={'categoryorder':'total ascending'})

# Worst Performing Product (Bottom 5)
worst_df = sum_order_items_df.sort_values(by="order_item_count", ascending=True).head(5)
fig_worst = px.bar(
    worst_df, 
    x="order_item_count", 
    y="product_category_name_english", 
    orientation="h",
    title="Worst Performing Product",
    labels={"order_item_count": "Number of Sales (Order Item)", "product_category_name_english": "Product Category"},
    color="order_item_count",
    color_continuous_scale=["#72BF78", "#72BF78"]  # Pastikan ada dua warna
)
fig_worst.update_layout(yaxis={'categoryorder':'total descending'})

# Tampilkan chart interaktif pada dua kolom
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_best, use_container_width=True)
with col2:
    st.plotly_chart(fig_worst, use_container_width=True)

# ==================== Pertanyaan 2: Evaluasi Performa Pengiriman ====================
st.subheader("Pertanyaan 2: Evaluasi Performa Pengiriman")

# Tambahkan kolom delivery_status pada filtered_orders
filtered_orders['delivery_status'] = filtered_orders.apply(
    lambda row: 'on time' if row['order_delivered_customer_date'] <= row['order_estimated_delivery_date'] else 'late',
    axis=1
)

# Hitung jumlah order per delivery_status
delivery_status_df = filtered_orders.groupby("delivery_status").order_id.count().reset_index()
delivery_status_df = delivery_status_df.sort_values(by="order_id", ascending=False)
st.write("Data Delivery Status:", delivery_status_df)

# Buat chart interaktif: Bar Chart
fig_bar = px.bar(
    delivery_status_df, 
    x="order_id", 
    y="delivery_status", 
    orientation="h",
    title="Shipping Performance (Number of Orders)",
    labels={"order_id": "Number of Orders", "delivery_status": "Delivery Status"},
    color="delivery_status",
    color_discrete_map={"on time": "#72BF78", "late": "#D3D3D3"}
)

# Buat chart interaktif: Pie Chart
fig_pie = px.pie(
    delivery_status_df, 
    names="delivery_status", 
    values="order_id",
    title="Shipping Performance Distribution",
    color="delivery_status",
    color_discrete_map={"on time": "#72BF78", "late": "#D3D3D3"}
)

# Tampilkan chart interaktif pada dua kolom
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig_bar, use_container_width=True)
with col4:
    st.plotly_chart(fig_pie, use_container_width=True)

# Tampilkan peta interaktif (jika modul peta sudah diimplementasikan)
st.subheader("Customer Geolocation")
st.write("Klik pada peta untuk melihat informasi geospasial pelanggan.")
geo_plotter.plot()

st.caption('Copyright (C) Akbar Widianto 2025')
