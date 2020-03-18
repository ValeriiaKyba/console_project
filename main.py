from collections import Counter

import os
import rasterio

from db import create_photo, create_frequencies


class Calculator:
    def __init__(self, counter):
        self._counter = counter
        self._filtered_counter = {key: val
                                  for key, val in counter.items()
                                  if key not in (0, 254, 255)}

    @property
    def weighted_average(self):
        a = sum([key*val for key, val in self._filtered_counter.items()])
        b = sum([val for _, val in self._filtered_counter.items()])
        if not b:
            return 0
        return a / b

    @property
    def mean_square(self):
        w_avg = self.weighted_average
        a = sum([val*(key - w_avg)**2 for key, val in self._filtered_counter.items()])
        b = sum([val for _, val in self._filtered_counter.items()])
        if not b:
            return 0
        return a / b

    @property
    def root_mean_square(self):
        return self.mean_square**0.5

    @property
    def min_confidence_interval(self):
        root_mean = self.root_mean_square
        w_avg = self.weighted_average
        b = (sum([val for _, val in self._filtered_counter.items()]))**0.5
        if not b:
            return 0
        return w_avg - 1.96 * (root_mean / b)

    @property
    def max_confidence_interval(self):
        root_mean = self.root_mean_square
        w_avg = self.weighted_average
        b = (sum([val for _, val in self._filtered_counter.items()])) ** 0.5
        if not b:
            return 0
        return w_avg + 1.96 * (root_mean / b)

    @property
    def cloudiness(self):
        a = self._counter.get(254, 0) + self._counter.get(255, 0)
        b = sum([val for key, val in self._counter.items() if key])
        if not b:
            return 0
        return a / b


def main():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '254 NDVI')
    f_list = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory, i)) and i.endswith('.PNG')]
    for i in f_list:

        with rasterio.open(os.path.join(directory, i)) as f:
            sample = []
            im_array = f.read()
            for row in im_array:
                for j in row:
                    for o in j:
                        if not isinstance(o, int):
                            sample.append(int(o))

            counter = Counter(sample)
            calc = Calculator(counter)
            f_id = create_photo(i, calc)
            create_frequencies(f_id, counter)


if __name__ == '__main__':
    main()
    print('done')
