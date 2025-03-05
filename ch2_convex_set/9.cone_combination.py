"""
《最优化方法》
第二章: 凸集
授课教师: 柳文章
代码演示: 锥组合
代码语言: Python
主要工具包: matplotlib.pyplot
代码地址: https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import argparse
import matplotlib.pyplot as plt
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser("Convex Optimization.")
    parser.add_argument("--step", type=float, default=0.10)  # 步长
    return parser.parse_args()


if __name__ == '__main__':
    parser = parse_args()
    step = parser.step
    plt.rcParams['font.family'] = 'Heiti TC'  # 设置中文字体

    x_1 = np.array([1.0, 3.0])  # 点x_1的坐标（二维）
    x_2 = np.array([3.0, 3.0])  # 点x_2的坐标（二维）
    x_3 = np.array([2.0, 1.0])  # 点x_3的坐标（二维）

    plt.title('锥组合')
    plt.xlim([0, 4.0])
    plt.ylim([0, 5.0])
    plt.grid()
    plt.plot([x_1[0], x_2[0]], [x_1[1], x_2[1]], color='gray', linewidth=2)
    plt.plot([x_2[0], x_3[0]], [x_2[1], x_3[1]], color='gray', linewidth=2)
    plt.plot([x_3[0], x_1[0]], [x_3[1], x_1[1]], color='gray', linewidth=2)
    plt.scatter(*x_1, color='red', s=100, zorder=2, label="x_1")  # 绘制点x_1
    plt.scatter(*x_2, color='red', s=100, zorder=2, label="x_2")  # 绘制点x_2
    plt.scatter(*x_3, color='red', s=100, zorder=2, label="x_3")  # 绘制点x_3
    plt.text(x_1[0] - 0.2, x_1[1] - 0.3, r'$x_1$', fontsize=12)
    plt.text(x_2[0], x_2[1] - 0.3, r'$x_2$', fontsize=12)
    plt.text(x_3[0], x_3[1] - 0.3, r'$x_3$', fontsize=12)

    theta_1_set = np.arange(0.0, 2.0, step=step)
    theta_2_set = np.arange(0.0, 2.0, step=step)
    theta_3_set = np.arange(0.0, 2.0, step=step)

    for theta_1 in theta_1_set:
        for theta_2 in theta_2_set:
            for theta_3 in theta_3_set:
                new_point = theta_1 * x_1 + theta_2 * x_2 + theta_3 * x_3
                plt.scatter(*new_point, color='blue', s=5, zorder=2)  # 绘制新点

    plt.show()
