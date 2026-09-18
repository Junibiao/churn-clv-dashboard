import pandas as pd
import plotly.express as px
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Customer CLV & Churn Dashboard", layout="wide")

st.title("📊 E-Commerce Customer CLV & Churn Risk Engine")
st.markdown(
    "แดชบอร์ดวิเคราะห์มูลค่าลูกค้า (CLV) และความเสี่ยงในการเลิกซื้อ (Churn Risk)"
)


# โหลดข้อมูล
@st.cache_data
def load_data():
    return pd.read_csv("customer_churn_clv_data.csv")


df = load_data()

# Summary Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("จำนวนลูกค้าทั้งหมด", f"{len(df):,} คน")
col2.metric("ยอดขายรวม (CLV Total)", f"${df['CLV'].sum():,.2f}")
col3.metric("เสี่ยง Churn สูง (>70%)", f"{len(df[df['Churn_Risk_%'] > 70]):,} คน")
col4.metric("อัตรา Churn โดยรวม", f"{(df['Churn'].mean()*100):.1f}%")

st.markdown("---")

# Section: Risk Distribution & Top High-Risk Customers
c1, c2 = st.columns(2)

with c1:
    st.subheader("🎯 การกระจายตัวของความเสี่ยง Churn")
    fig = px.histogram(
        df,
        x="Churn_Risk_%",
        nbins=20,
        title="จำนวนลูกค้าแยกตาม % ความเสี่ยง",
        color_discrete_sequence=["#EF553B"],
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader(
        "⚠️ 10 อันดับลูกค้าเสี่ยงสูงที่ต้องเร่งรักษา (High Value & High Churn)"
    )
    high_risk_high_val = df.sort_values(
        by=["Churn_Risk_%", "CLV"], ascending=[False, False]
    ).head(10)
    st.dataframe(
        high_risk_high_val[
            ["CustomerID", "Recency", "Frequency", "CLV", "Churn_Risk_%"]
        ],
        use_container_width=True,
    )

# Section: Customer Lookup
st.markdown("---")
st.subheader("🔍 ค้นหาข้อมูลรายลูกค้า (Customer Lookup)")
cust_id = st.number_input(
    "ใส่ CustomerID ที่ต้องการค้นหา:", value=int(df["CustomerID"].iloc[0])
)
cust_data = df[df["CustomerID"] == cust_id]

if not cust_data.empty:
    st.dataframe(cust_data, use_container_width=True)
else:
    st.warning("ไม่พบ CustomerID นี้ในระบบ")
