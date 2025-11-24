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
    # 네가 준 스키마 중 실제로 쓰는 컬럼만 예시값 채움:
    # BRD_CD, SALE_DT, SHOP_ID, SHOP_NM, PART_CD, QTY, SALE_AMT
    rows = [
        # ===== 브랜드 X =====
        # X - 네이버 - CP
        {
            "BRD_CD": "X",
            "SALE_DT": "2024-01-05",
            "SHOP_ID": "NAVER01",
            "SHOP_NM": "네이버",
            "PART_CD": "3ACP7701N",   # CP
            "QTY": 3,
            "SALE_AMT": 270000,
        },
        # X - 네이버 - DJ
        {
            "BRD_CD": "X",
            "SALE_DT": "2024-01-06",
            "SHOP_ID": "NAVER01",
            "SHOP_NM": "네이버",
            "PART_CD": "3ADJ2201N",   # DJ
            "QTY": 2,
            "SALE_AMT": 230000,
        },
        # X - 무신사 - CP
        {
            "BRD_CD": "X",
            "SALE_DT": "2024-01-07",
            "SHOP_ID": "MUSINSA01",
            "SHOP_NM": "무신사",
            "PART_CD": "3ACP7702N",   # CP
            "QTY": 5,
            "SALE_AMT": 445000,
        },
        # X - 무신사 - DJ
        {
            "BRD_CD": "X",
            "SALE_DT": "2024-01-08",
            "SHOP_ID": "MUSINSA01",
            "SHOP_NM": "무신사",
            "PART_CD": "3ADJ2202N",   # DJ
            "QTY": 4,
            "SALE_AMT": 390000,
        },

        # ===== 브랜드 M =====
        # M - 네이버 - CP
        {
            "BRD_CD": "M",
            "SALE_DT": "2024-01-10",
            "SHOP_ID": "NAVER01",
            "SHOP_NM": "네이버",
            "PART_CD": "3ACP8801N",   # CP
            "QTY": 6,
            "SALE_AMT": 480000,
        },
        # M - 네이버 - DJ
        {
            "BRD_CD": "M",
            "SALE_DT": "2024-01-11",
            "SHOP_ID": "NAVER01",
            "SHOP_NM": "네이버",
            "PART_CD": "3ADJ3301N",   # DJ
            "QTY": 3,
            "SALE_AMT": 310000,
        },
        # M - 무신사 - CP
        {
            "BRD_CD": "M",
            "SALE_DT": "2024-01-12",
            "SHOP_ID": "MUSINSA01",
            "SHOP_NM": "무신사",
            "PART_CD": "3ACP8802N",   # CP
            "QTY": 4,
            "SALE_AMT": 360000,
        },
        # M - 무신사 - DJ
        {
            "BRD_CD": "M",
            "SALE_DT": "2024-01-13",
            "SHOP_ID": "MUSINSA01",
            "SHOP_NM": "무신사",
            "PART_CD": "3ADJ3302N",   # DJ
            "QTY": 5,
            "SALE_AMT": 420000,
        },
    ]

    df = pd.DataFrame(rows)
    df["SALE_DT"] = pd.to_datetime(df["SALE_DT"])
    # 카테고리 컬럼 (3~4번째 글자)
    df["CAT"] = df["PART_CD"].str[2:4]
    return df


df_raw = load_sample_data()

# -----------------------------
# UI 영역
# -----------------------------
st.title("📊 온라인 채널 비교 대시보드 (샘플 데이터)")

# 1) 브랜드 단일 선택
brand = st.selectbox("브랜드 선택", sorted(df_raw["BRD_CD"].unique().tolist()))

# 2) 기간 선택
col1, col2 = st.columns(2)
start_date = col1.date_input("시작일", date(2024, 1, 1))
end_date = col2.date_input("종료일", date(2024, 1, 31))

# 3) SHOP_NM 채널 선택
shop_list = sorted(df_raw["SHOP_NM"].unique().tolist())  # ["네이버", "무신사"]
shops = st.multiselect("채널 선택", shop_list, default=shop_list)

# 4) 카테고리 = PART_CD 중 3~4번째 글자
category_list = sorted(df_raw["CAT"].unique().tolist())  # ["CP", "DJ"]
categories = st.multiselect("카테고리 선택", category_list, default=category_list)

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
        .agg({"SALE_AMT": "sum", "QTY": "sum"})
        .reset_index()
    )

st.subheader("채널 · 카테고리별 매출 vs 수량 분포")

fig = px.scatter(
    scatter_df,
    x="SALE_AMT",
    y="QTY",
    color="SHOP_NM",
    text="CAT",
    size="SALE_AMT",
    size_max=60,  # 점 너무 커지는 것 방지
    labels={"SALE_AMT": "매출", "QTY": "수량"},
    hover_data={
        "SHOP_NM": True,
        "CAT": True,
        "SALE_AMT": True,
        "QTY": True,
    }
)

# 점 테두리 추가 (시인성 ↑)
fig.update_traces(
    marker=dict(
        line=dict(width=1, color="black")
    ),
    textfont=dict(size=14)
)

# 레이아웃 더 깔끔하게
fig.update_layout(
    title_font_size=20,
    xaxis=dict(
        title="매출",
        gridcolor="rgba(200,200,200,0.3)",
        zeroline=False,
        tickformat=",d"
    ),
    yaxis=dict(
        title="수량",
        gridcolor="rgba(200,200,200,0.3)",
        zeroline=False,
    ),
    legend_title_text="채널",
    plot_bgcolor="white",
)

st.plotly_chart(fig, use_container_width=True)
