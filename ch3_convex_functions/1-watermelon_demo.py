#!/usr/bin/env python3
"""用二元函数演示凸函数的直线限制判据（切西瓜）。

安装：python -m pip install numpy matplotlib
运行：python watermelon_demo.py
导图：python watermelon_demo.py --save watermelon.png
验证：python watermelon_demo.py --self-test
中文字体自动检测，无可用中文字体时自动显示英文；也可 --lang zh / en。
Jupyter 可先运行 %matplotlib widget（另需 ipympl），推荐直接在终端运行。

数学：在凸定义域 D 上，f 凸等价于对任意直线 p+t*v，
g(t)=f(p+t*v) 在 I={t:p+t*v 属于 D} 上凸。
程序使用 D=[-2.5,2.5]^2；三维空间中的“刀”是竖直平面，
它在定义域上的投影是一条直线。不是用任意倾斜平面切曲面。

课堂步骤：
1. 选择凸碗面，旋转、平移切平面，每条切片都是凸的。
2. 点“看反例”：鞍面沿 y 方向切出凹曲线；中点高于弦，立即否定凸性。
3. 鞍面沿 x 方向切却是凸的：一条线通过检验，不代表整体凸。
4. 双谷曲面有凸切片与非凸切片；调节 A、B、lambda 找违反凸性的不等式。
5. 所有坐标范围固定。三维图可鼠标拖动旋转视角，控件更新保留视角。

切片凸性用二阶导数在完整切片区间的解析最小值判断；
弦线标记只检验当前 A、B、lambda，绝不把单次通过说成整体凸。
"""

import argparse
import warnings
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.widgets import Slider, RadioButtons, Button
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

L = 2.5
ZLIM = (-14, 14)  # 固定范围，覆盖加陡马鞍面的完整高度 ±12.5。
SADDLE_CURVATURE = 4.0  # f_xx=+4、f_yy=-4；原版为 ±1。
TLIM = (-3.6, 3.6)
BLUE, RED, GREEN, ORANGE = '#2563eb', '#db4266', '#059669', '#ea9319'


def f(kind, x, y):
    if kind == 0:
        return (x*x+2*y*y)/2
    if kind == 1:
        return SADDLE_CURVATURE*(x*x-y*y)/2
    return x**4/4-.8*x*x+y*y/2


def line_segment(angle, offset):
    """p=d*n 为离原点最近的直线点；精确求直线与方形 D 的交区间。"""
    theta = np.deg2rad(angle)
    v = np.array([np.cos(theta), np.sin(theta)])
    p = offset*np.array([-v[1], v[0]])
    low, high = -np.inf, np.inf
    for pi, vi in zip(p, v):
        if abs(vi) < 1e-12:
            if abs(pi) > L:
                raise ValueError('直线未与定义域相交')
        else:
            t1, t2 = sorted(((-L-pi)/vi, (L-pi)/vi))
            low, high = max(low, t1), min(high, t2)
    if low >= high:
        raise ValueError('没有非退化切片')
    return p, v, float(low), float(high)


def minimum_curvature(kind, p, v, low, high):
    """g''(t)=v^T Hessian(f)(p+tv)v 在整个切片区间的最小值。"""
    vx, vy = v
    if kind == 0:
        return vx*vx+2*vy*vy
    if kind == 1:
        return SADDLE_CURVATURE*(vx*vx-vy*vy)
    if abs(vx) < 1e-12:
        xmin = abs(p[0])
    else:
        t0 = np.clip(-p[0]/vx, low, high)
        xmin = abs(p[0]+t0*vx)
    return (3*xmin*xmin-1.6)*vx*vx+vy*vy


def setup_font(lang):
    names = {item.name for item in font_manager.fontManager.ttflist}
    chosen = next((name for name in ['PingFang SC', 'Microsoft YaHei', 'SimHei',
                   'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei',
                   'Heiti SC', 'Arial Unicode MS'] if name in names), None)
    zh = lang == 'zh' or (lang == 'auto' and chosen is not None)
    if chosen and zh:
        plt.rcParams['font.family'] = [chosen, 'DejaVu Sans']
    elif zh:
        warnings.warn('未找到中文字体。可安装中文字体或使用 --lang en。')
    plt.rcParams.update({'font.size': 11, 'axes.unicode_minus': False,
                         'axes.spines.top': False, 'axes.spines.right': False})
    return zh


