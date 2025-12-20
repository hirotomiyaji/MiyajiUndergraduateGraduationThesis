from manim import *
import numpy as np

class TorusKnotMorph(ThreeDScene):
    def construct(self):
        # カメラの初期位置
        self.set_camera_orientation(phi=30 * DEGREES, theta=45 * DEGREES)
        axes = ThreeDAxes()

        # --- 共通: チューブの表面を生成する関数を作る関数 ---
        # 異なる結び目関数(curve_func)を渡すと、それに対応するSurfaceを返す
        def create_surface(curve_func):
            def tube_func(u, v):
                radius = 0.3  # チューブの太さ
                
                # 中心点 P
                P = curve_func(u)
                
                # 接線 T, 法線 N, 従法線 B を計算
                dt = 0.001
                P_next = curve_func(u + dt)
                T = P_next - P
                T = T / np.linalg.norm(T)
                
                up = np.array([0, 0, 1])
                if np.linalg.norm(np.cross(T, up)) < 0.01:
                    up = np.array([0, 1, 0])
                
                N = np.cross(T, up)
                N = N / np.linalg.norm(N)
                
                B = np.cross(T, N)
                B = B / np.linalg.norm(B)
                
                return P + radius * (np.cos(v) * N + np.sin(v) * B)

            return Surface(
                tube_func,
                u_range=[0, 2 * np.pi],
                v_range=[0, 2 * np.pi],
                resolution=(64, 16),
                checkerboard_colors=[BLUE_D, TEAL_D],
                stroke_width=0.5,
                stroke_color=WHITE,
                fill_opacity=0.8
            )

        # --- 1. 最初の結び目 (元のコード) ---
        def knot_func_1(t):
            theta = t
            r = np.cos(-3 * theta) + 2
            y = r * np.cos(2 * theta)
            x = r * np.sin(2 * theta)
            z = -np.sin(-3 * theta) + 2
            return np.array([x, y, z])

        # --- 2. 新しい結び目の数式 (リクエスト) ---
        def knot_func_2(t):
            a = t # パラメータ theta
            # x = (2 + cos(2a))cos(3a)
            # y = (2 + cos(2a))sin(3a)
            # z = sin(4a)
            
            # 係数部分
            factor = 2 + np.cos(2 * a)
            
            x = factor * np.cos(3 * a)
            y = factor * np.sin(3 * a)
            # z = np.sin(4 * a)
            z = 0
            return np.array([x, y, z])
        def knot_func_3(t):
            theta = t
            r = np.cos(-5 * theta) + 2
            y = r * np.cos(2 * theta)
            x = r * np.sin(2 * theta)
            z = -np.sin(-5 * theta) + 2
            return np.array([x, y, z])

        # サーフェスの生成
        knot_surface = create_surface(knot_func_1)

        # --- アニメーション開始 ---
        self.play(Create(axes), run_time=1)
        self.play(Create(knot_surface), run_time=2)

        # カメラワーク
        self.move_camera(
            phi=0 * DEGREES,
            theta=270 * DEGREES,
            run_time=1
        )
        self.wait(0.5)
        
        self.move_camera(phi=70 * DEGREES, theta=300 * DEGREES, run_time=1)
        self.wait(0.5)

        # 圧縮アニメーション (z軸方向に潰す)
        self.play(
            knot_surface.animate.apply_function(lambda p: np.array([p[0], p[1], p[2]*0.1])),
            run_time=1,
        )
        self.wait(0.5)
        
        # カメラを真上に戻す
        self.move_camera(phi=0 * DEGREES, theta=270 * DEGREES, run_time=1)
        
        # ==========================================
        # ここから追加部分: 新しい形状への変形
        # ==========================================
        
        # ターゲットとなる新しい形状のSurfaceを作成（シーンにはまだ追加しない）
        target_surface = create_surface(knot_func_2)

        # Transformを使って、現在の knot_surface を target_surface の形へモーフィング
        # 直前の apply_function で潰れていた形状から、新しい形状へ膨らみながら変化します
        self.play(
            Transform(knot_surface, target_surface),
            run_time=1.5
        )
        self.wait(1)
        target_surface = create_surface(knot_func_3)
        self.play(
            Transform(knot_surface, target_surface),
            run_time=1.5
        )
        self.wait(2)