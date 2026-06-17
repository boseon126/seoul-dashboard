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

# ── Session State 초기화 ───────────────────────────────────
if "itinerary_stops"   not in st.session_state: st.session_state.itinerary_stops   = None
if "itinerary_budget"  not in st.session_state: st.session_state.itinerary_budget  = 0
if "itinerary_title"   not in st.session_state: st.session_state.itinerary_title   = ""
if "itinerary_meta"    not in st.session_state: st.session_state.itinerary_meta    = ""
if "itinerary_map_nbs" not in st.session_state: st.session_state.itinerary_map_nbs = []
if "lang"              not in st.session_state: st.session_state.lang              = "KO"

# ── 언어 텍스트 딕셔너리 ───────────────────────────────────
T = {
    "KO": {
        "title":        "🗺️ Seoul Neighborhood Travel Style Dashboard",
        "subtitle":     "**나만의 서울 발견하기** — 내 여행 스타일에 맞는 동네를 찾아봐요",
        "tab1":         "🗺️  지도 탐색",
        "tab2":         "🎯  내 스타일 찾기",
        "tab3":         "🏘️  동네 프로필",
        "tab4":         "📍  주요 스팟",
        "tab5":         "📊  데이터 표",
        "tab6":         "📸  SNS vs 현실",
        "tab7":         "🗓️  나만의 코스",
        "stat1":        "동네",
        "stat2":        "주요 스팟",
        "stat3":        "여행 스타일",
        "stat4":        "평균 평점",
        "map_title":    "📍 서울 동네 탐색",
        "map_caption":  "👆 마커를 클릭하거나 커서를 올리면 동네 정보를 볼 수 있어요!",
        "map_legend":   "💡 범례: 색깔 원 = 동네 마커 | ⭐ 흰 별 = 주요 스팟",
        "nb_overview":  "🏘️ 동네 한눈에 보기",
        "planner_title":"🗓️ 나만의 서울 하루 코스",
        "planner_sub":  "동네와 취향을 선택하면 맞춤 하루 여행 코스를 만들어드려요!",
        "plan_step1":   "① 방문할 동네 선택 (1~3개)",
        "plan_step2":   "② 여행 스타일",
        "plan_step3":   "③ 여행 인원",
        "plan_step4":   "④ 시작 시간",
        "plan_btn":     "✨  나만의 코스 생성하기!",
        "plan_preview": "💡 선택한 동네 미리보기",
        "plan_warn":    "동네를 최소 1개 선택해주세요!",
        "plan_budget":  "📊 하루 예상 총 비용",
        "plan_map":     "#### 📍 코스 지도",
        "transit_label":"이동",
        "styles":       ["🌿 Healing — 여유롭고 감성적인 하루",
                         "⚡ Active — 에너지 넘치고 바쁜 하루",
                         "🍜 Food Travel — 먹방 중심 하루",
                         "🏛️ Culture — 역사와 문화 탐방 하루"],
        "who":          ["혼자 solo", "커플 couple", "친구들 friends", "가족 family"],
        "preview_none": "왼쪽에서 동네를 선택해주세요!",
        "generated":    "📋 Generated Itinerary",
        "footer":       "📊 Data: Google Maps · 공개 여행 가이드 · 자체 조사 | 🛠️ Built with Streamlit, Folium & Plotly | Arts and Big Data — SKKU 2026",
        "lang_toggle":  "🌐 English",
        # Tab2 - Find My Style
        "find_title":   "### 🎯 내 여행 스타일 찾기",
        "find_sub":     "아래 질문에 답하면 나에게 맞는 동네를 추천해드려요!",
        "style_label":  "#### ① 여행 스타일을 선택하세요",
        "cat_label":    "#### ② 선호하는 카테고리 (복수 선택)",
        "vibe_label":   "#### ③ 분위기 선호도",
        "vibe_slider":  "조용함 ← → 활기참",
        "find_btn":     "🔍  나에게 맞는 동네 찾기!",
        "style_guide_title": "#### 📖 여행 스타일 가이드",
        "result_title": "### 🏆 추천 결과",
        "rank_title":   "#### 📊 전체 동네 매칭 점수",
        "cat_cafe":     "☕ Cafe  카페",
        "cat_food":     "🍜 Food  맛집",
        "cat_shop":     "🛍️ Shopping  쇼핑",
        "cat_culture":  "🏛️ Culture  문화/역사",
        "match_label":  "Match",
        "guide_best":   "추천 동네",
        # Tab3 - Neighborhoods
        "nb_select":    "동네를 선택해서 자세한 정보를 보세요:",
        "radar_title":  "Neighborhood Score Profile",
        "time_title":   "Best Time to Visit",
        "cat_comp":     "#### 🗂️ Category Composition",
        "style_match":  "#### 🎯 Travel Style Match Score",
        # Tab4 - Key Spots
        "spots_title":  "### 📍 주요 스팟",
        "area_filter":  "동네 선택:",
        "cat_filter":   "카테고리 선택:",
        "must_filter":  "⭐ Must-visit 장소만 보기",
        "spots_count":  "개 장소 표시 중",
        "gmaps_btn":    "🗺️ Google Maps에서 보기",
        # Tab5 - Data
        "data_title":   "### 📊 Neighborhood Data Overview",
        "data_sub":     "모든 동네의 데이터를 한눈에 비교해보세요.",
        "col_select":   "보고 싶은 항목 선택:",
        "dl_btn":       "📥 데이터 다운로드 (CSV)",
        "compare_title":"#### 📈 Score Comparison Chart",
        # Tab6 - SNS
        "sns_title":    "### 📸 SNS 인기도 vs 실제 만족도",
        "sns_sub":      "Instagram 언급량이 많은 동네가 실제로도 만족도가 높을까요?",
        "sns_card1":    "가장 인스타그래머블",
        "sns_card2":    "실제 만족도 1위",
        "sns_card3":    "숨은 보석 (과소평가)",
        "sns_scatter":  "#### 🔍 Instagram Mentions vs. Google Rating",
        "sns_scatter_cap": "버블 크기 = 리뷰 수 | 오른쪽 위 = SNS도 인기, 평점도 높음",
        "sns_gap":      "#### 📊 SNS 순위 vs 평점 순위 — Gap 분석",
        "sns_gap_cap":  "양수(+) = 숨은 보석 | 음수(-) = 과대평가",
        "sns_insight":  "#### 💡 Key Insights",
        "mentions":     "mentions",
        "quad1":        "🌟 SNS 인기 + 고평점",
        "quad2":        "💎 숨은 보석",
        "quad3":        "📸 SNS만 화려",
        "ins1_title":   "📸 SNS 버블 주의",
        "ins1_body":    "성수동과 홍대는 Instagram 언급량이 압도적으로 높지만, 실제 Google 평점은 북촌·연남동보다 낮아요. SNS 인기가 반드시 높은 만족도를 보장하지 않아요.",
        "ins2_title":   "💎 숨은 보석을 찾아라",
    },
    "EN": {
        "title":        "🗺️ Seoul Neighborhood Travel Style Dashboard",
        "subtitle":     "**Discover Your Personal Seoul** — Find the neighborhood that matches your travel style",
        "tab1":         "🗺️  Map Explorer",
        "tab2":         "🎯  Find My Style",
        "tab3":         "🏘️  Neighborhoods",
        "tab4":         "📍  Key Spots",
        "tab5":         "📊  Data Table",
        "tab6":         "📸  SNS vs Reality",
        "tab7":         "🗓️  My Seoul Planner",
        "stat1":        "Neighborhoods",
        "stat2":        "Key Spots",
        "stat3":        "Travel Styles",
        "stat4":        "Avg Rating",
        "map_title":    "📍 Explore Seoul's Neighborhoods",
        "map_caption":  "👆 Click on any marker or hover to see neighborhood details!",
        "map_legend":   "💡 Legend: Colored circle = neighborhood | ⭐ White star = key spot",
        "nb_overview":  "🏘️ All Neighborhoods at a Glance",
        "planner_title":"🗓️ My Seoul Day Planner",
        "planner_sub":  "Select neighborhoods and preferences to get your custom day itinerary!",
        "plan_step1":   "① Select neighborhoods to visit (1–3)",
        "plan_step2":   "② Travel style",
        "plan_step3":   "③ Traveling with",
        "plan_step4":   "④ Start time",
        "plan_btn":     "✨  Generate My Itinerary!",
        "plan_preview": "💡 Selected neighborhoods preview",
        "plan_warn":    "Please select at least one neighborhood!",
        "plan_budget":  "📊 Estimated total budget for the day",
        "plan_map":     "#### 📍 Itinerary Map",
        "transit_label":"Transit",
        "styles":       ["🌿 Healing — Relaxed and sensory day",
                         "⚡ Active — Energetic and packed day",
                         "🍜 Food Travel — Food-focused day",
                         "🏛️ Culture — History and culture day"],
        "who":          ["Solo", "Couple", "Friends", "Family"],
        "preview_none": "Select a neighborhood on the left!",
        "generated":    "📋 Generated Itinerary",
        "footer":       "📊 Data: Google Maps · Public travel guides · Manual research | 🛠️ Built with Streamlit, Folium & Plotly | Arts and Big Data — SKKU 2026",
        "lang_toggle":  "🌐 한국어",
        # Tab2
        "find_title":   "### 🎯 Find Your Perfect Neighborhood",
        "find_sub":     "Answer a few questions and we'll match you with the best neighborhood!",
        "style_label":  "#### ① Choose your travel style",
        "cat_label":    "#### ② Preferred categories (multi-select)",
        "vibe_label":   "#### ③ Atmosphere preference",
        "vibe_slider":  "Quiet ← → Lively",
        "find_btn":     "🔍  Find My Neighborhood!",
        "style_guide_title": "#### 📖 Travel Style Guide",
        "result_title": "### 🏆 Recommended Neighborhoods",
        "rank_title":   "#### 📊 Match Score — All Neighborhoods",
        "cat_cafe":     "☕ Cafe",
        "cat_food":     "🍜 Food",
        "cat_shop":     "🛍️ Shopping",
        "cat_culture":  "🏛️ Culture",
        "match_label":  "Match",
        "guide_best":   "Best for",
        # Tab3
        "nb_select":    "Select a neighborhood to see its detailed profile:",
        "radar_title":  "Neighborhood Score Profile",
        "time_title":   "Best Time to Visit",
        "cat_comp":     "#### 🗂️ Category Composition",
        "style_match":  "#### 🎯 Travel Style Match Score",
        # Tab4
        "spots_title":  "### 📍 Key Spots",
        "area_filter":  "Filter by neighborhood:",
        "cat_filter":   "Filter by category:",
        "must_filter":  "⭐ Must-visit only",
        "spots_count":  "spots shown",
        "gmaps_btn":    "🗺️ View on Google Maps",
        # Tab5
        "data_title":   "### 📊 Neighborhood Data Overview",
        "data_sub":     "Compare all neighborhoods side by side.",
        "col_select":   "Select columns to display:",
        "dl_btn":       "📥 Download Data (CSV)",
        "compare_title":"#### 📈 Score Comparison Chart",
        # Tab6
        "sns_title":    "### 📸 SNS Popularity vs. Real Satisfaction",
        "sns_sub":      "Do neighborhoods with more Instagram mentions actually satisfy visitors more?",
        "sns_card1":    "Most Instagrammable",
        "sns_card2":    "Highest Real Rating",
        "sns_card3":    "Hidden Gem (Underrated)",
        "sns_scatter":  "#### 🔍 Instagram Mentions vs. Google Rating",
        "sns_scatter_cap": "Bubble size = review count | Top right = popular AND well-rated",
        "sns_gap":      "#### 📊 SNS Rank vs. Rating Rank — Gap Analysis",
        "sns_gap_cap":  "Positive = hidden gem | Negative = overrated on SNS",
        "sns_insight":  "#### 💡 Key Insights",
        "mentions":     "mentions",
        "quad1":        "🌟 SNS popular + high rating",
        "quad2":        "💎 Hidden gem",
        "quad3":        "📸 SNS only",
        "ins1_title":   "📸 SNS Bubble Warning",
        "ins1_body":    "Seongsu and Hongdae have the highest Instagram mentions, but their Google ratings are lower than Bukchon and Yeonnam. SNS popularity doesn't guarantee real satisfaction.",
        "ins2_title":   "💎 Find the Hidden Gems",
    },
}

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
@st.cache_data(ttl=1)
def load_data():
    nb = pd.read_csv("neighborhoods.csv")
    spots = pd.read_csv("spots.csv")
    return nb, spots

