import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def preprocess_data(data):
    data = data[['last_name, first_name', 'player_id', 'pa', 'k_percent', 'bb_percent', 
                 'woba', 'xwoba', 'avg_swing_speed', 'sweet_spot_percent', 
                 'barrel_batted_rate', 'hard_hit_percent']]
    data.dropna(inplace=True)

# 2. 점수 계산 함수
def calculate_scores(data):
    # wOBA, xwOBA, sweet_spot_percent, barrel_batted_rate에 가중치를 적용한 점수 계산
    data['score'] = (
        0.3 * data['woba'] +
        0.3 * data['xwoba'] +
        0.2 * data['sweet_spot_percent'] +
        0.2 * data['barrel_batted_rate']
    )
    # 상위 20명 추출
    top_scorers = data.nlargest(20, 'score')
    return top_scorers

# 3. 데이터 분석 함수
def analyze_data(data):
    return data.describe()

# 4. 시각화 함수: 상위 20명의 점수 시각화
def visualize_top_scorers(data):
    # 그래프 스타일 설정
    sns.set_theme(style="whitegrid")

    # 가로형 막대 그래프
    fig, ax = plt.subplots(figsize=(10, 8))  # 크기 조정
    sns.barplot(
        y='last_name, first_name', 
        x='score', 
        data=data, 
        palette="viridis",  # 색상 테마
        ax=ax
    )

    # 그래프 제목 및 레이블
    ax.set_title("Top 20 Valuable Batters by JH", fontsize=16, weight='bold')
    ax.set_xlabel("Score", fontsize=12)
    ax.set_ylabel("Player", fontsize=12)

    # 막대 위에 점수 값 표시
    for i, row in enumerate(data.itertuples()):
        ax.text(row.score + 0.01, i, f"{row.score:.2f}", va='center', fontsize=10)

    plt.tight_layout()  # 그래프 간격 자동 조정
    return fig


# 5. 추가 시각화 함수
def visualize_woba_xwoba(data):
    data = data.nlargest(20, 'pa')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        x='woba', 
        y='xwoba', 
        hue='last_name, first_name',  # 타자별 색상
        palette='tab10',             # 색상 팔레트
        data=data, 
        ax=ax
    )
    ax.set_title("wOBA vs xwOBA", fontsize=14, weight='bold')
    ax.set_xlabel("wOBA", fontsize=12)
    ax.set_ylabel("xwOBA", fontsize=12)
    ax.legend(title="Player", bbox_to_anchor=(1.05, 1), loc='upper left')  # 범례 위치
    plt.tight_layout()
    return fig

def visualize_barrel_vs_hard_hit(data):
    data = data.nlargest(20, 'pa')
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = sns.scatterplot(
        x='barrel_batted_rate', 
        y='hard_hit_percent', 
        data=data, 
        ax=ax,
        s=100,                     # 점 크기
        color='steelblue',         # 점 색상
        edgecolor='black'          # 점 테두리 색상
    )
    ax.set_title("Barrel Batted Rate vs Hard Hit Percent", fontsize=14, weight='bold')
    ax.set_xlabel("Barrel Batted Rate", fontsize=12)
    ax.set_ylabel("Hard Hit Percent", fontsize=12)

    # 각 점에 이름 표시
    for i, row in data.iterrows():
        ax.text(
            row['barrel_batted_rate'] + 0.005,  # x 위치 조정
            row['hard_hit_percent'],           # y 위치
            row['last_name, first_name'],      # 타자 이름
            fontsize=9, 
            color='darkred'
        )
    plt.tight_layout()
    return fig


# Streamlit 앱
st.title("MLB 2024 데이터 분석")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    # 데이터 로드 및 전처리
    data = pd.read_csv(uploaded_file)
    data = preprocess_data(data)
    
    # 데이터 요약
    st.write("📊 데이터 요약")
    st.dataframe(analyze_data(data))
    
    # 상위 20명 점수 계산 및 시각화
    top_scorers = calculate_scores(data)
    st.write("🏆 상위 20 타자 (점수 기반)")
    st.dataframe(top_scorers[['last_name, first_name', 'score']])
    st.pyplot(visualize_top_scorers(top_scorers))
    
    # 추가 그래프
    st.write("📈 추가 데이터 시각화")
    additional_charts = visualize_woba_xwoba(data), visualize_barrel_vs_hard_hit(data)
    for fig in additional_charts:
        st.pyplot(fig)
