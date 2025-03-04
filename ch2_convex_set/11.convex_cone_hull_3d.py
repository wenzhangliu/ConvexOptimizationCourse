"""
《最优化方法》
第二章：凸集
授课教师：柳文章
代码演示：凸锥包（三维）
代码语言：Python
主要工具包：matplotlib.pyplot
代码地址：https://github.com/wenzhangliu/ConvexOptimizationCourse
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Heiti TC'  # 设置中文字体

# **创建 3D 画布**
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# **定义射线的起点 (原点)**
origin = np.array([0, 0, 0])

# **定义两条射线的方向向量**
direction_1 = np.array([1, 2, 3])  # 第一条射线的方向
direction_2 = np.array([3, 1, 2])  # 第二条射线的方向
direction_3 = np.array([1, 3, 2])  # 第二条射线的方向
direction_4 = np.array([3, 3, 1])  # 第二条射线的方向
ratio = 2.0
ax.scatter(ratio * direction_1[0], ratio * direction_1[1], ratio * direction_1[2], c='r', s=20)
ax.scatter(ratio * direction_2[0], ratio * direction_2[1], ratio * direction_2[2], c='r', s=20)
ax.scatter(ratio * direction_3[0], ratio * direction_3[1], ratio * direction_3[2], c='r', s=20)
ax.scatter(ratio * direction_4[0], ratio * direction_4[1], ratio * direction_4[2], c='r', s=20)
ax.text(ratio * direction_1[0], ratio * direction_1[1], ratio * direction_1[2], r'$x_1$')
ax.text(ratio * direction_2[0], ratio * direction_2[1], ratio * direction_2[2], r'$x_2$')
ax.text(ratio * direction_3[0], ratio * direction_3[1], ratio * direction_3[2], r'$x_3$')
ax.text(ratio * direction_4[0], ratio * direction_4[1], ratio * direction_4[2], r'$x_4$')

# **延长射线**
t_max = 5  # 控制射线长度
end_1 = origin + t_max * direction_1
end_2 = origin + t_max * direction_2
end_3 = origin + t_max * direction_3
end_4 = origin + t_max * direction_4

# **绘制射线**
ax.plot([origin[0], end_1[0]], [origin[1], end_1[1]], [origin[2], end_1[2]], 'r-', linewidth=2, label="射线 1")
ax.plot([origin[0], end_2[0]], [origin[1], end_2[1]], [origin[2], end_2[2]], 'b-', linewidth=2, label="射线 2")
ax.plot([origin[0], end_3[0]], [origin[1], end_3[1]], [origin[2], end_3[2]], 'b-', linewidth=2, label="射线 3")
ax.plot([origin[0], end_4[0]], [origin[1], end_4[1]], [origin[2], end_4[2]], 'b-', linewidth=2, label="射线 4")

# 创建平面网格
plane_x = np.array([origin[0], end_1[0], end_2[0]])
plane_y = np.array([origin[1], end_1[1], end_2[1]])
plane_z = np.array([origin[2], end_1[2], end_2[2]])
ax.plot_trisurf(plane_x, plane_y, plane_z, color='gray', alpha=0.5)

plane_x = np.array([origin[0], end_1[0], end_3[0]])
plane_y = np.array([origin[1], end_1[1], end_3[1]])
plane_z = np.array([origin[2], end_1[2], end_3[2]])
ax.plot_trisurf(plane_x, plane_y, plane_z, color='gray', alpha=0.5)

plane_x = np.array([origin[0], end_2[0], end_4[0]])
plane_y = np.array([origin[1], end_2[1], end_4[1]])
plane_z = np.array([origin[2], end_2[2], end_4[2]])
ax.plot_trisurf(plane_x, plane_y, plane_z, color='gray', alpha=0.5)

plane_x = np.array([origin[0], end_3[0], end_4[0]])
plane_y = np.array([origin[1], end_3[1], end_4[1]])
plane_z = np.array([origin[2], end_3[2], end_4[2]])
ax.plot_trisurf(plane_x, plane_y, plane_z, color='gray', alpha=0.5)

# **设置坐标轴范围**
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_zlim(0, 10)

# **设置标签**
ax.set_xlabel("X 轴")
ax.set_ylabel("Y 轴")
ax.set_zlabel("Z 轴")
ax.set_title("凸锥包示例（三维）")

# **显示图例**
ax.legend()

# **显示图形**
plt.show()