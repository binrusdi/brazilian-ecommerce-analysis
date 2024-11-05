import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Baca data dari file CSV
all_data = pd.read_csv('data/all_data.csv')
monthly_performance = pd.read_csv('data/monthly_performance.csv', index_col='month')
product_sales = pd.read_csv('data/product_sales.csv')
customer_state = pd.read_csv('data/customer_state.csv')

# Ubah tipe data order_purchase_timestamp menjadi datetime (jika diperlukan)
all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])
monthly_performance.index = pd.to_datetime(monthly_performance.index)

# Judul Dashboard
st.title('Dashboard Analisis E-commerce')

# Sidebar
st.sidebar.title('Filter Data')

# Filter berdasarkan Bulan (untuk Pertanyaan 1)
selected_months = st.sidebar.multiselect(
    'Pilih Bulan',
    options=monthly_performance.index.strftime('%Y-%m').unique(),
    default=monthly_performance.index.strftime('%Y-%m').unique()
)

# Filter berdasarkan Kategori Produk (untuk Pertanyaan 2)
selected_categories = st.sidebar.multiselect(
    'Pilih Kategori Produk',
    options=product_sales['product_category_name'].unique(),
    default=product_sales['product_category_name'].unique()
)

# Filter berdasarkan State (untuk Pertanyaan 3)
selected_states = st.sidebar.multiselect(
    'Pilih State',
    options=customer_state['customer_state'].unique(),
    default=customer_state['customer_state'].unique()
)

# Menampilkan Visualisasi dan Analisis
# Pertanyaan 1: Performa Penjualan dan Revenue
filtered_monthly_performance = monthly_performance[monthly_performance.index.strftime('%Y-%m').isin(selected_months)]

st.header('Performa Penjualan dan Revenue')
st.line_chart(filtered_monthly_performance[['order_count', 'total_revenue']])

# Pertanyaan 2: Produk Terlaris dan Paling Sedikit Terjual
filtered_product_sales = product_sales[product_sales['product_category_name'].isin(selected_categories)]
top_10_products = filtered_product_sales.sort_values(by='total_sold', ascending=False).head(10)

st.header('Top 10 Produk Terlaris')
st.bar_chart(top_10_products.set_index('product_category_name')['total_sold'])

# Pertanyaan 3: Demografi Pelanggan
filtered_customer_state = customer_state[customer_state['customer_state'].isin(selected_states)]

st.header('Demografi Pelanggan')
st.bar_chart(filtered_customer_state.set_index('customer_state')['customer_count'])


# Performa Penjualan dan Revenue
st.header('Performa Penjualan dan Revenue')
fig_performance = px.line(monthly_performance, x=monthly_performance.index, y=['order_count', 'total_revenue'],
                          title='Tren Penjualan dan Revenue')
fig_performance.update_traces(mode="lines+markers", hovertemplate=None)
fig_performance.update_layout(hovermode="x unified")
st.plotly_chart(fig_performance)

# Penjualan Produk (Heatmap)
st.header('Penjualan Produk')
top_categories = product_sales.groupby('product_category_name')['total_sold'].sum().nlargest(10).index
filtered_sales = product_sales[product_sales['product_category_name'].isin(top_categories)]
fig_heatmap = px.density_heatmap(filtered_sales, x='product_category_name', y='product_name_lenght', z='total_sold',
                                  title='Heatmap Penjualan Produk', color_continuous_scale='Viridis')
st.plotly_chart(fig_heatmap)

# Demografi Pelanggan (Map)
st.header('Demografi Pelanggan')
fig_map = px.choropleth(customer_state, geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson", 
                        locations='customer_state', featureidkey="properties.sigla",
                        color='customer_count', color_continuous_scale="Viridis",
                        scope="south america", title='Distribusi Pelanggan per State')
fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map)

# --- Penyesuaian Estetika ---
st.markdown("""
<style>
.reportview-container .main .block-container{{
    max-width: 1000px;
    padding-top: 2rem;
    padding-right: 2rem;
    padding-left: 2rem;
    padding-bottom: 2rem;
}}
</style>
""", unsafe_allow_html=True)