class WatermelonDemo:
    def __init__(self, chinese):
        self.zh, self.kind, self.playing = chinese, 0, False
        self.busy = False
        self.fig = plt.figure(figsize=(17, 10), facecolor='#f5f7fb')
        self.fig.canvas.manager.set_window_title('切西瓜 | Convexity along lines')
        self.fig.suptitle(self.tr('切西瓜：沿每条直线看，都是凸的吗？',
                                  'Slice the surface: is every line restriction convex?'),
                          y=.967, fontsize=22, fontweight='bold')
        self.fig.text(.5, .916, self.tr('凸定义域 D 上：f 凸 ⇔ 每条直线限制 g(t) = f(p + tv) 都凸',
                                       'On a convex domain D: f is convex iff every restriction g(t) = f(p + tv) is convex'),
                      ha='center', fontsize=14, color='#172554')
        self.formula = self.fig.text(.055, .872, '', fontsize=17, color=BLUE)
        self.fig.text(.515, .86, r'$g((1-\lambda)t_A+\lambda t_B)\ \leq\ (1-\lambda)g(t_A)+\lambda g(t_B)$',
                      fontsize=15, color='#172554')
        self.ax3 = self.fig.add_axes([.025, .365, .45, .46], projection='3d')
        self.ax3.view_init(elev=27, azim=-58)
        self.axxy = self.fig.add_axes([.515, .425, .18, .34], facecolor='white')
        self.axg = self.fig.add_axes([.755, .425, .22, .34], facecolor='white')
        self.fig.text(.035, .835, self.tr('① 竖直平面切曲面（可拖动视角）',
                                         '1. Slice with a vertical plane (drag to orbit)'), fontsize=13)
        self.fig.text(.515, .79, self.tr('② 刀在定义域中的位置', '2. The line in the domain'), fontsize=13)
        self.fig.text(.755, .79, self.tr('③ 展开切片，检查弦线', '3. Unfold the slice; inspect chords'), fontsize=13)
        self.verdict = self.fig.text(.515, .352, '', fontsize=12, va='top', linespacing=1.6)
        self.line_text = self.fig.text(.055, .306, '', fontsize=11, color='#475569')
        self.chord_text = self.fig.text(.515, .29, '', fontsize=11, color='#475569', va='top')
        self.angle = Slider(self.fig.add_axes([.14, .229, .32, .023]),
                            self.tr('方向角 θ', 'Angle'), 0, 180, valinit=30)
        self.offset = Slider(self.fig.add_axes([.14, .177, .32, .023]),
                             self.tr('平移距离 d', 'Offset'), -2, 2, valinit=0)
        self.weight = Slider(self.fig.add_axes([.14, .125, .32, .023]),
                             r'$\lambda$', 0, 1, valinit=.5)
        self.end_a = Slider(self.fig.add_axes([.66, .229, .29, .023]),
                            self.tr('端点 A 位置', 'A position'), 0, 1, valinit=.25)
        self.end_b = Slider(self.fig.add_axes([.66, .177, .29, .023]),
                            self.tr('端点 B 位置', 'B position'), 0, 1, valinit=.75)
        self.fig.text(.61, .134, self.tr('端点位置按当前切片区间的比例设置（0 到 1）。',
                                        'Endpoint positions are fractions of the slice interval (0 to 1).'),
                      fontsize=10, color='#475569')
        self.labels = [self.tr('凸碗面', 'Convex bowl'), self.tr('非凸鞍面', 'Nonconvex saddle'),
                       self.tr('非凸双谷曲面', 'Nonconvex double well')]
        self.radio = RadioButtons(self.fig.add_axes([.055, .015, .25, .085], facecolor='white'),
                                  self.labels)
        self.play = Button(self.fig.add_axes([.345, .042, .115, .045]),
                           self.tr('自动旋转切面', 'Rotate the slice'))
        self.example = Button(self.fig.add_axes([.515, .042, .105, .045]),
                              self.tr('看反例', 'Counterexample'), color='#ffe4e6')
        self.reset_button = Button(self.fig.add_axes([.635, .042, .08, .045]), self.tr('重置', 'Reset'))
        self.fig.text(.75, .065, self.tr('一条切片不凸 ⇒ 整体不凸。', 'One nonconvex slice disproves convexity.'),
                      color=RED, fontsize=11)
        self.fig.text(.75, .031, self.tr('一条切片凸，不能证明整体凸。', 'One convex slice does not prove convexity.'),
                      color='#475569', fontsize=11)
        for slider in self.sliders:
            slider.on_changed(self.update)
        self.radio.on_clicked(self.select)
        self.play.on_clicked(self.toggle_play)
        self.example.on_clicked(self.counterexample)
        self.reset_button.on_clicked(self.reset)
        self.timer = self.fig.canvas.new_timer(interval=130)
        self.timer.add_callback(self.tick)
        self.fig.canvas.mpl_connect('close_event', lambda event: self.timer.stop())
        self.update()

    @property
    def sliders(self):
        return [self.angle, self.offset, self.weight, self.end_a, self.end_b]

    def tr(self, chinese, english):
        return chinese if self.zh else english

    def select(self, label):
        self.kind = self.labels.index(label)
        self.update()

    def toggle_play(self, *_):
        self.playing = not self.playing
        self.play.label.set_text(self.tr('暂停', 'Pause') if self.playing else self.tr('自动旋转切面', 'Rotate the slice'))
        if self.playing:
            self.timer.start()
        else:
            self.timer.stop()
        self.fig.canvas.draw_idle()

    def tick(self):
        if self.playing:
            self.angle.set_val((self.angle.val+2) % 180)

    def set_controls(self, kind, angle, offset, weight, pos_a, pos_b):
        self.busy = True
        try:
            self.radio.set_active(kind)
            for slider, value in zip(self.sliders, [angle, offset, weight, pos_a, pos_b]):
                slider.set_val(value)
        finally:
            self.busy = False
        self.update()

    def counterexample(self, *_):
        if self.playing:
            self.toggle_play()
        self.set_controls(1, 90, 0, .5, .25, .75)

    def reset(self, *_):
        if self.playing:
            self.toggle_play()
        self.ax3.view_init(27, -58)
        self.set_controls(0, 30, 0, .5, .25, .75)

    def update(self, *_):
        if self.busy:
            return
        p, v, low, high = line_segment(self.angle.val, self.offset.val)
        t = np.linspace(low, high, 501)
        xy = p[:, None]+v[:, None]*t
        g = f(self.kind, *xy)
        ta, tb = low+(high-low)*np.array([self.end_a.val, self.end_b.val])
        lam = self.weight.val
        tm = (1-lam)*ta+lam*tb
        xa, xb, xm = p+ta*v, p+tb*v, p+tm*v
        ga, gb, gm = [float(f(self.kind, *point)) for point in [xa, xb, xm]]
        chord_m = (1-lam)*ga+lam*gb
        gap = chord_m-gm
        self.last_gap = gap
        curvature = minimum_curvature(self.kind, p, v, low, high)
        self.last_curvature = curvature
        convex_slice = curvature >= -1e-9
        passes = gap >= -1e-9
        color = GREEN if passes else RED

        # 重绘保留学生用鼠标设置的相机角度，所有坐标轴范围固定。
        elev, azim = self.ax3.elev, self.ax3.azim
        self.ax3.clear()
        self.ax3.view_init(elev, azim)
        grid = np.linspace(-L, L, 41)
        xx, yy = np.meshgrid(grid, grid)
        zz = f(self.kind, xx, yy)
        cmap = 'coolwarm' if self.kind == 1 else 'Blues'
        self.ax3.plot_surface(xx, yy, zz, cmap=cmap, alpha=.62 if self.kind == 1 else .48, linewidth=0,
                              rcount=41, ccount=41, vmin=ZLIM[0], vmax=ZLIM[1])
        if self.kind == 1:
            self.ax3.plot_wireframe(xx, yy, zz, rstride=5, cstride=5,
                                    color='#475569', linewidth=.5, alpha=.3)
        ends = np.array([p+low*v, p+high*v])
        vertices = [[*ends[0], ZLIM[0]], [*ends[1], ZLIM[0]],
                    [*ends[1], ZLIM[1]], [*ends[0], ZLIM[1]]]
        plane = Poly3DCollection([vertices], facecolor='#fbbf24', edgecolor='#b7791f', alpha=.13)
        self.ax3.add_collection3d(plane)
        self.ax3.plot(*xy, g, color=RED, lw=3.6, label=self.tr('切片曲线', 'Slice g(t)'))
        self.ax3.plot(*xy, np.full_like(t, ZLIM[0]), '--', color='#b7791f', lw=1.8)
        self.ax3.plot([xa[0], xb[0]], [xa[1], xb[1]], [ga, gb], color=ORANGE, lw=2.5,
                      label=self.tr('两点之间的弦', 'Chord A-B'))
        self.ax3.scatter([xa[0], xb[0]], [xa[1], xb[1]], [ga, gb], color=ORANGE, s=40, depthshade=False)
        self.ax3.scatter([xm[0]], [xm[1]], [gm], color=color, s=45, depthshade=False)
        self.ax3.set(xlim=(-L, L), ylim=(-L, L), zlim=ZLIM, xlabel='x', ylabel='y', zlabel='f(x,y)')
        self.ax3.set_box_aspect((1, 1, .85))
        self.ax3.legend(loc='upper left', fontsize=10)

        self.axxy.clear()
        self.axxy.contourf(xx, yy, zz, levels=np.linspace(*ZLIM, 22), cmap=cmap, alpha=.7)
        self.axxy.plot(*xy, color=RED, lw=2.4)
        self.axxy.scatter([p[0]], [p[1]], color='#475569', s=22)
        for point, label in [(xa, 'A'), (xb, 'B')]:
            self.axxy.scatter(*point, color=ORANGE, s=45, zorder=4)
            self.axxy.annotate(label, point, xytext=(7, 5), textcoords='offset points', fontsize=11)
        self.axxy.arrow(p[0], p[1], .7*v[0], .7*v[1], width=.025, color=RED,
                        length_includes_head=True)
        self.axxy.set(xlim=(-L, L), ylim=(-L, L), xlabel='x', ylabel='y', aspect='equal')
        self.axxy.set_xticks([-2, 0, 2])
        self.axxy.set_yticks([-2, 0, 2])

        self.axg.clear()
        self.axg.grid(alpha=.2)
        self.axg.axhline(0, lw=.7, color='#94a3b8')
        self.axg.axvline(0, lw=.7, color='#94a3b8')
        self.axg.plot(t, g, color=RED, lw=2.8, label=r'$g(t)=f(p+tv)$')
        self.axg.plot([ta, tb], [ga, gb], color=ORANGE, lw=2.8, label=self.tr('弦线', 'Chord'))
        self.axg.scatter([ta, tb], [ga, gb], color=ORANGE, s=45, zorder=6)
        self.axg.scatter([tm], [gm], color=color, s=58, zorder=7)
        self.axg.scatter([tm], [chord_m], facecolor='white', edgecolor=ORANGE, s=48, zorder=6)
        self.axg.plot([tm, tm], [gm, chord_m], '--', color=color, lw=2)
        for tx, gx, label in [(ta, ga, 'A'), (tb, gb, 'B')]:
            self.axg.annotate(label, (tx, gx), xytext=(5, 7), textcoords='offset points')
        self.axg.set(xlim=TLIM, ylim=ZLIM, xlabel='t', ylabel='g(t)')
        self.axg.legend(loc='upper left', fontsize=10)
        formulas = [r'$f(x,y)=\frac{1}{2}(x^2+2y^2)$',
                    rf'$f(x,y)={SADDLE_CURVATURE/2:g}(x^2-y^2)$',
                    r'$f(x,y)=\frac{1}{4}x^4-0.8x^2+\frac{1}{2}y^2$']
        self.formula.set_text(formulas[self.kind])
        if self.zh:
            status = '当前整条切片：凸' if convex_slice else '当前整条切片：非凸 → 足以否定整体凸性'
            sample = '当前 A、B、λ 满足凸性不等式' if passes else '当前 A、B、λ 违反凸性不等式！'
            self.verdict.set_text(status+'\n'+sample)
            self.line_text.set_text(f'直线：(x,y) = ({p[0]:.2f}, {p[1]:.2f}) + t({v[0]:.2f}, {v[1]:.2f})\n'
                                    f'定义域 D = [−2.5, 2.5]²；当前 t 区间：[{low:.2f}, {high:.2f}]')
            self.chord_text.set_text(f'弦上高度 − 曲线高度 = {chord_m:.3f} − ({gm:.3f}) = {gap:.3f}\n'
                                     '绿色：当前检验通过；红色：当前检验失败。')
        else:
            status = 'Whole current slice: CONVEX' if convex_slice else 'Slice NONCONVEX: f is not convex'
            self.verdict.set_text(status+'\n'+('This A, B, lambda: inequality holds' if passes else 'This A, B, lambda: inequality VIOLATED'))
            self.line_text.set_text(f'(x,y) = ({p[0]:.2f}, {p[1]:.2f}) + t({v[0]:.2f}, {v[1]:.2f})\n'
                                    f'D = [-2.5, 2.5]^2; t in [{low:.2f}, {high:.2f}]')
            self.chord_text.set_text(f'Chord height - curve height = {chord_m:.3f} - ({gm:.3f}) = {gap:.3f}\n'
                                     'Green: this test passes. Red: this test fails.')
        self.verdict.set_color(GREEN if convex_slice else RED)
        self.fig.canvas.draw_idle()


