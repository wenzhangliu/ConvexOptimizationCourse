"""
《最优化方法》
第二章: 凸集
授课教师: 柳文章
代码演示: 透视函数（三维）
代码语言: Python
主要工具包: matplotlib.pyplot
代码地址: https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Slider
plt.rcParams['font.family'] = 'Heiti TC'  # 设置中文字体

# 创建 3D 画布
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制一个平面 z=1
x = np.linspace(-3, 3, 2)
y = np.linspace(-3, 3, 2)
X, Y = np.meshgrid(x, y)
global z_initial, z_initial_phase
z_initial, z_initial_phase = 1, -1  # 初始z值
Z = np.full_like(X, z_initial)
Z_ground = np.full_like(X, 0)
Z_phase = np.full_like(X, z_initial_phase)

# plane = ax.plot_surface(X, Y, Z, color='cyan', alpha=0.5)  # 绘制初始平面
plane_phase = ax.plot_surface(X, Y, Z_phase, color='cyan', alpha=0.5)  # 绘制初始平面的相平面
plane_ground = ax.plot_surface(X, Y, Z_ground, color='gray', alpha=0.8)  # 绘制初始平面

# 绘制圆形及其投影
radius = 1.0  
theta = np.linspace(0, 2 * np.pi, 100)  # 角度范围 [0, 2π]
r = np.linspace(0, radius, 50)  # 半径范围
Theta, R = np.meshgrid(theta, r)
X_circle = R * np.cos(Theta)
Y_circle = R * np.sin(Theta)
Z_circle = np.full_like(X_circle, z_initial)  # Z 轴固定值
X_circle_phase = -X_circle / z_initial
Y_circle_phase = -Y_circle / z_initial
Z_circle_phase = np.full_like(X_circle, z_initial_phase)  # 相平面初始Z值
circle = ax.plot_surface(X_circle, Y_circle, Z_circle, color='red', alpha=1.0)
circle_phase = ax.plot_surface(X_circle_phase, Y_circle_phase, Z_circle_phase, color='darkred', alpha=1.0)

# 绘制小孔
radius_hole = 0.1
theta_hole = np.linspace(0, 2 * np.pi, 10)  # 角度范围 [0, 2π]
r_hole = np.linspace(0, radius_hole, 50)  # 半径范围
Theta_hole, R_hole = np.meshgrid(theta_hole, r_hole)
X_circle_hole = R_hole * np.cos(Theta_hole)
Y_circle_hole = R_hole * np.sin(Theta_hole)
Z_circle_hole = np.full_like(X_circle_hole, 0)  # Z 轴固定值
circle_hole = ax.plot_surface(X_circle_hole, Y_circle_hole, Z_circle_hole, color='black', alpha=0.7)

# 绘制三角形
x_A, y_A = 1, 0
x_B, y_B = 2, 1
x_C, y_C = 2, -1
triangle_vertices = np.array([
    [x_A, y_A, z_initial],  # 点 A
    [x_B, y_B, z_initial],  # 点 B
    [x_C, y_C, z_initial] # 点 C
])
triangle_vertices_phase = np.array([
    [-x_A, -y_A, z_initial_phase],  # 点 A'
    [-x_B, -y_B, z_initial_phase],  # 点 B'
    [-x_C, -y_C, z_initial_phase] # 点 C'
])
triangle = ax.add_collection3d(Poly3DCollection([triangle_vertices], color='red', alpha=1.0))
triangle_phase = ax.add_collection3d(Poly3DCollection([triangle_vertices_phase], color='darkred', alpha=1.0))

text = ax.text(-3, -3, z_initial + 0.1, '物体')
text_phase = ax.text(-3, -3, z_initial_phase + 0.1, '相平面')

# 添加滑块
ax_slider = plt.axes([0.15, 0.07, 0.50, 0.03])  # 滑块位置
z_slider = Slider(ax_slider, "图像位置", -5, 5, valinit=1)  # 设定初始值为1

ax_slider_phase = plt.axes([0.15, 0.03, 0.50, 0.03])  # 滑块位置
Z_phase_slider = Slider(ax_slider_phase, "相平面位置", -5, 5, valinit=-1)  # 设定初始值为-1

# 更新函数
def update(val):
    global circle, circle_phase, triangle, triangle_phase, z_initial  # 需要修改全局变量
    z_initial = z_slider.val
    # plane.remove()  # 移除旧的超平面
    circle.remove()  # 移除旧的圆
    circle_phase.remove()  # 移除旧的投影圆
    triangle.remove()  # 移除旧的三角形
    triangle_phase.remove()  # 移除旧的三角形的相平面

    # plane = ax.plot_surface(X, Y, np.full_like(X, z_initial), color='cyan', alpha=0.2)  # 重新绘制

    Z_circle = np.full_like(X_circle, z_initial)  # 相平面初始Z值
    circle = ax.plot_surface(X_circle, Y_circle, Z_circle, color='red', alpha=0.7)

    X_circle_phase = X_circle / z_initial * z_initial_phase
    Y_circle_phase = Y_circle / z_initial * z_initial_phase
    Z_circle_phase = np.full_like(X_circle_phase, z_initial_phase)  # 相平面初始Z值
    circle_phase = ax.plot_surface(X_circle_phase, Y_circle_phase, Z_circle_phase, color='darkred', alpha=1.0)

    # 三角形的三个顶点 (x, y, z)
    triangle_vertices = np.array([
        [x_A, y_A, z_initial],  # 点 A
        [x_B, y_B, z_initial],  # 点 B
        [x_C, y_C, z_initial] # 点 C
    ])
    triangle_vertices_phase = np.array([
        [x_A / z_initial * z_initial_phase, y_A / z_initial * z_initial_phase, z_initial_phase],  # 点 A
        [x_B / z_initial * z_initial_phase, y_B / z_initial * z_initial_phase, z_initial_phase],  # 点 B
        [x_C / z_initial * z_initial_phase, y_C / z_initial * z_initial_phase, z_initial_phase] # 点 C
    ])
    triangle = ax.add_collection3d(Poly3DCollection([triangle_vertices], color='red', alpha=0.7))
    triangle_phase = ax.add_collection3d(Poly3DCollection([triangle_vertices_phase], color='darkred', alpha=1.0))

    text.set_position((-3, -3, z_initial + 0.1))
    
    fig.canvas.draw_idle()  # 刷新画布

def update_phase(val):
    global plane_phase, circle_phase, triangle_phase, z_initial_phase  # 需要修改全局变量
    z_initial_phase = Z_phase_slider.val
    plane_phase.remove()  # 移除旧的相平面
    circle_phase.remove()  # 移除相平面上的圆
    triangle_phase.remove()  # 移除相平面上的三角形
    
    plane_phase = ax.plot_surface(X, Y, np.full_like(X, z_initial_phase), color='cyan', alpha=0.5)  # 重新绘制

    X_circle_phase = X_circle / z_initial * z_initial_phase
    Y_circle_phase = Y_circle / z_initial * z_initial_phase
    Z_circle_phase = np.full_like(X_circle, z_initial_phase)  # 相平面初始Z值
    circle_phase = ax.plot_surface(X_circle_phase, Y_circle_phase, Z_circle_phase, color='darkred', alpha=1.0)

    # 三角形的三个顶点 (x, y, z)
    triangle_vertices_phase = np.array([
        [x_A / z_initial * z_initial_phase, y_A / z_initial * z_initial_phase, z_initial_phase],  # 点 A
        [x_B / z_initial * z_initial_phase, y_B / z_initial * z_initial_phase, z_initial_phase],  # 点 B
        [x_C / z_initial * z_initial_phase, y_C / z_initial * z_initial_phase, z_initial_phase] # 点 C
    ])
    triangle_phase = ax.add_collection3d(Poly3DCollection([triangle_vertices_phase], color='darkred', alpha=1.0))
    
    text_phase.set_position((-3, -3, z_initial_phase + 0.1))

    fig.canvas.draw_idle()  # 刷新画布

# 绑定滑块更新事件
z_slider.on_changed(update)
Z_phase_slider.on_changed(update_phase)

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-2, 2)

ax.set_xlabel("X 轴")
ax.set_ylabel("Y 轴")
ax.set_zlabel("Z 轴")
ax.set_title("透视函数演示")

ax.grid(False)
plt.show()