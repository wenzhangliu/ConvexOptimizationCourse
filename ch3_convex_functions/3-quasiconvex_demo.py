#!/usr/bin/env python3
"""左右三维对照：拟凸但非凸 vs 非拟凸。只依赖 numpy、matplotlib。

安装：python -m pip install numpy matplotlib
运行：python quasiconvex_3d_comparison.py
静态图：python quasiconvex_3d_comparison.py --save comparison.png
验证：python quasiconvex_3d_comparison.py --self-test
字体：自动中文（有可用中文字体时），否则英文；可 --lang zh / en。
Jupyter 可使用 %matplotlib widget（另需 ipympl），推荐桌面终端运行。

左：f(x,y)=(x²+y²)^(1/4)。alpha>=0 的下水平集为半径 alpha²
的圆盘；alpha<0 为空集，所以拟凸。但沿正 x 轴是 sqrt(x)，并不凸。
右：h(x,y)=(x²-1)²+y²。低下水平集分为两块；较高时虽连通，
仍可用两点及其中点给出不凸的反例。

水平切面上下移动，底部平面图同步显示下水平集。两幅三维图可分别
用鼠标拖动旋转，控件更新保留视角；自动视角旋转与水平升降分别控制。
所有坐标范围固定。升降水平 alpha 与底图所示的下水平集对应；
投影和可视曲面均在有限显示窗口内，函数本身定义在整个 R²。
"""

import argparse
import warnings
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

BLUE, GREEN, ORANGE, RED = '#2563eb', '#059669', '#ec9419', '#df4268'


def f(x, y):
    return (np.asarray(x)**2+np.asarray(y)**2)**.25


def h(x, y):
    return (np.asarray(x)**2-1)**2+np.asarray(y)**2


def witness(alpha):
    """整个滑块范围内：P、Q 在 h 的下水平集中，中点 M 在集合外。"""
    height = .85*np.sqrt(alpha)
    return np.array([-1., height]), np.array([1., height]), np.array([0., height])


def setup_font(lang):
    names = {item.name for item in font_manager.fontManager.ttflist}
    chosen = next((n for n in ['PingFang SC', 'Microsoft YaHei', 'SimHei',
                  'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei',
                  'Heiti SC', 'Arial Unicode MS'] if n in names), None)
    zh = lang == 'zh' or (lang == 'auto' and chosen is not None)
    if chosen and zh:
        plt.rcParams['font.family'] = [chosen, 'DejaVu Sans']
    elif zh:
        warnings.warn('未找到中文字体；可使用 --lang en。')
    plt.rcParams.update({'font.size': 11, 'axes.unicode_minus': False,
                         'axes.spines.top': False, 'axes.spines.right': False})
    return zh


