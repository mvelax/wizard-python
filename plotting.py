import numpy as np
import matplotlib.pyplot as plt

def moving_average(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.apply_along_axis(lambda m: np.convolve(m, window, 'valid'),
                               axis=0, arr=interval)


def plot_moving_average_scores(scores, window_size=25):
    moving_avg = moving_average(scores, window_size)
    plt.plot(moving_avg)
    plt.show()
