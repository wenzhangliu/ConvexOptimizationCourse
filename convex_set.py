"""
《最优化方法》
第二章：凸集
授课教师：柳文章
代码演示：凸组合、凸包
代码语言：Python
主要工具包：matplotlib
代码地址：
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

x = np.ndarray([1, 2])  # 横坐标集合
y = np.ndarray([2, 1])  # 纵坐标集合

num_dots = 100  # 采样次数
plt.scatter(x, y, color='red', s=100)

# for i in range(num_dots):
#     a = np.random.random()
#     b = 1 - a
#     x = a * x_1 + b * x_2
#     plt.plot(x)


plt.xlim([0, 4])
plt.ylim([0, 4])
plt.xlabel("$x^{(1)}$")
plt.ylabel("$x^{(2)}$")
plt.title('单个点示例')
plt.show()
