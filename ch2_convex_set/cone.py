import numpy as np
import matplotlib.pyplot as plt

# **创建 3D 画布**
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# **定义射线的起点 (原点)**
origin = np.array([0, 0, 0])

# **定义两条射线的方向向量**
direction_1 = np.array([1, 2, 3])  # 第一条射线的方向
direction_2 = np.array([3, 1, 2])  # 第二条射线的方向

# **延长射线**
t_max = 5  # 控制射线长度
end_1 = origin + t_max * direction_1
end_2 = origin + t_max * direction_2

# **绘制射线**
ax.plot([origin[0], end_1[0]], [origin[1], end_1[1]], [origin[2], end_1[2]], 'r-', linewidth=2, label="射线 1")
ax.plot([origin[0], end_2[0]], [origin[1], end_2[1]], [origin[2], end_2[2]], 'b-', linewidth=2, label="射线 2")

# **绘制平面**
# 计算平面上的 3 个点（原点 + 2 个射线终点）
p1 = origin
p2 = end_1
p3 = end_2

# 创建平面网格
plane_x = np.array([p1[0], p2[0], p3[0]])
plane_y = np.array([p1[1], p2[1], p3[1]])
plane_z = np.array([p1[2], p2[2], p3[2]])

# 使用 `plot_trisurf()` 绘制三角形平面
ax.plot_trisurf(plane_x, plane_y, plane_z, color='gray', alpha=0.5)

# **设置坐标轴范围**
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_zlim(0, 10)

# **设置标签**
ax.set_xlabel("X 轴")
ax.set_ylabel("Y 轴")
ax.set_zlabel("Z 轴")
ax.set_title("3D 射线 & 平面")

# **显示图例**
ax.legend()

# **显示图形**
plt.show()