class ComparisonDemo:
    def __init__(self, chinese=False):
        self.zh = chinese
        self.playing = False
        self.orbiting = False
        self.direction = 1
        self.fig = plt.figure(figsize=(16, 10), facecolor='#f5f7fb')
        self.fig.canvas.manager.set_window_title('拟凸与非拟凸 | 3D comparison')
        self.fig.suptitle(self.tr('拟凸与非拟凸：用水平切面看下水平集',
                                  'Quasiconvex vs. not quasiconvex: inspect sublevel sets'),
                          fontsize=22, fontweight='bold', y=.97)
        self.fig.text(.25, .91, self.tr('拟凸，但非凸', 'Quasiconvex, but not convex'),
                      ha='center', fontsize=18, fontweight='bold', color=GREEN)
        self.fig.text(.75, .91, self.tr('非拟凸', 'Not quasiconvex'),
                      ha='center', fontsize=18, fontweight='bold', color=RED)
        self.fig.text(.25, .867, r'$f(x,y)=(x^2+y^2)^{1/4}$', ha='center', fontsize=18, color=BLUE)
        self.fig.text(.75, .867, r'$h(x,y)=(x^2-1)^2+y^2$', ha='center', fontsize=18, color=BLUE)
        self.ax3s = [self.fig.add_axes([left, .40, .45, .43], projection='3d')
                     for left in [.025, .525]]
        self.insets = [self.fig.add_axes([left, .16, .18, .18], facecolor='white')
                       for left in [.07, .57]]
        self.left_note = self.fig.text(.285, .29, '', va='top', fontsize=12, linespacing=1.7)
        self.right_note = self.fig.text(.78, .29, '', va='top', fontsize=12, linespacing=1.7)
        self.fig.text(.16, .349, self.tr('下水平集（俯视）', 'Sublevel set: top view'), ha='center', fontsize=11)
        self.fig.text(.66, .349, self.tr('下水平集（俯视）', 'Sublevel set: top view'), ha='center', fontsize=11)
        for ax in self.ax3s:
            ax.view_init(28, -57)
        self.alpha = Slider(self.fig.add_axes([.15, .095, .37, .025]),
                            r'$\alpha$', .05, 1.4, valinit=.55)
        self.play = Button(self.fig.add_axes([.58, .087, .115, .045]), self.tr('升降播放', 'Animate level'))
        self.orbit = Button(self.fig.add_axes([.715, .087, .115, .045]), self.tr('旋转视角', 'Rotate views'))
        self.reset_button = Button(self.fig.add_axes([.85, .087, .09, .045]), self.tr('重置', 'Reset'))
        self.fig.text(.5, .037,
                      self.tr('绿色区域：函数值 ≤ α。右侧橙色两点在集合内，红色中点在集合外，因此下水平集不是凸集。',
                              'Green: function value ≤ alpha. On the right, P and Q are inside, but their midpoint M is outside.'),
                      ha='center', fontsize=12, color='#475569')
        self.alpha.on_changed(self.update)
        self.play.on_clicked(self.toggle_level)
        self.orbit.on_clicked(self.toggle_orbit)
        self.reset_button.on_clicked(self.reset)
        self.timer = self.fig.canvas.new_timer(interval=110)
        self.timer.add_callback(self.tick)
        self.fig.canvas.mpl_connect('close_event', lambda event: self.timer.stop())
        self.update()

    def tr(self, zh, en):
        return zh if self.zh else en

    def sync_timer(self):
        if self.playing or self.orbiting:
            self.timer.start()
        else:
            self.timer.stop()
        self.play.label.set_text(self.tr('暂停升降', 'Pause level') if self.playing else self.tr('升降播放', 'Animate level'))
        self.orbit.label.set_text(self.tr('暂停旋转', 'Pause views') if self.orbiting else self.tr('旋转视角', 'Rotate views'))
        self.fig.canvas.draw_idle()

    def toggle_level(self, *_):
        self.playing = not self.playing
        self.sync_timer()

    def toggle_orbit(self, *_):
        self.orbiting = not self.orbiting
        self.sync_timer()

    def tick(self):
        if self.orbiting:
            for ax in self.ax3s:
                ax.view_init(ax.elev, ax.azim+1.6)
        if self.playing:
            level = self.alpha.val+.018*self.direction
            if level <= self.alpha.valmin or level >= self.alpha.valmax:
                self.direction *= -1
            self.alpha.set_val(float(np.clip(level, self.alpha.valmin, self.alpha.valmax)))
        elif self.orbiting:
            self.fig.canvas.draw_idle()

    def reset(self, *_):
        self.playing = self.orbiting = False
        self.direction = 1
        self.sync_timer()
        for ax in self.ax3s:
            ax.view_init(28, -57)
        self.alpha.reset()
        self.update()

    def update(self, *_):
        alpha = self.alpha.val
        p, q, m = witness(alpha)
        configs = [(f, (-2, 2), (-2, 2), (-.18, 2), -.15),
                   (h, (-1.6, 1.6), (-1.3, 1.3), (-.3, 4.4), -.26)]
        for i, (fun, xlim, ylim, zlim, floor) in enumerate(configs):
            ax, top = self.ax3s[i], self.insets[i]
            elev, azim = ax.elev, ax.azim
            ax.clear()
            ax.view_init(elev, azim)
            coords = np.linspace(-1, 1, 65)
            # 原点附近加密，保留左侧 sqrt(norm) 的尖点。
            ux = xlim[1]*np.sign(coords)*np.abs(coords)**2
            uy = ylim[1]*np.sign(coords)*np.abs(coords)**2
            xx, yy = np.meshgrid(ux, uy)
            zz = fun(xx, yy)
            ax.plot_surface(xx, yy, np.where(zz > alpha, zz, np.nan),
                            color='#70a8de', alpha=.27, linewidth=0, rcount=40, ccount=40)
            ax.plot_surface(xx, yy, np.where(zz <= alpha, zz, np.nan),
                            color='#43bd91', alpha=.74, linewidth=0, rcount=40, ccount=40)
            plane = Poly3DCollection([[[xlim[0], ylim[0], alpha], [xlim[1], ylim[0], alpha],
                                       [xlim[1], ylim[1], alpha], [xlim[0], ylim[1], alpha]]],
                                     facecolor=ORANGE, edgecolor=ORANGE, alpha=.075)
            ax.add_collection3d(plane)
            # 规则密网格绘制精确形状的等高线和下水平集投影。
            gx, gy = np.meshgrid(np.linspace(*xlim, 201), np.linspace(*ylim, 201))
            gz = fun(gx, gy)
            top.clear()
            if i == 0:
                # 圆盘使用解析边界，小 alpha 时也不依赖网格分辨率。
                theta = np.linspace(0, 2*np.pi, 241)
                cx, cy = alpha**2*np.cos(theta), alpha**2*np.sin(theta)
                ax.plot(cx, cy, np.full_like(cx, alpha), color=GREEN, lw=2.1)
                disk = np.column_stack([cx, cy, np.full_like(cx, floor)])
                ax.add_collection3d(Poly3DCollection([disk], facecolor='#90dfbd',
                                                      edgecolor=GREEN, alpha=.7))
                top.add_patch(Circle((0, 0), alpha**2, facecolor='#a7f3d0',
                                     edgecolor=GREEN, lw=1.7))
            else:
                ax.contour(gx, gy, gz, levels=[alpha], colors=[GREEN], linewidths=2.1)
                ax.contourf(gx, gy, gz, levels=[-1, alpha], colors=['#90dfbd'],
                            zdir='z', offset=floor, alpha=.7)
                ax.contour(gx, gy, gz, levels=[alpha], colors=[GREEN], linewidths=1,
                           zdir='z', offset=floor)
                top.contourf(gx, gy, gz, levels=[-1, alpha], colors=['#a7f3d0'])
                top.contour(gx, gy, gz, levels=[alpha], colors=[GREEN], linewidths=1.7)
            if i == 0:
                # 沿 y=0 画弦，直接证实该拟凸函数并非凸函数。
                tx = np.linspace(0, 1.8, 151)
                ax.plot(tx, np.zeros_like(tx), np.sqrt(tx), color=BLUE, lw=2.6)
                ax.plot([0, 1.8], [0, 0], [0, np.sqrt(1.8)], color=ORANGE, lw=2.5)
                ax.scatter([.9], [0], [np.sqrt(.9)], color=BLUE, s=30, depthshade=False)
            else:
                hp, hq, hm = [float(h(*pt)) for pt in [p, q, m]]
                ax.plot([p[0], q[0]], [p[1], q[1]], [hp, hq], color=ORANGE, lw=2.7)
                ax.scatter([p[0], q[0]], [p[1], q[1]], [hp, hq], color=ORANGE, s=42, depthshade=False)
                ax.scatter([m[0]], [m[1]], [hm], color=RED, s=50, depthshade=False)
                ax.plot([m[0], m[0]], [m[1], m[1]], [hp, hm], ':', color=RED, lw=2)
                top.plot([p[0], q[0]], [p[1], q[1]], color=ORANGE, lw=2)
                top.scatter([p[0], q[0]], [p[1], q[1]], color=ORANGE, s=22, zorder=5)
                top.scatter([m[0]], [m[1]], color=RED, s=25, zorder=6)
                for point, name in [(p, 'P'), (q, 'Q'), (m, 'M')]:
                    top.annotate(name, point, xytext=(4, 6), textcoords='offset points', fontsize=9)
            ax.set(xlim=xlim, ylim=ylim, zlim=zlim, xlabel='x', ylabel='y',
                   zlabel='f(x,y)' if i == 0 else 'h(x,y)')
            ax.set_box_aspect((1, 1, .85))
            ax.set_zticks([0, .5, 1, 1.5, 2] if i == 0 else [0, 1, 2, 3, 4])
            top.set(xlim=xlim, ylim=ylim, aspect='equal', xlabel='x', ylabel='y')
            top.tick_params(labelsize=9)
        if self.zh:
            self.left_note.set_text(f'α = {alpha:.2f}\n圆盘半径：α² = {alpha**2:.2f}\n所有下水平集均凸。\n橙色弦低于曲线：\n函数并非凸函数。')
            state = '两个分离区域' if alpha < 1-1e-9 else '区域连通，仍非凸'
            self.right_note.set_text(f'α = {alpha:.2f}\n{state}\nh(P) = h(Q) = {hp:.2f}\nh(M) = {hm:.2f} > α\n中点在集合外。')
        else:
            self.left_note.set_text(f'alpha = {alpha:.2f}\nDisk radius = {alpha**2:.2f}\nEvery sublevel set is convex.\nCurve above orange chord:\nthe function is NOT convex.')
            state = 'Two separate regions' if alpha < 1-1e-9 else 'Connected, still NOT convex'
            self.right_note.set_text(f'alpha = {alpha:.2f}\n{state}\nh(P) = h(Q) = {hp:.2f}\nh(M) = {hm:.2f} > alpha\nMidpoint M is outside.')
        self.fig.canvas.draw_idle()


