import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go

# ── 페이지 설정 ────────────────────────────────────────────
st.set_page_config(
    page_title="Seoul Travel Style Dashboard",
    page_icon="🗺️",
    layout="wide"
)

# ── 커스텀 CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp { background-color: #f8f9fa; }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ffffff;
        padding: 8px 12px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
        font-size: 14px;
        color: #555;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A5F !important;
        color: white !important;
    }

    /* 카드 스타일 */
    .neighborhood-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid;
        transition: transform 0.2s;
        cursor: pointer;
    }
    .neighborhood-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }

    /* 결과 박스 */
    .result-box {
        background: linear-gradient(135deg, #1E3A5F, #2563EB);
        color: white;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 16px 0;
    }

    /* 헤더 배너 */
    .main-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #2563EB 100%);
        color: white;
        padding: 32px 40px;
        border-radius: 16px;
        margin-bottom: 24px;
    }

    /* 스팟 카드 */
    .spot-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 16px;
    }

    /* 통계 카드 */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ── 데이터 불러오기 ────────────────────────────────────────
@st.cache_data
def load_data():
    nb = pd.read_csv("neighborhoods.csv")
    spots = pd.read_csv("spots.csv")
    return nb, spots

nb, spots = load_data()

# ── 색상 & 이모지 설정 ─────────────────────────────────────
COLORS = {
    "Hongdae":    "#FF6B6B",
    "Seongsu":    "#4ECDC4",
    "Bukchon":    "#45B7D1",
    "Insadong":   "#52B788",
    "Itaewon":    "#F4A261",
    "Gangnam":    "#9B5DE5",
    "Euljiro":    "#F0A500",
    "Yeonnam":    "#74C69D",
    "Myeongdong": "#F28B82",
}

STYLE_EMOJI = {
    "Healing 힐링": "🌿",
    "Active 액티브": "⚡",
    "Food Travel 미식": "🍜",
    "Culture 문화탐방": "🏛️",
}

# ── 메인 헤더 ──────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size:32px; font-weight:700;">
        🗺️ Seoul Neighborhood Travel Style Dashboard
    </h1>
    <p style="margin:8px 0 0; font-size:16px; opacity:0.85;">
        Discover Your Personal Seoul — Find the neighborhood that matches your travel style
    </p>
</div>
""", unsafe_allow_html=True)

# ── 상단 통계 ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""<div class="stat-card">
        <div style="font-size:28px; font-weight:700; color:#1E3A5F;">9</div>
        <div style="font-size:13px; color:#888; margin-top:4px;">Neighborhoods</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="stat-card">
        <div style="font-size:28px; font-weight:700; color:#2563EB;">37</div>
        <div style="font-size:13px; color:#888; margin-top:4px;">Key Spots</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="stat-card">
        <div style="font-size:28px; font-weight:700; color:#F0A500;">4</div>
        <div style="font-size:13px; color:#888; margin-top:4px;">Travel Styles</div>
    </div>""", unsafe_allow_html=True)
