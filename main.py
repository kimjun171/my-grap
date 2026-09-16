import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Streamlit 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)


# 데이터 불러오기 및 캐싱 (1시간)
@st.cache_data(ttl=3600)
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    # CSV 데이터 로드 (날짜 열을 문자열 타입으로 먼저 읽음)
    df = pd.read_csv(url, dtype={"날짜": str})

    # '날짜' 열을 YYYYMMDD 형식을 연-월-일(datetime) 타입으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")

    # 숫자형 데이터 기본 정제
    numeric_cols = ["순위", "일관객", "누적관객", "스크린수", "상영횟수"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            )

    return df


# 데이터 로드
df = load_data()

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("1년치(365일) 일별 박스오피스 10위권 기록 데이터 분석")

st.markdown("---")

# ==========================================
# [섹션 1] 개별 영화의 날짜별 일관객수 변화
# ==========================================
st.header("📌 1. 개별 영화의 날짜별 일관객수 변화")

# 데이터에 존재하는 영화 목록 추출 (영화명 기준 오름차순 정렬)
movie_list = sorted(df["영화명"].unique())

# 영화 선택 드롭다운
selected_movie = st.selectbox(
    "관객수 추이를 확인할 영화를 선택하세요:",
    options=movie_list,
    index=0,
)

# 선택한 영화의 데이터만 필터링 후 날짜순 정렬
movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values(by="날짜")
    .reset_index(drop=True)
)

# Plotly 선 그래프(Line Chart) 생성
fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    title=f"'{selected_movie}' 날짜별 일관객수 추이",
    labels={"날짜": "날짜", "일관객": "일일 관객수 (명)"},
    markers=True,
)

# 마우스 오버(Hover) 시 날짜 및 관객수 콤마 서식 적용
fig1.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>",
    line_color="#E50914",
)

fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객수 (명)",
    hovermode="x unified",
    height=450,
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    "(여기에 분석 소감을 작성해 주세요. 예: 개봉 초기 관객수가 가장 높았다가 주말마다 반등하는 패턴을 보입니다.)"
)

st.markdown("---")

# ==========================================
# [섹션 2] 관객수 Top 5 영화 비교
# ==========================================
st.header("📌 2. 관객수 Top 5 영화의 일관객수 추이 비교")

# 1. 기간 내 전체 일관객 합계 기준 상위 5개 영화 선정
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .nlargest(5)
    .index
    .tolist()
)

# 2. 상위 5개 영화 데이터만 필터링 후 날짜순 정렬
top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values(by="날짜")
    .reset_index(drop=True)
)

# 3. 색상 구분 선 그래프 생성
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="기간 내 관객수 상위 5개 영화의 일관객수 비교",
    labels={"날짜": "날짜", "일관객": "일일 관객수 (명)", "영화명": "영화 제목"},
)

# 마우스 오버(Hover) 서식 설정
fig2.update_traces(
    hovertemplate="<b>영화명:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객수 (명)",
    hovermode="x unified",
    height=500,
    legend=dict(
        title_text="영화 제목 (클릭 시 ON/OFF)",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    "(여기에 분석 소감을 작성해 주세요. 예: 흥행 상위 영화들의 개봉 시기와 최전성기 관객 규모를 한눈에 비교할 수 있습니다.)"
)

st.markdown("---")

# ==========================================
# [섹션 3] 날짜별 TOP 10 총 관객수 영역 그래프
# ==========================================
st.header("📌 3. 날짜별 박스오피스 TOP 10 총 관객수 추이")

# 1. 날짜별 일관객 합계 구하기
daily_sum = (
    df.groupby("날짜")["일관객"]
    .sum()
    .reset_index()
    .sort_values("날짜")
)

# 2. 영역 그래프(Area Chart) 생성
fig3 = px.area(
    daily_sum,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 TOP 10 총 관객수 (영역 그래프)",
    labels={"날짜": "날짜", "일관객": "TOP 10 총 관객수 (명)"},
)

# 마우스 오버 서식 지정
fig3.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>TOP 10 총 관객수:</b> %{y:,}명<extra></extra>",
    line_color="#2b5c8f",
    fillcolor="rgba(43, 92, 143, 0.3)",
)

# 3. 관객수 합계 상위 3일 구하기
top3_days = daily_sum.nlargest(3, "일관객")

# 4. 상위 3일을 그래프 위에 강조 포인트(Scatter) 및 날짜 텍스트로 표시
fig3.add_trace(
    go.Scatter(
        x=top3_days["날짜"],
        y=top3_days["일관객"],
        mode="markers+text",
        name="관객수 Peak Top 3",
        text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
        textposition="top center",
        marker=dict(size=12, color="red", symbol="diamond"),
        hovertemplate="<b>[Peak Top 3]</b><br>날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>",
    )
)

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="총 관객수 (명)",
    hovermode="x unified",
    height=500,
    showlegend=False,
)

