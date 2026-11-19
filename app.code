import streamlit as st
import pandas as pd
from scipy.stats import spearmanr

# Web App
st.title("SteamPick")
st.write("Find your next game to stream using Steam data!")

# Data Set
@st.cache_data
def load_games():
    url = "https://raw.githubusercontent.com/meghanthota/MIST-4600-SteamPick/main/steam_games.csv"
    return pd.read_csv(url)

games = load_games()

st.write("Explore 1,000 Steam games based on popularity, playtime, and ratings.")

# Question 1
def most_popular(games):
    popular = games.sort_values("peak_ccu", ascending=False)
    return popular[["name", "peak_ccu"]].head(5)

# Question 2
def longest_playtime(games):
    playtime = games.sort_values("avg_playtime_hours", ascending=False)
    return playtime[["name", "avg_playtime_hours"]].head(5)

# Question 3
def highest_rated(games):
    reviewed = games[games["num_reviews_total"] >= 1000]
    rated = reviewed.sort_values("pct_pos_total", ascending=False)
    return rated[["name", "pct_pos_total", "num_reviews_total"]].head(5)

# Class Reccomendations
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

# User Selection
st.subheader("Explore the Data")

choice = st.selectbox(
    "What would you like to see?",
    [
        "Most Popular Games",
        "Longest Average Playtime",
        "Highest Rated Games"
    ]
)

if choice == "Most Popular Games":
    st.dataframe(most_popular(games), hide_index=True)

elif choice == "Longest Average Playtime":
    st.dataframe(longest_playtime(games), hide_index=True)

else:
    st.dataframe(highest_rated(games), hide_index=True)

# Final recommendation
st.subheader("Get Game Recommendations")

if st.button("Recommend Games"):
    picker = SteamPick(games)
    recommendations = picker.recommend()
    st.success("Here are your top 5 recommended games!")
    st.dataframe(recommendations, hide_index=True)

# SciPy analysis
st.subheader("Popularity vs. Ratings")

comparison = games[["peak_ccu", "pct_pos_total"]].dropna()
correlation, p_value = spearmanr(
    comparison["peak_ccu"],
    comparison["pct_pos_total"]
)

st.write("Correlation:", round(correlation, 2))
st.write(
    "Popularity and positive player ratings have a weak "
    "relationship in this dataset."
)