def self_test(demo):
    for angle in np.linspace(0, 180, 37):
        for offset in [-2, 0, 2]:
            p, v, low, high = line_segment(angle, offset)
            assert np.isclose(np.linalg.norm(v), 1)
            assert abs(p@v) < 1e-10
            t = np.linspace(low, high, 301)
            x, y = p[:, None]+v[:, None]*t
            assert np.max(np.abs([x, y])) <= L+1e-10
            for kind in range(3):
                curvature = [v[0]**2+2*v[1]**2, SADDLE_CURVATURE*(v[0]**2-v[1]**2),
                             (3*x*x-1.6)*v[0]**2+v[1]**2][kind]
                exact = minimum_curvature(kind, p, v, low, high)
                # 对双谷曲面，精确最小值不高于网格值；网格误差有二次上界。
                assert exact <= np.min(curvature)+1e-10
                if kind == 2:
                    assert np.min(curvature)-exact <= 3*(high-low)**2/300**2+1e-9
    demo.counterexample()
    assert demo.last_gap < -.1 and demo.last_curvature < 0
    demo.angle.set_val(0)
    assert demo.last_gap > 0 and demo.last_curvature > 0
    demo.set_controls(2, 0, 0, .5, .25, .75)
    assert demo.last_gap < 0 and demo.last_curvature < 0
    # 一条切片本身非凸，选取另一些点却可以通过弦线检验。
    demo.set_controls(2, 0, 0, .5, .8, 1)
    assert demo.last_gap > 0 and demo.last_curvature < 0
    demo.ax3.view_init(36, -40)
    demo.weight.set_val(.3)
    assert demo.ax3.elev == 36 and demo.ax3.azim == -40
    assert demo.ax3.get_zlim() == ZLIM
    assert demo.axg.get_xlim() == TLIM and demo.axg.get_ylim() == ZLIM
    demo.toggle_play()
    old = demo.angle.val
    demo.tick()
    assert demo.angle.val != old
    demo.reset()
    assert demo.kind == 0 and not demo.playing
    demo.fig.canvas.draw()
    print('PASS: line clipping, exact slice curvature, counterexamples, single-test distinction, camera, fixed axes, widgets, timer, rendering.')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--lang', choices=['auto', 'zh', 'en'], default='auto')
    parser.add_argument('--save', metavar='PNG')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.save or args.self_test:
        plt.switch_backend('Agg')
    demo = WatermelonDemo(setup_font(args.lang))
    if args.self_test:
        self_test(demo)
    if args.save:
        output = Path(args.save).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        demo.fig.savefig(output, dpi=140, facecolor=demo.fig.get_facecolor())
        print(output)
    if not args.save and not args.self_test:
        if matplotlib.get_backend().lower() == 'agg':
            warnings.warn('Agg 不支持交互，请在桌面终端运行或在 Jupyter 中使用 %matplotlib widget。')
        plt.show()


if __name__ == '__main__':
    main()
