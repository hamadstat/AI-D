
import streamlit as st
import pandas as pd
import plotly.express as px

# تحميل البيانات
@st.cache_data
def load_data():
    orders = pd.read_excel("Dropshipping_Recommendation_System_2024.xlsx", sheet_name="Orders")
    customers = pd.read_excel("Dropshipping_Recommendation_System_2024.xlsx", sheet_name="Customers")
    products = pd.read_excel("Dropshipping_Recommendation_System_2024.xlsx", sheet_name="Products")
    return orders, customers, products

# واجهة التطبيق
st.set_page_config(page_title="Dropshipping AI Dashboard", layout="wide")

st.title("📊 AI-Powered Dropshipping Dashboard - Saudi Arabia")
st.markdown("### 🔍 تحليل بيانات المبيعات في السعودية باستخدام الذكاء الاصطناعي")

# تحميل البيانات
orders, customers, products = load_data()

# تصفية البيانات بناءً على المدينة أو الفئة
st.sidebar.header("🔍 فلترة البيانات")
selected_city = st.sidebar.selectbox("اختر مدينة:", ["الكل"] + list(customers["Location"].unique()))
selected_category = st.sidebar.selectbox("اختر فئة المنتج:", ["الكل"] + list(products["Category"].unique()))

# تطبيق الفلترة
if selected_city != "الكل":
    customers = customers[customers["Location"] == selected_city]
    orders = orders[orders["CustomerID"].isin(customers["CustomerID"])]

if selected_category != "الكل":
    products = products[products["Category"] == selected_category]
    orders = orders[orders["ProductID"].isin(products["ProductID"])]

# عدد العملاء والطلبات والمبيعات
col1, col2, col3 = st.columns(3)
col1.metric("📦 إجمالي الطلبات", orders.shape[0])
col2.metric("👥 إجمالي العملاء", customers.shape[0])
col3.metric("💰 إجمالي الإيرادات", f"{orders['Price'].sum():,.2f} SAR")

# عرض الطلبات الأخيرة
st.subheader("📝 آخر 10 طلبات")
st.dataframe(orders.sort_values("OrderDate", ascending=False).head(10))

# تحليل المبيعات حسب المنتج
st.subheader("📈 أكثر المنتجات مبيعًا")
product_sales = orders.groupby("ProductID")["Quantity"].sum().reset_index()
product_sales = product_sales.merge(products, on="ProductID")
fig = px.bar(product_sales, x="ProductName", y="Quantity", title="💡 المنتجات الأكثر مبيعًا", color="Category")
st.plotly_chart(fig, use_container_width=True)

# تحليل المبيعات حسب المدينة
st.subheader("🏙️ المبيعات حسب المدينة")
city_sales = orders.merge(customers, on="CustomerID").groupby("Location")["Quantity"].sum().reset_index()
fig2 = px.pie(city_sales, names="Location", values="Quantity", title="📍 توزيع الطلبات حسب المدن")
st.plotly_chart(fig2, use_container_width=True)

# تحليل اتجاهات المبيعات عبر الزمن
st.subheader("📅 اتجاهات المبيعات بمرور الوقت")
orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])
daily_sales = orders.groupby("OrderDate")["Price"].sum().reset_index()
fig3 = px.line(daily_sales, x="OrderDate", y="Price", title="📊 الإيرادات اليومية")
st.plotly_chart(fig3, use_container_width=True)