nb, spots = load_data()

# ── 색상 & 이모지 설정 ─────────────────────────────────────
def hex_to_rgba(hex_color, alpha=0.2):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

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
# 언어 토글
_lang_col, _btn_col = st.columns([6, 1])
with _btn_col:
    if st.button(T[st.session_state.lang]["lang_toggle"], use_container_width=True):
        st.session_state.lang = "EN" if st.session_state.lang == "KO" else "KO"
        st.rerun()

L = T[st.session_state.lang]

st.markdown(f"""
<div class="main-header">
    <h1 style="margin:0; font-size:32px; font-weight:700;">
        {L["title"]}
    </h1>
    <p style="margin:8px 0 0; font-size:16px; opacity:0.85;">
        {L["subtitle"].replace("**","").replace("**","")}
    </p>
</div>
""", unsafe_allow_html=True)

# ── 상단 통계 ──────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="stat-card">
        <div style="font-size:28px; font-weight:700; color:#1E3A5F;">9</div>
        <div style="font-size:13px; color:#888; margin-top:4px;">{L["stat1"]}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="stat-card">
        <div style="font-size:28px; font-weight:700; color:#2563EB;">37</div>
        <div style="font-size:13px; color:#888; margin-top:4px;">{L["stat2"]}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="stat-card">
        <div style="font-size:28px; font-weight:700; color:#F0A500;">4</div>
        <div style="font-size:13px; color:#888; margin-top:4px;">{L["stat3"]}</div>
    </div>""", unsafe_allow_html=True)
with c4:
    avg_rating = nb["google_rating"].mean()
    st.markdown(f"""<div class="stat-card">
        <div style="font-size:28px; font-weight:700; color:#52B788;">⭐ {avg_rating:.1f}</div>
        <div style="font-size:13px; color:#888; margin-top:4px;">{L["stat4"]}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:20px 0'></div>", unsafe_allow_html=True)

# ── 탭 구성 ───────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    L["tab1"], L["tab2"], L["tab3"], L["tab4"],
    L["tab5"], L["tab6"], L["tab7"],
])

