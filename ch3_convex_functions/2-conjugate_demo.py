#!/usr/bin/env python3
"""共轭函数课堂演示（所有函数定义域均为 R）。

安装：python -m pip install numpy matplotlib
运行：python conjugate_demo.py
在 Jupyter 中先运行 %matplotlib widget（另需安装 ipympl），或在终端运行本文件。
中文字体自动检测；没有中文字体时自动用英文，也可传入 --lang en / --lang zh。
无界面导图：python conjugate_demo.py --save demo.png
数学与控件检查：python conjugate_demo.py --self-test

课堂顺序：
1. 拖动 y：中图的最大值成为右图上的一个点。
2. 左图橙线 yx 与蓝色 f 的最大竖直差，等于 f*(y)，可以为负。
3. 将橙线减去 f*(y)，得到绿色支撑线，其纵截距为 -f*(y)。
4. 勾选“保留支撑线”，拖动 y，观察直线族的上包络。
5. 改变 a 观察曲率影响；改变 c 观察 f 上移、f* 下移。
6. 切到带尖点的函数，观察 |y|<=1 时接触点一直停在 x=0。
7. 非凸函数有三个局部极小点（0、±3）和两个局部极大点（±1.5）。
   y=0 时支撑线同时接触两侧最低点；y 过零时最优接触点跳变。
   非凸函数也有凸的共轭函数，但支撑线族的上包络一般不能恢复原函数。

所有坐标范围固定，切换函数和拖动滑块均不改变坐标范围。
曲线远端可能超出显示窗口；求共轭仍然在整个实数域进行。
仅用 NumPy + Matplotlib。凸例子用解析解；非凸例子求全部实驻点并比较，
避免把单个局部极大值或有限网格最大值误当成全域上确界。
"""

import argparse
import warnings
from pathlib import Path

import numpy as np
import matplotlib
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button, CheckButtons

BLUE, ORANGE, GREEN, RED = '#2563eb', '#e78a16', '#059669', '#dc4267'
# 全部图统一使用固定范围；范围覆盖全部允许参数的最优接触点与共轭值。
X_LIMIT = (-6.8, 6.8)
Y_LIMITS = [(-22, 24), (-35, 28), (-3, 28)]
SLOPE_LIMIT = (-3.25, 3.25)


def evaluate(kind, x, a, c):
    x = np.asarray(x)
    if kind == 0:
        return a * x**2 / 2 + c
    if kind == 1:
        return a * x**4 / 4 + c
    if kind == 2:
        return a * x**2 / 2 + np.abs(x) + c
    # 导数 = 0.18*a*x*(x²-2.25)*(x²-9)，具有五个实驻点。
    return .18 * a * (x**6/6 - 11.25*x**4/4 + 20.25*x**2/2) + c


def stationary_points(y, a):
    """非凸 f 的 f'(x)=y 的全部实解（双精度数值求根）。

    f(x) 六次项系数为正，因此 yx-f(x) 在两端趋于负无穷；
    全局最大值必在这些实驻点中，可以逐一比较，不依赖局部优化初值。
    """
    roots = np.roots([.18*a, 0, -2.025*a, 0, 3.645*a, -float(y)])
    return np.sort(roots.real[np.abs(roots.imag) < 1e-7])


def conjugate(kind, y, a, c):
    """返回 (f*(y), 接触点 x*)，支持数组。"""
    y = np.asarray(y)
    if kind == 0:
        xstar = y / a
    elif kind == 1:
        xstar = np.cbrt(y / a)
    elif kind == 2:
        xstar = np.sign(y) * np.maximum(np.abs(y) - 1, 0) / a
    else:
        def best(slope):
            candidates = stationary_points(slope, a)
            profits = slope*candidates-evaluate(kind, candidates, a, c)
            return candidates[np.argmax(profits)]
        xstar = np.array([best(slope) for slope in y.flat]).reshape(y.shape)
    return y * xstar - evaluate(kind, xstar, a, c), xstar


