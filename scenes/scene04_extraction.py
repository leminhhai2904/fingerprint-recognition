"""
Scene 4: Trích xuất đặc trưng (Feature Extraction) (Section 2.3)
- Hướng đường vân (Orientation) & Tần số đường vân (Frequency)
- Phân vùng ảnh (Segmentation) & Vùng kỳ dị (Poincaré Index)
- Quy trình xử lý ảnh: xám -> tăng cường -> nhị phân -> xương + Quét laser đồng bộ
- Thuật toán Crossing Number (CN)
"""
from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene04Extraction(Scene):
    def construct(self):
        scene_setup(self)
        self.section_title()
        self.orientation_and_frequency()
        self.segmentation_and_singularities()
        self.enhancement_pipeline()
        self.crossing_number_extraction()

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
        """Tiêu đề mục — Segment 1 = 5.76s."""
        num = self.ct("03", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Trích Xuất Đặc Trưng", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Các thuật toán xử lý ảnh vân tay số", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)

        # Total play = 2.5s. Target = 5.76s.
        self.wait(2.26)
        self.play(FadeOut(group), run_time=1.0)
        self.wait(0.8)

    def orientation_and_frequency(self):
        """Trường hướng & Trường tần số — Segment 2 = 13.25s."""
        section = self.get_section_hdr("Trường hướng & Trường tần số")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Trực quan hóa trường hướng (Trái)
        orient_label = self.ct("Trường hướng (Orientation Field)", font_size=18, color=CHART_BLUE, weight=BOLD)
        field = create_orientation_field(rows=7, cols=9, width=4.5, height=3.2)
        field_box = create_rounded_box(width=5.0, height=3.6, fill_color=CHART_BLUE, fill_opacity=0.05, stroke_color=CHART_BLUE, stroke_width=1.5)
        field.move_to(field_box)
        orient_label.next_to(field_box, UP, buff=0.25)
        orient_group = VGroup(field_box, field, orient_label).shift(LEFT * 3 + DOWN * 0.2)

        formula_part = MathTex(r"\theta(x, y)", font_size=26, color=PRIMARY)
        text_part = self.ct("= hướng cục bộ của đường vân", font_size=14, color=TEXT_DIM)
        orient_formula = VGroup(formula_part, text_part).arrange(RIGHT, buff=0.1).next_to(field_box, DOWN, buff=0.4)
        orient_desc = self.ct("Tính bằng gradient cường độ pixel", font_size=13, color=TEXT_DIM).next_to(orient_formula, DOWN, buff=0.15)

        # Trực quan hóa trường tần số (Phải)
        freq_label = self.ct("Trường tần số (Ridge Frequency)", font_size=18, color=CHART_ORANGE, weight=BOLD)
        freq_ridges = VGroup()
        for i in range(12):
            x = (i - 5.5) * 0.28
            freq_ridges.add(Line(UP * 1.2 + RIGHT * x, DOWN * 1.2 + RIGHT * x, color=RIDGE_COLOR, stroke_width=3))
        freq_box = create_rounded_box(width=5.0, height=3.6, fill_color=CHART_ORANGE, fill_opacity=0.05, stroke_color=CHART_ORANGE, stroke_width=1.5)
        freq_ridges.move_to(freq_box)
        freq_label.next_to(freq_box, UP, buff=0.25)
        freq_group = VGroup(freq_box, freq_ridges, freq_label).shift(RIGHT * 3 + DOWN * 0.2)

        brace = Brace(freq_ridges[4:7], DOWN, color=CHART_ORANGE, buff=0.1)
        spacing_label = self.ct("Khoảng cách d", font_size=13, color=CHART_ORANGE).next_to(brace, DOWN, buff=0.1)

        formula_part_f = MathTex(r"f(x, y) = 1 / d", font_size=26, color=PRIMARY)
        text_part_f = self.ct("= tần số đường vân cục bộ", font_size=14, color=TEXT_DIM)
        freq_formula = VGroup(formula_part_f, text_part_f).arrange(RIGHT, buff=0.1).next_to(freq_box, DOWN, buff=0.4)

        self.play(FadeIn(orient_label), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(seg, scale=0) for seg in field], lag_ratio=0.01),
            run_time=1.5,
        )
        self.play(FadeIn(orient_formula), FadeIn(orient_desc), run_time=0.8)
        
        self.play(FadeIn(freq_label), run_time=0.5)
        self.play(
            LaggedStart(*[Create(r) for r in freq_ridges], lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(GrowFromCenter(brace), FadeIn(spacing_label), run_time=0.8)
        self.play(FadeIn(freq_formula), run_time=0.8)

        # Target = 13.25s. Anim play = 0.6 + 0.5 + 1.5 + 0.8 + 0.5 + 1.0 + 0.8 + 0.8 = 6.5s. FadeOut = 1.0s. Need 5.75s wait.
        self.wait(5.75)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    def segmentation_and_singularities(self):
        """Phân vùng & Phát hiện vùng kỳ dị — Segment 3 = 17.59s."""
        section = self.get_section_hdr("Phân vùng & Vùng Kỳ dị")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Left box: Segmentation
        seg_box = create_rounded_box(
            width=5.0, height=3.5,
            fill_color=SECONDARY, fill_opacity=0.2,
            stroke_color=CHART_ORANGE, stroke_width=1.5,
        )
        seg_title = self.ct("Phân vùng (Segmentation)", font_size=18, color=CHART_ORANGE, weight=BOLD)
        
        # Simple fingerprint outline inside seg_box
        outline = Circle(radius=0.9, color=TEXT_DIM, stroke_width=1.5).set_opacity(0.4)
        active_area = Circle(radius=0.9, color=CHART_ORANGE, fill_color=CHART_ORANGE, fill_opacity=0.15, stroke_width=2.5)
        bg_label = self.ct("Nền nhiễu (Background)", font_size=12, color=TEXT_DIM).move_to(DOWN*0.9)
        fg_label = self.ct("Vân tay (Foreground)", font_size=12, color=CHART_ORANGE).move_to(ORIGIN)
        seg_vis = VGroup(outline, active_area, bg_label, fg_label).scale(0.8).move_to(DOWN*0.2)

        seg_content = VGroup(seg_title, seg_vis).arrange(DOWN, buff=0.3)
        seg_content.move_to(seg_box)
        seg_group = VGroup(seg_box, seg_content)

        # Right box: Poincaré Index
        poincare_box = create_rounded_box(
            width=5.0, height=3.5,
            fill_color=SECONDARY, fill_opacity=0.3,
            stroke_color=CHART_BLUE, stroke_width=1.5,
        )
        poincare_title = self.ct("Chỉ số Poincaré", font_size=18, color=CHART_BLUE, weight=BOLD)
        
        formula = MathTex(
            r"P(C) = \frac{1}{2\pi} \oint_C d\theta",
            font_size=26, color=TEXT_BRIGHT,
        )
        
        results = VGroup(
            self.ct("Loop / Core: P(C) = 180° (π)", font_size=13, color=CHART_BLUE),
            self.ct("Delta: P(C) = -180° (-π)", font_size=13, color=DELTA_COLOR),
            self.ct("Whorl: P(C) = 360° (2π)", font_size=13, color=CHART_PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        
        poincare_content = VGroup(poincare_title, formula, results).arrange(DOWN, buff=0.35)
        poincare_content.move_to(poincare_box)
        poincare_group = VGroup(poincare_box, poincare_content)

        both = VGroup(seg_group, poincare_group).arrange(RIGHT, buff=0.8).shift(DOWN * 0.3)

        self.play(FadeIn(seg_group, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(3.0)
        self.play(FadeIn(poincare_group, shift=LEFT * 0.3), run_time=0.8)

        # Target = 17.59s. Anim play so far = 0.6 + 0.8 + 3.0 + 0.8 = 5.2s. FadeOut = 1.0s. Need 11.39s wait.
        self.wait(11.39)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    def enhancement_pipeline(self):
        """Hiển thị pipeline: tăng cường → nhị phân → thinning — Segment 4 = 17.21s."""
        section = self.get_section_hdr("Quy trình xử lý ảnh")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        stages = [
            ("Ảnh xám", TEXT_DIM, self._create_grayscale_sim()),
            ("Ảnh tăng cường", RIDGE_COLOR, self._create_enhanced_sim()),
            ("Ảnh nhị phân", CHART_BLUE, self._create_binary_sim()),
            ("Ảnh xương", CORE_POINT, self._create_thinned_sim()),
        ]

        stage_groups = VGroup()
        for title_text, color, content in stages:
            box = create_rounded_box(
                width=2.6, height=2.6,
                fill_color=color, fill_opacity=0.05,
                stroke_color=color, stroke_width=1.5,
            )
            label = self.ct(title_text, font_size=14, color=color, weight=BOLD)
            label.next_to(box, DOWN, buff=0.2)
            content.move_to(box).scale(0.8)
            stage_groups.add(VGroup(box, content, label))

        stage_groups.arrange(RIGHT, buff=0.7).shift(DOWN * 0.3)

        arrows = VGroup()
        for i in range(len(stage_groups) - 1):
            arrow = Arrow(
                stage_groups[i][0].get_right(), stage_groups[i + 1][0].get_left(),
                color=PRIMARY, buff=0.1, stroke_width=2,
                max_tip_length_to_length_ratio=0.25,
            )
            arrows.add(arrow)

        filter_desc = self.ct(
            "Tăng cường: Bộ lọc Gabor ngữ cảnh tự thích ứng theo θ và f",
            font_size=16, color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.5)

        # Scanning Line Reveal Effect (Premium visual transition)
        scan_bar = Line(UP * 2.2, DOWN * 2.2, color=PRIMARY, stroke_width=3).set_opacity(0.8)
        scan_bar.move_to(LEFT * 6.0)
        self.play(FadeIn(scan_bar, run_time=0.4))

        for i, sg in enumerate(stage_groups):
            card_center = sg.get_center()
            self.play(
                scan_bar.animate.move_to([card_center[0], 0, 0]),
                FadeIn(sg, shift=UP * 0.3),
                run_time=0.8
            )
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.3)

        self.play(FadeOut(scan_bar, run_time=0.4))
        self.play(FadeIn(filter_desc, shift=UP * 0.2), run_time=0.8)

        # Target = 17.21s. Anim play = 0.6 + 0.4 + 4*0.8 + 3*0.3 + 0.4 + 0.8 = 6.3s. FadeOut = 1.0s. Need 9.91s wait.
        self.wait(9.91)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    def crossing_number_extraction(self):
        """Thuật toán Crossing Number (CN) — Segment 5 = 13.66s."""
        section = self.get_section_hdr("Thuật toán Crossing Number (CN)")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        formula = MathTex(
            r"\text{CN}(P) = \frac{1}{2} \sum_{i=1}^{8} |P_i - P_{i+1}|",
            font_size=32, color=TEXT_BRIGHT,
        ).shift(LEFT * 3 + UP * 0.8)

        grid = create_crossing_number_grid(scale=1.5)
        grid.shift(RIGHT * 3 + UP * 0.2)
        grid_lbl = self.ct("Cửa sổ quét 3x3 pixel", font_size=15, color=TEXT_DIM).next_to(grid, DOWN, buff=0.3)

        # Giả lập điểm trung tâm P và 8 pixel lân cận
        p_center = Dot(grid[4].get_center(), color=PRIMARY, radius=0.1)
        p_label = MathTex(r"P", font_size=20, color=PRIMARY).next_to(p_center, UR, buff=0.05)

        # Minh họa P_i chạy xung quanh cửa sổ
        neighbors = VGroup()
        for idx in [1, 2, 5, 8, 7, 6, 3, 0]: # vòng tròn xung quanh
            dot = Dot(grid[idx].get_center(), color=CHART_BLUE, radius=0.08)
            neighbors.add(dot)

        cases = VGroup(
            self.ct("CN(P) = 1  →  Kết thúc (Termination)", font_size=15, color=MINUTIA_TERM),
            self.ct("CN(P) = 3  →  Phân nhánh (Bifurcation)", font_size=15, color=MINUTIA_BIFUR),
            self.ct("Khác 1 hoặc 3  →  Đường vân bình thường", font_size=14, color=TEXT_DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(LEFT * 3.2 + DOWN * 1.2)

        self.play(Write(formula), run_time=0.8)
        self.play(Create(grid), FadeIn(grid_lbl), run_time=1.0)
        self.play(FadeIn(p_center), FadeIn(p_label), run_time=0.5)
        
        # Cho chạy quét vòng tròn minh họa (Premium effect)
        self.play(
            LaggedStart(*[FadeIn(n, scale=1.5) for n in neighbors], lag_ratio=0.1),
            run_time=1.2,
        )
        self.play(FadeIn(cases), run_time=0.8)

        # Target = 13.66s. Anim play = 0.6 + 0.8 + 1.0 + 0.5 + 1.2 + 0.8 = 4.9s. FadeOut = 1.0s. Need 7.76s wait.
        self.wait(7.76)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)

    # ─── MÔ PHỎNG XỬ LÝ ẢNH ───────────────────────────────────────────────────

    def _create_grayscale_sim(self):
        """Tạo ảnh xám giả lập."""
        g = VGroup()
        for i in range(5):
            y = (i - 2) * 0.22
            g.add(Line(LEFT * 0.9 + UP * y, RIGHT * 0.9 + UP * y, color=TEXT_DIM, stroke_width=6).set_opacity(0.4))
        return g

    def _create_enhanced_sim(self):
        """Tạo ảnh tăng cường giả lập."""
        g = VGroup()
        for i in range(5):
            y = (i - 2) * 0.22
            g.add(Line(LEFT * 0.9 + UP * y, RIGHT * 0.9 + UP * y, color=TEXT_COLOR, stroke_width=6))
        return g

    def _create_binary_sim(self):
        """Tạo ảnh nhị phân giả lập."""
        g = VGroup()
        for i in range(5):
            y = (i - 2) * 0.22
            g.add(Line(LEFT * 0.9 + UP * y, RIGHT * 0.9 + UP * y, color=CHART_BLUE, stroke_width=4))
        return g

    def _create_thinned_sim(self):
        """Tạo ảnh thon hóa (xương) giả lập."""
        g = VGroup()
        for i in range(5):
            y = (i - 2) * 0.22
            g.add(Line(LEFT * 0.9 + UP * y, RIGHT * 0.9 + UP * y, color=CORE_POINT, stroke_width=1.5))
        return g
