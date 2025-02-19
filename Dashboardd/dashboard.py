import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from function import AnalyticsTool, BrazilGeospatial

# Atur gaya visualisasi
sns.set(style='dark')

# Kolom-kolom yang berisi data waktu
datetime_columns = [
    "order_approved_at", 
    "order_delivered_carrier_date", 
    "order_delivered_customer_date", 
    "order_estimated_delivery_date", 
    "order_purchase_timestamp", 
    "shipping_limit_date"
]

# Memuat dataset pesanan
orders_df = pd.read_csv("https://raw.githubusercontent.com/Wakbarr/Proyek-Analisis-Data/refs/heads/main/Dashboardd/all_df.csv")
orders_df.sort_values(by="order_purchase_timestamp", inplace=True)
orders_df.reset_index(drop=True, inplace=True)

# Memuat dataset geolokasi dan menghilangkan duplikasi berdasarkan ID pelanggan
geo_df = pd.read_csv("https://raw.githubusercontent.com/Wakbarr/Proyek-Analisis-Data/refs/heads/main/Dashboardd/geolocation.csv")
geo_data = geo_df.drop_duplicates(subset='customer_unique_id')

# Konversi kolom waktu menjadi format datetime
for col in datetime_columns:
    orders_df[col] = pd.to_datetime(orders_df[col])

# Tentukan rentang tanggal minimum dan maksimum
min_date = orders_df["order_purchase_timestamp"].min()
max_date = orders_df["order_purchase_timestamp"].max()

# Sidebar Streamlit
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

    # Input rentang tanggal
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
geo_plotter = BrazilGeospatial(geo_data, plt, mpimg, urllib, st)

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

# --- Analisis Order Items ---
st.subheader("Order Items")
col_total, col_avg = st.columns(2)

with col_total:
    total_items = order_items_summary["order_item_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col_avg:
    avg_items = order_items_summary["order_item_count"].mean()
    st.markdown(f"Average Items: **{avg_items:.2f}**")

fig_items, axes = plt.subplots(1, 2, figsize=(50, 25))
bar_palette = ["#72BF78", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Produk dengan performa terbaik
sns.barplot(
    x="order_item_count", 
    y="product_category_name_english", 
    data=order_items_summary.head(5), 
    palette=bar_palette, 
    ax=axes[0]
)
axes[0].set_ylabel(None)
axes[0].set_xlabel("Order Item", fontsize=80)
axes[0].set_title("Best Performing Product", fontsize=90, loc="center")
axes[0].tick_params(axis='y', labelsize=55)
axes[0].tick_params(axis='x', labelsize=50)

# Produk dengan performa terendah
sns.barplot(
    x="order_item_count", 
    y="product_category_name_english", 
    data=order_items_summary.sort_values(by="order_item_count", ascending=True).head(5), 
    palette=bar_palette, 
    ax=axes[1]
)
axes[1].set_ylabel(None)
axes[1].set_xlabel("Order Item", fontsize=80)
axes[1].invert_xaxis()
axes[1].yaxis.set_label_position("right")
axes[1].yaxis.tick_right()
axes[1].set_title("Worst Performing Product", fontsize=90, loc="center")
axes[1].tick_params(axis='y', labelsize=55)
axes[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig_items)

# --- Performa Pesanan Bulanan ---
st.subheader("Number of Orders in Recent Months")
fig_orders, ax_orders = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x="order_purchase_timestamp",
    y="order_count",
    data=monthly_perf,
    marker="o",
    linewidth=2,
    color="#72BF78",
    ax=ax_orders
)
ax_orders.set_ylim(bottom=0)
ax_orders.set_title("Number of Orders in Recent Months (2018)", fontsize=20, loc="center")
ax_orders.set_ylabel("Number of Orders", fontsize=12)
ax_orders.set_xlabel("Month", fontsize=12)
ax_orders.tick_params(axis='x', labelsize=10)
ax_orders.tick_params(axis='y', labelsize=10)
st.pyplot(fig_orders)

# --- Performa Pendapatan Bulanan ---
st.subheader("Revenue in Recent Months")
fig_revenue, ax_revenue = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x="order_purchase_timestamp",
    y="total_revenue",
    data=monthly_perf,
    marker="o",
    linewidth=2,
    color="#72BF78",
    ax=ax_revenue
)
ax_revenue.set_ylim(bottom=0)
ax_revenue.set_title("Revenue in Recent Months (2018)", fontsize=20, loc="center")
ax_revenue.set_ylabel("Revenue", fontsize=12)
ax_revenue.set_xlabel("Month", fontsize=12)
ax_revenue.tick_params(axis='x', labelsize=10)
ax_revenue.tick_params(axis='y', labelsize=10)
st.pyplot(fig_revenue)

