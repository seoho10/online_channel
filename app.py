import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="온라인 채널 비교 대시보드", layout="wide")

# -----------------------------
# 샘플 데이터 생성
# -----------------------------
@st.cache_data
def load_sample_data():
    data = {
        "SALE_DT": pd.date_range("2024-01-01", periods=30).tolist() * 4,
        "BRD_CD": (["X"] * 60 + ["M"] * 60),
        "SHOP_NM": (["자사몰"] * 30 + ["무신사"] * 30 + ["네이버"] * 30 + ["카카오"] * 30),
        "PART_CD": (
            ["3ACP7701N"] * 15
            + ["3ADJ2201N"] * 15
            + ["3AEX1101N"] * 15
            + ["3ASK5501N"] * 15
        ) * 2,
        "SALE_QTY": [i % 10 + 1 for i in range(120)],
        "SALE_AMT": [(i % 10 + 1) * 10000 for i in range(120)],
    }
    df = pd.DataFrame(data)
    # 카테고리 컬럼 (3~4번째 글자)
    df["CAT"] = df["PART_CD"].str[2:4]
    return df


df_raw = load_sample_data()

# -----------------------------
# UI 영역
# -----------------------------
st.title("📊 온라인 채널 비교 대시보드 (샘플 데이터)")

# 1) 브랜드 단일 선택
brand = st.selectbox("브랜드 선택", ["X", "M"])

# 2) 기간 선택
col1, col2 = st.columns(2)
start_date = col1.date_input("시작일", date(2024, 1, 1))
end_date = col2.date_input("종료일", date(2024, 1, 31))

# 3) SHOP_NM 채널 선택
shop_list = sorted(df_raw["SHOP_NM"].unique().tolist())
shops = st.multiselect("채널 선택", shop_list, default=shop_list[:2])

# 4) 카테고리 = PART_CD 중 3~4번째 글자
category_list = sorted(df_raw["CAT"].unique().tolist())
categories = st.multiselect("카테고리 선택", category_list, default=category_list[:2])

# -----------------------------
# 필터링
# -----------------------------
df = df_raw.copy()

df = df[df["BRD_CD"] == brand]
df = df[(df["SALE_DT"] >= pd.to_datetime(start_date)) & (df["SALE_DT"] <= pd.to_datetime(end_date))]

if shops:
    df = df[df["SHOP_NM"].isin(shops)]

if categories:
    df = df[df["CAT"].isin(categories)]

# -----------------------------
# 분산그래프 (매출 = x축 / 수량 = y축)
# -----------------------------
if df.empty:
    st.warning("데이터가 없습니다. 조건을 다시 선택하세요.")
else:
    scatter_df = (
        df.groupby(["SHOP_NM", "CAT"])
        .agg({"SALE_AMT": "sum", "SALE_QTY": "sum"})
        .reset_index()
    )

    st.subheader("채널 · 카테고리별 매출 vs 수량 분포")

    fig = px.scatter(
        scatter_df,
        x="SALE_AMT",
        y="SALE_QTY",
        color="SHOP_NM",
        text="CAT",
        size="SALE_AMT",
