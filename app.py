import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ── 페이지 설정 ─────────────────────────────
st.set_page_config(
    page_title="Seoul Travel Style Dashboard",
    page_icon="🗺️",
    layout="wide"
)

# ── 데이터 불러오기 ─────────────────────────
@st.cache_data
def load_data():
    nb = pd.read_csv("neighborhoods.csv")
    spots = pd.read_csv("spots.csv")
    return nb, spots

nb, spots = load_data()

# ── 헤더 ────────────────────────────────────
st.title("🗺️ Seoul Neighborhood Travel Style Dashboard")
st.markdown("**Discover Your Personal Seoul** — Find the neighborhood that matches your travel style")
st.divider()

# ── 지도 ────────────────────────────────────
st.subheader("📍 Explore Seoul's Neighborhoods")
st.caption("👆 Click on any marker to see neighborhood details")

style_colors = {
    "Hongdae":    "#FF6B6B",
    "Seongsu":    "#4ECDC4",
    "Bukchon":    "#45B7D1",
    "Insadong":   "#96CEB4",
    "Itaewon":    "#FFEAA7",
    "Gangnam":    "#DDA0DD",
    "Euljiro":    "#F0A500",
    "Yeonnam":    "#A8E6CF",
    "Myeongdong": "#FFB6C1",
}

m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="CartoDB positron"
)

for _, row in nb.iterrows():
    color = style_colors.get(row["neighborhood"], "#888888")

    popup_html = f"""
    <div style='font-family:sans-serif; width:210px; padding:5px'>
        <h4 style='margin:0 0 5px 0; color:#1E3A5F'>
            {row['neighborhood_kr']} ({row['neighborhood']})
        </h4>
        <hr style='margin:4px 0'>
        ⭐ <b>Rating:</b> {row['google_rating']} / 5.0<br>
        📸 <b>Instagram:</b> {int(row['instagram_mentions']):,}<br>
        🎯 <b>Vibe:</b> {row['vibe_score']} / 10<br>
        🍽️ <b>Food:</b> {row['food_score']} / 10<br>
        🚇 <b>Subway:</b> {row['subway_lines']}<br>
        ☕ <b>Avg Coffee:</b> ₩{int(row['avg_coffee_price']):,}<br>
        <hr style='margin:6px 0'>
        <small style='color:#666'>{row['description_en'][:90]}...</small>
    </div>
    """

    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=16,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.75,
        popup=folium.Popup(popup_html, max_width=230),
        tooltip=f"📍 {row['neighborhood_kr']} — click for details"
    ).add_to(m)

    folium.Marker(
        location=[row["lat"] + 0.003, row["lng"]],
        icon=folium.DivIcon(
            html=f"<div style='font-size:10px; font-weight:bold; color:#1E3A5F; white-space:nowrap'>{row['neighborhood_kr']}</div>",
            icon_size=(80, 20),
            icon_anchor=(40, 0)
        )
    ).add_to(m)

st_folium(m, width=1100, height=520)

# ── 동네 카드 ───────────────────────────────
st.divider()
st.subheader("🏘️ All Neighborhoods at a Glance")

cols = st.columns(3)
for i, (_, row) in enumerate(nb.iterrows()):
    with cols[i % 3]:
        color = style_colors.get(row["neighborhood"], "#888")
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {color}22, {color}11);
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 12px;
        '>
            <b style='font-size:16px'>{row['neighborhood_kr']}</b>
            <span style='color:#666; font-size:13px'> {row['neighborhood']}</span><br>
            ⭐ {row['google_rating']} &nbsp;|&nbsp;
            📸 {int(row['instagram_mentions'])//10000}만<br>
            <small style='color:#555'>{", ".join(row["persona_tags"].split()[:3])}</small>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption("📊 Data: Google Maps · Public travel guides · Manual research | Built with Streamlit & Folium")
