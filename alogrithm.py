import random
import string
import numpy as np
import pandas as pd
import time
from matplotlib import pyplot as plt

def LCS(i, j, str_a, str_b):
    if i == 0 or j == 0:
        if str_a[i] == str_b[j]:
            # print(str_b[i], end="")
            return 1, str_a[i]
        else:
            return 0, ""
    elif str_a[i] == str_b[j]:
        lenth, s = LCS(i - 1, j - 1, str_a, str_b)
        # print(str_b[i], end="")
        return lenth+1, s+str_a[i]
    else:
        lenth1, s1 = LCS(i - 1, j, str_a, str_b)
        lenth2, s2 = LCS(i, j - 1, str_a, str_b)
        if lenth1>lenth2:
            return lenth1, s1
        else:
            return lenth2, s2


def dynamic(str_a, str_b):
    m = len(str_a)
    n = len(str_b)
    map_str = np.zeros((m + 1, n + 1))
    map_count = np.zeros((m + 1, n + 1))
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str_a[i - 1] == str_b[j - 1]:
                map_count[i][j] = map_count[i - 1][j - 1] + 1
                map_str[i][j] = 0
            elif map_count[i - 1][j] > map_count[i][j - 1]:
                map_count[i][j] = map_count[i - 1][j]
                map_str[i][j] = 1
            else:
                map_count[i][j] = map_count[i][j - 1]
                map_str[i][j] = -1
    # print(map_str)
    i = m
    j = n
    result = ""
    while i * j:
        if map_str[i][j] == -1:
            j -= 1
        elif map_str[i][j] == 1:
            i -= 1
        else:
            j -= 1
            i -= 1
            result = str_b[j] + result
    print(result)


if __name__ == "__main__":
    random.seed(10)
    result = []
    for i in range(50):
        str_a = "".join(random.sample(string.ascii_letters, random.randint(1, 15)))
        str_b = "".join(random.sample(string.ascii_letters, random.randint(1, 15)))
        print(str_a)
        print(str_b)
        m = len(str_a)
        n = len(str_b)
        start = time.clock()
        lenth, s = LCS(m - 1, n - 1, str_a, str_b)
        print(s)
        mid = time.clock()
        dynamic(str_a, str_b)
        end = time.clock()
        print(mid - start)
        print(end - mid)
        result.append([str_a, str_b, s, mid - start, end - mid, min(m, n), -1])
    columns = ['str_a', 'str_a', 'result', 'recursion_time', 'dynamic_time', 'len(str_a)', 'len(str_b)']
    df = pd.DataFrame(data=result, columns=columns)
    # df.to_csv("./result.csv")
    x = np.arange(0, 50)
    plt.plot(x, df.loc[:, 'recursion_time'], color='red', label='recursion_time')
    plt.plot(x, df.loc[:, 'dynamic_time'], color='green', label='dynamic_time')
    plt.plot(x, df.loc[:, 'len(str_a)'], color='blue', label='len(str_a)')
    plt.plot(x, df.loc[:, 'len(str_b)'], color='y', label='len(str_b)')
    plt.legend()  # 显示图例
    plt.xlabel('x label')
    plt.ylabel('time cost')
    plt.show()


