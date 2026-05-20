"""
Scene 3: Tổng quan Trích xuất Đặc trưng (Không có giọng nói)
- Đường vân vs Rãnh (nhìn tổng thể)
- Vùng kỳ dị: Loop, Delta, Whorl
- Điểm core
- Minutiae: Kết thúc và Phân nhánh
"""
from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene03Features(Scene):
    def construct(self):
        scene_setup(self)
        self.section_title()
        self.singular_regions()
        self.minutiae_types()
        self.minutiae_representation()

    def section_title(self):
        """Tiêu đề mục."""
        num = Text("02", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = Text("Trích Xuất Đặc Trưng", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = Text(
            "Trích xuất các đặc trưng phân biệt từ ảnh vân tay",
            font_size=22, color=TEXT_DIM,
        )
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3))
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        self.wait(0.5)
        self.play(FadeOut(group))

    def singular_regions(self):
        """Hiển thị ba loại vùng kỳ dị: Loop, Delta, Whorl."""
        section = get_section_title("Vùng kỳ dị (Singular Regions)")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        intro_text = Text(
            "Ở mức tổng thể, các đường vân tạo thành các hình dạng đặc biệt",
            font_size=19, color=TEXT_COLOR,
        ).next_to(section, DOWN, buff=0.5)
        self.play(FadeIn(intro_text, shift=UP * 0.2))

        # Loop (∩)
        loop = create_loop_pattern(scale=0.9, color=RIDGE_COLOR)
        loop_box = create_rounded_box(
            width=3.2, height=3.2,
            fill_color=SECONDARY, fill_opacity=0.15,
            stroke_color=CHART_BLUE, stroke_width=1.5,
        )
        loop_label = Text("Vòng lặp (Loop)", font_size=18, color=CHART_BLUE, weight=BOLD)
        core_dot = Dot(loop.get_center() + UP * 0.2, color=CORE_POINT, radius=0.08)
        core_label = Text("core", font_size=12, color=CORE_POINT)
        core_label.next_to(core_dot, UR, buff=0.1)
        loop_content = VGroup(loop, core_dot, core_label)
        loop_content.move_to(loop_box)
        loop_label.next_to(loop_box, DOWN, buff=0.2)
        loop_group = VGroup(loop_box, loop_content, loop_label)

        # Delta (∆)
        delta = create_delta_pattern(scale=0.9, color=RIDGE_COLOR)
        delta_box = create_rounded_box(
            width=3.2, height=3.2,
            fill_color=SECONDARY, fill_opacity=0.15,
            stroke_color=DELTA_COLOR, stroke_width=1.5,
        )
        delta_label = Text("Tam giác (Delta)", font_size=18, color=DELTA_COLOR, weight=BOLD)
        delta.move_to(delta_box)
        delta_label.next_to(delta_box, DOWN, buff=0.2)
        delta_group = VGroup(delta_box, delta, delta_label)

        # Whorl (O)
        whorl = create_whorl_pattern(scale=0.9, color=RIDGE_COLOR)
        whorl_box = create_rounded_box(
            width=3.2, height=3.2,
            fill_color=SECONDARY, fill_opacity=0.15,
            stroke_color=CHART_PURPLE, stroke_width=1.5,
        )
        whorl_label = Text("Xoáy (Whorl)", font_size=18, color=CHART_PURPLE, weight=BOLD)
        whorl.move_to(whorl_box)
        whorl_label.next_to(whorl_box, DOWN, buff=0.2)
        whorl_group = VGroup(whorl_box, whorl, whorl_label)

        all_singular = VGroup(loop_group, delta_group, whorl_group)
        all_singular.arrange(RIGHT, buff=0.6).shift(DOWN * 0.5)

        for sg in [loop_group, delta_group, whorl_group]:
            self.play(FadeIn(sg, shift=UP * 0.4, scale=0.9), run_time=0.8)
            self.wait(0.5)
        self.play(
            core_dot.animate.scale(2),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.wait(1)
        self.play(FadeOut(VGroup(section, intro_text, all_singular)))

    def minutiae_types(self):
        """Hiển thị chi tiết minutiae: kết thúc và phân nhánh."""
        section = get_section_title("Minutiae: Đặc trưng cục bộ")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        definition = Text(
            "Minutiae = các điểm mà đường vân bị gián đoạn",
            font_size=20, color=TEXT_COLOR,
        ).next_to(section, DOWN, buff=0.5)
        self.play(FadeIn(definition, shift=UP * 0.2))

        # KẾT THÚC (Termination)
        term_title = Text("Kết thúc (Termination)", font_size=22, color=MINUTIA_TERM, weight=BOLD)
        term_ridges = VGroup()
        for i in range(5):
            y = (i - 2) * 0.35
            length = 4 if i != 2 else 2.5
            ridge = Line(
                LEFT * 2.5 + UP * y,
                LEFT * 2.5 + RIGHT * length + UP * y,
                color=RIDGE_COLOR, stroke_width=4,
            )
            term_ridges.add(ridge)

        term_point = Dot(term_ridges[2].get_end(), color=MINUTIA_TERM, radius=0.1)
        term_glow = Circle(radius=0.25, color=MINUTIA_TERM, stroke_width=2).move_to(term_point)
        term_desc = Text("Đường vân đột ngột\nkết thúc", font_size=15, color=TEXT_DIM)
        term_content = VGroup(term_ridges, term_point, term_glow)
        term_group = VGroup(term_title, term_content, term_desc).arrange(DOWN, buff=0.3)

        # PHÂN NHÁNH (Bifurcation)
        bifur_title = Text("Phân nhánh (Bifurcation)", font_size=22, color=MINUTIA_BIFUR, weight=BOLD)
        bifur_ridges = VGroup()
        for i in range(5):
            y = (i - 2) * 0.35
            if i == 2:
                main = Line(LEFT * 2.5 + UP * y, RIGHT * 0 + UP * y, color=RIDGE_COLOR, stroke_width=4)
                branch1 = Line(RIGHT * 0 + UP * y, RIGHT * 2 + UP * (y + 0.25), color=RIDGE_COLOR, stroke_width=4)
                branch2 = Line(RIGHT * 0 + UP * y, RIGHT * 2 + UP * (y - 0.25), color=RIDGE_COLOR, stroke_width=4)
                bifur_ridges.add(main, branch1, branch2)
            elif i == 1:
                continue
            else:
                ridge = Line(LEFT * 2.5 + UP * y, RIGHT * 2 + UP * y, color=RIDGE_COLOR, stroke_width=4)
                bifur_ridges.add(ridge)

        bifur_point = Dot(ORIGIN, color=MINUTIA_BIFUR, radius=0.1)
        bifur_glow = Circle(radius=0.25, color=MINUTIA_BIFUR, stroke_width=2).move_to(bifur_point)
        bifur_desc = Text("Đường vân tách\nthành hai nhánh", font_size=15, color=TEXT_DIM)
        bifur_content = VGroup(bifur_ridges, bifur_point, bifur_glow)
        bifur_group = VGroup(bifur_title, bifur_content, bifur_desc).arrange(DOWN, buff=0.3)

        both = VGroup(term_group, bifur_group).arrange(RIGHT, buff=1.5).shift(DOWN * 0.3)
        divider = DashedLine(
            UP * 2 + both.get_center()[0] * RIGHT,
            DOWN * 2.5 + both.get_center()[0] * RIGHT,
            color=TEXT_DIM, stroke_width=1,
        )

        self.play(FadeIn(term_title))
        self.play(
            LaggedStart(*[Create(r) for r in term_ridges], lag_ratio=0.1),
            run_time=1,
        )
        self.play(FadeIn(term_point, scale=2), Create(term_glow), FadeIn(term_desc))
        self.play(Create(divider), run_time=0.3)
        self.play(FadeIn(bifur_title))
        self.play(
            LaggedStart(*[Create(r) for r in bifur_ridges], lag_ratio=0.1),
            run_time=1,
        )
        self.play(FadeIn(bifur_point, scale=2), Create(bifur_glow), FadeIn(bifur_desc))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def minutiae_representation(self):
        """Hiển thị cách biểu diễn minutiae: m = {x, y, θ}."""
        section = get_section_title("Biểu diễn Minutiae")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 5, 1],
            x_length=5, y_length=4,
            axis_config={"color": TEXT_DIM, "stroke_width": 1.5, "include_numbers": True, "font_size": 16},
        ).shift(LEFT * 2 + DOWN * 0.3)
        axes_labels = axes.get_axis_labels(
            x_label=Text("x", font_size=18, color=TEXT_DIM),
            y_label=Text("y", font_size=18, color=TEXT_DIM),
        )

        self.play(Create(axes), FadeIn(axes_labels))

        minutiae_data = [
            (2, 3, PI / 4, "termination"),
            (4, 4, PI / 6, "bifurcation"),
            (3, 1.5, PI * 3 / 4, "termination"),
            (5, 2.5, -PI / 3, "bifurcation"),
            (1, 1, PI / 2, "termination"),
        ]

        points = VGroup()
        for x, y, theta, mtype in minutiae_data:
            pos = axes.c2p(x, y)
            point = create_minutia_point(pos, minutia_type=mtype, angle=theta, scale=1.2)
            points.add(point)

        formula = MathTex(r"m = \{x, y, \theta\}", font_size=42, color=TEXT_BRIGHT).shift(RIGHT * 3.5 + UP * 1)
        desc = VGroup(
            MathTex(r"(x, y)", font_size=24, color=RIDGE_COLOR),
            Text(" = tọa độ vị trí", font_size=20, color=TEXT_DIM),
        ).arrange(RIGHT, buff=0.1)
        desc2 = VGroup(
            MathTex(r"\theta", font_size=24, color=MINUTIA_BIFUR),
            Text(" = góc đường vân", font_size=20, color=TEXT_DIM),
        ).arrange(RIGHT, buff=0.1)
        descs = VGroup(desc, desc2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        descs.next_to(formula, DOWN, buff=0.5)

        legend = VGroup(
            VGroup(Dot(color=MINUTIA_TERM, radius=0.06), Text("Kết thúc", font_size=14, color=MINUTIA_TERM)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=MINUTIA_BIFUR, radius=0.06), Text("Phân nhánh", font_size=14, color=MINUTIA_BIFUR)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(descs, DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(p, scale=2) for p in points], lag_ratio=0.15),
            run_time=1.5,
        )
        self.play(Write(formula))
        self.play(FadeIn(descs))
        self.play(FadeIn(legend))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))
