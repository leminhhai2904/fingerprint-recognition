"""
Scene 6: Đối sánh dựa trên Minutiae (Phần trọng tâm) (Không có giọng nói)
- Bài toán đối sánh mẫu điểm
- Phương pháp Hough Transform
- So sánh đối sánh cục bộ vs toàn cục
- Phương pháp FingerCode (Jain et al.)
"""
from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene06Minutiae(Scene):
    def construct(self):
        scene_setup(self)
        self.section_title()
        self.minutiae_matching_intro()
        self.hough_transform()
        self.local_vs_global()
        self.fingercode()

    def section_title(self):
        """Tiêu đề mục."""
        num = Text("05", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = Text("Đối Sánh Dựa Trên Minutiae", font_size=42, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = Text(
            "Phương pháp đối sánh vân tay phổ biến nhất",
            font_size=22, color=TEXT_DIM,
        )
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3))
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        self.wait(0.5)
        self.play(FadeOut(group))

    def minutiae_matching_intro(self):
        """Hiển thị bài toán đối sánh mẫu điểm cơ bản."""
        section = get_section_title("Bài toán đối sánh mẫu điểm")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Minutiae mẫu (trái)
        t_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=3.5, y_length=3.5,
            axis_config={"color": TEXT_DIM, "stroke_width": 1, "include_numbers": False},
        ).shift(LEFT * 3.5 + DOWN * 0.3)

        t_label = Text("Mẫu T", font_size=20, color=CHART_BLUE, weight=BOLD)
        t_label.next_to(t_axes, UP, buff=0.3)

        t_boundary = Ellipse(
            width=3, height=3.8,
            color=CHART_BLUE, stroke_width=1, stroke_opacity=0.3,
        ).move_to(t_axes.c2p(2.5, 2.5))

        t_minutiae_data = [
            (1, 1.5, PI/3, "t"), (2, 3.5, PI/4, "b"),
            (1.5, 2.5, PI/6, "t"), (3, 4, PI/2, "b"),
            (3.5, 2, -PI/4, "t"), (4, 3, PI/5, "b"),
            (2.5, 1, PI*2/3, "t"), (4.2, 1.5, PI/3, "b"),
        ]

        t_points = VGroup()
        for x, y, theta, mtype in t_minutiae_data:
            pos = t_axes.c2p(x, y)
            p = create_minutia_point(
                pos, minutia_type="termination" if mtype == "t" else "bifurcation",
                angle=theta, scale=1.0,
            )
            t_points.add(p)

        # Minutiae đầu vào (phải)
        i_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=3.5, y_length=3.5,
            axis_config={"color": TEXT_DIM, "stroke_width": 1, "include_numbers": False},
        ).shift(RIGHT * 3.5 + DOWN * 0.3)

        i_label = Text("Đầu vào I", font_size=20, color=CHART_ORANGE, weight=BOLD)
        i_label.next_to(i_axes, UP, buff=0.3)

        i_boundary = Ellipse(
            width=3, height=3.8,
            color=CHART_ORANGE, stroke_width=1, stroke_opacity=0.3,
        ).move_to(i_axes.c2p(2.5, 2.5))

        dx, dy, dtheta = 0.3, -0.2, 0.15
        i_minutiae_data = []
        np.random.seed(42)
        for x, y, theta, mtype in t_minutiae_data:
            nx = x + dx + np.random.normal(0, 0.1)
            ny = y + dy + np.random.normal(0, 0.1)
            ntheta = theta + dtheta + np.random.normal(0, 0.05)
            i_minutiae_data.append((nx, ny, ntheta, mtype))
        i_minutiae_data.append((0.8, 4, PI/2, "t"))
        i_minutiae_data.append((4.5, 4.2, -PI/6, "b"))

        i_points = VGroup()
        for x, y, theta, mtype in i_minutiae_data:
            pos = i_axes.c2p(x, y)
            p = create_minutia_point(
                pos, minutia_type="termination" if mtype == "t" else "bifurcation",
                angle=theta, scale=1.0,
            )
            i_points.add(p)

        vs_label = Text("vs", font_size=28, color=TEXT_DIM)

        problem = Text(
            "Tìm phép căn chỉnh tốt nhất giữa hai tập điểm",
            font_size=18, color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.5)

        self.play(
            Create(t_axes), FadeIn(t_label), FadeIn(t_boundary),
            Create(i_axes), FadeIn(i_label), FadeIn(i_boundary),
        )
        self.play(FadeIn(vs_label))
        self.play(
            LaggedStart(*[FadeIn(p, scale=2) for p in t_points], lag_ratio=0.08),
            LaggedStart(*[FadeIn(p, scale=2) for p in i_points], lag_ratio=0.08),
            run_time=2,
        )
        self.play(FadeIn(problem, shift=UP * 0.2))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def hough_transform(self):
        """Giải thích phương pháp Hough Transform cho đối sánh minutiae."""
        section = get_section_title("Đối sánh bằng Hough Transform")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Bước 1
        step1_text = Text(
            "Bước 1: Với mỗi cặp minutiae, tính tham số biến đổi (Δx, Δy, Δθ)",
            font_size=17, color=TEXT_COLOR,
        ).next_to(section, DOWN, buff=0.5)
        self.play(FadeIn(step1_text, shift=UP * 0.2))

        mt_pos = LEFT * 3 + UP * 0.5
        mi_pos = LEFT * 1 + DOWN * 0.3

        mt = create_minutia_point(mt_pos, "termination", PI/4, scale=1.5)
        mi = create_minutia_point(mi_pos, "termination", PI/3, scale=1.5)
        mt_label = MathTex(r"m_T", font_size=24, color=CHART_BLUE).next_to(mt, UP, buff=0.2)
        mi_label = MathTex(r"m_I", font_size=24, color=CHART_ORANGE).next_to(mi, UP, buff=0.2)
        pair_arrow = Arrow(mt_pos, mi_pos, color=TEXT_DIM, stroke_width=1.5, buff=0.2)
        params = MathTex(r"\Delta x, \Delta y, \Delta\theta", font_size=28, color=PRIMARY)
        params.next_to(pair_arrow, RIGHT, buff=0.5)

        # Bước 2 - Bộ tích lũy Hough
        step2_text = Text(
            "Bước 2: Tích lũy bằng chứng trong không gian tham số",
            font_size=17, color=TEXT_COLOR,
        ).shift(DOWN * 0.5)

        hough_title = Text("Không gian Hough (Δx, Δy)", font_size=16, color=PRIMARY)
        grid_size = 6
        cell_size = 0.35
        hough_grid = VGroup()

        accumulator = np.zeros((grid_size, grid_size))
        peak_r, peak_c = 3, 4
        np.random.seed(123)
        for r in range(grid_size):
            for c in range(grid_size):
                dist = np.sqrt((r - peak_r)**2 + (c - peak_c)**2)
                accumulator[r][c] = max(0, 5 - dist * 1.5) + np.random.random() * 0.5

        for r in range(grid_size):
            for c in range(grid_size):
                val = accumulator[r][c] / 5.0
                color = interpolate_color(ManimColor(SECONDARY), ManimColor(PRIMARY), val)
                cell = Square(
                    side_length=cell_size,
                    fill_color=color, fill_opacity=0.6 + val * 0.4,
                    stroke_color=TEXT_DIM, stroke_width=0.5,
                )
                cell.move_to(RIGHT * 3 + np.array([
                    (c - grid_size/2) * cell_size,
                    (grid_size/2 - r) * cell_size, 0
                ]))
                hough_grid.add(cell)

        hough_title.next_to(hough_grid, UP, buff=0.2)

        peak_pos = RIGHT * 3 + np.array([
            (peak_c - grid_size/2) * cell_size,
            (grid_size/2 - peak_r) * cell_size, 0
        ])
        peak_circle = Circle(radius=cell_size * 0.6, color=MATCH_COLOR, stroke_width=2).move_to(peak_pos)
        peak_label = Text("Đỉnh!", font_size=14, color=MATCH_COLOR, weight=BOLD)
        peak_label.next_to(peak_circle, RIGHT, buff=0.2)

        step3_text = Text(
            "Bước 3: Đỉnh = phép biến đổi tốt nhất → tìm được căn chỉnh!",
            font_size=17, color=MATCH_COLOR,
        ).shift(DOWN * 1.5)

        self.play(FadeIn(mt), FadeIn(mt_label))
        self.play(FadeIn(mi), FadeIn(mi_label))
        self.play(GrowArrow(pair_arrow), FadeIn(params))
        self.wait(0.5)
        self.play(FadeIn(step2_text, shift=UP * 0.2))
        self.play(FadeIn(hough_grid, shift=LEFT * 0.3), FadeIn(hough_title), run_time=1)
        self.wait(0.5)
        self.play(Create(peak_circle), FadeIn(peak_label, shift=LEFT * 0.2), FadeIn(step3_text))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def local_vs_global(self):
        """So sánh đối sánh cục bộ và toàn cục."""
        section = get_section_title("Cục bộ vs Toàn cục")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Cục bộ
        local_box = create_rounded_box(
            width=5, height=3.5,
            fill_color=CHART_BLUE, fill_opacity=0.05,
            stroke_color=CHART_BLUE, stroke_width=1.5,
        )
        local_title = Text("Đối sánh cục bộ", font_size=22, color=CHART_BLUE, weight=BOLD)
        local_pros = VGroup(
            Text("✓ Không cần căn chỉnh toàn cục", font_size=14, color=MATCH_COLOR),
            Text("✓ Chịu được biến dạng tốt", font_size=14, color=MATCH_COLOR),
            Text("✓ Tính toán đơn giản hơn", font_size=14, color=MATCH_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        local_cons = VGroup(
            Text("✗ Kém phân biệt hơn", font_size=14, color=MISMATCH_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        local_content = VGroup(local_title, local_pros, local_cons).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        local_content.move_to(local_box)
        local_group = VGroup(local_box, local_content)

        # Toàn cục
        global_box = create_rounded_box(
            width=5, height=3.5,
            fill_color=CHART_ORANGE, fill_opacity=0.05,
            stroke_color=CHART_ORANGE, stroke_width=1.5,
        )
        global_title = Text("Đối sánh toàn cục", font_size=22, color=CHART_ORANGE, weight=BOLD)
        global_pros = VGroup(
            Text("✓ Khả năng phân biệt cao", font_size=14, color=MATCH_COLOR),
            Text("✓ Sử dụng quan hệ không gian", font_size=14, color=MATCH_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        global_cons = VGroup(
            Text("✗ Cần căn chỉnh trước", font_size=14, color=MISMATCH_COLOR),
            Text("✗ Nhạy cảm với biến dạng", font_size=14, color=MISMATCH_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        global_content = VGroup(global_title, global_pros, global_cons).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        global_content.move_to(global_box)
        global_group = VGroup(global_box, global_content)

        both = VGroup(local_group, global_group).arrange(RIGHT, buff=0.6).shift(DOWN * 0.3)

        tradeoff = Text(
            "Các phương pháp hiện đại kết hợp cả hai!",
            font_size=18, color=PRIMARY, weight=BOLD,
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(local_group, shift=RIGHT * 0.3))
        self.wait(0.5)
        self.play(FadeIn(global_group, shift=LEFT * 0.3))
        self.wait(0.5)
        self.play(FadeIn(tradeoff, shift=UP * 0.2))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def fingercode(self):
        """Minh họa phương pháp FingerCode của Jain et al."""
        section = get_section_title("Phương pháp FingerCode")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        ref = Text(
            "(Jain, Prabhakar, Hong & Pankanti, 2000)",
            font_size=14, color=TEXT_DIM,
        ).next_to(section, DOWN, buff=0.2)
        self.play(FadeIn(ref))

        core_pos = LEFT * 3 + DOWN * 0.5

        # Tessellation
        tessellation = VGroup()
        num_bands = 4
        sectors_per_band = 8
        colors = [CHART_BLUE, CHART_ORANGE, CHART_PURPLE, PRIMARY]

        for i in range(num_bands):
            inner_r = 0.4 + i * 0.35
            outer_r = 0.4 + (i + 1) * 0.35
            for j in range(sectors_per_band):
                start_angle = j * TAU / sectors_per_band
                angle = TAU / sectors_per_band
                sector = AnnularSector(
                    inner_radius=inner_r, outer_radius=outer_r,
                    angle=angle, start_angle=start_angle,
                    fill_color=colors[i], fill_opacity=0.1 + 0.05 * (j % 3),
                    stroke_color=colors[i], stroke_width=1, stroke_opacity=0.5,
                ).move_to(core_pos)
                tessellation.add(sector)

        core = Dot(core_pos, color=CORE_POINT, radius=0.08)
        core_label = Text("Core", font_size=14, color=CORE_POINT).next_to(core, UR, buff=0.1)
        tess_label = Text("Phân vùng quanh điểm core", font_size=16, color=TEXT_COLOR)
        tess_label.next_to(tessellation, DOWN, buff=0.5)

        arrow = Arrow(LEFT * 1 + DOWN * 0.5, RIGHT * 0.5 + DOWN * 0.5, color=PRIMARY, stroke_width=2)
        arrow_label = Text("Bộ lọc\nGabor", font_size=14, color=PRIMARY).next_to(arrow, UP, buff=0.15)

        fc_label = Text("FingerCode", font_size=18, color=TEXT_BRIGHT, weight=BOLD)
        fc_label.shift(RIGHT * 3.5 + UP * 1)

        bars = VGroup()
        np.random.seed(42)
        for i in range(16):
            height = 0.2 + np.random.random() * 1.5
            bar = Rectangle(
                width=0.2, height=height,
                fill_color=interpolate_color(ManimColor(CHART_BLUE), ManimColor(PRIMARY), i / 16),
                fill_opacity=0.7, stroke_width=0.5, stroke_color=TEXT_DIM,
            )
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
        bars.shift(RIGHT * 3.5 + DOWN * 0.5)
        fc_label.next_to(bars, UP, buff=0.3)

        formula = MathTex(
            r"d(FC_1, FC_2) = \|FC_1 - FC_2\|_2",
            font_size=26, color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.5)
        match_desc = Text(
            "Đối sánh = Khoảng cách Euclid giữa hai FingerCode",
            font_size=15, color=TEXT_DIM,
        ).next_to(formula, DOWN, buff=0.2)

        self.play(FadeIn(core, scale=2), FadeIn(core_label))
        self.play(
            LaggedStart(*[FadeIn(s) for s in tessellation], lag_ratio=0.02),
            run_time=2,
        )
        self.play(FadeIn(tess_label))
        self.play(GrowArrow(arrow), FadeIn(arrow_label))
        self.play(FadeIn(fc_label))
        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05),
            run_time=1.5,
        )
        self.play(Write(formula), FadeIn(match_desc))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))
