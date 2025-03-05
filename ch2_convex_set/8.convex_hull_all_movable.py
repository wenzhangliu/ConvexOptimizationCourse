"""
《最优化方法》
第二章：凸集
授课教师：柳文章
代码演示：凸包
代码语言：Python
主要工具包：matplotlib, scipy.spatial
代码地址：https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
plt.rcParams['font.family'] = 'Heiti TC'  # 设置中文字体

# 初始化若干个点
points = np.array([[1.0, 3.0],
                   [3.0, 3.0],
                   [2.0, 1.0],
                   [0.5, 1.5],
                   [2.0, 2.0]])  # 点集

# 创建画布
fig, ax = plt.subplots()
ax.set_xlim(-2, 5)
ax.set_ylim(-2, 5)
ax.set_title("二维空间下的凸包演示案例-2")
plt.grid()
text_1 = plt.text(points[0, 0], points[0, 1]-0.3, r'$x_1$', fontsize=12)
text_2 = plt.text(points[1, 0], points[1, 1]-0.3, r'$x_2$', fontsize=12)
text_3 = plt.text(points[2, 0], points[2, 1]-0.3, r'$x_3$', fontsize=12)
text_4 = plt.text(points[3, 0], points[3, 1]-0.3, r'$x_4$', fontsize=12)
text_5 = plt.text(points[4, 0], points[4, 1]-0.3, r'$x_5$', fontsize=12)

# 计算凸包，并绘制初始多边形
hull = ConvexHull(points)
convex_hull_points = points[hull.vertices]
polygon_surface = Polygon(convex_hull_points, closed=True, edgecolor='b', facecolor='lightblue', alpha=0.6)
ax.add_patch(polygon_surface)

# 绘制可拖动的点
x_move_1, = ax.plot(points[0][0], points[0][1], 'ro', markersize=5)
x_move_2, = ax.plot(points[1][0], points[1][1], 'ro', markersize=5)
x_move_3, = ax.plot(points[2][0], points[2][1], 'ro', markersize=5)
x_move_4, = ax.plot(points[3][0], points[3][1], 'ro', markersize=5)
x_move_5, = ax.plot(points[4][0], points[4][1], 'ro', markersize=5)

# **拖动顶点的类**
class DraggablePoint:
    def __init__(self, point_plot, text, polygon_surface, index):
        self.point_plot = point_plot
        self.text = text
        self.polygon_surface = polygon_surface
        self.index = index
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
        self.text.set_position((event.xdata, event.ydata-0.3))

        # 更新凸包
        points[self.index] = np.array([event.xdata, event.ydata])
        hull = ConvexHull(points)
        convex_hull_points = points[hull.vertices]
        self.polygon_surface.set_xy(convex_hull_points)

        # 刷新画布
        self.point_plot.figure.canvas.draw()


# **创建可拖动点对象**
draggable_point_1 = DraggablePoint(x_move_1, text_1, polygon_surface, 0)
draggable_point_2 = DraggablePoint(x_move_2, text_2, polygon_surface, 1)
draggable_point_3 = DraggablePoint(x_move_3, text_3, polygon_surface, 2)
draggable_point_4 = DraggablePoint(x_move_4, text_4, polygon_surface, 3)
draggable_point_5 = DraggablePoint(x_move_5, text_5, polygon_surface, 4)
plt.show()