# ═══════════════════════════════════════════════════════════
# TAB 1 — MAP EXPLORER
# ═══════════════════════════════════════════════════════════
with tab1:
    st.markdown("### " + L["map_title"])
    st.caption(L["map_caption"])

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

    st.markdown("<div style='background:#f0f4ff; border-radius:10px; padding:12px 16px; font-size:13px; color:#444; margin-top:8px'>" + L["map_legend"] + "</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 2 — FIND MY STYLE
# ═══════════════════════════════════════════════════════════
with tab2:
    st.markdown(L["find_title"])
    st.markdown("아래 질문에 답하면 나에게 맞는 동네를 추천해드려요!")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_q, col_r = st.columns([1.2, 1])

    with col_q:
        st.markdown(L["style_label"])
        travel_style = st.radio(
            "",
            ["Healing 힐링", "Active 액티브", "Food Travel 미식", "Culture 문화탐방"],
            format_func=lambda x: f"{STYLE_EMOJI[x]} {x}",
            horizontal=False,
            label_visibility="collapsed"
        )

        st.markdown(L["cat_label"])
        cat_cafe     = st.checkbox(L["cat_cafe"], value=True)
        cat_food     = st.checkbox(L["cat_food"], value=True)
        cat_shopping = st.checkbox(L["cat_shop"])
        cat_culture  = st.checkbox(L["cat_culture"])

        st.markdown(L["vibe_label"])
        vibe_pref = st.slider(
            L["vibe_slider"],
            min_value=1, max_value=10, value=5,
            help="1 = 매우 조용한 곳, 10 = 매우 활기찬 곳"
        )

        find_btn = st.button(L["find_btn"], use_container_width=True)

    with col_r:
        st.markdown(L["style_guide_title"])
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
        st.markdown(L["result_title"])

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
        st.markdown(L["rank_title"])
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
                    <div style='font-size:12px; color:#888'>{L["match_label"]}: {pct}%</div>
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
        L["nb_select"],
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
            fillcolor=hex_to_rgba(color, 0.2),
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
    st.markdown(L["cat_comp"])
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
    st.markdown(L["style_match"])
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
    st.markdown(L["spots_title"])

    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_area = st.selectbox(
            L["area_filter"],
            ["All"] + nb["neighborhood"].tolist(),
            format_func=lambda x: "🗺️ 전체 보기" if x == "All"
                else f"{x} ({nb[nb['neighborhood']==x]['neighborhood_kr'].values[0]})"
        )
    with col_filter2:
        selected_cat = st.selectbox(
            L["cat_filter"],
            ["All", "cafe", "landmark", "park", "museum", "market",
             "shopping", "nightlife", "kpop", "neighborhood"]
        )

    filtered = spots.copy()
    if selected_area != "All":
        filtered = filtered[filtered["neighborhood"] == selected_area]
    if selected_cat != "All":
        filtered = filtered[filtered["category"] == selected_cat]

    must_only = st.checkbox(L["must_filter"], value=False)
    if must_only:
        filtered = filtered[filtered["must_visit"] == True]

    st.markdown(f"**{len(filtered)}** " + L["spots_count"])
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
            spot_name    = str(spot["spot_name"])
            spot_name_kr = str(spot["spot_name_kr"])
            spot_desc    = str(spot["description"])[:88].replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&#39;").replace("—","&mdash;").replace("–","&ndash;")
            spot_nb      = str(spot["neighborhood"])
            spot_rating  = str(spot["google_rating"])
            is_must      = spot["must_visit"]

            with col:
                with st.container():
                    # 구글 사진 검색 URL (Places Photo API 없이 무료로 사용)
                    # Google Maps Embed 썸네일 방식
                    query = (spot_name + " " + spot_nb + " Seoul").replace(" ", "+")
                    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"
                    # Wikimedia / Unsplash fallback 이미지
                    # 스팟별 고유 Unsplash 사진 (photo ID로 각각 다른 사진)
                    spot_photos = {
                        "Hongdae Street":         "https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=600&q=80",
                        "Hongdae Free Market":    "https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?w=600&q=80",
                        "Club FF":                "https://images.unsplash.com/photo-1566417713940-fe7c737a9ef2?w=600&q=80",
                        "Cafe Bora":              "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&q=80",
                        "Gyeongui Line Forest Park": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80",
                        "Anthracite Coffee":      "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=600&q=80",
                        "Daelim Warehouse":       "https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&q=80",
                        "Cafe Onion":             "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=600&q=80",
                        "Seoul Forest":           "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?w=600&q=80",
                        "Seongsu Hangang Park":   "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=600&q=80",
                        "Bukchon Hanok Village":  "https://images.unsplash.com/photo-1548115184-bc6544d06a58?w=600&q=80",
                        "Gyeongbokgung Palace":   "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=600&q=80",
                        "National Folk Museum":   "https://images.unsplash.com/photo-1554907984-15263bfd63bd?w=600&q=80",
                        "Changdeokgung Palace":   "https://images.unsplash.com/photo-1596422846543-75c6fc197f11?w=600&q=80",
                        "Ssamziegil":             "https://images.unsplash.com/photo-1605902711622-cfb43c4437b5?w=600&q=80",
                        "Ikseon-dong Alley":      "https://images.unsplash.com/photo-1583425423900-5d7d3c2c1c54?w=600&q=80",
                        "Tapgol Park":            "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=600&q=80",
                        "Itaewon Food Street":    "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80",
                        "Leeum Samsung Museum":   "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80",
                        "Haebangchon":            "https://images.unsplash.com/photo-1514190051997-0f6f39ca5cde?w=600&q=80",
                        "COEX Mall":              "https://images.unsplash.com/photo-1519566335946-e6f65f0f4fdf?w=600&q=80",
                        "Gangnam Station":        "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=600&q=80",
                        "Apgujeong Rodeo Street": "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=600&q=80",
                        "SM Town":                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&q=80",
                        "Euljiro 3-ga Alley":     "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=600&q=80",
                        "Sewoon Plaza":           "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=600&q=80",
                        "Dongdaemun Design Plaza": "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=600&q=80",
                        "Gyeongui Line Forest Park (Yeonnam)": "https://images.unsplash.com/photo-1520962880247-cfaf541c8724?w=600&q=80",
                        "Tom N Toms Yeonnam":     "https://images.unsplash.com/photo-1481833761820-0509d3217039?w=600&q=80",
                        "Myeongdong Street":      "https://images.unsplash.com/photo-1573741718888-29fbfe7bfcf2?w=600&q=80",
                        "Myeongdong Cathedral":   "https://images.unsplash.com/photo-1548625149-fc4a29cf7092?w=600&q=80",
                        "Namdaemun Market":       "https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=600&q=80",
                        "Mangwon Market":         "https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=600&q=80",
                        "Yeonnam-dong Alley":     "https://images.unsplash.com/photo-1510133768164-a8f7e4d4e3dc?w=600&q=80",
                        "Hongje Stream":          "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80",
                        "Unhyeongung Palace":     "https://images.unsplash.com/photo-1596422846543-75c6fc197f11?w=600&q=80",
                        "Nagwon Arcade":          "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&q=80",
                    }
                    img_url = spot_photos.get(spot_name, {
                        "cafe":         "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=600&q=80",
                        "landmark":     "https://images.unsplash.com/photo-1548115184-bc6544d06a58?w=600&q=80",
                        "park":         "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?w=600&q=80",
                        "museum":       "https://images.unsplash.com/photo-1554907984-15263bfd63bd?w=600&q=80",
                        "market":       "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80",
                        "shopping":     "https://images.unsplash.com/photo-1605902711622-cfb43c4437b5?w=600&q=80",
                        "nightlife":    "https://images.unsplash.com/photo-1566417713940-fe7c737a9ef2?w=600&q=80",
                        "kpop":         "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&q=80",
                        "neighborhood": "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=600&q=80",
                    }.get(str(spot["category"]), "https://images.unsplash.com/photo-1548115184-bc6544d06a58?w=600&q=80"))

                    # 카드 상단 컬러 바
                    st.markdown(
                        f"<div style='height:4px; background:{nb_color}; "
                        f"border-radius:8px 8px 0 0; margin-bottom:0'></div>",
                        unsafe_allow_html=True
                    )

                    # 사진 + Must Visit 배지
                    badge_html = ""
                    if is_must:
                        badge_html = (
                            "<div style='position:absolute; top:8px; right:8px; "
                            "background:#FFD700; color:#333; border-radius:20px; "
                            "padding:3px 10px; font-size:11px; font-weight:700; "
                            "box-shadow:0 2px 4px rgba(0,0,0,0.2)'>⭐ Must Visit</div>"
                        )
                    st.markdown(
                        f"<div style='position:relative; overflow:hidden; "
                        f"border-radius:0; height:160px'>"
                        f"<img src='{img_url}' "
                        f"style='width:100%; height:160px; object-fit:cover; "
                        f"display:block; border-radius:0' "
                        f"onerror=\"this.src='https://images.unsplash.com/photo-1534430480872-3498386e7856?w=400&q=80'\">"
                        f"{badge_html}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    # 카드 내용
                    with st.container():
                        st.markdown(
                            f"<div style='padding:12px 4px 4px'>"
                            f"<div style='font-size:14px; font-weight:700; "
                            f"color:#1E3A5F; margin-bottom:2px'>"
                            f"{emoji} {spot_name}</div>"
                            f"<div style='color:#666; font-size:12px; "
                            f"margin-bottom:6px'>{spot_name_kr}</div>"
                            f"<div style='font-size:12px; color:#555; line-height:1.5; "
                            f"margin-bottom:8px'>{spot_desc}...</div>"
                            f"<div style='display:flex; gap:6px; flex-wrap:wrap; "
                            f"font-size:11px; color:#888'>"
                            f"<span style='background:{nb_color}22; color:{nb_color}; "
                            f"border-radius:20px; padding:2px 8px'>{spot_nb}</span>"
                            f"<span>⭐ {spot_rating}</span>"
                            f"<span>💰 {price_label}</span>"
                            f"</div></div>",
                            unsafe_allow_html=True
                        )
                        # 구글 맵 링크 버튼
                        st.markdown(
                            f"<a href='{google_maps_url}' target='_blank' "
                            f"style='display:inline-block; margin-top:6px; "
                            f"background:#f0f4ff; color:#2563EB; border-radius:8px; "
                            f"padding:5px 12px; font-size:12px; "
                            f"text-decoration:none; font-weight:500'>"
                            f"{L['gmaps_btn']}</a>",
                            unsafe_allow_html=True
                        )
                    st.markdown(
                        "<hr style='margin:8px 0; border-color:#f0f0f0'>",
                        unsafe_allow_html=True
                    )


# ═══════════════════════════════════════════════════════════
# TAB 5 — DATA TABLE
# ═══════════════════════════════════════════════════════════
with tab5:
    st.markdown(L["data_title"])
    st.markdown(L["data_sub"])

    # 표시할 컬럼 선택
    display_cols = st.multiselect(
        L["col_select"],
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

        styled = table_df.style.map(
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
        st.markdown(L["compare_title"])
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
            label=L["dl_btn"],
            data=csv_export,
            file_name="seoul_neighborhoods_data.csv",
            mime="text/csv"
        )


# ═══════════════════════════════════════════════════════════
# TAB 6 — SNS VS REALITY
# ═══════════════════════════════════════════════════════════
with tab6:
    st.markdown(L["sns_title"])
    st.markdown(L["sns_sub"])

    # ── 인트로 인사이트 카드 3개 ────────────────────────────
    nb_sorted_insta = nb.sort_values("instagram_mentions", ascending=False)
    nb_sorted_rating = nb.sort_values("google_rating", ascending=False)

    top_insta = nb_sorted_insta.iloc[0]
    top_rating = nb_sorted_rating.iloc[0]
    # 인스타 1위인데 평점이 낮은 곳 (갭이 가장 큰 곳)
    nb["insta_rank"]  = nb["instagram_mentions"].rank(ascending=False)
    nb["rating_rank"] = nb["google_rating"].rank(ascending=False)
    nb["rank_gap"]    = nb["insta_rank"] - nb["rating_rank"]
    most_overrated    = nb.loc[nb["rank_gap"].idxmin()]   # 인스타 과대평가
    most_underrated   = nb.loc[nb["rank_gap"].idxmax()]   # 숨은 보석

    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#FF6B6B,#FF8E53);
                    color:white; border-radius:14px; padding:20px; text-align:center'>
            <div style='font-size:28px; margin-bottom:6px'>📸</div>
            <div style='font-size:13px; opacity:0.85; margin-bottom:4px'>
                가장 인스타그래머블
            </div>
            <div style='font-size:22px; font-weight:700'>
                {top_insta["neighborhood_kr"]}
            </div>
            <div style='font-size:13px; opacity:0.85; margin-top:4px'>
                {int(top_insta["instagram_mentions"]):,} mentions
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ic2:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#4ECDC4,#44A08D);
                    color:white; border-radius:14px; padding:20px; text-align:center'>
            <div style='font-size:28px; margin-bottom:6px'>⭐</div>
            <div style='font-size:13px; opacity:0.85; margin-bottom:4px'>
                실제 만족도 1위
            </div>
            <div style='font-size:22px; font-weight:700'>
                {top_rating["neighborhood_kr"]}
            </div>
            <div style='font-size:13px; opacity:0.85; margin-top:4px'>
                Google {top_rating["google_rating"]} / 5.0
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ic3:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#A78BFA,#7C3AED);
                    color:white; border-radius:14px; padding:20px; text-align:center'>
            <div style='font-size:28px; margin-bottom:6px'>💎</div>
            <div style='font-size:13px; opacity:0.85; margin-bottom:4px'>
                숨은 보석 (과소평가)
            </div>
            <div style='font-size:22px; font-weight:700'>
                {most_underrated["neighborhood_kr"]}
            </div>
            <div style='font-size:13px; opacity:0.85; margin-top:4px'>
                평점 높지만 SNS는 조용
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── 메인 산점도 ──────────────────────────────────────────
    st.markdown(L["sns_scatter"])
    st.caption(L["sns_scatter_cap"])

    fig_scatter = __import__('plotly.express', fromlist=['scatter']).scatter(
        nb,
        x="instagram_mentions",
        y="google_rating",
        size="review_count",
        color="neighborhood",
        color_discrete_map={
            row["neighborhood"]: COLORS.get(row["neighborhood"], "#888")
            for _, row in nb.iterrows()
        },
        hover_name="neighborhood_kr",
        hover_data={
            "instagram_mentions": ":,",
            "google_rating": True,
            "review_count": ":,",
            "neighborhood": False,
        },
        text="neighborhood_kr",
        size_max=60,
        labels={
            "instagram_mentions": "Instagram Mentions",
            "google_rating": "Google Rating (/ 5.0)",
        },
    )

    # 평균선 추가
    avg_insta  = nb["instagram_mentions"].mean()
    avg_rating = nb["google_rating"].mean()

    fig_scatter.add_vline(
        x=avg_insta, line_dash="dot", line_color="#aaa", line_width=1.5,
        annotation_text="Avg Instagram",
        annotation_position="top right",
        annotation_font_size=11,
    )
    fig_scatter.add_hline(
        y=avg_rating, line_dash="dot", line_color="#aaa", line_width=1.5,
        annotation_text="Avg Rating",
        annotation_position="bottom right",
        annotation_font_size=11,
    )

    # 사분면 라벨
    fig_scatter.add_annotation(
        x=nb["instagram_mentions"].max() * 0.92,
        y=nb["google_rating"].max() * 0.998,
        text=L["quad1"],
        showarrow=False, font=dict(size=11, color="#16a34a"),
        bgcolor="#dcfce7", borderpad=4
    )
    fig_scatter.add_annotation(
        x=nb["instagram_mentions"].min() * 1.05 + 50000,
        y=nb["google_rating"].max() * 0.998,
        text=L["quad2"],
        showarrow=False, font=dict(size=11, color="#7c3aed"),
        bgcolor="#ede9fe", borderpad=4
    )
    fig_scatter.add_annotation(
        x=nb["instagram_mentions"].max() * 0.92,
        y=nb["google_rating"].min() * 1.002,
        text=L["quad3"],
        showarrow=False, font=dict(size=11, color="#dc2626"),
        bgcolor="#fee2e2", borderpad=4
    )

    fig_scatter.update_traces(
        textposition="top center",
        textfont=dict(size=11, color="#1E3A5F"),
        marker=dict(opacity=0.8, line=dict(width=1.5, color="white"))
    )
    fig_scatter.update_layout(
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="#fafafa",
        height=480,
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickformat=","),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", range=[3.7, 4.7]),
        margin=dict(t=30, b=40, l=40, r=40),
        font=dict(family="sans-serif"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # ── 갭 분석 바 차트 ──────────────────────────────────────
    st.markdown(L["sns_gap"])
    st.caption(L["sns_gap_cap"])

    gap_df = nb[["neighborhood_kr", "rank_gap"]].copy()
    gap_df = gap_df.sort_values("rank_gap", ascending=True)
    gap_df["color"] = gap_df["rank_gap"].apply(
        lambda x: "#7C3AED" if x > 0 else "#EF4444"
    )
    gap_df["label"] = gap_df["rank_gap"].apply(
        lambda x: f"💎 +{x:.0f}" if x > 0 else f"📸 {x:.0f}"
    )

    fig_gap = __import__('plotly.graph_objects', fromlist=['Figure', 'Bar']).Figure(
        __import__('plotly.graph_objects', fromlist=['Bar']).Bar(
            x=gap_df["rank_gap"],
            y=gap_df["neighborhood_kr"],
            orientation="h",
            marker_color=gap_df["color"].tolist(),
            text=gap_df["label"],
            textposition="outside",
            textfont=dict(size=12),
        )
    )
    fig_gap.add_vline(x=0, line_color="#333", line_width=1.5)
    fig_gap.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=340,
        xaxis=dict(
            title="Rank Gap (평점 순위 - SNS 순위)",
            showgrid=True, gridcolor="#f0f0f0", zeroline=False
        ),
        yaxis=dict(title=""),
        margin=dict(t=20, b=40, l=20, r=80),
        font=dict(family="sans-serif"),
    )
    st.plotly_chart(fig_gap, use_container_width=True)

    # ── 인사이트 요약 ────────────────────────────────────────
    st.markdown(L["sns_insight"])
    col_ins1, col_ins2 = st.columns(2)
    with col_ins1:
        st.info(
            f"{L['ins1_title']}\n\n{L['ins1_body']}"
        )
    with col_ins2:
        st.success(
            f"{L['ins2_title']}\n\n{most_underrated['neighborhood_kr']} "
            f"is quiet on SNS but has a high Google rating — a true local gem!"
        )



# ═══════════════════════════════════════════════════════════
# TAB 7 — MY SEOUL PLANNER
# ═══════════════════════════════════════════════════════════
with tab7:
    st.markdown("### " + L["planner_title"])
    st.markdown("동네와 취향을 선택하면 **AI가 나만의 하루 여행 코스**를 만들어드려요!")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    p_col1, p_col2 = st.columns([1.2, 1])

    with p_col1:
        st.markdown("#### " + L["plan_step1"])
        selected_nbs = st.multiselect(
            "",
            nb["neighborhood"].tolist(),
            default=["Seongsu", "Hongdae"],
            max_selections=3,
            format_func=lambda x: (
                f"{x}  "
                f"({nb[nb['neighborhood']==x]['neighborhood_kr'].values[0]})"
            ),
            label_visibility="collapsed"
        )

        st.markdown("#### " + L["plan_step2"])
        planner_style = st.selectbox(
            "",
            L["styles"],
            label_visibility="collapsed"
        )

        st.markdown("#### " + L["plan_step3"])
        planner_who = st.radio(
            "",
            L["who"],
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown("#### " + L["plan_step4"])
        start_time = st.select_slider(
            "",
            options=["08:00", "09:00", "10:00", "11:00", "12:00"],
            value="09:00",
            label_visibility="collapsed"
        )

        generate_btn = st.button(
            L["plan_btn"],
            use_container_width=True,
            type="primary"
        )

    with p_col2:
        st.markdown("#### " + L["plan_preview"])
        if selected_nbs:
            for nb_name in selected_nbs:
                row_prev = nb[nb["neighborhood"] == nb_name].iloc[0]
                c = COLORS.get(nb_name, "#888")
                tags = " ".join(row_prev["persona_tags"].split()[:3])
                st.markdown(
                    f"<div style='background:white; border-left:4px solid {c}; "
                    f"border-radius:8px; padding:12px 14px; margin-bottom:8px; "
                    f"box-shadow:0 1px 4px rgba(0,0,0,0.06)'>"
                    f"<b style='color:#1E3A5F'>{row_prev['neighborhood_kr']}</b> "
                    f"<span style='color:#888; font-size:12px'>{nb_name}</span><br>"
                    f"<span style='font-size:12px; color:#555'>{tags}</span><br>"
                    f"<span style='font-size:12px; color:#888'>"
                    f"⭐ {row_prev['google_rating']}  "
                    f"☕ ₩{int(row_prev['avg_coffee_price']):,}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info(L["preview_none"])

    # ── AI 코스 생성 ─────────────────────────────────────────
    if generate_btn:
        if not selected_nbs:
            st.warning(L["plan_warn"])
        else:
            # session_state 초기화 (새로 생성)
            st.session_state.itinerary_stops   = None
            st.session_state.itinerary_budget  = 0
            st.session_state.itinerary_map_nbs = list(selected_nbs)
            st.session_state.itinerary_title   = " + ".join([
                nb[nb["neighborhood"]==n]["neighborhood_kr"].values[0]
                for n in selected_nbs
            ])
            style_clean_save = planner_style.split("—")[0].strip()
            who_clean_save   = planner_who.split(" ")[0]
            st.session_state.itinerary_meta = f"{style_clean_save} · {who_clean_save} · {start_time}"

            # 선택된 동네 데이터 수집
            nb_details = []
            all_spots_for_plan = []
            for nb_name in selected_nbs:
                row_nb = nb[nb["neighborhood"] == nb_name].iloc[0]
                nb_spots = spots[spots["neighborhood"] == nb_name]
                must_spots = nb_spots[nb_spots["must_visit"] == True]["spot_name"].tolist()
                nb_details.append({
                    "name": nb_name,
                    "kr": row_nb["neighborhood_kr"],
                    "vibe": row_nb["vibe_score"],
                    "food": row_nb["food_score"],
                    "culture": row_nb["culture_score"],
                    "tags": row_nb["persona_tags"],
                    "desc": row_nb["description_en"],
                    "must_spots": must_spots,
                    "avg_coffee": int(row_nb["avg_coffee_price"]),
                    "subway": row_nb["subway_lines"],
                })
                for _, s in nb_spots.iterrows():
                    all_spots_for_plan.append(
                        f"{s['spot_name']} ({s['spot_name_kr']}, {s['category']})"
                    )

            # 프롬프트 구성
            nb_info_str = "\n".join([
                f"- {d['kr']} ({d['name']}): {d['desc'][:80]} "
                f"| Must-visit: {', '.join(d['must_spots'][:3])} "
                f"| Subway: {d['subway']} "
                f"| Avg coffee: ₩{d['avg_coffee']:,}"
                for d in nb_details
            ])
            spots_str = ", ".join(all_spots_for_plan[:15])
            style_clean = planner_style.split("—")[0].strip()
            who_clean = planner_who.split(" ")[0]

            prompt = f"""You are a Seoul travel expert. Create a detailed one-day itinerary in Korean.

Travel details:
- Neighborhoods: {", ".join([d["kr"] + "(" + d["name"] + ")" for d in nb_details])}
- Style: {style_clean}
- Traveling with: {who_clean}
- Start time: {start_time}

Neighborhood info:
{nb_info_str}

Available spots to include: {spots_str}

Create a time-based itinerary with exactly this format for each stop:
⏰ [TIME] | 📍 [PLACE NAME (Korean + English)] | [CATEGORY EMOJI]
💬 [1-2 sentences about what to do/see here and why it suits the travel style]
💰 예상 비용: [amount in KRW]
---

Rules:
- Include 6-9 stops total across all neighborhoods
- Group stops by neighborhood to minimize travel time
- Add subway directions between neighborhoods
- End with a dinner recommendation
- Add a brief intro paragraph at the top (2-3 sentences in Korean)
- Add a "📊 하루 예상 총 비용" summary at the end
- Write warmly and personally, like a local friend giving advice
- ALL text must be in Korean except place names"""

            # ── 규칙 기반 코스 자동 생성 ──────────────────
            import time as _time

            # 시간 계산 헬퍼
            def next_time(current, minutes):
                h, m = map(int, current.split(":"))
                total = h * 60 + m + minutes
                return f"{total // 60:02d}:{total % 60:02d}"

            # 스타일별 시간 배분 (분)
            style_durations = {
                "🌿 Healing": {"cafe": 60, "park": 50, "landmark": 40, "museum": 50,
                               "market": 35, "shopping": 40, "nightlife": 30,
                               "kpop": 30, "neighborhood": 45},
                "⚡ Active":  {"cafe": 30, "park": 30, "landmark": 30, "museum": 40,
                               "market": 30, "shopping": 50, "nightlife": 60,
                               "kpop": 45, "neighborhood": 30},
                "🍜 Food Travel": {"cafe": 50, "park": 25, "landmark": 30, "museum": 35,
                                   "market": 60, "shopping": 35, "nightlife": 50,
                                   "kpop": 25, "neighborhood": 35},
                "🏛️ Culture": {"cafe": 40, "park": 35, "landmark": 60, "museum": 70,
                               "market": 40, "shopping": 30, "nightlife": 30,
                               "kpop": 30, "neighborhood": 50},
            }
            style_key = next((k for k in style_durations if k in planner_style), "⚡ Active")
            durations = style_durations[style_key]

            # 스타일별 코멘트 템플릿
            style_comments = {
                "cafe": {
                    "🌿 Healing": "여유롭게 커피 한 잔 즐기며 하루를 시작해요. 감성 인테리어를 구경하는 것도 놓치지 마세요!",
                    "⚡ Active": "빠르게 에너지 충전! 테이크아웃으로 시작해 바로 다음 장소로 이동해요.",
                    "🍜 Food Travel": "이 동네의 시그니처 카페에서 특색 있는 음료를 꼭 맛봐요.",
                    "🏛️ Culture": "역사적인 골목 사이 숨어있는 카페에서 잠깐 쉬어가요.",
                },
                "landmark": {
                    "🌿 Healing": "천천히 걸으며 사진을 찍고, 분위기를 온몸으로 느껴보세요.",
                    "⚡ Active": "핵심 포인트만 빠르게 둘러보고 다음 스팟으로 출발!",
                    "🍜 Food Travel": "관광 후 근처 로컬 식당을 찾아보는 것도 좋아요.",
                    "🏛️ Culture": "안내판을 꼼꼼히 읽으며 역사적 배경을 깊이 이해해봐요.",
                },
                "park": {
                    "🌿 Healing": "벤치에 앉아 아무것도 안 해도 좋아요. 진정한 힐링 타임!",
                    "⚡ Active": "조깅이나 자전거 대여로 에너지를 발산해봐요.",
                    "🍜 Food Travel": "피크닉 도시락을 사 와서 공원에서 먹어요.",
                    "🏛️ Culture": "공원의 역사적 의미와 주변 문화 공간을 함께 탐방해요.",
                },
                "museum": {
                    "🌿 Healing": "천천히 작품 하나하나를 감상하며 내면을 들여다봐요.",
                    "⚡ Active": "하이라이트 작품 위주로 빠르게 관람해요.",
                    "🍜 Food Travel": "뮤지엄 카페나 레스토랑에서 식사도 즐겨봐요.",
                    "🏛️ Culture": "오디오 가이드나 도슨트 투어를 적극 활용해요.",
                },
                "market": {
                    "🌿 Healing": "시장 구경하며 소소한 행복을 찾아요. 현지인들의 일상 속으로!",
                    "⚡ Active": "길거리 음식을 빠르게 먹으며 에너지 보충!",
                    "🍜 Food Travel": "이 코스의 하이라이트! 다양한 음식을 조금씩 맛봐요.",
                    "🏛️ Culture": "오래된 상인들과 이야기 나누며 서울의 역사를 느껴봐요.",
                },
                "shopping": {
                    "🌿 Healing": "마음에 드는 독립 브랜드 제품을 찾아 소소한 쇼핑을 즐겨요.",
                    "⚡ Active": "원하는 것 리스트업 후 효율적으로 쇼핑 완료!",
                    "🍜 Food Travel": "쇼핑몰 푸드코트에서 다양한 음식도 즐겨봐요.",
                    "🏛️ Culture": "전통 공예품이나 독립 아티스트 작품을 찾아봐요.",
                },
                "nightlife": {
                    "🌿 Healing": "조용한 바에서 음악을 들으며 하루를 마무리해요.",
                    "⚡ Active": "신나는 클럽이나 라이브 공연으로 하루를 화끈하게 마무리!",
                    "🍜 Food Travel": "야식 문화를 제대로 경험해봐요.",
                    "🏛️ Culture": "재즈바나 인디 음악 공연장에서 서울의 밤을 느껴봐요.",
                },
                "kpop": {
                    "🌿 Healing": "좋아하는 아티스트의 흔적을 조용히 찾아봐요.",
                    "⚡ Active": "K-pop 댄스 체험이나 팬샵 투어를 즐겨요!",
                    "🍜 Food Travel": "아이돌이 자주 가는 식당을 찾아봐요.",
                    "🏛️ Culture": "한국 대중음악의 역사와 산업을 탐구해봐요.",
                },
                "neighborhood": {
                    "🌿 Healing": "골목길을 따라 발길 닿는 대로 천천히 걸어요.",
                    "⚡ Active": "동네 전체를 빠르게 둘러보며 포토존을 찾아요.",
                    "🍜 Food Travel": "동네 숨은 맛집을 찾는 재미를 느껴봐요.",
                    "🏛️ Culture": "동네의 역사와 변천사를 생각하며 골목을 탐방해요.",
                },
            }

            # 영어 코멘트
            style_comments_en = {
                "cafe": {
                    "🌿 Healing": "Start your day slowly with a great coffee. Take time to admire the aesthetic interior!",
                    "⚡ Active": "Quick energy boost! Grab a takeout and head to the next spot.",
                    "🍜 Food Travel": "Try this neighborhood's signature drink — a must-taste!",
                    "🏛️ Culture": "Rest for a moment at a cafe hidden in a historic alley.",
                },
                "landmark": {
                    "🌿 Healing": "Walk slowly, take photos, and soak in the atmosphere.",
                    "⚡ Active": "Hit the key highlights fast and move on!",
                    "🍜 Food Travel": "After sightseeing, look for a nearby local restaurant.",
                    "🏛️ Culture": "Read the info boards carefully and deepen your understanding of the history.",
                },
                "park": {
                    "🌿 Healing": "Just sit on a bench and do nothing. True healing time!",
                    "⚡ Active": "Go for a jog or rent a bike to burn some energy.",
                    "🍜 Food Travel": "Grab a picnic lunch and eat in the park.",
                    "🏛️ Culture": "Explore the park's historical significance and nearby cultural spaces.",
                },
                "museum": {
                    "🌿 Healing": "Take your time admiring each piece and reflect quietly.",
                    "⚡ Active": "Focus on the highlights and move through quickly.",
                    "🍜 Food Travel": "Don't miss the museum cafe or restaurant for a meal.",
                    "🏛️ Culture": "Make the most of the audio guide or docent tour.",
                },
                "market": {
                    "🌿 Healing": "Find small joys browsing the market. Step into locals' daily life!",
                    "⚡ Active": "Grab some street food fast and recharge!",
                    "🍜 Food Travel": "The highlight of this itinerary! Taste a little of everything.",
                    "🏛️ Culture": "Chat with long-time vendors and feel the history of Seoul.",
                },
                "shopping": {
                    "🌿 Healing": "Find something from an indie brand you love — enjoy light, mindful shopping.",
                    "⚡ Active": "Make a list in advance and shop efficiently!",
                    "🍜 Food Travel": "Don't miss the food court in the mall.",
                    "🏛️ Culture": "Look for traditional crafts or works by independent artists.",
                },
                "nightlife": {
                    "🌿 Healing": "Wind down at a quiet bar listening to music.",
                    "⚡ Active": "End the day with a bang at a club or live show!",
                    "🍜 Food Travel": "Experience Seoul's late-night food culture properly.",
                    "🏛️ Culture": "Feel the Seoul night at a jazz bar or indie music venue.",
                },
                "kpop": {
                    "🌿 Healing": "Quietly trace the footsteps of your favorite artist.",
                    "⚡ Active": "Enjoy a K-pop dance experience or fan shop tour!",
                    "🍜 Food Travel": "Seek out restaurants frequented by your favorite idols.",
                    "🏛️ Culture": "Explore the history and industry of Korean pop music.",
                },
                "neighborhood": {
                    "🌿 Healing": "Follow the alleys wherever your feet take you — no rush.",
                    "⚡ Active": "Quickly explore the whole neighborhood and find the best photo spots.",
                    "🍜 Food Travel": "Enjoy the hunt for hidden local gems in this neighborhood.",
                    "🏛️ Culture": "Walk the alleys while reflecting on the neighborhood's history and transformation.",
                },
            }

            # 이동 시간 (동네 간)
            travel_tips = {
                ("Seongsu", "Hongdae"):   ("2호선 성수 → 홍대입구", 25),
                ("Hongdae", "Seongsu"):   ("2호선 홍대입구 → 성수", 25),
                ("Seongsu", "Gangnam"):   ("2호선 성수 → 강남", 20),
                ("Gangnam", "Seongsu"):   ("2호선 강남 → 성수", 20),
                ("Hongdae", "Itaewon"):   ("6호선 이태원역 도보 이동", 20),
                ("Itaewon", "Hongdae"):   ("6호선 → 2호선 환승", 20),
                ("Bukchon", "Insadong"):  ("도보 10분 거리", 12),
                ("Insadong", "Bukchon"):  ("도보 10분 거리", 12),
                ("Gangnam", "Itaewon"):   ("지하철 2호선 → 6호선 환승", 18),
                ("Itaewon", "Gangnam"):   ("6호선 → 2호선 환승", 18),
                ("Yeonnam", "Hongdae"):   ("경의선 숲길 도보 15분", 15),
                ("Hongdae", "Yeonnam"):   ("경의선 숲길 도보 15분", 15),
                ("Euljiro", "Insadong"):  ("도보 15분 또는 지하철 1정거장", 15),
                ("Insadong", "Euljiro"):  ("도보 15분 또는 지하철 1정거장", 15),
                ("Myeongdong", "Insadong"): ("도보 15분", 15),
                ("Insadong", "Myeongdong"): ("도보 15분", 15),
            }

            # 예산 계산
            budget_base = {
                "🌿 Healing": {"cafe": 12000, "park": 0, "landmark": 5000,
                               "museum": 8000, "market": 15000, "shopping": 30000,
                               "nightlife": 20000, "kpop": 15000, "neighborhood": 0},
                "⚡ Active":  {"cafe": 7000, "park": 0, "landmark": 5000,
                               "museum": 8000, "market": 20000, "shopping": 50000,
                               "nightlife": 35000, "kpop": 20000, "neighborhood": 0},
                "🍜 Food Travel": {"cafe": 10000, "park": 5000, "landmark": 3000,
                                   "museum": 8000, "market": 25000, "shopping": 20000,
                                   "nightlife": 30000, "kpop": 10000, "neighborhood": 0},
                "🏛️ Culture": {"cafe": 8000, "park": 0, "landmark": 8000,
                               "museum": 12000, "market": 12000, "shopping": 15000,
                               "nightlife": 15000, "kpop": 10000, "neighborhood": 0},
            }
            budgets = budget_base.get(style_key, budget_base["⚡ Active"])

            # 코스 빌드
            current_time = start_time
            stops = []
            total_budget = 0

            for nb_idx, nb_name in enumerate(selected_nbs):
                # 동네 이동 안내
                if nb_idx > 0:
                    prev = selected_nbs[nb_idx - 1]
                    tip_key = (prev, nb_name)
                    tip_text, tip_min = travel_tips.get(
                        tip_key, ("지하철 또는 버스 이용", 20)
                    )
                    current_time = next_time(current_time, tip_min)
                    stops.append({
                        "type": "transit",
                        "time": current_time,
                        "text": tip_text,
                        "nb": nb_name,
                    })

                nb_row = nb[nb["neighborhood"] == nb_name].iloc[0]
                nb_spots_list = spots[spots["neighborhood"] == nb_name].copy()
                # must-visit 우선, 최대 3개
                must = nb_spots_list[nb_spots_list["must_visit"] == True].head(3)
                if len(must) < 2:
                    must = nb_spots_list.head(3)

                for _, sp in must.iterrows():
                    cat = str(sp["category"])
                    dur = durations.get(cat, 40)
                    bud = budgets.get(cat, 0)
                    comment = style_comments.get(cat, {}).get(style_key, "이 장소를 충분히 즐겨봐요!")
                    comment_en = style_comments_en.get(cat, {}).get(style_key, "Enjoy this spot!")
                    stops.append({
                        "type": "spot",
                        "time": current_time,
                        "name": sp["spot_name"],
                        "name_kr": sp["spot_name_kr"],
                        "cat": cat,
                        "nb": nb_name,
                        "nb_kr": nb_row["neighborhood_kr"],
                        "comment": comment,
                        "comment_en": comment_en,
                        "budget": bud,
                        "duration": dur,
                        "is_must": sp["must_visit"],
                    })
                    total_budget += bud
                    current_time = next_time(current_time, dur)

            # session_state에 저장
            st.session_state.itinerary_stops  = stops
            st.session_state.itinerary_budget = total_budget


    # ── 결과 표시 (session_state 기반 — 버튼 후에도 유지) ──
    if st.session_state.itinerary_stops:
        stops = st.session_state.itinerary_stops
        total_budget = st.session_state.itinerary_budget
        selected_nbs_display = st.session_state.itinerary_map_nbs
        nb_names_kr = st.session_state.itinerary_title
        st.markdown("---")

        # ── 결과 헤더 ──
        day_label = "하루 코스" if st.session_state.lang == "KO" else "Day Course"
        st.markdown(
            f"<div style='background:linear-gradient(135deg,#1E3A5F,#2563EB); "
            f"color:white; border-radius:16px; padding:20px 24px; margin-bottom:20px'>"
            f"<div style='font-size:13px; opacity:0.8'>{L['generated']}</div>"
            f"<div style='font-size:22px; font-weight:700; margin:4px 0'>"
            f"🗓️ {nb_names_kr} {day_label}</div>"
            f"<div style='font-size:13px; opacity:0.85'>"
            f"{st.session_state.itinerary_meta}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

        # ── 타임라인 ──
        CAT_EMOJI_PLAN = {
            "cafe": "☕", "landmark": "🏛️", "park": "🌿",
            "museum": "🖼️", "market": "🛒", "shopping": "🛍️",
            "nightlife": "🌙", "kpop": "🎵", "neighborhood": "📍",
        }
        free_label = "Free" if st.session_state.lang == "EN" else "무료"

        for stop in stops:
            if stop["type"] == "transit":
                c = COLORS.get(stop["nb"], "#888")
                st.markdown(
                    f"<div style='display:flex; align-items:center; gap:12px; "
                    f"padding:10px 16px; margin:6px 0; background:#f8f9fa; "
                    f"border-radius:10px; border-left:3px dashed {c}'>"
                    f"<span style='font-size:18px'>🚇</span>"
                    f"<div>"
                    f"<span style='font-size:12px; color:#888'>{stop['time']} {L['transit_label']}</span><br>"
                    f"<span style='font-size:13px; color:#555; font-weight:500'>"
                    f"{stop['text']}</span>"
                    f"</div></div>",
                    unsafe_allow_html=True
                )
            else:
                c = COLORS.get(stop["nb"], "#2563EB")
                emoji = CAT_EMOJI_PLAN.get(stop["cat"], "📍")
                bud_text = f"₩{stop['budget']:,}" if stop["budget"] > 0 else free_label
                # 언어에 따라 코멘트 선택
                raw_comment = stop.get("comment", "")
                if st.session_state.lang == "EN":
                    comment = stop.get("comment_en", raw_comment)
                else:
                    comment = raw_comment
                must_badge = (
                    "<span style='background:#FFD700; color:#333; border-radius:20px; "
                    "padding:1px 8px; font-size:11px; margin-left:6px'>⭐ Must</span>"
                    if stop["is_must"] else ""
                )
                st.markdown(
                    f"<div style='background:white; border-radius:12px; "
                    f"padding:16px 18px; margin:6px 0; "
                    f"box-shadow:0 2px 6px rgba(0,0,0,0.06); "
                    f"border-left:4px solid {c}'>"
                    f"<div style='display:flex; justify-content:space-between; "
                    f"align-items:center; margin-bottom:6px'>"
                    f"<span style='font-size:13px; color:{c}; font-weight:700'>"
                    f"⏰ {stop['time']}</span>"
                    f"<span style='font-size:11px; color:#888; "
                    f"background:#f0f4ff; padding:2px 8px; border-radius:20px'>"
                    f"💰 {bud_text}</span>"
                    f"</div>"
                    f"<div style='font-size:15px; font-weight:700; color:#1E3A5F'>"
                    f"{emoji} {stop['name']}{must_badge}</div>"
                    f"<div style='font-size:12px; color:#888; margin:2px 0 6px'>"
                    f"{stop['name_kr']} · {stop['nb_kr']}</div>"
                    f"<div style='font-size:13px; color:#555; line-height:1.6'>"
                    f"{comment}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        # ── 총 예산 ──
        st.markdown(
            f"<div style='background:#f0f9f0; border:1px solid #86efac; "
            f"border-radius:12px; padding:16px 20px; margin-top:16px; "
            f"display:flex; justify-content:space-between; align-items:center'>"
            f"<span style='font-size:15px; font-weight:700; color:#166534'>"
            f"{L['plan_budget']}</span>"
            f"<span style='font-size:22px; font-weight:700; color:#166534'>"
            f"₩{total_budget:,}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        # ── 코스 지도 ──
        st.markdown(L["plan_map"])
        import folium
        from streamlit_folium import st_folium as _st_folium
        m_plan = folium.Map(
            location=[37.5665, 126.9780],
            zoom_start=13,
            tiles="CartoDB positron"
        )
        for i, nb_name in enumerate(selected_nbs_display):
            row_m = nb[nb["neighborhood"] == nb_name].iloc[0]
            c = COLORS.get(nb_name, "#888")
            folium.Marker(
                location=[row_m["lat"], row_m["lng"]],
                icon=folium.DivIcon(
                    html=(f"<div style='background:{c}; color:white; "
                          f"border-radius:50%; width:32px; height:32px; "
                          f"display:flex; align-items:center; justify-content:center; "
                          f"font-weight:700; font-size:14px; "
                          f"box-shadow:0 2px 6px rgba(0,0,0,0.3)'>{i+1}</div>"),
                    icon_size=(32, 32), icon_anchor=(16, 16)
                ),
                tooltip=f"{i+1}. {row_m['neighborhood_kr']}"
            ).add_to(m_plan)
            for _, sp in spots[
                (spots["neighborhood"] == nb_name) &
                (spots["must_visit"] == True)
            ].iterrows():
                folium.CircleMarker(
                    location=[sp["lat"], sp["lng"]],
                    radius=7, color=c, fill=True,
                    fill_color=c, fill_opacity=0.7,
                    tooltip=sp["spot_name"]
                ).add_to(m_plan)
        _st_folium(m_plan, width=None, height=400, use_container_width=True)


# ── 푸터 ──────────────────────────────────────────────────
st.markdown(f"<div style='background:white; border-radius:12px; padding:16px 24px; margin-top:32px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.06)'><p style='margin:0; color:#888; font-size:13px'>{L['footer']}</p></div>", unsafe_allow_html=True)
