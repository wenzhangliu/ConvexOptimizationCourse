"""
《最优化方法》
第二章：凸集
授课教师：柳文章
代码演示：凸组合
代码语言：Python
主要工具包：matplotlib.pyplot
代码地址：https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np

plt.rcParams['font.family'] = 'Heiti TC'  # 设置中文字体

# 创建图形和轴
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.25)  # 给滑动条预留空间

# 点的坐标
x_1 = np.array([1.0, 3.0])  # 点x_1的坐标（二维）
x_2 = np.array([2.0, 4.0])  # 点x_2的坐标（二维）
x_3 = np.array([3.0, 3.0])  # 点x_3的坐标（二维）
x_4 = np.array([2.0, 1.0])  # 点x_4的坐标（二维）

# 绘制固定的 x_1, x_2, x_3 和 x_4
plt.title('凸组合示例')
plt.xlim([0, 4.0])
plt.ylim([0, 5.0])
plt.grid()
plt.plot([x_1[0], x_2[0]], [x_1[1], x_2[1]], color='gray', linewidth=2)
plt.plot([x_2[0], x_3[0]], [x_2[1], x_3[1]], color='gray', linewidth=2)
plt.plot([x_3[0], x_4[0]], [x_3[1], x_4[1]], color='gray', linewidth=2)
plt.plot([x_4[0], x_1[0]], [x_4[1], x_1[1]], color='gray', linewidth=2)
plt.scatter(*x_1, color='red', s=100, zorder=2, label="x_1")  # 绘制点x_1
plt.scatter(*x_2, color='red', s=100, zorder=2, label="x_2")  # 绘制点x_2
plt.scatter(*x_3, color='red', s=100, zorder=2, label="x_3")  # 绘制点x_3
plt.scatter(*x_4, color='red', s=100, zorder=2, label="x_4")  # 绘制点x_3
plt.text(x_1[0]-0.2, x_1[1]-0.3, r'$x_1$', fontsize=12)
plt.text(x_2[0], x_2[1]-0.3, r'$x_2$', fontsize=12)
plt.text(x_3[0], x_3[1]-0.3, r'$x_3$', fontsize=12)
plt.text(x_4[0], x_4[1]-0.3, r'$x_4$', fontsize=12)

# 初始凸组合点
initial_theta_1 = 0.0
initial_theta_2 = 0.0
initial_theta_3 = 0.0
initial_theta_4 = 1 - initial_theta_1 - initial_theta_2 - initial_theta_3
initial_x = initial_theta_1 * x_1 + initial_theta_2 * x_2 + initial_theta_3 * x_3 + initial_theta_4 * x_4
scatter_point = plt.scatter(*initial_x, color='blue', s=100, zorder=2, label="凸组合点")
text_label = ax.text(initial_x[0] + 0.1, initial_x[1], r"$\theta_1=0.0, \theta_2=0.0, \theta_3=1.0$",
                     fontsize=12, color='black')

# 创建滑动条
ax_slider_1 = fig.add_axes([0.15, 0.15, 0.50, 0.03])
slider_1 = Slider(ax=ax_slider_1, label=r"$\theta_1$", valmin=0, valmax=1.0, valinit=0.0, orientation="horizontal")

ax_slider_2 = fig.add_axes([0.15, 0.10, 0.50, 0.03])
slider_2 = Slider(ax=ax_slider_2, label=r"$\theta_2$", valmin=0, valmax=1.0 - slider_1.val, valinit=0.0, orientation="horizontal")

ax_slider_3 = fig.add_axes([0.15, 0.05, 0.50, 0.03])
slider_3 = Slider(ax=ax_slider_3, label=r"$\theta_3$", valmin=0, valmax=1.0 - slider_1.val - slider_2.val, valinit=0.0, orientation="horizontal")

reset_ax_1 = fig.add_axes([0.75, 0.15, 0.1, 0.03])
reset_ax_2 = fig.add_axes([0.75, 0.10, 0.1, 0.03])
reset_ax_3 = fig.add_axes([0.75, 0.05, 0.1, 0.03])

global theta_1, theta_2, theta_3

def update_1(val):
    theta_1 = np.clip(slider_1.val, 0, 1)
    theta_2 = np.clip(slider_2.val, 0, 1)
    theta_3 = np.clip(slider_3.val, 0, 1)
    slider_2.valmax = 1.0 - theta_1 - theta_3  # 动态调整 slider2 的最大值
    slider_2.set_val(min(slider_2.val, slider_2.valmax))  # 确保 slider2 值不超范围
    theta_4 = 1 - theta_1 - theta_2 - theta_3
    theta_4 = np.clip(theta_4, 0, 1)
    new_x = theta_1 * x_1 + theta_2 * x_2 + theta_3 * x_3 + theta_4 * x_4  # 计算凸组合点坐标
    scatter_point.set_offsets(np.array([new_x]))  # 直接更新散点位置
    text_label.set_position((new_x[0] + 0.1, new_x[1]))  # 更新文本位置
    text_label.set_text(
        r"$\theta_1=$" + f"{round(theta_1, 2)}, " + r"$\theta_2=$" + f"{round(theta_2, 2)}, " + r"$\theta_3=$" + f"{round(theta_3, 2)}, " + r"$\theta_4=$" + f"{round(theta_4, 2)}")  # 更新文本内容
    fig.canvas.draw_idle()  # 刷新画布
    update_2(slider_2.val)  # 更新凸组合点

def update_2(val):
    theta_1 = np.clip(slider_1.val, 0, 1)
    theta_2 = np.clip(slider_2.val, 0, 1)
    theta_3 = np.clip(slider_3.val, 0, 1)
    slider_3.valmax = 1.0 - theta_1 - theta_2  # 动态调整 slider2 的最大值
    slider_3.set_val(min(slider_3.val, slider_3.valmax))  # 确保 slider2 值不超范围
    theta_4 = 1 - theta_1 - theta_2 - theta_3
    theta_4 = np.clip(theta_4, 0, 1)
    new_x = theta_1 * x_1 + theta_2 * x_2 + theta_3 * x_3 + theta_4 * x_4  # 计算凸组合点坐标
    scatter_point.set_offsets(np.array([new_x]))  # 直接更新散点位置
    text_label.set_position((new_x[0] + 0.1, new_x[1]))  # 更新文本位置
    text_label.set_text(
        r"$\theta_1=$" + f"{round(theta_1, 2)}, " + r"$\theta_2=$" + f"{round(theta_2, 2)}, " + r"$\theta_3=$" + f"{round(theta_3, 2)}, " + r"$\theta_4=$" + f"{round(theta_4, 2)}")  # 更新文本内容
    fig.canvas.draw_idle()  # 刷新画布
    update_3(slider_3.val)  # 更新凸组合点


def update_3(val):
    theta_1 = np.clip(slider_1.val, 0, 1)
    theta_2 = np.clip(slider_2.val, 0, 1)
    theta_3 = np.clip(slider_3.val, 0, 1)
    theta_4 = 1 - theta_1 - theta_2 - theta_3
    theta_4 = np.clip(theta_4, 0, 1)
    new_x = theta_1 * x_1 + theta_2 * x_2 + theta_3 * x_3 + theta_4 * x_4  # 计算凸组合点坐标
    scatter_point.set_offsets(np.array([new_x]))  # 直接更新散点位置
    text_label.set_position((new_x[0] + 0.1, new_x[1]))  # 更新文本位置
    text_label.set_text(
        r"$\theta_1=$" + f"{round(theta_1, 2)}, " + r"$\theta_2=$" + f"{round(theta_2, 2)}, " + r"$\theta_3=$" + f"{round(theta_3, 2)}, " + r"$\theta_4=$" + f"{round(theta_4, 2)}")  # 更新文本内容
    fig.canvas.draw_idle()  # 刷新画布


def reset_1(event):
    slider_1.reset()


def reset_2(event):
    slider_2.reset()


def reset_3(event):
    slider_3.reset()


# 绑定滑动条事件和重置事件
slider_1.on_changed(update_1)
slider_2.on_changed(update_2)
slider_3.on_changed(update_3)
button_1 = Button(reset_ax_1, r'重置$\theta_1$', hovercolor='0.975')
button_2 = Button(reset_ax_2, r'重置$\theta_2$', hovercolor='0.975')
button_3 = Button(reset_ax_3, r'重置$\theta_3$', hovercolor='0.975')
button_1.on_clicked(reset_1)
button_2.on_clicked(reset_2)
button_3.on_clicked(reset_3)

# 显示图形
plt.show()