def setup_font(lang):
    candidates = ['PingFang SC', 'Microsoft YaHei', 'SimHei',
                  'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei',
                  'Heiti SC', 'Arial Unicode MS']
    available = {f.name for f in font_manager.fontManager.ttflist}
    chosen = next((name for name in candidates if name in available), None)
    chinese = lang == 'zh' or (lang == 'auto' and chosen is not None)
    if chosen and chinese:
        plt.rcParams['font.family'] = [chosen, 'DejaVu Sans']
    elif lang == 'zh':
        warnings.warn('未检测到中文字体；若出现方框，请安装中文字体或使用 --lang en。')
    plt.rcParams.update({'axes.unicode_minus': False, 'font.size': 11,
                         'axes.spines.top': False, 'axes.spines.right': False})
    return chinese


class ConjugateDemo:
    def __init__(self, chinese=True):
        self.zh = chinese
        self.kind = 3
        self.playing = False
        self.direction = 1
        self.history = []
        self.last_y = None
        self.curve_cache = None
        self.fig = plt.figure(figsize=(16, 9), facecolor='#f5f7fb')
        self.fig.canvas.manager.set_window_title('Conjugate function | 共轭函数')
        self.fig.suptitle(self.t('共轭函数：一个最大值，两种几何解释',
                                'Conjugate function: one maximum, two geometric views'),
                          fontsize=21, fontweight='bold', y=.97)
        self.fig.text(.5, .913,
                      self.t('固定斜率 y → 寻找最大竖直差 → 平移得到支撑线 → 记录共轭函数值',
                             'Fix slope y  →  maximize the vertical difference  →  find the support line  →  record f*(y)'),
                      ha='center', color='#475569', fontsize=12)
        self.axes = [self.fig.add_axes([left, .405, .268, .395], facecolor='white')
                     for left in [.065, .385, .705]]
        self.summary = self.fig.text(.065, .318, '', fontsize=13, linespacing=1.7,
                                     bbox=dict(facecolor='white', edgecolor='#dbe2ed',
                                               boxstyle='round,pad=.65'), va='top')
        self.fig.text(.065, .872, r'$f^*(y)=\sup_{x\in\mathbb{R}}\{yx-f(x)\}$',
                      fontsize=17, color='#172554')
        self.formula = self.fig.text(.705, .872, '', fontsize=14, color=BLUE)
        self.sy = Slider(self.fig.add_axes([.12, .207, .47, .023]),
                         self.t('斜率 y', 'Slope y'), -3, 3, valinit=1.5)
        self.sa = Slider(self.fig.add_axes([.12, .153, .47, .023]),
                         self.t('系数 a', 'Scale a'), .5, 2, valinit=1)
        self.sc = Slider(self.fig.add_axes([.12, .099, .47, .023]),
                         self.t('平移 c', 'Shift c'), -2, 2, valinit=0)
        self.names = [self.t('二次函数', 'Quadratic'), self.t('四次函数', 'Quartic'),
                      self.t('带尖点的凸函数', 'Convex with a corner'),
                      self.t('多峰非凸函数', 'Nonconvex: 3 wells')]
        self.radio = RadioButtons(self.fig.add_axes([.655, .10, .19, .14],
                                                   facecolor='white'), self.names, active=3)
        self.check = CheckButtons(self.fig.add_axes([.855, .185, .135, .055]),
                                  [self.t('保留支撑线', 'Keep supports')], [False])
        self.play = Button(self.fig.add_axes([.855, .112, .063, .048]),
                           self.t('播放', 'Play'), color='#e0e7ff', hovercolor='#c7d2fe')
        self.reset_button = Button(self.fig.add_axes([.928, .112, .062, .048]),
                                   self.t('重置', 'Reset'))
        self.note = self.fig.text(.065, .043, '',
                      fontsize=11, color='#475569')
        self.polynomial = self.fig.text(.065, .012, '', fontsize=11, color='#475569')
        self.sy.on_changed(self.update)
        self.sa.on_changed(self.change_shape)
        self.sc.on_changed(self.change_shape)
        self.radio.on_clicked(self.select)
        self.check.on_clicked(self.clear_history)
        self.play.on_clicked(self.toggle_play)
        self.reset_button.on_clicked(self.reset)
        self.timer = self.fig.canvas.new_timer(interval=70)
        self.timer.add_callback(self.tick)
        self.fig.canvas.mpl_connect('close_event', lambda event: self.timer.stop())
        self.update()

    def t(self, zh, en):
        return zh if self.zh else en

    def select(self, label):
        self.kind = self.names.index(label)
        self.clear_history()

    def clear_history(self, *_):
        self.history.clear()
        self.last_y = None
        self.update()

    def change_shape(self, *_):
        self.clear_history()

    def toggle_play(self, *_):
        self.playing = not self.playing
        self.play.label.set_text(self.t('暂停', 'Pause') if self.playing else self.t('播放', 'Play'))
        if self.playing:
            self.timer.start()
        else:
            self.timer.stop()
        self.fig.canvas.draw_idle()

    def tick(self):
        if not self.playing:
            return
        value = self.sy.val + .055 * self.direction
        if value >= 3 or value <= -3:
            self.direction *= -1
        self.sy.set_val(float(np.clip(value, -3, 3)))

    def reset(self, *_):
        self.playing = False
        self.timer.stop()
        self.play.label.set_text(self.t('播放', 'Play'))
        self.kind = 3
        self.radio.set_active(3)
        self.sy.reset()
        self.sa.reset()
        self.sc.reset()
        if self.check.get_status()[0]:
            self.check.set_active(0)
        self.clear_history()

    def update(self, *_):
        y, a, c = self.sy.val, self.sa.val, self.sc.val
        value, xs = conjugate(self.kind, y, a, c)
        value, xs = float(value), float(xs)
        # 显示窗口固定；最优值在整个实数域上计算。
        x = np.linspace(*X_LIMIT, 1401)
        fx = evaluate(self.kind, x, a, c)
        fs = float(evaluate(self.kind, xs, a, c))
        ax1, ax2, ax3 = self.axes
        for ax in self.axes:
            ax.clear()
            ax.grid(alpha=.18)
            ax.axhline(0, color='#94a3b8', lw=.8)
            ax.axvline(0, color='#94a3b8', lw=.8)
            ax.tick_params(labelsize=10)
        if self.check.get_status()[0] and (self.last_y is None or abs(y-self.last_y) > .06):
            self.history.append((y, value))
            self.history = self.history[-80:]
            self.last_y = y
        if self.check.get_status()[0]:
            for slope, intercept_negative in self.history:
                ax1.plot(x, slope*x-intercept_negative, color=GREEN, alpha=.12, lw=1)
        ax1.plot(x, fx, color=BLUE, lw=3, label=r'$f(x)$')
        ax1.plot(x, y*x, '--', color=ORANGE, lw=2, label=r'$yx$')
        ax1.plot(x, y*x-value, color=GREEN, lw=2.2, label=r'$yx-f^*(y)$')
        ax1.scatter([xs], [fs], color=GREEN, s=55, zorder=6)
        if self.kind == 3:
            candidates = stationary_points(y, a)
            candidate_gaps = y*candidates-evaluate(self.kind, candidates, a, c)
            ties = candidates[np.isclose(candidate_gaps, value, atol=1e-8, rtol=1e-9)]
            ax1.scatter(ties, evaluate(self.kind, ties, a, c), color=GREEN, s=55, zorder=6)
            extrema = np.array([-3., -1.5, 0., 1.5, 3.])
            ax1.scatter(extrema, evaluate(self.kind, extrema, a, c),
                        color=BLUE, s=23, zorder=5)
        ax1.scatter([0], [-value], color=GREEN, s=40, zorder=6)
        ax1.annotate(r'$-f^*(y)$', (0, -value), xytext=(7, -15),
                     textcoords='offset points', color=GREEN, fontsize=11)
        ax1.plot([xs, xs], [fs, y*xs], color=RED, lw=3, alpha=.75)
        if abs(value) > .02:
            ax1.annotate('', xy=(xs, y*xs), xytext=(xs, fs),
                         arrowprops=dict(arrowstyle='<->', color=RED, lw=1.8))
        ax1.annotate(self.t('有符号差', 'Signed gap') + f' = {value:.2f}',
                     (xs, (fs+y*xs)/2), xytext=(-10 if xs > 0 else 10, 12),
                     ha='right' if xs > 0 else 'left',
                     textcoords='offset points', color=RED, fontsize=10,
                     bbox=dict(facecolor='white', alpha=.85, edgecolor='none'))
        ax1.set(xlim=X_LIMIT, ylim=Y_LIMITS[0], xlabel='x')
        ax1.set_title(self.t('① 最大竖直差与支撑线', '1. Vertical gap & support line'), loc='left', pad=12)
        ax1.legend(loc='upper left', fontsize=10, framealpha=.95)

        gap = y*x-fx
        ax2.plot(x, gap, color=RED, lw=2.7, label=r'$yx-f(x)$')
        ax2.axhline(value, color=GREEN, ls='--', lw=1.5,
                    label=r'$\max_x\{yx-f(x)\}=f^*(y)$')
        ax2.scatter([xs], [value], color=RED, s=65, zorder=5)
        if self.kind == 3:
            ax2.scatter(candidates, candidate_gaps, color='#64748b', s=25,
                        label=self.t('全部驻点', 'All stationary points'), zorder=4)
            ax2.scatter(ties, np.full_like(ties, value), color=RED, s=65, zorder=6)
        ax2.plot([xs, xs], [Y_LIMITS[1][0], value], ':', color='#94a3b8')
        ax2.annotate(f'x* = {xs:.2f}\nf*(y) = {value:.2f}', (xs, value),
                     xytext=(0, -48), textcoords='offset points', ha='center',
                     color=RED, bbox=dict(facecolor='white', edgecolor='none', alpha=.9))
        ax2.set(xlim=X_LIMIT, ylim=Y_LIMITS[1], xlabel='x')
        ax2.set_title(self.t('② 固定 y，对 x 求最大值', '2. Fix y; maximize over x'), loc='left', pad=12)
        ax2.legend(loc='lower left', fontsize=10)

        ys = np.linspace(-3, 3, 601)
        cache_key = (self.kind, a, c)
        if self.curve_cache is None or self.curve_cache[0] != cache_key:
            self.curve_cache = (cache_key, conjugate(self.kind, ys, a, c)[0])
        vals = self.curve_cache[1]
        ax3.plot(ys, vals, color=RED, lw=2.7, label=r'$f^*(y)$')
        ax3.scatter([y], [value], color=RED, s=75, zorder=5)
        ax3.plot([y, y], [0, value], ':', color=RED, alpha=.6)
        ax3.annotate(f'({y:.2f}, {value:.2f})', (y, value),
                     xytext=(-10 if y > 0 else 10, 15),
                     textcoords='offset points', ha='right' if y > 0 else 'left', color=RED)
        ax3.set(xlim=SLOPE_LIMIT, ylim=Y_LIMITS[2], xlabel='y')
        ax3.set_title(self.t('③ 把最大值画成新函数', '3. Plot the maximum as a function'), loc='left', pad=12)
        ax3.legend(loc='upper left', fontsize=11)
        formulas = [r'$f(x)=\frac{a}{2}x^2+c$', r'$f(x)=\frac{a}{4}x^4+c$',
                    r'$f(x)=\frac{a}{2}x^2+|x|+c$', r'$f(x)=a\,p(x)+c$']
        self.formula.set_text(formulas[self.kind])
        self.note.set_text(self.t('非凸例子：拖动 y 穿过 0，接触点会跳变；共轭函数仍然是凸的。所有坐标范围固定。',
                                 'Nonconvex case: cross y = 0 to see the contact jump. The conjugate is still convex. Axes stay fixed.')
                           if self.kind == 3 else
                           self.t('先拖 y，再保留支撑线；抬高 c 时右图下移。所有坐标范围固定，定义域均为实数。',
                                  'Try y, then keep supports. Raise c: f* moves down. Axes stay fixed; all domains are R.'))
        self.polynomial.set_text(r'$p(x)=0.18\,(x^6/6-11.25x^4/4+20.25x^2/2)$'
                                 if self.kind == 3 else '')
        if self.zh:
            text = (f'斜率 y = {y:.2f}     接触点 x* = {xs:.2f}     最大有符号差 f*(y) = {value:.2f}\n'
                    f'绿色支撑线：ℓ(x) = {y:.2f}x − ({value:.2f})     纵截距 = −f*(y) = {-value:.2f}')
        else:
            text = (f'Slope y = {y:.2f}     Contact x* = {xs:.2f}     Maximum signed gap f*(y) = {value:.2f}\n'
                    f'Support line: l(x) = {y:.2f}x - ({value:.2f})     Intercept = -f*(y) = {-value:.2f}')
        self.summary.set_text(text)
        self.fig.canvas.draw_idle()