# --- Pesanan Harian yang Dikirim ---
st.subheader("Daily Orders Delivered")
col_daily_orders, col_daily_revenue = st.columns(2)

with col_daily_orders:
    total_daily = daily_orders["order_count"].sum()
    st.markdown(f"Total Order: **{total_daily}**")

with col_daily_revenue:
    total_daily_rev = daily_orders["total_revenue"].sum()
    st.markdown(f"Total Revenue: **{total_daily_rev}**")

fig_daily, ax_daily = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x="order_purchase_timestamp",
    y="order_count",
    data=daily_orders,
    marker="o",
    linewidth=2,
    color="#72BF78",
    ax=ax_daily
)
ax_daily.tick_params(axis="x", rotation=45)
ax_daily.tick_params(axis="y", labelsize=15)
st.pyplot(fig_daily)

# --- Pengeluaran Pelanggan ---
st.subheader("Customer Spend Money")
col_spend_total, col_spend_avg = st.columns(2)

with col_spend_total:
    total_spend = customer_spending["total_spend"].sum()
    st.markdown(f"Total Spend: **{total_spend}**")

with col_spend_avg:
    avg_spend = customer_spending["total_spend"].mean()
    st.markdown(f"Average Spend: **{avg_spend:.2f}**")

fig_spend, ax_spend = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=customer_spending,
    x="order_purchase_timestamp",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#72BF78",
    ax=ax_spend
)
ax_spend.tick_params(axis="x", rotation=45)
ax_spend.tick_params(axis="y", labelsize=15)
st.pyplot(fig_spend)

# --- Pelanggan Berdasarkan Kota ---
st.subheader("Customer By City")
tab_city, tab_map = st.tabs(["City", "Map"])

with tab_city:
    st.markdown(f"Most Common City: **{top_city}**")
    fig_city, ax_city = plt.subplots(figsize=(10, 5))
    city_palette = ["#72BF78"] + ["#D3D3D3"] * 4  
    sns.barplot(
        x="customer_city",
        y="customer_count",
        data=city_stats.head(5),
        palette=city_palette,
        ax=ax_city
    )
    ax_city.set_title("Number of Customers by City", fontsize=20)
    ax_city.set_xlabel("City")
    ax_city.set_ylabel("Number of Customers")
    ax_city.tick_params(axis='x', rotation=45, labelsize=12)
    ax_city.tick_params(axis='y', labelsize=12)
    st.pyplot(fig_city)

with tab_map:
    geo_plotter.plot()

# --- Analisis RFM ---
st.subheader("Best Customer Based on RFM Parameters")
fig_rfm, axes_rfm = plt.subplots(1, 3, figsize=(35, 15))
rfm_palette = ["#72BF78"] * 5

# Analisis berdasarkan Recency
sns.barplot(
    y="recency", 
    x="customer_unique_id", 
    data=rfm_metrics.sort_values(by="recency", ascending=True).head(5), 
    palette=rfm_palette, 
    ax=axes_rfm[0]
)
axes_rfm[0].set_ylabel(None)
axes_rfm[0].set_xlabel("Customer Unique ID", fontsize=30)
axes_rfm[0].set_title("By Recency (days)", fontsize=50)
axes_rfm[0].tick_params(axis='y', labelsize=30)
axes_rfm[0].tick_params(axis='x', labelsize=35, rotation=90)

# Analisis berdasarkan Frequency
sns.barplot(
    y="frequency", 
    x="customer_unique_id", 
    data=rfm_metrics.sort_values(by="frequency", ascending=False).head(5), 
    palette=rfm_palette, 
    ax=axes_rfm[1]
)
axes_rfm[1].set_ylabel(None)
axes_rfm[1].set_xlabel("Customer Unique ID", fontsize=30)
axes_rfm[1].set_title("By Frequency", fontsize=50)
axes_rfm[1].tick_params(axis='y', labelsize=30)
axes_rfm[1].tick_params(axis='x', labelsize=35, rotation=90)

# Analisis berdasarkan Monetary
sns.barplot(
    y="monetary", 
    x="customer_unique_id", 
    data=rfm_metrics.sort_values(by="monetary", ascending=False).head(5), 
    palette=rfm_palette, 
    ax=axes_rfm[2]
)
axes_rfm[2].set_ylabel(None)
axes_rfm[2].set_xlabel("Customer Unique ID", fontsize=30)
axes_rfm[2].set_title("By Monetary", fontsize=50)
axes_rfm[2].tick_params(axis='y', labelsize=30)
axes_rfm[2].tick_params(axis='x', labelsize=35, rotation=90)

st.pyplot(fig_rfm)

st.caption('Copyright (C) Akbar Widianto 2025')