def self_test(app):
    for alpha in np.linspace(.05, 1.4, 101):
        p, q, m = witness(alpha)
        assert h(*p) <= alpha and h(*q) <= alpha and h(*m) > alpha
        theta = np.linspace(0, 2*np.pi, 100)
        assert np.allclose(f(alpha**2*np.cos(theta), alpha**2*np.sin(theta)), alpha)
    assert f(.9, 0) > .5*f(1.8, 0)
    for alpha in [.05, .55, 1, 1.4]:
        app.alpha.set_val(alpha)
        assert app.ax3s[0].get_zlim() == (-.18, 2)
        assert app.ax3s[1].get_zlim() == (-.3, 4.4)
    app.ax3s[0].view_init(32, -44)
    app.alpha.set_val(.6)
    assert app.ax3s[0].elev == 32 and app.ax3s[0].azim == -44
    app.toggle_level()
    app.toggle_orbit()
    old_alpha, old_azim = app.alpha.val, app.ax3s[0].azim
    app.tick()
    assert app.alpha.val != old_alpha and app.ax3s[0].azim != old_azim
    app.reset()
    assert not app.playing and not app.orbiting
    app.fig.canvas.draw()
    print('PASS: all-level witnesses, disk boundaries, nonconvexity, fixed axes, camera, animation, controls, render.')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--save', metavar='PNG')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--lang', choices=['auto', 'zh', 'en'], default='auto')
    args = parser.parse_args()
    if args.save or args.self_test:
        plt.switch_backend('Agg')
    app = ComparisonDemo(setup_font(args.lang))
    if args.self_test:
        self_test(app)
    if args.save:
        path = Path(args.save).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        app.fig.savefig(path, dpi=140, facecolor=app.fig.get_facecolor())
        print(path)
    if not args.save and not args.self_test:
        if matplotlib.get_backend().lower() == 'agg':
            warnings.warn('Agg 后端不支持交互；请在桌面终端运行，或在 Jupyter 使用 %matplotlib widget。')
        plt.show()


if __name__ == '__main__':
    main()
