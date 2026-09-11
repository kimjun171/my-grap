import pandas as pd
import plotly.express as px
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
# [섹션 1] 영화별 일관객수 시간 추이 분석
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
    markers=True,  # 데이터 포인트 마커 표시
)

# 마우스 오버(Hover) 시 날짜 및 관객수 콤마 서식 적용
fig1.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>",
    line_color="#E50914",  # 강조 라인 색상
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
# [섹션 2] 향후 추가될 그래프 구역
# ==========================================
st.header("📌 2. (추가 예정 구역)")
st.caption(
    "앞으로 '시간'과 관련된 다양한 영화 그래프(예: 주말 vs 평일 관객 비교, 상영 기간별 누적 관객 추이 등)가 추가될 영역입니다."
)
