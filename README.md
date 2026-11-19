
# StreamPick: Game Recommendation Tool

Python tool that recommends Steam games for Twitch and YouTube streamers.

## Problem

StreamPick helps Twitch and YouTube streamers decide which Steam games to play next based on popularity, average playtime, and player ratings.

## What it does

The app uses a dataset of 1,000 Steam games to answer three questions:

1. Which games have the highest peak concurrent players?
2. Which games have the longest average playtime?
3. Which games have the highest percentage of positive reviews, and how do ratings relate to popularity?

Each question is answered using pandas and a separate Python function.

For Question 3, SciPy is used to calculate the correlation between game popularity and positive player ratings.

The StreamPick class combines popularity, playtime, and ratings into a ranking system to recommend five games with strong streaming potential.

## How to run it

1. Open `SteamPick.ipynb` in Google Colab.
2. The notebook automatically loads `steam_games.csv` from this GitHub repository.
3. Select Runtime → Run all.
4. View the analysis and final game recommendations.

The project uses Python, pandas, and SciPy. No API key is required.

## Example output

### Top 5 Recommended Games

1. Stardew Valley
2. Factorio
3. The Binding of Isaac: Rebirth
4. Slay the Spire
5. Baldur's Gate 3

### SciPy Analysis

Correlation between popularity and positive player ratings: **0.02**

This shows almost no relationship between game popularity and positive review percentages in the dataset.

For streamers, this means a popular game is not necessarily highly rated. StreamPick considers popularity, playtime, and ratings separately when making recommendations.

## AI Use Disclosure

I have reviewed the code and am working to understand each part so I can explain it independently.
