import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# grab list of shows
def get_available_shows():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('_ratings.csv')]
    return sorted([f.replace('_ratings.csv', '') for f in csv_files])

list_of_shows = get_available_shows()
list_of_shows = list_of_shows[:1]
print(list_of_shows)

# process each show
for show in list_of_shows:
    print(f"Processing {show}...")
    data = pd.read_csv(f'data/{show}_ratings.csv')

    # pivot data
    data = data.pivot(index='season', columns='episode', values='rating')
    print(data.head())

    # generate heatmap
    plt.figure(figsize=(10, 10))
    sns.heatmap(data, annot=True, cmap='coolwarm', cbar=False, square=True)
    plt.title(f'{show.strip("_").replace("_", " ").title()} Ratings Heatmap')
    plt.savefig(f'graphs/heatmaps/{show}_heatmap.png')
    plt.show()
    print(f"Saved {show} heatmap")
    print("\n"*3)