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
    rows = [
        # BRD X - 자사몰 - CP
        {
            "BRD_CD": "X",
            "SALE_DT": pd.to_datetime("2024-01-05"),
            "SHOP_ID": "30004",
            "SHOP_NM": "자사몰",
            "USR_ID": "USR001",
            "SEQ": 1,
            "PRDT_CD": "PRD_X_CP_01",
            "SESN": "24SS",
            "PART_CD": "3ACP7701N",   # CP
            "COLOR_CD": "BLK",
            "SIZE_CD": "095",
            "RET_YN": "N",
            "PRICE": 99000,
            "TAG_PRICE": 99000,
            "QTY": 3,
            "SALE_QTY": 3,            # 코드에서 쓰는 컬럼도 같이 만들어줌
            "VAT": 2700,
            "SUPP_AMT": 90000,
            "SALE_AMT": 270000,
            "TAG_AMT": 297000,
            "DSCT_AMT": 27000,
            "REFUND_AMT": 0,
            "DSCT_RATE": 0.1,
            "MRGN_RATE": 0.4,
            "SALE_TYPE": "N",
            "DIST_CLS": "ON",
            "PAY_CLS": "CARD",
            "PROM_CD": "PROM01",
            "REFUND_YN": "N",
            "EVENT_YN": "Y",
            "RESALE_YN": "N",
            "ONLINE_YN": "Y",
            "DIRECT_DELV_YN": "Y",
            "RESVE_YN": "N",
            "DEPART_ONLINE_YN": "N",
            "SMALL_GRP_YN": "N",
            "PRE_YN": "N",
            "CUST_TYPE": "M",
            "CUST_ID": "C001",
            "POS_DATE": pd.to_datetime("2024-01-05"),
            "REG_NO": "R001",
            "CURRENCY_UNIT": "KRW",
            "LOCAL_TAG_PRICE": 99000,
            "LOCAL_SALE_AMT": 270000,
            "INPUT_DATE": pd.to_datetime("2024-01-06"),
        },
        # BRD X - 자사몰 - DJ
        {
            "BRD_CD": "X",
            "SALE_DT": pd.to_datetime("2024-01-07"),
            "SHOP_ID": "30004",
            "SHOP_NM": "자사몰",
            "USR_ID": "USR002",
            "SEQ": 2,
            "PRDT_CD": "PRD_X_DJ_01",
            "SESN": "24SS",
            "PART_CD": "3ADJ2201N",   # DJ
            "COLOR_CD": "GRY",
            "SIZE_CD": "100",
            "RET_YN": "N",
            "PRICE": 129000,
            "TAG_PRICE": 129000,
            "QTY": 2,
            "SALE_QTY": 2,
            "VAT": 3200,
            "SUPP_AMT": 110000,
            "SALE_AMT": 258000,
            "TAG_AMT": 258000,
            "DSCT_AMT": 0,
            "REFUND_AMT": 0,
            "DSCT_RATE": 0.0,
            "MRGN_RATE": 0.45,
            "SALE_TYPE": "N",
            "DIST_CLS": "ON",
            "PAY_CLS": "CARD",
            "PROM_CD": "PROM02",
            "REFUND_YN": "N",
            "EVENT_YN": "N",
            "RESALE_YN": "N",
            "ONLINE_YN": "Y",
            "DIRECT_DELV_YN": "Y",
            "RESVE_YN": "N",
            "DEPART_ONLINE_YN": "N",
            "SMALL_GRP_YN": "N",
            "PRE_YN": "N",
            "CUST_TYPE": "M",
            "CUST_ID": "C002",
            "POS_DATE": pd.to_datetime("2024-01-07"),
            "REG_NO": "R002",
            "CURRENCY_UNIT": "KRW",
            "LOCAL_TAG_PRICE": 129000,
            "LOCAL_SALE_AMT": 258000,
            "INPUT_DATE": pd.to_datetime("2024-01-08"),
        },
        # BRD X - 무신사 - CP
        {
            "BRD_CD": "X",
            "SALE_DT": pd.to_datetime("2024-01-10"),
            "SHOP_ID": "MUSINSA01",
            "SHOP_NM": "무신사",
            "USR_ID": "USR003",
            "SEQ": 3,
            "PRDT_CD": "PRD_X_CP_02",
            "SESN": "24SS",
            "PART_CD": "3ACP7702N",
            "COLOR_CD": "NAV",
            "SIZE_CD": "095",
            "RET_YN": "N",
            "PRICE": 89000,
            "TAG_PRICE": 89000,
            "QTY": 5,
            "SALE_QTY": 5,
            "VAT": 4000,
            "SUPP_AMT": 80000,
            "SALE_AMT": 445000,
            "TAG_AMT": 445000,
            "DSCT_AMT": 0,
            "REFUND_AMT": 0,
            "DSCT_RATE": 0.0,
            "MRGN_RATE": 0.38,
            "SALE_TYPE": "N",
            "DIST_CLS": "ON",
            "PAY_CLS": "CARD",
            "PROM_CD": "PROM03",
            "REFUND_YN": "N",
            "EVENT_YN": "Y",
            "RESALE_YN": "N",
            "ONLINE_YN": "Y",
            "DIRECT_DELV_YN": "N",
            "RESVE_YN": "N",
            "DEPART_ONLINE_YN": "N",
            "SMALL_GRP_YN": "N",
            "PRE_YN": "N",
            "CUST_TYPE": "M",
            "CUST_ID": "C003",
            "POS_DATE": pd.to_datetime("2024-01-10"),
            "REG_NO": "R003",
            "CURRENCY_UNIT": "KRW",
            "LOCAL_TAG_PRICE": 89000,
            "LOCAL_SALE_AMT": 445000,
            "INPUT_DATE": pd.to_datetime("2024-01-11"),
        },
        # BRD X - 네이버 - DJ
        {
            "BRD_CD": "X",
            "SALE_DT": pd.to_datetime("2024-01-12"),
            "SHOP_ID": "NAVER01",
            "SHOP_NM": "네이버",
            "USR_ID": "USR004",
            "SEQ": 4,
            "PRDT_CD": "PRD_X_DJ_02",
            "SESN": "24SS",
            "PART_CD": "3ADJ2202N",
            "COLOR_CD": "BLK",
            "SIZE_CD": "100",
            "RET_YN": "N",
            "PRICE": 139000,
            "TAG_PRICE": 139000,
            "QTY": 4,
            "SALE_QTY": 4,
            "VAT": 5000,
            "SUPP_AMT": 120000,
            "SALE_AMT": 556000,
            "TAG_AMT": 556000,
            "DSCT_AMT": 0,
            "REFUND_AMT": 0,
            "DSCT_RATE": 0.0,
            "MRGN_RATE": 0.42,
            "SALE_TYPE": "N",
            "DIST_CLS": "ON",
            "PAY_CLS": "CARD",
            "PROM_CD": "PROM04",
            "REFUND_YN": "N",
            "EVENT_YN": "Y",
            "RESALE_YN": "N",
            "ONLINE_YN": "Y",
            "DIRECT_DELV_YN": "N",
            "RESVE_YN": "N",
            "DEPART_ONLINE_YN": "N",
            "SMALL_GRP_YN": "N",
            "PRE_YN": "N",
            "CUST_TYPE": "M",
            "CUST_ID": "C004",
            "POS_DATE": pd.to_datetime("2024-01-12"),
            "REG_NO": "R004",
            "CURRENCY_UNIT": "KRW",
            "LOCAL_TAG_PRICE": 139000,
            "LOCAL_SALE_AMT": 556000,
            "INPUT_DATE": pd.to_datetime("2024-01-13"),
        },
        # BRD M - 카카오 - CP
        {
            "BRD_CD": "M",
            "SALE_DT": pd.to_datetime("2024-01-15"),
            "SHOP_ID": "KAKAO01",
            "SHOP_NM": "카카오",
            "USR_ID": "USR005",
            "SEQ": 5,
            "PRDT_CD": "PRD_M_CP_01",
            "SESN": "24SS",
            "PART_CD": "3ACP8801N",
            "COLOR_CD": "WHT",
            "SIZE_CD": "090",
            "RET_YN": "N",
            "PRICE": 79000,
            "TAG_PRICE": 79000,
            "QTY": 6,
            "SALE_QTY": 6,
            "VAT": 3500,
            "SUPP_AMT": 70000,
            "SALE_AMT": 474000,
            "TAG_AMT": 474000,
            "DSCT_AMT": 0,
            "REFUND_AMT": 0,
            "DSCT_RATE": 0.0,
            "MRGN_RATE": 0.35,
            "SALE_TYPE": "N",
            "DIST_CLS": "ON",
            "PAY_CLS": "CARD",
            "PROM_CD": "PROM05",
            "REFUND_YN": "N",
            "EVENT_YN": "N",
            "RESALE_YN": "N",
            "ONLINE_YN": "Y",
            "DIRECT_DELV_YN": "N",
            "RESVE_YN": "N",
            "DEPART_ONLINE_YN": "N",
            "SMALL_GRP_YN": "N",
            "PRE_YN": "N",
            "CUST_TYPE": "M",
            "CUST_ID": "C005",
            "POS_DATE": pd.to_datetime("2024-01-15"),
            "REG_NO": "R005",
            "CURRENCY_UNIT": "KRW",
            "LOCAL_TAG_PRICE": 79000,
            "LOCAL_SALE_AMT": 474000,
            "INPUT_DATE": pd.to_datetime("2024-01-16"),
        },
        # BRD M - 자사몰 - DJ
        {
            "BRD_CD": "M",
            "SALE_DT": pd.to_datetime("2024-01-18"),
            "SHOP_ID": "510",
            "SHOP_NM": "자사몰",
            "USR_ID": "USR006",
            "SEQ": 6,
            "PRDT_CD": "PRD_M_DJ_01",
            "SESN": "24SS",
            "PART_CD": "3ADJ3301N",
            "COLOR_CD": "BLU",
            "SIZE_CD": "095",
            "RET_YN": "N",
            "PRICE": 119000,
            "TAG_PRICE": 119000,
            "QTY": 2,
            "SALE_QTY": 2,
            "VAT": 3200,
            "SUPP_AMT": 100000,
            "SALE_AMT": 238000,
            "TAG_AMT": 238000,
            "DSCT_AMT": 0,
            "REFUND_AMT": 0,
            "DSCT_RATE": 0.0,
            "MRGN_RATE": 0.4,
            "SALE_TYPE": "N",
            "DIST_CLS": "ON",
            "PAY_CLS": "CARD",
            "PROM_CD": "PROM06",
            "REFUND_YN": "N",
            "EVENT_YN": "Y",
            "RESALE_YN": "N",
            "ONLINE_YN": "Y",
            "DIRECT_DELV_YN": "Y",
            "RESVE_YN": "N",
            "DEPART_ONLINE_YN": "N",
            "SMALL_GRP_YN": "N",
            "PRE_YN": "N",
            "CUST_TYPE": "M",
            "CUST_ID": "C006",
            "POS_DATE": pd.to_datetime("2024-01-18"),
            "REG_NO": "R006",
            "CURRENCY_UNIT": "KRW",
            "LOCAL_TAG_PRICE": 119000,
            "LOCAL_SALE_AMT": 238000,
            "INPUT_DATE": pd.to_datetime("2024-01-19"),
        },
    ]

    df = pd.DataFrame(rows)
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
df = df[
    (df["SALE_DT"] >= pd.to_datetime(start_date))
    & (df["SALE_DT"] <= pd.to_datetime(end_date))
]

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
        labels={"SALE_AMT": "매출", "SALE_QTY": "수량"},
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 집계 데이터 보기"):
        st.dataframe(scatter_df)
