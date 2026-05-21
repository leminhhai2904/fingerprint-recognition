"""
Scene 6: Đối sánh dựa trên Minutiae (Minutiae-based Matching)
- Quy trình đối sánh điểm đặc trưng
- Thuật toán Hough Transform + Trực quan bay phiếu bầu biểu đồ không gian Hough
- Mô hình đối sánh toàn cục (Global Minutiae Matching)
- Trích xuất đặc trưng vùng vân (FingerCode)
"""
from manim import *
import numpy as np
import sys
import random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene06Minutiae(Scene):
    def construct(self):
        scene_setup(self)
        self.section_title()
        self.hough_transform()
        self.global_matching()
        self.fingercode_concept()

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kwargs):
        """create_text with CMU Serif kerning workaround (render big → scale down)."""
        return Text(text_str, font_size=36, color=color, weight=weight, **kwargs).scale(font_size / 36)

    def get_section_hdr(self, text):
        title = self.ct(text, font_size=30, color=TEXT_BRIGHT, weight=BOLD)
        underline = Line(
            start=title.get_left() + DOWN * 0.3,
            end=title.get_right() + DOWN * 0.3,
            color=PRIMARY,
            stroke_width=3,
        )
        return VGroup(title, underline)

    def section_title(self):
        """Tiêu đề mục — Segment 1 = 15.05s."""
        num = self.ct("05", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Đối Sánh Dựa Trên Minutiae", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Tiêu chuẩn vàng trong nhận dạng vân tay thương mại", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)

        # Target = 15.05s. Anim play = 2.5s. FadeOut = 1.0s. Need 11.55s wait.
        self.wait(11.55)
        self.play(FadeOut(group), run_time=1.0)
        self.wait(0.8) # Silence gap

    def hough_transform(self):
        """Giải thích phương pháp Hough Transform cho đối sánh minutiae — Segment 2 = 15.55s."""
        section = self.get_section_hdr("Đối sánh bằng Hough Transform")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        step1_text = self.ct(
            "Bước 1: Với mỗi cặp minutiae tương thích, tính tham số (Δx, Δy, Δθ)",
            font_size=17, color=TEXT_COLOR,
        ).next_to(section, DOWN, buff=0.5)
        self.play(FadeIn(step1_text, shift=UP * 0.2), run_time=0.6)

        mt_pos = LEFT * 3.5 + UP * 0.5
        mi_pos = LEFT * 1.5 + DOWN * 0.3

        mt = create_minutia_point(mt_pos, "termination", PI/4, scale=1.5)
        mi = create_minutia_point(mi_pos, "termination", PI/3, scale=1.5)
        mt_label = MathTex(r"m_T", font_size=24, color=CHART_BLUE).next_to(mt, UP, buff=0.2)
        mi_label = MathTex(r"m_I", font_size=24, color=CHART_ORANGE).next_to(mi, UP, buff=0.2)
        pair_arrow = Arrow(mt_pos, mi_pos, color=TEXT_DIM, stroke_width=1.5, buff=0.2)
        params = MathTex(r"\Delta x, \Delta y, \Delta\theta", font_size=28, color=PRIMARY)
        params.next_to(pair_arrow, RIGHT, buff=0.5)

        step2_text = self.ct("Bước 2: Tích lũy bằng chứng trong không gian Hough", font_size=17, color=TEXT_COLOR)
        step2_text.shift(DOWN * 0.5)

        hough_title = self.ct("Không gian Hough (Δx, Δy)", font_size=16, color=PRIMARY)
        grid_size = 6
        cell_size = 0.35
        hough_grid = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                cell = Square(
                    side_length=cell_size,
                    stroke_color=TEXT_DIM,
                    stroke_width=1,
                    fill_opacity=0.08,
                    fill_color=SECONDARY,
                ).move_to([
                    2.8 + (j - grid_size/2) * cell_size,
                    -0.2 + (grid_size/2 - i) * cell_size,
                    0
                ])
                hough_grid.add(cell)

        hough_title.next_to(hough_grid, UP, buff=0.25)
        
        peak_idx = 14  # Tọa độ đỉnh (2, 2) giả lập
        peak_cell = hough_grid[peak_idx]
        peak_pos = peak_cell.get_center()
        
        peak_circle = Circle(radius=0.25, color=MATCH_COLOR, stroke_width=2.5).move_to(peak_pos)
        peak_label = self.ct("Đỉnh!", font_size=13, color=MATCH_COLOR, weight=BOLD).next_to(peak_circle, UR, buff=0.05)

        step3_text = self.ct("Bước 3: Đỉnh tích lũy cao nhất cho biết tham số khớp", font_size=16, color=TEXT_COLOR).to_edge(DOWN, buff=0.4)

        self.play(
            FadeIn(mt), FadeIn(mt_label),
            FadeIn(mi), FadeIn(mi_label),
            GrowArrow(pair_arrow), FadeIn(params),
            run_time=1.5
        )
        self.play(FadeIn(step2_text, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(hough_grid, shift=LEFT * 0.3), FadeIn(hough_title), run_time=1.0)

        # Voting Dots Animation (Premium voting metaphor)
        voting_dots = VGroup(*[
            Dot(params.get_center(), color=PRIMARY, radius=0.06).set_opacity(0.8)
            for _ in range(12)
        ])
        self.play(FadeIn(voting_dots, run_time=0.3))
        
        random.seed(42)
        votes_anims = []
        for idx, dot in enumerate(voting_dots):
            if idx < 4:
                # Land on the peak cell
                target_pos = peak_pos
            else:
                # Land on other cells
                target_cell = random.choice(list(hough_grid))
                target_pos = target_cell.get_center()
            votes_anims.append(
                dot.animate(rate_func=smooth).move_to(target_pos).set_opacity(0.1)
            )

        # Fly votes across screen to the accumulator
        self.play(LaggedStart(*votes_anims, lag_ratio=0.08), run_time=1.5)

        # Peak accumulator cell flashes
        flash_cell = peak_cell.copy().set_fill(color=MATCH_COLOR, opacity=0.6).set_stroke(color=MATCH_COLOR, width=2.5)
        self.play(
            Create(peak_circle),
            FadeIn(peak_label, shift=LEFT * 0.2),
            FadeIn(step3_text),
            FadeIn(flash_cell),
            run_time=1.0
        )
        self.play(FadeOut(flash_cell), run_time=0.3)
        self.remove(voting_dots)

        # Target = 15.55s. Anim play = 0.6+0.6+1.5+0.6+1.0+0.3+1.5+1.0+0.3 = 7.4s. FadeOut = 1.0s. Need 7.15s wait.
        self.wait(7.15)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8) # Silence gap

    def global_matching(self):
        """Đối sánh minutiae toàn cục — Segment 3 = 17.40s."""
        section = self.get_section_hdr("Đối sánh Minutiae toàn cục")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Biểu diễn thuật toán
        desc = self.ct("Tìm phép biến đổi hình học (quay, tịnh tiến, tỷ lệ) tốt nhất giữa 2 tập đặc trưng", font_size=15, color=TEXT_COLOR)
        desc.next_to(section, DOWN, buff=0.45)
        self.play(FadeIn(desc), run_time=0.6)

        left_side = Square(side_length=3.0, color=CHART_BLUE, stroke_width=2).shift(LEFT * 3.5 + DOWN * 0.3)
        right_side = Square(side_length=3.0, color=CHART_ORANGE, stroke_width=2).shift(RIGHT * 0.5 + DOWN * 0.3)
        left_lbl = self.ct("Tập điểm T (Template)", font_size=16, color=CHART_BLUE, weight=BOLD).next_to(left_side, UP, buff=0.2)
        right_lbl = self.ct("Tập điểm I (Input)", font_size=16, color=CHART_ORANGE, weight=BOLD).next_to(right_side, UP, buff=0.2)

        t_data = [(0.5, 0.5, PI/4), (-0.8, 0.9, PI/6), (-0.4, -0.6, -PI/3)]
        i_data = [(0.7, 0.3, PI/4 + 0.1), (-0.6, 1.0, PI/6 + 0.15), (-0.2, -0.8, -PI/3 + 0.05)]

        t_points = VGroup(*[create_minutia_point(left_side.get_center() + np.array([x, y, 0]) * 1.2, "termination", th, scale=1.0) for x, y, th in t_data])
        i_points = VGroup(*[create_minutia_point(right_side.get_center() + np.array([x, y, 0]) * 1.2, "termination", th, scale=1.0) for x, y, th in i_data])

        arrow = Arrow(left_side.get_right(), right_side.get_left(), color=PRIMARY, stroke_width=3, buff=0.2)
        arrow_lbl = MathTex(r"\mathbf{R}, \mathbf{t}", font_size=28, color=PRIMARY).next_to(arrow, UP, buff=0.15)

        params_desc = VGroup(
            self.ct("Ma trận quay R", font_size=13, color=TEXT_DIM),
            self.ct("Véc-tơ tịnh tiến t", font_size=13, color=TEXT_DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(arrow, DOWN, buff=0.2)

        self.play(
            FadeIn(left_side), FadeIn(right_side),
            FadeIn(left_lbl), FadeIn(right_lbl),
            run_time=1.0
        )
        self.play(
            LaggedStart(*[FadeIn(p, scale=1.5) for p in t_points], lag_ratio=0.18),
            LaggedStart(*[FadeIn(p, scale=1.5) for p in i_points], lag_ratio=0.18),
            run_time=1.2,
        )
        self.play(GrowArrow(arrow), FadeIn(arrow_lbl), FadeIn(params_desc), run_time=0.8)

        # Target = 17.40s. Anim play = 0.6 + 0.6 + 1.0 + 1.2 + 0.8 = 4.2s. FadeOut = 1.0s. Need 12.20s wait.
        self.wait(12.20)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    def fingercode_concept(self):
        """Khái niệm FingerCode — Segment 4 = 17.04s."""
        section = self.get_section_hdr("Trích xuất đặc trưng vùng vân (FingerCode)")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Draw a center core point and concentric sectors representing FingerCode
        core = Dot(LEFT * 3 + DOWN * 0.2, color=CORE_POINT, radius=0.1)
        core_lbl = self.ct("Core (Tâm)", font_size=14, color=CORE_POINT, weight=BOLD).next_to(core, UP, buff=0.15)

        sectors = VGroup()
        colors = [CHART_BLUE, CHART_ORANGE, CHART_PURPLE, PRIMARY]
        for i in range(3): # 3 concentric bands
            radius_inner = 0.4 + i * 0.5
            radius_outer = 0.9 + i * 0.5
            for j in range(8): # 8 sectors
                sector = AnnularSector(
                    inner_radius=radius_inner,
                    outer_radius=radius_outer,
                    angle=PI / 4,
                    start_angle=j * (PI / 4),
                    color=colors[(i + j) % len(colors)],
                    fill_opacity=0.25,
                    stroke_color=TEXT_DIM,
                    stroke_width=1,
                ).move_to(core.get_center(), aligned_edge=ORIGIN)
                sectors.add(sector)

        sectors_lbl = self.ct("Vùng ảnh tròn được chia thành 80 cung rẻ quạt", font_size=16, color=TEXT_BRIGHT).next_to(sectors, DOWN, buff=0.3)

        # Feature vector (Right)
        vector_box = create_rounded_box(
            width=5.5, height=3.6,
            fill_color=SECONDARY, fill_opacity=0.2,
            stroke_color=PRIMARY, stroke_width=1.5,
        ).shift(RIGHT * 3.5 + DOWN * 0.2)
        vector_title = self.ct("Véc-tơ đặc trưng FingerCode", font_size=18, color=PRIMARY, weight=BOLD)
        vector_desc = self.ct("Độ lệch tuyệt đối trung bình (AAD) trong từng rẻ quạt", font_size=12, color=TEXT_DIM)
        
        # Draw dynamic vector matrix representation
        vector_mat = MathTex(
            r"\mathbf{v} = [v_1, v_2, v_3, \dots, v_{640}]",
            font_size=32, color=TEXT_BRIGHT,
        )
        vector_content = VGroup(vector_title, vector_desc, vector_mat).arrange(DOWN, buff=0.35)
        vector_content.move_to(vector_box)
        vector_group = VGroup(vector_box, vector_content)

        self.play(FadeIn(core), FadeIn(core_lbl), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(s, scale=0.8) for s in sectors], lag_ratio=0.03),
            run_time=1.5,
        )
        self.play(FadeIn(sectors_lbl), run_time=0.6)
        self.play(FadeIn(vector_group, shift=LEFT * 0.3), run_time=0.8)

        # Target = 17.04s. Anim play = 0.6 + 0.8 + 1.5 + 0.6 + 0.8 = 4.3s. FadeOut = 1.0s. Need 11.74s wait.
        self.wait(11.74)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
