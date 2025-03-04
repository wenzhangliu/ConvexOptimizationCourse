"""
《最优化方法》
第二章：凸集
授课教师：柳文章
代码演示：凸包，三维空间下的
代码语言：Python
主要工具包：matplotlib.pyplot
代码地址：https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import argparse
import matplotlib.pyplot as plt
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser("Convex Optimization.")
    parser.add_argument("--step", type=float, default=0.3)  # 采样步长
    parser.add_argument("--N-base", type=int, default=4)  # 基点个数
    return parser.parse_args()


if __name__ == '__main__':
    parser = parse_args()
    step = parser.step
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

    theta_1_set = np.arange(0.0, 1.2, step=step)
    theta_2_set = np.arange(0.0, 1.2, step=step)
    theta_3_set = np.arange(0.0, 1.2, step=step)
    theta_4_set = np.arange(0.0, 1.2, step=step)
    base_points = np.stack([x[:num_base_points], y[:num_base_points], z[:num_base_points]], axis=-1)
    for theta_1 in theta_1_set:
        for theta_2 in theta_2_set:
            for theta_3 in theta_3_set:
                for theta_4 in theta_4_set:
                    theta = np.array([theta_1, theta_2, theta_3, theta_4]).reshape(-1, 1)
                    new_point = (theta * base_points).sum(0)
                    ax.scatter(*new_point, c='blue', s=20)

    # 设置坐标轴显示范围
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_zlim(0, 4)
    # 设置坐标轴刻度
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_zticks([0, 1, 2, 3, 4])
    plt.show()
