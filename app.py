
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SteamPick | Game Discovery",
    page_icon="🎮",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #10121D;
    color: #F5F5FA;
}
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #F5F5FA !important;
}
.stButton > button {
    background-color: #7546DB;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 1.5rem;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #9066F0;
    color: white;
}
.game-card {
    background-color: #202337;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 12px;
    border: 1px solid #34364A;
}
.game-name {
    font-size: 21px;
    font-weight: 650;
    color: #FFFFFF;
}
.game-info {
    color: #B8B8C8;
    margin-top: 8px;
}
.small-label {
    color: #BBA9FF;
    font-weight: 600;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# Load data
@st.cache_data
def load_games():
    url = "https://raw.githubusercontent.com/meghanthota/MIST-4600-SteamPick/main/steam_games.csv"
    return pd.read_csv(url)


games = load_games()


# Original analysis functions
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


# Original recommendation class
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
            ["name", "peak_ccu", "avg_playtime_hours", "pct_pos_total"]
        ]


# Header
st.markdown(
    '<p class="small-label">🎮 STEAMPICK | GAME DISCOVERY</p>',
    unsafe_allow_html=True
)

st.title("Find Your Next Game to Stream.")

st.write(
    "Stop guessing what to play next. SteamPick analyzes "
    "popularity, average playtime, and player ratings "
    "to recommend games worth exploring."
)

st.divider()

# Quick statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Games Analyzed", f"{len(games):,}")

with col2:
    st.metric("Ranking Factors", "3")

with col3:
    st.metric("Top Recommendations", "5")

st.divider()

# Main recommendation section
st.header("Your Next Game Starts Here")
st.write(
    "Get five recommendations based on a combination "
    "of popularity, playtime, and positive player reviews."
)

if st.button("🎯 Discover My Top Games", type="primary"):
    picker = SteamPick(games)
    recommendations = picker.recommend()

    st.subheader("Your Top 5 Picks")

    for rank, (_, game) in enumerate(
        recommendations.iterrows(), start=1
    ):
        st.markdown(
            f"""
            <div class="game-card">
                <div class="small-label">PICK #{rank}</div>
                <div class="game-name">{game['name']}</div>
                <div class="game-info">
                    👥 Peak players: {game['peak_ccu']:,.0f}
                    &nbsp; | &nbsp;
                    ⏱️ Avg. playtime: {game['avg_playtime_hours']:.1f} hrs
                    &nbsp; | &nbsp;
                    ⭐ Positive reviews: {game['pct_pos_total']:.0f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Recommendations are based on historical Steam data, "
        "not live Twitch or YouTube viewership."
    )

st.divider()

# Explore section
st.header("Explore the Data")

st.write(
    "Want to see what makes a game stand out? "
    "Explore the top games in each category."
)

tab1, tab2, tab3 = st.tabs([
    "🔥 Most Popular",
    "⏱️ Longest Playtime",
    "⭐ Highest Rated"
])

with tab1:
    st.subheader("Most Popular Games")
    st.write("Top five games by peak concurrent players.")
    st.dataframe(
        most_popular(games),
        hide_index=True,
        use_container_width=True
    )

with tab2:
    st.subheader("Longest Average Playtime")
    st.write("Top five games by average hours played.")
    st.dataframe(
        longest_playtime(games),
        hide_index=True,
        use_container_width=True
    )

with tab3:
    st.subheader("Highest Rated Games")
    st.write("Top five games with at least 1,000 reviews.")
    st.dataframe(
        highest_rated(games),
        hide_index=True,
        use_container_width=True
    )

st.divider()

st.caption(
    "SteamPick | MIST 4600 Python Project | "
    "Steam data collected March 2025"
)
