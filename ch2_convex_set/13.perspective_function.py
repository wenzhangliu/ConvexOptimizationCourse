"""
《最优化方法》
第二章: 凸集（保凸变换）
授课教师: 柳文章
代码演示: 透视函数（二维）
代码语言: Python
主要工具包: matplotlib.pyplot
代码地址: https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np

plt.rcParams['font.family'] = 'Heiti TC'  # 设置中文字体

# 创建图形和轴
fig, ax = plt.subplots(figsize=(6, 8))
plt.subplots_adjust(bottom=0.25)  # 给滑动条预留空间
plt.title('保凸变换：透视函数演示（二维）')
plt.xlim([-4, 4])
plt.ylim([-4, 4])
ax.axhline(y=0, color='black', linewidth=0.1)  # X 轴
ax.axvline(x=0, color='black', linewidth=0.1)  # Y 轴
X = np.linspace(-4, 4, 100)
X_Gound_0 = np.linspace(-4, -0.1, 50)
X_Gound_1 = np.linspace(0.1, 4, 50)
Y_Ground_0 = np.full_like(X_Gound_0, 0)
Y_Ground_1 = np.full_like(X_Gound_1, 0)

plane_ground_0 = ax.plot(X_Gound_0, Y_Ground_0, color='black', linewidth=2)  # 绘制地平线
plane_ground_0 = ax.plot(X_Gound_1, Y_Ground_1, color='black', linewidth=2)  # 绘制地平线

# 相平面
y_init_phase = -1.0
y_phase = np.full_like(X, y_init_phase)
plane_phase, = ax.plot(X, y_phase, color='gray', linewidth=2)

# 箭头起始点
y_init = 1.0
arrow_vector = np.array([2, 0])
x_A, y_A = -1, y_init  # 箭头起始点
x_B, y_B = x_A + arrow_vector[0], y_A + arrow_vector[1]  # 箭头终点
arrow = ax.annotate("", xy=(x_B, y_B), xytext=(x_A, y_A), arrowprops=dict(arrowstyle="->", linewidth=2, color="red"))
arrow_vector_phase = arrow_vector * y_init_phase / y_init
x_A_phase, y_A_phase = x_A * y_init_phase / y_init, y_A * y_init_phase / y_init  # 箭头起始点
x_B_phase, y_B_phase = x_B * y_init_phase / y_init, y_B * y_init_phase / y_init  # 箭头终点
arrow_phase = ax.annotate("", xy=(x_B_phase, y_B_phase), xytext=(x_A_phase, y_A_phase), arrowprops=dict(arrowstyle="->", linewidth=2, color="tomato"))

line_A_1, = ax.plot([0, x_A], [0, y_A], linestyle='--', color='gray', linewidth=1)
line_A_2, = ax.plot([0, x_A_phase], [0, y_A_phase], linestyle='--', color='gray', linewidth=1)
line_B_1, = ax.plot([0, x_B], [0, y_B], linestyle='--', color='gray', linewidth=1)
line_B_2, = ax.plot([0, x_B_phase], [0, y_B_phase], linestyle='--', color='gray', linewidth=1)

# 创建滑动条
ax_slider = fig.add_axes([0.15, 0.15, 0.50, 0.03])
slider = Slider(ax=ax_slider, label=r"图像位置", valmin=-4.0, valmax=4.0, valinit=y_init, orientation="horizontal")

ax_slider_phase = fig.add_axes([0.15, 0.05, 0.50, 0.03])
slider_phase = Slider(ax=ax_slider_phase, label=r"相平面位置", valmin=-4.0, valmax=4.0, valinit=y_init_phase, orientation="horizontal")
text = ax.text(-4, y_init + 0.1, '物体')
text_phase = ax.text(-4, y_init_phase + 0.1, '相平面')

reset_ax_1 = fig.add_axes([0.75, 0.15, 0.1, 0.03])
reset_ax_2 = fig.add_axes([0.75, 0.05, 0.1, 0.03])

def update(val):
    global y_init, x_A, x_B, y_A, y_B, x_A_phase, x_B_phase, y_A_phase, y_B_phase
    y_init = slider.val

    y_A = y_init  # 箭头起始点
    x_B, y_B = x_A + arrow_vector[0], y_A + arrow_vector[1]  # 箭头终点
    x_A_phase, y_A_phase = x_A * y_init_phase / y_init, y_init_phase  # 箭头起始点
    x_B_phase, y_B_phase = x_B * y_init_phase / y_init, y_init_phase  # 箭头终点
    
    arrow.set_position((x_A, y_A))
    arrow.xy = (x_B, y_B)
    arrow_phase.set_position((x_A_phase, y_A_phase))
    arrow_phase.xy = (x_B_phase, y_B_phase)

    line_A_1.set_data([0, x_A], [0, y_A])
    line_A_2.set_data([0, x_A_phase], [0, y_A_phase])
    line_B_1.set_data([0, x_B], [0, y_B])
    line_B_2.set_data([0, x_B_phase], [0, y_B_phase])

    text.set_position((-4, y_init))

    fig.canvas.draw_idle()  # 刷新画布

def update_phase(val):
    global y_init_phase, x_A, x_B, y_A, y_B, x_A_phase, x_B_phase, y_A_phase, y_B_phase
    y_init_phase = slider_phase.val
    plane_phase.set_ydata(np.full_like(X, y_init_phase))

    x_A_phase, y_A_phase = x_A * y_init_phase / y_init, y_init_phase  # 箭头起始点
    x_B_phase, y_B_phase = x_B * y_init_phase / y_init, y_init_phase  # 箭头终点
    
    arrow.set_position((x_A, y_A))
    arrow.xy = (x_B, y_B)
    arrow_phase.set_position((x_A_phase, y_A_phase))
    arrow_phase.xy = (x_B_phase, y_B_phase)

    line_A_1.set_data([0, x_A], [0, y_A])
    line_A_2.set_data([0, x_A_phase], [0, y_A_phase])
    line_B_1.set_data([0, x_B], [0, y_B])
    line_B_2.set_data([0, x_B_phase], [0, y_B_phase])

    text_phase.set_position((-4, y_init_phase + 0.1))

    fig.canvas.draw_idle()  # 刷新画布


def reset_1(event):
    slider.reset()


def reset_2(event):
    slider_phase.reset()


# 绑定滑动条事件和重置事件
slider.on_changed(update)
slider_phase.on_changed(update_phase)
button_1 = Button(reset_ax_1, '重置', hovercolor='0.975')
button_2 = Button(reset_ax_2, '重置', hovercolor='0.975')
button_1.on_clicked(reset_1)
button_2.on_clicked(reset_2)

# 显示图形
plt.show()
