import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(data, key, region='Philipines', figsize=(5, 3)):
    plt.figure(figsize=figsize)
    annotate_props = {"fontsize": 12,
                      "color": "red",
                      "xycoords": "axes fraction"}
    
    if region == 'Philippines':
        data_ = data
        plt.title(f'{key} Distribution in the Philippines')
    else:
        data_ = data[data['Region'] == region]
        plt.title(f'{key} Distribution in ' + region)
        
    bins = int(np.sqrt(len(data_)))
    plt.hist(data_[key], bins=bins,edgecolor='black', alpha=0.7)
    
    # count, mean, std, min_val, q1, q2, q3, max_val = data_[key].describe()
    
    mean = data_[key].mean()
    median = data_[key].median()
    mode = data_[key].mode()
    
    plt.annotate(f'Mean = {"{0:.2f}".format(mean)}', xy=(0.75, 0.75), **annotate_props)
    plt.annotate(f'Median = {"{0:.2f}".format(median)}', xy=(0.75, 0.70), **annotate_props)
    plt.annotate(f'Mode = {"{0:.2f}".format(mode[0])}', xy=(0.75, 0.65), **annotate_props)
    plt.xlabel(key)
    plt.ylabel('Frequency')
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.show()