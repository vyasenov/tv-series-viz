# load libraries
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os

# apply LOWESS smoothing to ratings within a season
def lowess_smooth(group, frac=0.8, it=3):
    x = group['episode']
    y = group['rating']
    group['rating_lowess'] = sm.nonparametric.lowess(y, x, frac=frac, return_sorted=False ,it=it)
    group['season'] = group.name  # add back the grouping key
    return group

# grab list of shows
def get_available_shows():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('_ratings.csv')]
    return sorted([f.replace('_ratings.csv', '') for f in csv_files])

# generate normalized episode number for each season on the 0-1 scale
def normalize_episode(group):
    n = len(group)
    if n == 1:  # edge case: season with only 1 episode
        return pd.Series([1.0], index=group.index)
    return pd.Series(1 + (group['episode'] - 1) / (n - 1), index=group.index)

def plot_ratings(tvshow):
    print(f"Processing {tvshow}...")
    
    # load data
    data = pd.read_csv(f'data/{tvshow}_ratings.csv')

    # generate normalized episode number for each season on the 0-1 scale
    #data['episode_norm'] = data.groupby('season').apply(normalize_episode).reset_index(level=0, drop=True) + data['season'] - 1
    data['episode_norm'] = data.groupby('season')['episode'].transform(lambda x: 1 + (x - 1) / (len(x) - 1) if len(x) > 1 else 1.0) + data['season'] - 1
    # apply LOWESS smoothing to ratings within a season
    data = data.groupby('season', group_keys=False).apply(lowess_smooth, include_groups=False)

    # save season endpoints (for vertical lines)
    season_endpoints = list(range(2, data['season'].max() + 1))
    print(season_endpoints)

    # show data
    print(data.head(n=20))

    # Create single figure for continuous timeline plotting
    plt.figure(figsize=(12, 6))

    # Plot each season as a separate line segment with only LOWESS smoothed data
    for season in sorted(data['season'].unique()):
        season_data = data[data['season'] == season]

        # Plot smoothed line for this season
        plt.plot(season_data['episode_norm'], season_data['rating_lowess'], 
                linewidth=3, color='darkblue', alpha=0.9)

    # Add vertical lines at season boundaries (excluding the last one)
    for boundary in season_endpoints:
        plt.axvline(x=boundary, color='red', linestyle='--', alpha=0.7, linewidth=1)

    plt.title(f'{tvshow.replace("_", " ").title()} Ratings')
    plt.xlabel('Season')
    plt.ylabel('IMDB Rating')

    # Set x-axis labels to show integers only at midpoints
    max_season = data['season'].max()
    x_ticks = [i + 0.5 for i in range(1, max_season + 1)]
    x_labels = [str(i) for i in range(1, max_season + 1)]
    plt.xticks(x_ticks, x_labels)

    #plt.grid(True, alpha=0.3)
    plt.savefig(f'graphs/time_series/{tvshow}_time_series.png')
    plt.show()
    print(f"Saved {tvshow} time series")
    print("\n"*3)

# get list of shows
list_of_shows = get_available_shows() #[1:2]
print(list_of_shows)

# loop through each show
for show in list_of_shows:
    plot_ratings(show)