with c4:
    avg_rating = nb["google_rating"].mean()
    st.markdown(f"""<div class="stat-card">
        <div style="font-size:28px; font-weight:700; color:#52B788;">⭐ {avg_rating:.1f}</div>
        <div style="font-size:13px; color:#888; margin-top:4px;">Avg Google Rating</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:20px 0'></div>", unsafe_allow_html=True)

# ── 탭 구성 ───────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️  Map Explorer",
    "🎯  Find My Style",
    "🏘️  Neighborhoods",
    "📍  Key Spots",
    "📊  Data Table",
])

# ═══════════════════════════════════════════════════════════
# TAB 1 — MAP EXPLORER
# ═══════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 📍 Interactive Seoul Map")
    st.caption("마커 위에 커서를 올리거나 클릭하면 동네 정보를 볼 수 있어요!")

    m = folium.Map(
        location=[37.5665, 126.9780],
        zoom_start=12,
        tiles="CartoDB positron"
    )

    for _, row in nb.iterrows():
        color = COLORS.get(row["neighborhood"], "#888")

        popup_html = f"""
        <div style='font-family:sans-serif; width:220px; padding:8px'>
            <div style='background:{color}22; border-left:4px solid {color};
                        border-radius:6px; padding:8px 10px; margin-bottom:8px'>
                <b style='font-size:15px; color:#1E3A5F'>
                    {row['neighborhood_kr']}
                </b>
                <span style='color:#666; font-size:12px'> {row['neighborhood']}</span>
            </div>
            <table style='width:100%; font-size:12px; border-collapse:collapse'>
                <tr><td style='color:#888; padding:2px 0'>⭐ Rating</td>
                    <td style='font-weight:600'>{row['google_rating']} / 5.0</td></tr>
                <tr><td style='color:#888; padding:2px 0'>📸 Instagram</td>
                    <td style='font-weight:600'>{int(row['instagram_mentions']):,}</td></tr>
                <tr><td style='color:#888; padding:2px 0'>🎯 Vibe</td>
                    <td style='font-weight:600'>{row['vibe_score']} / 10</td></tr>
                <tr><td style='color:#888; padding:2px 0'>🍽️ Food</td>
                    <td style='font-weight:600'>{row['food_score']} / 10</td></tr>
                <tr><td style='color:#888; padding:2px 0'>🚇 Subway</td>
                    <td style='font-weight:600'>{row['subway_lines']}</td></tr>
                <tr><td style='color:#888; padding:2px 0'>☕ Avg Coffee</td>
                    <td style='font-weight:600'>₩{int(row['avg_coffee_price']):,}</td></tr>
            </table>
            <div style='margin-top:8px; font-size:11px; color:#666;
                        border-top:1px solid #eee; padding-top:6px'>
                {row['description_en'][:100]}...
            </div>
        </div>
        """

        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=18,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            popup=folium.Popup(popup_html, max_width=240),
            tooltip=folium.Tooltip(
                f"<b>{row['neighborhood_kr']}</b> {row['neighborhood']}<br>"
                f"⭐ {row['google_rating']}  |  📸 {int(row['instagram_mentions'])//10000}만",
                style="font-family:sans-serif; font-size:13px;"
            )
        ).add_to(m)

        folium.Marker(
            location=[row["lat"] + 0.0028, row["lng"]],
            icon=folium.DivIcon(
                html=f"<div style='font-size:11px; font-weight:700; "
                     f"color:#1E3A5F; white-space:nowrap; "
                     f"text-shadow:1px 1px 2px white, -1px -1px 2px white'>"
                     f"{row['neighborhood_kr']}</div>",
                icon_size=(90, 20),
                icon_anchor=(45, 0)
            )
        ).add_to(m)

    # 주요 스팟 마커도 추가
    for _, row in spots[spots["must_visit"] == True].iterrows():
        folium.Marker(
            location=[row["lat"], row["lng"]],
            icon=folium.Icon(color="white", icon="star", prefix="fa"),
            tooltip=folium.Tooltip(
                f"⭐ {row['spot_name']}<br>{row['spot_name_kr']}",
                style="font-family:sans-serif; font-size:12px;"
            ),
            popup=folium.Popup(
                f"<div style='font-family:sans-serif; width:180px'>"
                f"<b>{row['spot_name']}</b><br>"
                f"<span style='color:#666; font-size:11px'>{row['spot_name_kr']}</span><br>"
                f"<hr style='margin:5px 0'>"
                f"📍 {row['neighborhood']}<br>"
                f"🏷️ {row['category']}<br>"
                f"⭐ {row['google_rating']}<br>"
                f"<small>{row['description'][:70]}...</small>"
                f"</div>",
                max_width=200
            )
        ).add_to(m)

    st_folium(m, width=None, height=560, use_container_width=True)

    st.markdown("""
    <div style='background:#f0f4ff; border-radius:10px; padding:12px 16px;
                font-size:13px; color:#444; margin-top:8px'>
        💡 <b>범례:</b> 색깔 원 = 동네 마커 (클릭/호버) &nbsp;|&nbsp;
        ⭐ 흰 별 = 주요 스팟 (must-visit 장소)
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 2 — FIND MY STYLE
# ═══════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🎯 Find Your Perfect Seoul Neighborhood")
    st.markdown("아래 질문에 답하면 나에게 맞는 동네를 추천해드려요!")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_q, col_r = st.columns([1.2, 1])

    with col_q:
        st.markdown("#### ① 여행 스타일을 선택하세요")
        travel_style = st.radio(
            "",
            ["Healing 힐링", "Active 액티브", "Food Travel 미식", "Culture 문화탐방"],
            format_func=lambda x: f"{STYLE_EMOJI[x]} {x}",
            horizontal=False,
            label_visibility="collapsed"
        )

        st.markdown("#### ② 선호하는 카테고리 (복수 선택)")
        cat_cafe     = st.checkbox("☕ Cafe  카페", value=True)
        cat_food     = st.checkbox("🍜 Food  맛집", value=True)
        cat_shopping = st.checkbox("🛍️ Shopping  쇼핑")
        cat_culture  = st.checkbox("🏛️ Culture  문화/역사")

        st.markdown("#### ③ 분위기 선호도")
        vibe_pref = st.slider(
            "조용함 ← → 활기참",
            min_value=1, max_value=10, value=5,
            help="1 = 매우 조용한 곳, 10 = 매우 활기찬 곳"
        )

        find_btn = st.button("🔍  나에게 맞는 동네 찾기!", use_container_width=True)

    with col_r:
        st.markdown("#### 📖 여행 스타일 가이드")
        style_guide = {
            "Healing 힐링": {
                "desc": "조용하고 여유로운 여행을 좋아해요. 카페에서 책 읽기, 공원 산책, 감성 골목 탐방이 좋아요.",
                "best": ["Yeonnam", "Seongsu", "Bukchon"],
                "icon": "🌿"
            },
            "Active 액티브": {
                "desc": "에너지 넘치는 여행! 버스킹, 클럽, 쇼핑, 나이트라이프를 즐겨요.",
                "best": ["Hongdae", "Itaewon", "Gangnam"],
                "icon": "⚡"
            },
            "Food Travel 미식": {
                "desc": "먹는 게 여행의 전부! 트렌디한 맛집, 길거리 음식, 다국적 요리를 탐험해요.",
                "best": ["Seongsu", "Itaewon", "Myeongdong"],
                "icon": "🍜"
            },
            "Culture 문화탐방": {
                "desc": "역사와 문화에 관심이 많아요. 궁궐, 한옥, 박물관, 독립 문화 공간을 좋아해요.",
                "best": ["Bukchon", "Insadong", "Euljiro"],
                "icon": "🏛️"
            },
        }

        guide = style_guide[travel_style]
        best_names = ", ".join(guide["best"])
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:20px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06)'>
            <div style='font-size:36px; margin-bottom:8px'>{guide["icon"]}</div>
            <b style='font-size:16px; color:#1E3A5F'>{travel_style}</b>
            <p style='color:#555; font-size:14px; margin:8px 0 12px'>{guide["desc"]}</p>
            <div style='background:#f0f4ff; border-radius:8px; padding:10px 12px;
                        font-size:13px; color:#2563EB'>
                🏆 추천 동네: <b>{best_names}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── 결과 계산 ────────────────────────────────────────
    if find_btn:
        st.markdown("---")
        st.markdown("### 🏆 추천 결과")

        style_col_map = {
            "Healing 힐링":       "healing_score",
            "Active 액티브":      "active_score",
            "Food Travel 미식":   "food_travel_score",
            "Culture 문화탐방":   "culture_travel_score",
        }
        style_col = style_col_map[travel_style]

        # 카테고리 가중치 점수
        def calc_score(row):
            base = float(row[style_col]) * 4.0
            if cat_cafe:     base += float(row["cafe_ratio"])  * 0.05
            if cat_food:     base += float(row["food_ratio"])  * 0.05
            if cat_shopping: base += float(row["shopping_ratio"]) * 0.05
            if cat_culture:  base += float(row["culture_ratio"]) * 0.05
            # 분위기 유사도 (거리 역수)
            vibe_diff = abs(float(row["vibe_score"]) - vibe_pref)
            base += (10 - vibe_diff) * 0.5
            return round(base, 1)

        nb["match_score"] = nb.apply(calc_score, axis=1)
        ranked = nb.sort_values("match_score", ascending=False).reset_index(drop=True)

        # TOP 1 결과
        top = ranked.iloc[0]
        top_color = COLORS.get(top["neighborhood"], "#2563EB")
        top_tags = " ".join([f'<span style="background:{top_color}22; color:{top_color}; '
                             f'border-radius:20px; padding:3px 10px; font-size:12px; '
                             f'margin:2px; display:inline-block">{t}</span>'
                             for t in top["persona_tags"].split()[:5]])

        st.markdown(f"""
        <div style='background:linear-gradient(135deg, #1E3A5F, #2563EB);
                    color:white; border-radius:16px; padding:28px 32px; margin-bottom:20px'>
            <div style='font-size:13px; opacity:0.8; margin-bottom:4px'>
                {STYLE_EMOJI[travel_style]} 당신의 여행 스타일에 가장 잘 맞는 동네는
            </div>
            <div style='font-size:36px; font-weight:700; margin-bottom:4px'>
                {top["neighborhood_kr"]} ({top["neighborhood"]})
            </div>
            <div style='font-size:15px; opacity:0.9; margin-bottom:12px'>
                {top["description_en"][:120]}...
            </div>
            <div style='display:flex; gap:16px; font-size:14px'>
                <span>⭐ {top["google_rating"]}</span>
                <span>📸 {int(top["instagram_mentions"])//10000}만</span>
                <span>🚇 {top["subway_lines"]}</span>
                <span>☕ ₩{int(top["avg_coffee_price"]):,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # TOP 3 랭킹
        st.markdown("#### 📊 전체 동네 매칭 점수")
        r_cols = st.columns(3)
        medals = ["🥇", "🥈", "🥉"]
        for i, (_, row) in enumerate(ranked.head(3).iterrows()):
            color = COLORS.get(row["neighborhood"], "#888")
            pct = int((row["match_score"] / ranked["match_score"].max()) * 100)
            with r_cols[i]:
                st.markdown(f"""
                <div style='background:white; border-radius:12px; padding:16px;
                            box-shadow:0 2px 8px rgba(0,0,0,0.06);
                            border-top:4px solid {color}'>
                    <div style='font-size:22px'>{medals[i]}</div>
                    <b style='font-size:16px; color:#1E3A5F'>{row["neighborhood_kr"]}</b>
                    <div style='color:#666; font-size:12px; margin:4px 0'>{row["neighborhood"]}</div>
                    <div style='background:#f0f0f0; border-radius:20px;
                                height:8px; margin:8px 0; overflow:hidden'>
                        <div style='background:{color}; width:{pct}%;
                                    height:100%; border-radius:20px'></div>
                    </div>
                    <div style='font-size:12px; color:#888'>Match: {pct}%</div>
                </div>
                """, unsafe_allow_html=True)

        # 전체 바 차트
        fig = px.bar(
            ranked,
            x="match_score",
            y="neighborhood_kr",
            orientation="h",
            color="neighborhood",
            color_discrete_map={row["neighborhood"]: COLORS.get(row["neighborhood"], "#888")
                                 for _, row in ranked.iterrows()},
            labels={"match_score": "Match Score", "neighborhood_kr": ""},
            title=f"All Neighborhoods — Match Score for '{travel_style}'"
        )
        fig.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            height=360,
            font=dict(family="sans-serif"),
            yaxis=dict(categoryorder="total ascending"),
        )
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 3 — NEIGHBORHOODS
# ═══════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🏘️ Neighborhood Profiles")

    selected_nb = st.selectbox(
        "동네를 선택해서 자세한 정보를 보세요:",
        nb["neighborhood"].tolist(),
        format_func=lambda x: f"{x}  ({nb[nb['neighborhood']==x]['neighborhood_kr'].values[0]})"
    )

    row = nb[nb["neighborhood"] == selected_nb].iloc[0]
    color = COLORS.get(selected_nb, "#2563EB")

    # 헤더 카드
    tags_html = " ".join([
        f'<span style="background:{color}22; color:{color}; border-radius:20px; '
        f'padding:4px 12px; font-size:12px; margin:2px; display:inline-block">{t}</span>'
        for t in row["persona_tags"].split()[:6]
    ])

    st.markdown(f"""
    <div style='background:white; border-radius:16px; padding:24px;
                box-shadow:0 2px 12px rgba(0,0,0,0.08); margin-bottom:16px;
                border-left:6px solid {color}'>
        <h2 style='margin:0 0 4px; color:#1E3A5F'>
            {row["neighborhood_kr"]}
            <span style='color:#888; font-size:18px; font-weight:400'>
                &nbsp;{row["neighborhood"]}
            </span>
        </h2>
        <p style='color:#555; margin:8px 0 12px; font-size:15px'>
            {row["description_en"]}
        </p>
        <div>{tags_html}</div>
        <div style='display:flex; gap:20px; margin-top:14px; font-size:14px; color:#444'>
            <span>⭐ <b>{row["google_rating"]}</b></span>
            <span>📸 <b>{int(row["instagram_mentions"]):,}</b></span>
            <span>🚇 <b>{row["subway_lines"]}</b></span>
            <span>☕ <b>₩{int(row["avg_coffee_price"]):,}</b></span>
            <span>📝 <b>{int(row["review_count"]):,} reviews</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        # 레이더 차트
        categories = ["Vibe", "Food", "Shopping", "Culture", "Accessibility", "Nightlife"]
        values = [
            row["vibe_score"], row["food_score"], row["shopping_score"],
            row["culture_score"], row["accessibility"], row["nightlife_score"]
        ]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=f"{color}33",
            line=dict(color=color, width=2),
            name=selected_nb
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            title="Neighborhood Score Profile",
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=320,
            margin=dict(t=50, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_right:
        # 시간대 바 차트
        time_data = pd.DataFrame({
            "Time": ["🌅 Morning", "☀️ Afternoon", "🌆 Evening", "🌙 Night"],
            "Activity": [row["morning"], row["afternoon"], row["evening"], row["night"]]
        })
        fig_time = px.bar(
            time_data, x="Time", y="Activity",
            color="Activity",
            color_continuous_scale=[[0, "#e8f4fd"], [1, color]],
            title="Best Time to Visit",
            labels={"Activity": "Activity Level (1-10)"},
            range_y=[0, 10]
        )
        fig_time.update_layout(
            showlegend=False, coloraxis_showscale=False,
            paper_bgcolor="white", plot_bgcolor="white",
            height=320, margin=dict(t=50, b=20)
        )
        st.plotly_chart(fig_time, use_container_width=True)

    # 카테고리 비율 도넛 차트
    st.markdown("#### 🗂️ Category Composition")
    fig_donut = px.pie(
        values=[row["cafe_ratio"], row["food_ratio"],
                row["culture_ratio"], row["shopping_ratio"]],
        names=["☕ Cafe", "🍜 Food", "🏛️ Culture", "🛍️ Shopping"],
        hole=0.45,
        color_discrete_sequence=["#4ECDC4", "#FF6B6B", "#45B7D1", "#9B5DE5"]
    )
    fig_donut.update_layout(
        paper_bgcolor="white", height=300,
        margin=dict(t=20, b=20), showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    # 여행 스타일 적합도
    st.markdown("#### 🎯 Travel Style Match Score")
    style_scores = pd.DataFrame({
        "Style": ["🌿 Healing", "⚡ Active", "🍜 Food Travel", "🏛️ Culture"],
        "Score": [row["healing_score"], row["active_score"],
                  row["food_travel_score"], row["culture_travel_score"]]
    })
    for _, s in style_scores.iterrows():
        pct = int(s["Score"] * 10)
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:8px'>
            <div style='width:120px; font-size:14px; color:#444'>{s["Style"]}</div>
            <div style='flex:1; background:#f0f0f0; border-radius:20px;
                        height:12px; overflow:hidden'>
                <div style='background:{color}; width:{pct}%;
                            height:100%; border-radius:20px'></div>
            </div>
            <div style='width:30px; font-size:13px; color:#666; text-align:right'>
                {int(s["Score"])}/10
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 4 — KEY SPOTS
# ═══════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📍 Key Spots by Neighborhood")

    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_area = st.selectbox(
            "동네 선택:",
            ["All"] + nb["neighborhood"].tolist(),
            format_func=lambda x: "🗺️ 전체 보기" if x == "All"
                else f"{x} ({nb[nb['neighborhood']==x]['neighborhood_kr'].values[0]})"
        )
    with col_filter2:
        selected_cat = st.selectbox(
            "카테고리 선택:",
            ["All", "cafe", "landmark", "park", "museum", "market",
             "shopping", "nightlife", "kpop", "neighborhood"]
        )

    filtered = spots.copy()
    if selected_area != "All":
        filtered = filtered[filtered["neighborhood"] == selected_area]
    if selected_cat != "All":
        filtered = filtered[filtered["category"] == selected_cat]

    must_only = st.checkbox("⭐ Must-visit 장소만 보기", value=False)
    if must_only:
        filtered = filtered[filtered["must_visit"] == True]

    st.markdown(f"**{len(filtered)}개 장소** 표시 중")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # 스팟 카드 그리드
    CAT_EMOJI = {
        "cafe": "☕", "landmark": "🏛️", "park": "🌿",
        "museum": "🖼️", "market": "🛒", "shopping": "🛍️",
        "nightlife": "🌙", "kpop": "🎵", "neighborhood": "📍"
    }
    PRICE_LABEL = {"$": "저렴", "$$": "보통", "$$$": "고급"}

    cols_per_row = 3
    rows = [filtered.iloc[i:i+cols_per_row]
            for i in range(0, len(filtered), cols_per_row)]

    for row_group in rows:
        cols = st.columns(cols_per_row)
        for col, (_, spot) in zip(cols, row_group.iterrows()):
            nb_color = COLORS.get(spot["neighborhood"], "#888")
            emoji = CAT_EMOJI.get(spot["category"], "📍")
            price_label = PRICE_LABEL.get(str(spot.get("price_range", "$")), "보통")
            must_badge = (
                '<span style="background:#FFD700; color:#333; border-radius:20px; '
                'padding:2px 8px; font-size:11px; font-weight:600">⭐ Must Visit</span>'
                if spot["must_visit"] else ""
            )
            with col:
                st.markdown(f"""
                <div style='background:white; border-radius:12px; padding:16px;
                            box-shadow:0 2px 8px rgba(0,0,0,0.07);
                            border-top:3px solid {nb_color}; margin-bottom:8px;
                            min-height:160px'>
                    <div style='display:flex; justify-content:space-between;
                                align-items:flex-start; margin-bottom:8px'>
                        <span style='font-size:22px'>{emoji}</span>
                        {must_badge}
                    </div>
                    <b style='font-size:14px; color:#1E3A5F'>{spot["spot_name"]}</b><br>
                    <span style='color:#666; font-size:12px'>{spot["spot_name_kr"]}</span>
                    <div style='margin:8px 0; font-size:12px; color:#555;
                                line-height:1.5'>
                        {spot["description"][:90]}...
                    </div>
                    <div style='display:flex; gap:8px; font-size:11px; color:#888;
                                flex-wrap:wrap; margin-top:6px'>
                        <span style='background:{nb_color}22; color:{nb_color};
                                     border-radius:20px; padding:2px 8px'>
                            {spot["neighborhood"]}
                        </span>
                        <span>⭐ {spot["google_rating"]}</span>
                        <span>💰 {price_label}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 5 — DATA TABLE
# ═══════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 📊 Neighborhood Data Overview")
    st.markdown("모든 동네의 데이터를 한눈에 비교해보세요.")

    # 표시할 컬럼 선택
    display_cols = st.multiselect(
        "보고 싶은 항목 선택:",
        ["neighborhood_kr", "google_rating", "review_count", "instagram_mentions",
         "vibe_score", "food_score", "shopping_score", "culture_score",
         "accessibility", "nightlife_score", "healing_score", "active_score",
         "food_travel_score", "culture_travel_score", "avg_coffee_price",
         "subway_lines"],
        default=["neighborhood_kr", "google_rating", "instagram_mentions",
                 "vibe_score", "food_score", "culture_score",
                 "healing_score", "active_score"]
    )

    if display_cols:
        table_df = nb[display_cols].copy()

        # 컬럼명 한국어로
        rename_map = {
            "neighborhood_kr": "동네",
            "google_rating": "⭐ Google 평점",
            "review_count": "📝 리뷰 수",
            "instagram_mentions": "📸 인스타 언급량",
            "vibe_score": "🎯 활기",
            "food_score": "🍜 음식",
            "shopping_score": "🛍️ 쇼핑",
            "culture_score": "🏛️ 문화",
            "accessibility": "🚇 교통",
            "nightlife_score": "🌙 나이트",
            "healing_score": "🌿 힐링 적합도",
            "active_score": "⚡ 액티브 적합도",
            "food_travel_score": "🍜 미식 적합도",
            "culture_travel_score": "🏛️ 문화 적합도",
            "avg_coffee_price": "☕ 평균 커피값(₩)",
            "subway_lines": "🚇 지하철 노선",
        }
        table_df = table_df.rename(columns=rename_map)

        # 스타일 적용
        def color_score(val):
            if isinstance(val, (int, float)):
                if val >= 8:
                    return "background-color: #d4edda; color: #155724; font-weight:600"
                elif val >= 6:
                    return "background-color: #fff3cd; color: #856404"
                elif val < 4:
                    return "background-color: #f8d7da; color: #721c24"
            return ""

        styled = table_df.style.applymap(
            color_score,
            subset=[c for c in table_df.columns
                    if any(x in c for x in
                           ["활기", "음식", "쇼핑", "문화", "교통", "나이트",
                            "힐링", "액티브", "미식", "평점"])]
        ).format({
            "📸 인스타 언급량": "{:,.0f}",
            "📝 리뷰 수": "{:,.0f}",
            "☕ 평균 커피값(₩)": "₩{:,.0f}",
        }, na_rep="-")

        st.dataframe(styled, use_container_width=True, height=400)

        # 비교 차트
        st.markdown("#### 📈 Score Comparison Chart")
        score_cols_chart = ["vibe_score", "food_score", "shopping_score",
                            "culture_score", "accessibility", "nightlife_score"]
        score_cols_available = [c for c in score_cols_chart if c in nb.columns]

        chart_df = nb[["neighborhood_kr"] + score_cols_available].melt(
            id_vars="neighborhood_kr",
            var_name="Category",
            value_name="Score"
        )
        cat_label = {
            "vibe_score": "🎯 Vibe",
            "food_score": "🍜 Food",
            "shopping_score": "🛍️ Shopping",
            "culture_score": "🏛️ Culture",
            "accessibility": "🚇 Access",
            "nightlife_score": "🌙 Nightlife",
        }
        chart_df["Category"] = chart_df["Category"].map(cat_label)

        fig_compare = px.bar(
            chart_df,
            x="neighborhood_kr",
            y="Score",
            color="Category",
            barmode="group",
            title="All Neighborhoods — Score Comparison",
            labels={"neighborhood_kr": "", "Score": "Score (1-10)"},
            height=420,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_compare.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3),
            margin=dict(b=80)
        )
        st.plotly_chart(fig_compare, use_container_width=True)

        # 다운로드 버튼
        csv_export = nb.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 데이터 다운로드 (CSV)",
            data=csv_export,
            file_name="seoul_neighborhoods_data.csv",
            mime="text/csv"
        )

# ── 푸터 ──────────────────────────────────────────────────
st.markdown("""
<div style='background:white; border-radius:12px; padding:16px 24px;
            margin-top:32px; text-align:center;
            box-shadow:0 2px 8px rgba(0,0,0,0.06)'>
    <p style='margin:0; color:#888; font-size:13px'>
        📊 Data: Google Maps · Public travel guides · Manual research |
        🛠️ Built with Streamlit, Folium & Plotly |
        Arts and Big Data — SKKU 2026
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()
st.caption("📊 Data: Google Maps · Public travel guides · Manual research | Built with Streamlit & Folium")
