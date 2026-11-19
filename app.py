
import streamlit as st
import pandas as pd
from html import escape

st.set_page_config(
    page_title="SteamPick | Find Your Next Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_games():
    url = (
        "https://raw.githubusercontent.com/meghanthota/"
        "MIST-4600-SteamPick/main/steam_games.csv"
    )
    return pd.read_csv(url)


games = load_games()


# -----------------------------
# ORIGINAL ANALYSIS FUNCTIONS
# -----------------------------

def most_popular(games):
    return games.sort_values(
        "peak_ccu", ascending=False
    )[["name", "peak_ccu"]].head(5)


def longest_playtime(games):
    return games.sort_values(
        "avg_playtime_hours", ascending=False
    )[["name", "avg_playtime_hours"]].head(5)


def highest_rated(games):
    reviewed = games[games["num_reviews_total"] >= 1000]
    return reviewed.sort_values(
        "pct_pos_total", ascending=False
    )[["name", "pct_pos_total", "num_reviews_total"]].head(5)


# -----------------------------
# ORIGINAL RECOMMENDATION CLASS
# -----------------------------

class SteamPick:
    def __init__(self, games):
        self.games = games.copy()

    def recommend(self):
        ranked = self.games.copy()

        ranked["popularity_rank"] = ranked["peak_ccu"].rank(
            ascending=False, pct=True
        )
        ranked["playtime_rank"] = ranked["avg_playtime_hours"].rank(
            ascending=False, pct=True
        )
        ranked["rating_rank"] = ranked["pct_pos_total"].rank(
            ascending=False, pct=True
        )

        ranked["score"] = (
            ranked["popularity_rank"]
            + ranked["playtime_rank"]
            + ranked["rating_rank"]
        )

        return ranked.sort_values("score").head(5)[
            [
                "appid",
                "name",
                "peak_ccu",
                "avg_playtime_hours",
                "pct_pos_total"
            ]
        ]


# -----------------------------
# CUSTOM DESIGN
# -----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 75% 5%, #26154C 0%, transparent 40%),
        radial-gradient(ellipse at 10% 35%, #10234A 0%, transparent 40%),
        #090B16;
    color: #F5F5FF;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

h1, h2, h3, p {
    color: #F5F5FF;
}

h1 {
    font-size: clamp(2.5rem, 5vw, 4.5rem) !important;
    font-weight: 800 !important;
    letter-spacing: -2px;
}

h2 {
    font-weight: 700 !important;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(170,140,255,0.18);
    padding: 20px;
    border-radius: 18px;
}

[data-testid="stMetricValue"] {
    color: #C4A8FF;
}

.stButton > button {
    background: linear-gradient(110deg, #8858FF, #5B74FF);
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 0.85rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    transition: all 0.25s ease;
    box-shadow: 0 8px 30px rgba(113,75,255,0.25);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(113,75,255,0.45);
}

.hero {
    padding: 55px 35px;
    border-radius: 24px;
    background:
        linear-gradient(90deg, rgba(10,12,28,0.96), rgba(10,12,28,0.35)),
        url("https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1600");
    background-size: cover;
    background-position: center;
    border: 1px solid rgba(180,150,255,0.2);
    margin-bottom: 25px;
}

.eyebrow {
    color: #BCA2FF !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-size: clamp(35px, 5vw, 65px);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -2px;
    color: white;
    margin: 12px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #CBA9FF, #7DAAFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    color: #C7C7DD !important;
    font-size: 17px;
    max-width: 540px;
    line-height: 1.6;
}

.game-card {
    background: linear-gradient(145deg, #1D2038, #131626);
    border: 1px solid #373453;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 14px;
    transition: transform 0.2s;
}

.game-card:hover {
    transform: translateY(-4px);
    border-color: #A783FF;
}

.game-image {
    width: 100%;
    aspect-ratio: 460 / 215;
    object-fit: cover;
    border-radius: 11px;
    margin-bottom: 12px;
}

.game-title {
    font-size: 19px;
    font-weight: 700;
    color: white;
    margin: 8px 0;
}

.game-stats {
    color: #B8B6CF;
    font-size: 13px;
    line-height: 1.9;
}

.rank-label {
    color: #C4A8FF;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}

.section-subtitle {
    color: #B5B4CC !important;
    margin-bottom: 22px;
}

[data-testid="stTabs"] button {
    font-weight: 600;
}

hr {
    border-color: #34334A;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<p class="eyebrow">🎮 STEAMPICK / GAME DISCOVERY</p>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR NEXT STREAM STARTS HERE</div>
    <div class="hero-title">
        Stop scrolling.<br>
        <span class="gradient-text">Start playing.</span>
    </div>
    <p class="hero-description">
        Discover Steam games worth streaming.
        Powered by real player data, not just hype.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# QUICK STATS
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("GAMES ANALYZED", f"{len(games):,}")

with col2:
    st.metric("RANKING FACTORS", "3")

with col3:
    st.metric("TOP PICKS", "5")

st.write("")
st.write("")


# -----------------------------
# RECOMMENDATIONS
# -----------------------------

st.markdown(
    '<p class="eyebrow">THE MAIN EVENT</p>',
    unsafe_allow_html=True
)

st.header("Find Your Next Game")

st.markdown(
    '<p class="section-subtitle">'
    'One click. Five data-powered recommendations.'
    '</p>',
    unsafe_allow_html=True
)

if st.button("🚀 FIND MY GAMES", type="primary",
             use_container_width=True):

    st.balloons()

    picker = SteamPick(games)
    recommendations = picker.recommend()

    st.subheader("Your Top 5 Picks")

    # Show game cards in two columns
    left, right = st.columns(2)

    for rank, (_, game) in enumerate(
        recommendations.iterrows(), start=1
    ):
        game_name = escape(str(game["name"]))

        # Official Steam image using the game ID
        image_url = (
            f"https://shared.fastly.steamstatic.com/store_item_assets/"
            f"steam/apps/{int(game['appid'])}/header.jpg"
        )

        card = f"""
        <div class="game-card">
            <img class="game-image" src="{image_url}">
            <div class="rank-label">PICK #{rank:02d}</div>
            <div class="game-title">{game_name}</div>
            <div class="game-stats">
                👥 {game['peak_ccu']:,.0f} peak players<br>
                ⏱️ {game['avg_playtime_hours']:.1f} average hours<br>
                ⭐ {game['pct_pos_total']:.0f}% positive reviews
            </div>
        </div>
        """

        with (left if rank % 2 else right):
            st.markdown(card, unsafe_allow_html=True)

    st.caption(
        "Ranked using historical Steam popularity, "
        "playtime, and player ratings. "
        "Not a prediction of live streaming performance."
    )


# -----------------------------
# EXPLORE SECTION
# -----------------------------

st.divider()

st.markdown(
    '<p class="eyebrow">GO DEEPER</p>',
    unsafe_allow_html=True
)

st.header("Explore the Leaderboards")

st.markdown(
    '<p class="section-subtitle">'
    'See which games lead in each category.'
    '</p>',
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs([
    "🔥 Most Popular",
    "⏱️ Longest Playtime",
    "⭐ Highest Rated"
])

with tab1:
    st.subheader("The Crowd Favorites")
    st.dataframe(
        most_popular(games),
        hide_index=True,
        use_container_width=True
    )

with tab2:
    st.subheader("Games That Keep Players Hooked")
    st.dataframe(
        longest_playtime(games),
        hide_index=True,
        use_container_width=True
    )

with tab3:
    st.subheader("The Fan Favorites")
    st.dataframe(
        highest_rated(games),
        hide_index=True,
        use_container_width=True
    )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.markdown(
    '<p style="text-align:center;color:#8989A8;font-size:13px;">'
    'STEAMPICK © 2026 | MIST 4600 | '
    'Built with Python, pandas & Streamlit<br>'
    'Steam dataset collected March 2025'
    '</p>',
    unsafe_allow_html=True
)