def self_test(demo):
    """验证全局上界、接触等式、平移关系及控件实际回调。"""
    rng = np.random.default_rng(7)
    for kind in range(4):
        for a in [.5, 1, 2]:
            for c in [-2, 0, 2]:
                y = np.linspace(-3, 3, 121)
                values, xs = conjugate(kind, y, a, c)
                assert np.allclose(y*xs-evaluate(kind, xs, a, c), values)
                probes = rng.uniform(-9, 9, (500, 1))
                assert np.all(y*probes-evaluate(kind, probes, a, c) <= values+1e-10)
                zero_values, _ = conjugate(kind, y, a, 0)
                assert np.allclose(values, zero_values-c)
                assert np.all(np.diff(values, n=2) >= -1e-8), '共轭必须为凸函数'
                assert np.all((xs >= X_LIMIT[0]) & (xs <= X_LIMIT[1]))
                assert np.all((values >= Y_LIMITS[2][0]) & (values <= Y_LIMITS[2][1]))
                supports = -values
                contacts = evaluate(kind, xs, a, c)
                revenues = y*xs
                assert all(np.all((v >= Y_LIMITS[0][0]) & (v <= Y_LIMITS[0][1]))
                           for v in (supports, contacts, revenues))
    # y=0 两个同样好的接触点，且小幅正负价格导致全局最优点跳变。
    candidates = stationary_points(0, 1)
    values = -evaluate(3, candidates, 1, 0)
    ties = candidates[np.isclose(values, values.max())]
    assert np.allclose(ties, [-3, 3])
    assert conjugate(3, -.001, 1, 0)[1] < -2.9
    assert conjugate(3, .001, 1, 0)[1] > 2.9
    for kind in range(4):
        demo.radio.set_active(kind)
        for y in [-3, -1, 0, 1, 3]:
            demo.sy.set_val(y)
        demo.sa.set_val(.5)
        demo.sc.set_val(2)
        assert [ax.get_xlim() for ax in demo.axes] == [X_LIMIT, X_LIMIT, SLOPE_LIMIT]
        assert [ax.get_ylim() for ax in demo.axes] == Y_LIMITS
    demo.check.set_active(0)
    demo.sy.set_val(1.4)
    assert demo.history
    demo.sc.set_val(1)
    assert len(demo.history) == 1
    demo.toggle_play()
    old_y = demo.sy.val
    demo.tick()
    assert demo.sy.val != old_y
    demo.reset()
    assert demo.kind == 3 and not demo.playing and not demo.check.get_status()[0]
    demo.fig.canvas.draw()
    print('PASS: global maxima (4 functions), supports, convexity, ties/jumps, fixed axes, shifts, widgets, timer, reset, render.')


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--lang', choices=['auto', 'zh', 'en'], default='auto')
    parser.add_argument('--save', metavar='PNG', help='保存静态预览，不打开交互窗口')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.save or args.self_test:
        plt.switch_backend('Agg')
    demo = ConjugateDemo(setup_font(args.lang))
    if args.self_test:
        self_test(demo)
    if args.save:
        output = Path(args.save).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        demo.fig.savefig(output, dpi=150, facecolor=demo.fig.get_facecolor())
        print(output)
    if not args.save and not args.self_test:
        if 'agg' == matplotlib.get_backend().lower():
            warnings.warn('当前后端 Agg 不支持交互。请在有桌面环境的终端运行，或在 Jupyter 使用 %matplotlib widget。')
        plt.show()


if __name__ == '__main__':
    main()
