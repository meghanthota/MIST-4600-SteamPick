
# StreamPick: Game Recommendation Tool

A Python tool that helps Twitch and YouTube streamers choose which Steam games to play next.

## Problem

StreamPick helps Twitch and YouTube streamers decide which Steam games to play next by comparing game popularity, average playtime, and player ratings.

With so many games available, streamers need a way to narrow down their choices using data rather than relying on popularity alone.

## What it does

StreamPick analyzes 1,000 Steam games using pandas and answers three questions:

| # | Sub-question | How the app answers it |
|---|---|---|
| 1 | Which games have the highest peak concurrent players? | Sorts games by peak concurrent player count to find the five most popular games. |
| 2 | Which games have the longest average playtime? | Sorts games by average hours played per player to find games with strong staying power. |
| 3 | Which games have the highest positive review percentages, and how do ratings relate to popularity? | Finds the five highest-rated games with at least 1,000 reviews and uses SciPy to measure the relationship between ratings and popularity. |

The `StreamPick` class combines all three factors into a ranking system. Each game receives a rank for popularity, playtime, and ratings. These ranks are added together, and the five games with the lowest combined scores are recommended.

The goal is to help streamers consider multiple factors when deciding what to play.

## How to run it

1. Open `SteamPick.ipynb` from this repository in Google Colab.
2. Make sure you have an internet connection. The notebook automatically loads `steam_games.csv` from this GitHub repository.
3. Select **Runtime → Run all**.
4. Review the results for each question and the final recommendations.

The notebook uses Python, pandas, and SciPy. No API key is required.

## Example output

The following results were generated using the Steam dataset of 1,000 games.

### Question 1: Which games are the most popular?

Top five games by peak concurrent players:

| Game | Peak concurrent players |
|---|---:|
| Counter-Strike 2 | 1,212,356 |
| Monster Hunter Wilds | 703,236 |
| PUBG: BATTLEGROUNDS | 616,738 |
| Dota 2 | 555,977 |
| Split Fiction | 201,694 |

**Finding:** Counter-Strike 2 had the highest peak concurrent player count in the dataset, with more than 1.2 million players.

This suggests that games with large player bases may offer streamers access to established gaming communities.

### Question 2: Which games have the longest average playtime?

Top five games by average hours played:

| Game | Average playtime (hours) |
|---|---:|
| FINAL FANTASY XIV Online | 837.6 |
| Dota 2 | 717.2 |
| Counter-Strike 2 | 553.2 |
| Killing Floor 2 | 546.2 |
| Rust | 353.2 |

**Finding:** FINAL FANTASY XIV Online had the highest average playtime, at 837.6 hours.

Games with longer average playtime may provide opportunities for recurring streams or longer-term content.

### Question 3: Which games have the highest positive review percentages?

Top five games by positive reviews, requiring at least 1,000 reviews:

| Game | Positive reviews | Total reviews |
|---|---:|---:|
| HoloCure - Save the Fans! | 99% | 37,057 |
| Cats Hidden in Paris | 98% | 17,041 |
| VPet-Simulator | 98% | 45,250 |
| Split Fiction | 98% | 17,370 |
| OneShot | 98% | 46,183 |

**Finding:** HoloCure - Save the Fans! had the highest positive review percentage at 99%.

Requiring at least 1,000 reviews helps avoid ranking games highly based on only a few reviews.

### Additional Analysis: SciPy

I used SciPy's Spearman correlation to examine whether games with higher positive review percentages also tend to have higher peak concurrent player counts.

**Correlation: 0.02**

This shows almost no monotonic relationship between popularity and positive player ratings in this dataset.

For streamers, this suggests that a popular game is not necessarily highly rated. Both factors are worth considering when choosing what to play.

### Final StreamPick Recommendations

After combining popularity, average playtime, and player ratings, StreamPick recommends:

| Rank | Recommended game |
|---|---|
| 1 | Stardew Valley |
| 2 | Factorio |
| 3 | The Binding of Isaac: Rebirth |
| 4 | Slay the Spire |
| 5 | Baldur's Gate 3 |

**Recommendation:** Stardew Valley is the top overall recommendation because it received the best combined ranking across the three factors.

The other four games are strong alternatives based on the same ranking system.

These results are based on Steam data rather than actual Twitch or YouTube viewership, so they do not guarantee streaming success.

## Data

The project uses `steam_games.csv`, a dataset containing 1,000 Steam games selected from the Steam Games Dataset on Kaggle.

The dataset includes information such as game titles, peak concurrent players, average playtime, positive reviews, prices, and genres.

The class dataset was collected in March 2025, so the analysis reflects historical Steam activity rather than live player counts.

## Built with

- **Python:** Main programming language
- **pandas:** Sorting, filtering, and analyzing Steam games
- **SciPy:** Calculating the correlation between popularity and ratings
- **Google Colab:** Writing and running the notebook
- **GitHub:** Storing the project code, dataset, and documentation

## AI Use Disclosure
