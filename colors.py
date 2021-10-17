import os
import sys
from PIL import Image
import pandas as pd
import numpy as np


def top_n_colors(image, color_array, color_name_array,n):
    '''
        image: jpg image
        color_array: np.array of the colors we want to shift to
        color_name_array: np.array containing names corresponding to the color_array
        n: number of dominant colors we want to find
        function calculates the distance from each of the image's pixels
        to each discrete color we want to include in our analysis
        then takes the closest color to each pixel and returns the top
        n of those closest colors
    '''
    # Open image with PIL's Image class .open() method
    # convert to np.array using getdata() method which
    # returns r,g,b for each pixel
    image_array = np.array(list(Image.open(image).getdata()))
    size = image_array.shape[0]

    # loop through colors and build distance array which is a
    # stack of each pixels distance to each color
    for i in range(len(color_array)):
        if i == 0:
            distance_array = ((image_array - color_array[i]) ** 2).sum(axis=1)
        else:
            distance_array = np.vstack((distance_array, ((image_array - color_array[i]) ** 2).sum(axis=1)))

    # indexes of min distance for each pixel where the index
    # corresponds to the color with that min distance
    mindexes = np.argmin(distance_array, axis=0)

    # index into the color_names_array with the mindexes
    # then grab the top n unique colors and counts
    unique_counts = list(np.unique(color_name_array[mindexes], return_counts=True))

    # unfortunate that is not sorted so we converted to list of np.arrays
    # and loop through taking the next highest frequency color and deleting
    colors = []
    for _ in range(n):
        # if image has less colors than we asked for
        if len(unique_counts[0]) == 0:
            break

        max_idx = np.argmax(unique_counts[1])
        # if next most frequent color makes up less than 10%
        if unique_counts[1][max_idx] / size < 0.1:
            break

        colors.append(unique_counts[0][max_idx])
        unique_counts[0] = np.delete(unique_counts[0], max_idx)
        unique_counts[1] = np.delete(unique_counts[1], max_idx)

    # if we broke the loop early
    if len(colors) < n:
        # add None's to fill the void
        colors += [None for _ in range(n-len(colors))]

    return colors

benchmarks = pd.read_csv('benchmark_colors.csv')  # benchmark color file with rgb values
color_array = benchmarks[['r', 'g', 'b']].to_numpy()  # convert to np array for speed
color_name_array = benchmarks['name'].to_numpy()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        n = 3
    else:
        n = int(sys.argv[1])
    cols = ['filename'] + [f'color_rank{i+1}' for i in range(n)]
    df = pd.DataFrame(columns=cols)
    for file in os.listdir('./images/'):
        tnc = top_n_colors('./images/' + f'{file}', color_array, color_name_array,n)
        df = df.append(pd.DataFrame([[file] + tnc], columns=cols))
    df.to_csv('results.csv', index=False)

