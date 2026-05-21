"""
Scene 3: Đặc trưng vân tay (Fingerprint Features)
- Định nghĩa Singularities (Loop, Delta, Whorl) + Hiệu ứng vòng xung
- Định nghĩa Minutiae (Termination, Bifurcation) + Radar ping
- Biểu diễn toán học m = {x, y, θ} + Quét lưới tọa độ
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
        self.singularities()
        self.minutiae_types()
        self.minutiae_representation()

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
        """Tiêu đề mục — Segment 1 = 11.23s."""
        num = self.ct("02", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Đặc Trưng Vân Tay", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Từ hình dạng vĩ mô đến chi tiết vi mô cục bộ", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)

        # Total anim play = 2.5s. Target 11.23s before FadeOut completes.
        self.wait(7.73)
        self.play(FadeOut(group), run_time=1.0)
        self.wait(0.8) # Silence gap

    def singularities(self):
        """Singularities (Loop, Delta, Whorl) — Segment 2 = 16.54s."""
        section = self.get_section_hdr("Điểm đặc biệt hệ thống (Singularities)")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        intro = self.ct("Mức toàn cục: Mật độ đường vân tạo ra ba cấu trúc kỳ dị chính", font_size=16, color=TEXT_COLOR)
        intro.next_to(section, DOWN, buff=0.3)
        self.play(FadeIn(intro), run_time=0.6)

        # ── 1. Loop (Móc) ──
        loop_box = create_rounded_box(width=3.4, height=3.4, fill_color=CHART_BLUE, fill_opacity=0.08, stroke_color=CHART_BLUE, stroke_width=1.5)
        loop = create_loop_pattern(scale=1.5, color=RIDGE_COLOR, stroke_width=3).move_to(loop_box.get_center())
        loop_lbl = self.ct("Loop (Móc) - ∩ shape", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        
        # Core marker
        core_dot = Dot(loop.get_center() + UP * 0.1 * 1.5, color=CORE_POINT, radius=0.08 * 1.5)
        core_lbl = self.ct("Core", font_size=12, color=CORE_POINT, weight=BOLD).next_to(core_dot, UP, buff=0.1)
        loop_group = VGroup(loop_box, loop, core_dot, core_lbl, loop_lbl)

        # ── 2. Delta (Tam sa) ──
        delta_box = create_rounded_box(width=3.4, height=3.4, fill_color=CHART_ORANGE, fill_opacity=0.08, stroke_color=CHART_ORANGE, stroke_width=1.5)
        delta = create_delta_pattern(scale=1.5, color=RIDGE_COLOR, stroke_width=3).move_to(delta_box.get_center())
        delta_lbl_name = self.ct("Delta (Tam sa) - ∆ shape", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        
        # Delta marker
        delta_dot = Dot(delta.get_center() + DOWN * 0.1 * 1.5, color=DELTA_COLOR, radius=0.08 * 1.5)
        delta_lbl = self.ct("Delta", font_size=12, color=DELTA_COLOR, weight=BOLD).next_to(delta_dot, DOWN, buff=0.1)
        delta_group = VGroup(delta_box, delta, delta_dot, delta_lbl, delta_lbl_name)

        # ── 3. Whorl (Xoáy) ──
        whorl_box = create_rounded_box(width=3.4, height=3.4, fill_color=CHART_PURPLE, fill_opacity=0.08, stroke_color=CHART_PURPLE, stroke_width=1.5)
        whorl = create_whorl_pattern(scale=1.5, color=RIDGE_COLOR, stroke_width=3).move_to(whorl_box.get_center())
        whorl_lbl = self.ct("Whorl (Xoáy) - O shape", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        
        # Whorl center marker
        whorl_dot = Dot(whorl.get_center(), color=CORE_POINT, radius=0.08 * 1.5)
        whorl_lbl_node = self.ct("Core (Tâm)", font_size=12, color=CORE_POINT, weight=BOLD).next_to(whorl_dot, UP, buff=0.1)
        whorl_group = VGroup(whorl_box, whorl, whorl_dot, whorl_lbl_node, whorl_lbl)

        all_singular = VGroup(loop_group, delta_group, whorl_group)
        all_singular.arrange(RIGHT, buff=0.6).shift(DOWN * 0.55)

        # Pulse circle helper
        pulse_anims = []
        pulses = []
        for sg, dot, color in [(loop_group, core_dot, CORE_POINT), (delta_group, delta_dot, DELTA_COLOR), (whorl_group, whorl_dot, CORE_POINT)]:
            self.play(FadeIn(sg, shift=UP * 0.4, scale=0.9), run_time=0.8)
            pulse1 = Circle(radius=0.05, color=color, stroke_width=2).move_to(dot.get_center())
            pulse2 = Circle(radius=0.05, color=color, stroke_width=2).move_to(dot.get_center())
            self.add(pulse1, pulse2)
            pulses.extend([pulse1, pulse2])
            pulse_anims.append(
                LaggedStart(
                    pulse1.animate.scale(6).set_stroke(opacity=0),
                    pulse2.animate.scale(6).set_stroke(opacity=0),
                    lag_ratio=0.3
                )
            )

        # Trigger all pulse waves (Premium visual highlight)
        self.play(*pulse_anims, run_time=1.0)
        self.remove(*pulses)
        
        self.play(core_dot.animate.scale(2.5), rate_func=there_and_back, run_time=0.7)

        # Target = 16.54s. Anim so far = 0.6 + 0.6 + 3*0.8 + 1.0 + 0.7 = 5.3s. FadeOut = 0.7s. Need 10.54s wait.
        self.wait(10.54)
        self.play(FadeOut(VGroup(section, intro, all_singular)), run_time=0.7)
        self.wait(0.8)

    def minutiae_types(self):
        """Minutiae Termination & Bifurcation — Segment 3 = 14.35s."""
        section = self.get_section_hdr("Minutiae: Đặc trưng cục bộ")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        definition = self.ct("Minutiae = các điểm mà đường vân bị gián đoạn", font_size=20, color=TEXT_COLOR)
        definition.next_to(section, DOWN, buff=0.45)
        self.play(FadeIn(definition, shift=UP * 0.2), run_time=0.6)

        # ── Kết thúc (Termination) ──
        term_title = self.ct("Kết thúc (Termination)", font_size=22, color=MINUTIA_TERM, weight=BOLD)
        term_ridges = VGroup()
        for i in range(5):
            y = (i - 2) * 0.35
            length = 4.0 if i != 2 else 2.5
            ridge = Line(
                LEFT * 2.5 + UP * y,
                LEFT * 2.5 + RIGHT * length + UP * y,
                color=RIDGE_COLOR, stroke_width=4,
            )
            term_ridges.add(ridge)

        term_point = Dot(term_ridges[2].get_end(), color=MINUTIA_TERM, radius=0.1)
        term_desc = self.ct("Đường vân đột ngột kết thúc", font_size=15, color=TEXT_DIM)
        term_content = VGroup(term_ridges, term_point)
        term_group = VGroup(term_title, term_content, term_desc).arrange(DOWN, buff=0.3)

        # ── Phân nhánh (Bifurcation) ──
        bifur_title = self.ct("Phân nhánh (Bifurcation)", font_size=22, color=MINUTIA_BIFUR, weight=BOLD)
        bifur_ridges = VGroup()
        for i in range(5):
            y = (i - 2) * 0.35
            if i == 2:
                main   = Line(LEFT * 2.5 + UP * y, RIGHT * 0 + UP * y, color=RIDGE_COLOR, stroke_width=4)
                branch1 = Line(RIGHT * 0 + UP * y, RIGHT * 2 + UP * (y + 0.25), color=RIDGE_COLOR, stroke_width=4)
                branch2 = Line(RIGHT * 0 + UP * y, RIGHT * 2 + UP * (y - 0.25), color=RIDGE_COLOR, stroke_width=4)
                bifur_ridges.add(main, branch1, branch2)
            elif i == 1:
                continue
            else:
                bifur_ridges.add(Line(LEFT * 2.5 + UP * y, RIGHT * 2 + UP * y, color=RIDGE_COLOR, stroke_width=4))

        bifur_point = Dot(ORIGIN, color=MINUTIA_BIFUR, radius=0.1)
        bifur_desc  = self.ct("Đường vân tách thành hai nhánh", font_size=15, color=TEXT_DIM)
        bifur_content = VGroup(bifur_ridges, bifur_point)
        bifur_group = VGroup(bifur_title, bifur_content, bifur_desc).arrange(DOWN, buff=0.3)

        both = VGroup(term_group, bifur_group).arrange(RIGHT, buff=1.5).shift(DOWN * 0.3)
        divider = DashedLine(
            UP * 2.2 + ORIGIN,
            DOWN * 2.5 + ORIGIN,
            color=TEXT_DIM, stroke_width=1,
        ).move_to([both.get_center()[0], 0, 0])

        # ── Animations ──
        self.play(FadeIn(term_title), run_time=0.5)
        self.play(
            LaggedStart(*[Create(r) for r in term_ridges], lag_ratio=0.1),
            run_time=1.0,
        )
        self.play(FadeIn(term_point, scale=2), FadeIn(term_desc), run_time=0.7)
        
        # Pulse Ping effect (Premium radar scan style)
        pulse_term = Circle(radius=0.05, color=MINUTIA_TERM, stroke_width=2.5).move_to(term_point.get_center())
        self.add(pulse_term)
        self.play(pulse_term.animate.scale(6).set_stroke(opacity=0), run_time=0.6)
        self.remove(pulse_term)

        self.play(Create(divider), run_time=0.4)
        self.play(FadeIn(bifur_title), run_time=0.5)
        self.play(
            LaggedStart(*[Create(r) for r in bifur_ridges], lag_ratio=0.1),
            run_time=1.0,
        )
        self.play(FadeIn(bifur_point, scale=2), FadeIn(bifur_desc), run_time=0.7)

        # Pulse Ping effect
        pulse_bifur = Circle(radius=0.05, color=MINUTIA_BIFUR, stroke_width=2.5).move_to(bifur_point.get_center())
        self.add(pulse_bifur)
        self.play(pulse_bifur.animate.scale(6).set_stroke(opacity=0), run_time=0.6)
        self.remove(pulse_bifur)

        # Target = 14.35s. Anim play = 0.6 + 0.6 + 0.5 + 1.0 + 0.7 + 0.6 + 0.4 + 0.5 + 1.0 + 0.7 + 0.6 = 7.2s. FadeOut = 0.8s. Need 6.35s wait.
        self.wait(6.35)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.8)

    def minutiae_representation(self):
        """Biểu diễn toán học m = {x, y, θ} — Segment 4 = 10.61s."""
        section = self.get_section_hdr("Biểu diễn Minutiae")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Trục tọa độ
        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 5, 1],
            x_length=5, y_length=4,
            axis_config={
                "color": TEXT_DIM, "stroke_width": 1.5,
                "include_numbers": True, "font_size": 16,
            },
        ).shift(LEFT * 2 + DOWN * 0.3)
        axes_labels = axes.get_axis_labels(
            x_label=Text("x", font_size=18, color=TEXT_DIM),
            y_label=Text("y", font_size=18, color=TEXT_DIM),
        )
        self.play(Create(axes), FadeIn(axes_labels), run_time=1.0)

        # Các điểm minutiae trên trục
        minutiae_data = [
            (2,   3,    PI / 4,      "termination"),
            (4,   4,    PI / 6,      "bifurcation"),
            (3,   1.5,  PI * 3 / 4,  "termination"),
            (5,   2.5, -PI / 3,      "bifurcation"),
            (1,   1,    PI / 2,      "termination"),
        ]
        points = VGroup()
        for x, y, theta, mtype in minutiae_data:
            pos = axes.c2p(x, y)
            points.add(create_minutia_point(pos, minutia_type=mtype, angle=theta, scale=1.2))

        self.play(
            LaggedStart(*[FadeIn(p, scale=2) for p in points], lag_ratio=0.18),
            run_time=1.5,
        )

        # Laser Scan effect on grid (Premium visual)
        scan_line = Line(axes.get_left() + UP * 2.0, axes.get_right() + UP * 2.0, color=PRIMARY, stroke_width=2.5).set_opacity(0.8)
        self.add(scan_line)
        self.play(scan_line.animate.move_to(axes.get_center() + DOWN * 2.0), run_time=1.2, rate_func=smooth)
        self.play(FadeOut(scan_line), run_time=0.3)

        # Công thức và mô tả — bên phải
        formula = MathTex(r"m = \{x,\; y,\; \theta\}", font_size=42, color=TEXT_BRIGHT)
        formula.shift(RIGHT * 3.5 + UP * 1.2)
        self.play(Write(formula), run_time=0.8)

        desc_xy = VGroup(
            MathTex(r"(x,\, y)", font_size=24, color=RIDGE_COLOR),
            self.ct("= tọa độ vị trí", font_size=18, color=TEXT_DIM),
        ).arrange(RIGHT, buff=0.12)
        desc_th = VGroup(
            MathTex(r"\theta", font_size=24, color=MINUTIA_BIFUR),
            self.ct("= góc hướng vân", font_size=18, color=TEXT_DIM),
        ).arrange(RIGHT, buff=0.12)
        descs = VGroup(desc_xy, desc_th).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        descs.next_to(formula, DOWN, buff=0.5)
        self.play(FadeIn(descs, shift=UP * 0.2), run_time=0.7)

        # Chú thích màu (legend)
        legend = VGroup(
            VGroup(
                Dot(color=MINUTIA_TERM, radius=0.07),
                self.ct("Kết thúc (Termination)", font_size=14, color=MINUTIA_TERM),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Dot(color=MINUTIA_BIFUR, radius=0.07),
                self.ct("Phân nhánh (Bifurcation)", font_size=14, color=MINUTIA_BIFUR),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.next_to(descs, DOWN, buff=0.5)
        self.play(FadeIn(legend), run_time=0.6)

        # Target = 10.61s. Anim play = 0.6 + 1.0 + 1.5 + 1.2 + 0.3 + 0.8 + 0.7 + 0.6 = 6.7s. FadeOut = 0.8s. Need 3.11s wait.
        self.wait(3.11)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
