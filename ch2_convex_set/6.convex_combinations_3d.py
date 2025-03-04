"""
《最优化方法》
第二章：凸集
授课教师：柳文章
代码演示：凸组合，三维空间下的
代码语言：Python
主要工具包：matplotlib.pyplot
代码地址：https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import argparse
import matplotlib.pyplot as plt
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser("Convex Optimization.")
    parser.add_argument("--N", type=int, default=1000)  # 随机生成的点集个数
    parser.add_argument("--N-base", type=int, default=5)  # 基点个数
    return parser.parse_args()


if __name__ == '__main__':
    parser = parse_args()
    num_points = parser.N
    num_base_points = parser.N_base
    plt.rcParams['font.family'] = 'Heiti TC'  # 设置中文字体
    # 基本点集
    x = np.array([1.0, 1.0, 1.0, 3.0, 3.0, 3.0])
    y = np.array([1.0, 3.0, 1.0, 1.0, 3.0, 3.0])
    z = np.array([1.0, 1.0, 3.0, 1.0, 3.0, 1.0])
    labels = [r'$x_1$', r'$x_2$', r'$x_3$', r'$x_4$', r'$x_5$', r'$x_6$']

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x[:num_base_points], y[:num_base_points], z[:num_base_points], c='red', s=20)
    for i in range(num_base_points):
        ax.text(x[i], y[i], z[i], labels[i])

    # sample convex combinations
    alpha_sets = [1 for _ in range(num_base_points)]
    samples = np.random.dirichlet(alpha=alpha_sets, size=num_points)  # 利用Dirichlet采样出满足要求的theta参数

    base_points = np.stack([x[:num_base_points], y[:num_base_points], z[:num_base_points]], axis=-1)
    for i in range(num_points):
        new_point = (samples[i].reshape(-1, 1) * base_points).sum(axis=0)
        ax.scatter(*new_point, c='blue', s=5, zorder=2)  # 绘制新点

    # 设置坐标轴显示范围
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_zlim(0, 4)
    # 设置坐标轴刻度
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_zticks([0, 1, 2, 3, 4])
    plt.show()
