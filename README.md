# 《最优化方法》--代码演示

课程简介：安徽大学人工智能专业本科必修课程。

授课教师：柳文章（教师主页：[https://ai.ahu.edu.cn/2025/0224/c19213a357831/page.htm](https://ai.ahu.edu.cn/2025/0224/c19213a357831/page.htm)）

代码语言：Python

主要工具包：[matplotlib](https://matplotlib.org/)

代码地址：https://github.com/wenzhangliu/ConvexOptimizationCourse

## 安装方法

### 步骤1：配置并激活Conda环境

首先安装Anaconda，并在终端输入如下指令配置Conda环境，建议Python版本为3.10，名字自定义（如cvxopt）：

```bash
conda create -n cvxopt python=3.10
```

配置完成后，激活该环境：

```bash
conda activate cvxopt
```

### 步骤2：安装依赖包

本课程主要涉及数学工具python包``matplotlib``和``numpy``，建议版本安装指令如下：

```bash
pip install -r requirements.txt
```

完成安装后，即可运行本项目下的任何代码。如有任何问题，欢迎在[**Issue**](https://github.com/wenzhangliu/ConvexOptimizationCourse/issues)栏目提问。

## 课程大纲

- 第一章：引言
  - 优化/数学规划
  - 全局最优与局部最优
  - 优化问题的分类
  - 案例解析
- 第二章：凸集
  - 向量求导与范数
  - 仿射集、凸集、凸锥
  - 保凸变换
- 第三章：凸函数
  - 凸函数的定义
  - 保凸运算
  - 拟凸运算
- 第四章：凸优化问题
  - 优化问题
  - 凸优化问题
  - 线性规划
  - 多目标优化
- 第五章：对偶性
  - 拉格朗日对偶
  - 几种解释
  - KKT条件
  - 敏感性分析
- 第六章：无约束优化
  - 无约束优化问题
  - 梯度下降法
  - 最速下降法
  - 牛顿法
- 第七章：等式约束优化
  - 等式约束优化问题
  - 拉格朗日法
  - 增广拉格朗日法
  - 交替方向乘子法

## 参考书目

- Stephen Boyd and Lieven Vandenberghe. Convex Optimization. Cambridge University Press, 2004. [**Link**](https://stanford.edu/~boyd/cvxbook/)
- Stephen Boyd and Lieven Vandenberghe. 凸优化. Trans. by 王 书宁，许鋆，黄晓霖. 清华大学出版社, 2012. [**Link**](http://www.tup.tsinghua.edu.cn/upload/books/yz/031849-02.pdf)
- Yurii Nesterov. Lectures on Convex Optimization. Springer, 2018. [**Link**](https://shuyuej.com/books/Lectures%20on%20Convex%20Optimization.pdf)
- Jorge Nocedal and Stephen J Wright. Numerical Optimization. Springer, 1999. [**Link**](https://www.math.uci.edu/~qnie/Publications/NumericalOptimization.pdf)
- Dimitri P Bertsekas. Nonlinear Programming. Athena Scientific, 1999.[**Link**](https://mcube.lab.nycu.edu.tw/~cfung/docs/books/bertsekas1999nonlinear_programming.pdf)
- 袁亚湘，孙文瑜. 最优化理论与方法. 科学出版社, 1997.[**Link**]()
