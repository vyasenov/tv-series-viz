import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

shows = ["slow_horses", "succession", "white_lotus", "peaky_blinders", "true_detective", 
         "narcos", "the_undoing", "adolescence", "1883", "1923", 
         "big_little_lies", "chernobyl", "dark", "severance", "the_mandalorian",
         "westworld", "ozark", "yellowstone", "queens_gambit"]

def plot_heatmap(show):
    # Load the data
    data = pd.read_csv(f'{show}_ratings.csv')

    # Print the first few rows of the data
    print(data.head())

    # Pivot the data to create a proper heatmap structure
    # Episodes as rows, seasons as columns, ratings as values
    heatmap_data = data.pivot(index='episode', columns='season', values='rating')

    print("\nPivoted data for heatmap:")
    print(heatmap_data)

    plt.figure(figsize=(6, 6))
    sns.set(font_scale=1.0)

    # Create the heatmap with proper data structure
    heatmap = sns.heatmap(
        heatmap_data,
        cmap='viridis',
        annot=True,           # Show the rating value in each cell
        fmt=".1f",           # Format to 1 decimal place
        linewidths=0.5,
        square=True,         # Make cells square
        cbar=False           # Remove the colorbar legend
    )

    # Customize ticks & labels
    heatmap.set_xlabel('Season', fontsize=12)
    heatmap.set_ylabel('Episode', fontsize=12)
    heatmap.set_title(f'{show.replace("_", " ").title()} Ratings Heatmap', fontsize=14, fontweight='bold')

    # Rotate x-axis labels for better readability
    heatmap.set_xticklabels(heatmap.get_xmajorticklabels(), rotation=0)
    heatmap.set_yticklabels(heatmap.get_ymajorticklabels(), rotation=0)

    plt.tight_layout()

    # Save the visualization
    plt.savefig(f'{show.title()}_ratings_heatmap.png', dpi=300, bbox_inches='tight')

    plt.show()
    
for show in shows:  
    plot_heatmap(show)