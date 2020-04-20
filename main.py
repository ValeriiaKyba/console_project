from collections import Counter

import os
import rasterio
import numpy as np
import scipy.stats as stats

from db import create_photo, create_frequencies


class Calculator:
    def __init__(self, im_array):
        self._im_array = im_array

    @property
    def weighted_average(self):
        return np.average(self._im_array)

    @property
    def mean_square(self):
        return np.mean(self._im_array)

    @property
    def root_mean_square(self):
        return np.std(self._im_array)

    @property
    def confidence_interval(self):
        alpha = 0.05
        array_mean = np.nanmean(self._im_array)
        sd = np.sqrt(np.nansum(np.power(self._im_array - array_mean, 2))
                     / self._im_array.size - 1)
        interval = stats.t.ppf(1.0 - (alpha / 2.0), self._im_array.size - 1) * \
                   (sd / np.sqrt(self._im_array.size))
        return array_mean - interval, array_mean + interval

    @property
    def cloudiness(self):
        boolean_mask = np.logical_or(self._im_array == 254,
                                     self._im_array == 255)
        return np.count_nonzero(boolean_mask) / self._im_array.size


def main():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '254 NDVI')
    f_list = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory)
              for f in filenames if os.path.splitext(f)[1] == '.PNG']
    for i in f_list:

        with rasterio.open(os.path.join(directory, i)) as f:
            im_array = f.read()
            im_array = im_array.ravel()

            counter = Counter(im_array)
            calc = Calculator(im_array)
            f_id = create_photo(i, calc)
            create_frequencies(f_id, counter)




if __name__ == '__main__':
    main()
    print('done')
