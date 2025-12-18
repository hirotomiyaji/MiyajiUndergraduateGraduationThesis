from manim import *
import numpy as np

class TorusKnot(ThreeDScene):
    def construct(self):
        # カメラの初期位置設定
        self.set_camera_orientation(phi=30 * DEGREES, theta=45 * DEGREES)

        # 3次元座標軸の作成
        axes = ThreeDAxes()

        # パラメータ方程式の定義
        # x = r cos(2Θ)
        # y = r sin(2Θ)
        # z = -sin(-3Θ)
        # r = cos(-3Θ) + 2
        def knot_func(t):
            # t を theta (Θ) として扱います
            theta = t
            r = np.cos(-3 * theta) + 2
            
            y = r * np.cos(2 * theta)
            x = r * np.sin(2 * theta)
            z = -np.sin(-3 * theta) + 2
            
            return np.array([x, y, z])
        knot_outline = ParametricFunction(
            knot_func,
            t_range=np.array([0, 2 * np.pi, 0.01]),
            color=BLACK,        # 背景色が黒の場合
            stroke_width=30,    # メインの線より太くする（重要）
        )

        # 2. 前面のメインの線
        knot_core = ParametricFunction(
            knot_func,
            t_range=np.array([0, 2 * np.pi, 0.01]),
            color=BLUE,
            stroke_width=20,    # アウトラインより細くする
        )
        knot_core.set_color_by_gradient(BLUE, TEAL, GREEN, YELLOW)

        # 2つをグループ化して、1つのオブジェクトとして扱う
        knot_group = VGroup(knot_outline, knot_core)
        # シーンへの追加とアニメーション
        # self.add(axes)
        self.play(Create(axes), run_time=1)
        # 描画アニメーション
        self.play(Create(knot_group, lag_ratio=0), run_time=1, rate_func=linear)
        
        # カメラを少し回転させて立体感を確認する
        # self.begin_ambient_camera_rotation(rate=1)
        self.move_camera(
            phi=0 * DEGREES,       # 真上からの視点 (z軸方向)
            theta=270 * DEGREES,   # 任意: x軸を横、y軸を縦に見やすく調整
            run_time=1.5
        )
        self.wait(0.5)
        self.move_camera(phi=70 * DEGREES, theta=300 * DEGREES, run_time=1)
        self.wait(0.5)
        self.play(
            knot_group.animate.apply_function(lambda p: np.array([p[0], p[1], p[2]*0.1])),
            run_time=1,
        )
        self.wait(0.5)
        self.move_camera(phi=0 * DEGREES, theta=270 * DEGREES, run_time=1)
        self.wait(1)
        # self.sto_ambient_camera_rotation()