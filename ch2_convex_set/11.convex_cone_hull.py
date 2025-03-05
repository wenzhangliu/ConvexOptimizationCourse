"""
《最优化方法》
第二章: 凸集
授课教师: 柳文章
代码演示: 凸锥包（二维）
代码语言: Python
主要工具包: matplotlib.pyplot
代码地址: https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import Button
from scipy.spatial import ConvexHull
plt.rcParams['font.family'] = 'Heiti TC'  # 设置中文字体

# 初始化若干个点
points = np.array([[1.0, 4.0],
                   [3.0, 3.0],
                   [2.0, 1.0],
                   [0.5, 1.5]])  # 点集
x = np.array([2.0, 2.0])
all_points = np.concatenate([points, x.reshape(1, -1)], axis=0)
theta = np.tanh(all_points[:, 1] / all_points[:, 0])  # 计算角度
max_index = np.argmax(theta)
min_index = np.argmin(theta)

# 创建画布
fig, ax = plt.subplots()
ax.set_xlim(0, 8)
ax.set_ylim(0, 8)
ax.set_title("二维空间下的凸锥包演示案例")
plt.grid()
plt.scatter(points[:, 0], points[:, 1], c='r', label="初始点集")
plt.text(points[0, 0]-0.2, points[0, 1]-0.3, r'$x_1$', fontsize=12)
plt.text(points[1, 0], points[1, 1]-0.3, r'$x_2$', fontsize=12)
plt.text(points[2, 0], points[2, 1]-0.3, r'$x_3$', fontsize=12)
plt.text(points[3, 0], points[3, 1]-0.3, r'$x_4$', fontsize=12)

# 并绘制三角形平面
t_max = 5  # 控制射线长度
origin = np.array([0, 0])
end_1 = t_max * all_points[max_index]
end_2 = t_max * all_points[min_index]
polygon_surface = ax.triangle = Polygon([origin, end_1, end_2], closed=True, edgecolor='b', facecolor='lightblue', alpha=0.6)
ax.add_patch(polygon_surface)

# 绘制可拖动的点
x_move, = ax.plot(x[0], x[1], 'ro', markersize=6, label="可拖动点")

# **拖动顶点的类**
class DraggablePoint:
    def __init__(self, point_plot, polygon_surface):
        self.point_plot = point_plot
        self.polygon_surface = polygon_surface
        self.press = None  # 记录鼠标点击状态
        self.cidpress = point_plot.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = point_plot.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = point_plot.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        """鼠标点击点"""
        contains, _ = self.point_plot.contains(event)
        if contains:
            self.press = (event.xdata, event.ydata)

    def on_release(self, event):
        """鼠标松开"""
        self.press = None

    def on_motion(self, event):
        """鼠标拖动事件"""
        if self.press is None:
            return
        if event.xdata is None or event.ydata is None:
            return

        # 更新点的新位置
        self.point_plot.set_data(event.xdata, event.ydata)

        # **更新三角形的第三个点**
        new_point = np.array([event.xdata, event.ydata])
        new_sets = np.concatenate([points, new_point.reshape(1, -1)], axis=0)
        new_theta = np.tanh(new_sets[:, 1] / new_sets[:, 0])  # 计算角度
        max_index = np.argmax(new_theta)
        min_index = np.argmin(new_theta)
        end_1 = t_max * new_sets[max_index]
        end_2 = t_max * new_sets[min_index]
        self.polygon_surface.set_xy([origin, end_1, end_2])
        # self.triangle_patch.set_xy(convex_hull_points)
        # self.polygon_surface = Polygon(convex_hull_points, closed=True, edgecolor='b', facecolor='lightblue', alpha=0.6)

        # 刷新画布
        self.point_plot.figure.canvas.draw()


# **创建可拖动点对象**
draggable_point = DraggablePoint(x_move, polygon_surface)
plt.show()