# 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    "(여기에 분석 소감을 작성해 주세요. 예: 연휴나 명절 기간에 박스오피스 전체 관객수가 크게 솟구치는 피크를 형성합니다.)"
)

st.markdown("---")

# ==========================================
# [섹션 4] 전체 기간 일관객 TOP 10 가로 막대그래프
# ==========================================
st.header("📌 4. 전체 기간 관객수 TOP 10 영화")

# 1. 영화별 일관객 합계 및 TOP 10 진입 일수 집계
top10_sum = (
    df.groupby("영화명")
    .agg(
        총관객수=("일관객", "sum"),
        진입일수=("날짜", "nunique"),
    )
    .reset_index()
    .nlargest(10, "총관객수")
)

# 막대그래프 상단에 관객수가 가장 많은 영화가 오도록 오름차순 정렬
top10_sum = top10_sum.sort_values(by="총관객수", ascending=True)

# 2. 가로 막대그래프(Horizontal Bar Chart) 생성
fig4 = px.bar(
    top10_sum,
    x="총관객수",
    y="영화명",
    orientation="h",
    title="기간 내 일관객 합계 TOP 10 영화",
    labels={"총관객수": "총 관객수 (명)", "영화명": "영화 제목"},
    text_auto=",",
)

# 마우스 오버 시 총 관객수와 10위권 진입 일수 표시
fig4.update_traces(
    textposition="outside",
    marker_color="#2ca02c",
    customdata=top10_sum[["진입일수"]],
    hovertemplate="<b>영화명:</b> %{y}<br><b>총 관객수:</b> %{x:,}명<br><b>10위권 진입 일수:</b> %{customdata[0]}일<extra></extra>",
)

fig4.update_layout(
    xaxis_title="총 관객수 (명)",
    yaxis_title="",
    height=500,
)

# 그래프 출력
st.plotly_chart(fig4, use_container_width=True)

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    "(여기에 분석 소감을 작성해 주세요. 예: 누적 관객수가 높은 영화일수록 10위권 내에 오래 머물렀음을 알 수 있습니다.)"
)

st.markdown("---")

# ==========================================
# [섹션 5] 월×요일별 일관객 합계 히트맵
# ==========================================
st.header("📌 5. 월별·요일별 관객수 분포 (히트맵)")

# 1. 월 및 요일 컬럼 추출
df_heatmap = df.copy()
df_heatmap["월"] = df_heatmap["날짜"].dt.strftime("%m월")

# 요일명을 한국어로 변환 및 월요일~일요일 순서 범주형 지정
weekday_map = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일",
}
weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]

df_heatmap["요일"] = df_heatmap["날짜"].dt.weekday.map(weekday_map)

# 2. 월, 요일별 일관객 합계 피벗 테이블 생성
pivot_df = df_heatmap.pivot_table(
    index="월", columns="요일", values="일관객", aggfunc="sum"
).fillna(0)

# 요일을 월요일~일요일 순서로 정렬
pivot_df = pivot_df.reindex(columns=weekday_order)

# 3. Plotly 히트맵(Heatmap) 생성
fig5 = px.imshow(
    pivot_df,
    labels=dict(x="요일", y="월", color="총 관객수 (명)"),
    title="월별 × 요일별 일관객 합계 히트맵",
    color_continuous_scale="Reds",  # 색이 진할수록 높은 관객수
    text_auto=",",  # 셀 안에 관객수 콤마 서식 표시
)

# 마우스 오버 툴팁 서식 지정
fig5.update_traces(
    hovertemplate="<b>월:</b> %{y}<br><b>요일:</b> %{x}<br><b>관객수 합계:</b> %{z:,}명<extra></extra>"
)

fig5.update_layout(
    height=500,
    xaxis_title="요일",
    yaxis_title="월",
)

# 그래프 출력
st.plotly_chart(fig5, use_container_width=True)

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    "(여기에 분석 소감을 작성해 주세요. 예: 연중 특정 월의 주말(토·일)에 관객 몰림 현상이 가장 두드러지며, 평일 중 수요일 및 금요일에 관객수가 상승하는 경향을 확인할 수 있습니다.)"
)

st.markdown("---")

# ==========================================
# [섹션 6] 향후 추가될 그래프 구역
# ==========================================
st.header("📌 6. (추가 예정 구역)")
st.caption(
    "앞으로 '시간'과 관련된 다양한 영화 데이터 그래프가 계속 추가될 영역입니다."
)
