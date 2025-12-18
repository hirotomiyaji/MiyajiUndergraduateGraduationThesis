from manim import *
import numpy as np

class TorusKnotSurface(ThreeDScene):
    def construct(self):
        # カメラの初期位置
        self.set_camera_orientation(phi=30 * DEGREES, theta=45 * DEGREES)
        axes = ThreeDAxes()

        # --- ユーザー定義の結び目関数 ---
        def knot_func(t):
            theta = t
            r = np.cos(-3 * theta) + 2
            
            y = r * np.cos(2 * theta)
            x = r * np.sin(2 * theta)
            z = -np.sin(-3 * theta) + 2
            return np.array([x, y, z])

        # --- チューブの表面を計算する関数 ---
        def tube_func(u, v):
            # u: 結び目に沿ったパラメータ (0 ~ 2π)
            # v: チューブの断面の円周パラメータ (0 ~ 2π)
            radius = 0.3  # チューブの太さ（半径）

            # 中心点 P
            P = knot_func(u)
            
            # 接線ベクトル T (微分を近似)
            dt = 0.001
            P_next = knot_func(u + dt)
            T = P_next - P
            T = T / np.linalg.norm(T) # 正規化

            # 法線ベクトル N と 従法線ベクトル B を作る (Frenet-Serretのような枠)
            # 便宜的に、上方向(0,0,1)との外積を使って垂直なベクトルを見つける
            up = np.array([0, 0, 1])
            if np.linalg.norm(np.cross(T, up)) < 0.01:
                # もし接線が真上を向いていたら、別の軸を選ぶ
                up = np.array([0, 1, 0])
            
            N = np.cross(T, up)
            N = N / np.linalg.norm(N)
            
            B = np.cross(T, N)
            B = B / np.linalg.norm(B)

            # 中心点から、NとBが張る平面上に円を描く
            return P + radius * (np.cos(v) * N + np.sin(v) * B)

        # Surfaceでチューブを作成
        knot_surface = Surface(
            tube_func,
            u_range=[0, 2 * np.pi],
            v_range=[0, 2 * np.pi],
            resolution=(64, 16), # 解像度 (u方向の分割数, v方向の分割数)
            checkerboard_colors=[BLUE_D, TEAL_D], # ここで模様（市松模様）をつける
            stroke_width=0.5,     # メッシュの線の太さ
            stroke_color=WHITE,   # メッシュの線の色
            fill_opacity=0.8      # 透明度
        )

        # アニメーション
        self.play(Create(axes), run_time=1)
        
        # DrawBorderThenFill は Surface の描画にかっこいいエフェクトです
        # self.play(DrawBorderThenFill(knot_surface), run_time=2)
        self.play(Create(knot_surface), run_time=2)

        # カメラワーク（元のコードを踏襲）
        self.move_camera(
            phi=0 * DEGREES,
            theta=270 * DEGREES,
            run_time=1
        )
        self.wait(0.5)
        
        self.move_camera(phi=70 * DEGREES, theta=300 * DEGREES, run_time=1)
        self.wait(0.5)

        # 圧縮アニメーション（Surfaceにも適用可能）
        # Surfaceの各点に対して適用する必要があるため、少し重い場合があります
        self.play(
            knot_surface.animate.apply_function(lambda p: np.array([p[0], p[1], p[2]*0.1])),
            run_time=1,
        )
        self.wait(0.5)
        self.move_camera(phi=0 * DEGREES, theta=270 * DEGREES, run_time=1)
        self.wait(2)