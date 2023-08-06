# import timeit
# from pricetree import PriceTree, OldPriceTree
# import pandas as pd
# import matplotlib.pyplot as plt
# import random

# new_times = []
# old_times = []
# trials = 500
# max_branch = 1000

# for i in range(1, max_branch):
#     print(i)
#     def test_fn():
#         OldPriceTree(40, 1, 0.1, i, 0.26)
#     old_times.append(timeit.timeit(lambda: test_fn(), number = trials))

# for i in range(1, max_branch):
#     print(i)
#     def test_fn():
#         PriceTree(40, 1, 0.1, i, 0.26)
#     new_times.append(timeit.timeit(lambda: test_fn(), number = trials))

# data = pd.DataFrame([new_times, old_times]).transpose()
# data.plot()
# print(data)

# data.to_csv('speedtest_output.csv')

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('speedtest_output.csv')
plt.plot(data.iloc[:, 1:])

plt.show()