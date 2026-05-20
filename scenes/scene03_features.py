"""
Scene 3: Trích xuất Đặc trưng (Feature Extraction)
- Tiêu đề mục
- Vùng kỳ dị: Loop, Delta, Whorl
- Minutiae: Kết thúc và Phân nhánh
- Biểu diễn toán học: m = {x, y, θ}

Audio timings (voice_scene03.mp3):
  seg_01 =  5.93s  → section_title()
  seg_02 =  9.05s  → singular_regions()
  seg_03 = 11.95s  → minutiae_types()
  seg_04 = 11.11s  → minutiae_representation()
  pauses =  0.80s x3 between segments
  Total  = 40.44s
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

    # ─── helpers ────────────────────────────────────────────────────────────

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kw):
        """create_text with CMU Serif kerning workaround (render big → scale down)."""
        return Text(text_str, font_size=36, color=color, weight=weight, **kw).scale(font_size / 36)

    def get_section_hdr(self, text):
        title = Text(text, font_size=36, color=TEXT_BRIGHT, weight=BOLD)
        underline = Line(
            title.get_left() + DOWN * 0.3,
            title.get_right() + DOWN * 0.3,
            color=PRIMARY, stroke_width=3,
        )
        return VGroup(title, underline)

    # ─── seg_01  (5.93s) ────────────────────────────────────────────────────

    def section_title(self):
        """Tiêu đề mục — seg_01 = 5.93s."""
        num = Text("02", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Trích Xuất Đặc Trưng", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct(
            "Trích xuất các đặc trưng phân biệt từ ảnh vân tay",
            font_size=22, color=TEXT_DIM,
        )
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.7)

        # seg_01 = 5.93s; anim above ≈ 2.0s → wait 3.13s then 0.8s pause handled by FadeOut gap
        self.wait(3.53)         # → 6.03s elapsed  (+0.9s)
        self.play(FadeOut(group), run_time=0.8)  # → 5.93s ✓

    # ─── seg_02  (9.05s) + 0.8s pause ──────────────────────────────────────

    def singular_regions(self):
        """Hiển thị ba loại vùng kỳ dị — seg_02 = 9.05s."""
        section = self.get_section_hdr("Vùng kỳ dị (Singular Regions)")
        section.to_edge(UP, buff=0.6)

        intro = self.ct(
            "Ở mức tổng thể, các đường vân tạo thành các hình dạng đặc biệt",
            font_size=19, color=TEXT_COLOR,
        ).next_to(section, DOWN, buff=0.45)

        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)  # 0.6s
        self.play(FadeIn(intro, shift=UP * 0.2), run_time=0.6)       # 1.2s total

        # ── Loop ──
        loop = create_loop_pattern(scale=0.9, color=RIDGE_COLOR)
        loop_box = create_rounded_box(
            width=3.2, height=3.2,
            fill_color=SECONDARY, fill_opacity=0.15,
            stroke_color=CHART_BLUE, stroke_width=1.5,
        )
        core_dot = Dot(loop.get_center() + UP * 0.2, color=CORE_POINT, radius=0.09)
        core_label = self.ct("core", font_size=12, color=CORE_POINT).next_to(core_dot, UR, buff=0.1)
        loop_content = VGroup(loop, core_dot, core_label)
        loop_content.move_to(loop_box)
        loop_lbl = self.ct("Vòng lặp (Loop)", font_size=18, color=CHART_BLUE, weight=BOLD)
        loop_lbl.next_to(loop_box, DOWN, buff=0.2)
        loop_group = VGroup(loop_box, loop_content, loop_lbl)

        # ── Delta ──
        delta = create_delta_pattern(scale=0.9, color=RIDGE_COLOR)
        delta_box = create_rounded_box(
            width=3.2, height=3.2,
            fill_color=SECONDARY, fill_opacity=0.15,
            stroke_color=DELTA_COLOR, stroke_width=1.5,
        )
        delta_lbl = self.ct("Tam giác (Delta)", font_size=18, color=DELTA_COLOR, weight=BOLD)
        delta.move_to(delta_box)
        delta_lbl.next_to(delta_box, DOWN, buff=0.2)
        delta_group = VGroup(delta_box, delta, delta_lbl)

        # ── Whorl ──
        whorl = create_whorl_pattern(scale=0.9, color=RIDGE_COLOR)
        whorl_box = create_rounded_box(
            width=3.2, height=3.2,
            fill_color=SECONDARY, fill_opacity=0.15,
            stroke_color=CHART_PURPLE, stroke_width=1.5,
        )
        whorl_lbl = self.ct("Xoáy (Whorl)", font_size=18, color=CHART_PURPLE, weight=BOLD)
        whorl.move_to(whorl_box)
        whorl_lbl.next_to(whorl_box, DOWN, buff=0.2)
        whorl_group = VGroup(whorl_box, whorl, whorl_lbl)

        all_singular = VGroup(loop_group, delta_group, whorl_group)
        all_singular.arrange(RIGHT, buff=0.6).shift(DOWN * 0.55)

        # Hiện từng card ~ 0.8s/card, chờ 0.4s rồi sang card tiếp
        for sg in [loop_group, delta_group, whorl_group]:
            self.play(FadeIn(sg, shift=UP * 0.4, scale=0.9), run_time=0.8)
            self.wait(0.35)
        # Pulse core dot để nhấn mạnh
        self.play(core_dot.animate.scale(2.5), rate_func=there_and_back, run_time=0.7)

        # Tổng elapsed đến đây ≈ 1.2 + 3*1.15 + 0.7 = 5.35s → cần đủ 9.05s
        self.wait(3.8)   # → ~9.95s  (+0.9s to close gap)

        self.play(FadeOut(VGroup(section, intro, all_singular)), run_time=0.7)
        self.wait(0.8)   # khoảng lặng 0.8s trước seg_03

    # ─── seg_03  (11.95s) + 0.8s pause ─────────────────────────────────────

    def minutiae_types(self):
        """Minutiae Termination & Bifurcation — seg_03 = 11.95s."""
        section = self.get_section_hdr("Minutiae: Đặc trưng cục bộ")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)  # 0.6s

        definition = self.ct(
            "Minutiae = các điểm mà đường vân bị gián đoạn",
            font_size=20, color=TEXT_COLOR,
        ).next_to(section, DOWN, buff=0.45)
        self.play(FadeIn(definition, shift=UP * 0.2), run_time=0.6)  # 1.2s

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
        term_glow = Circle(radius=0.25, color=MINUTIA_TERM, stroke_width=2).move_to(term_point)
        term_desc = self.ct("Đường vân đột ngột kết thúc", font_size=15, color=TEXT_DIM)

        term_content = VGroup(term_ridges, term_point, term_glow)
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
        bifur_glow  = Circle(radius=0.25, color=MINUTIA_BIFUR, stroke_width=2).move_to(bifur_point)
        bifur_desc  = self.ct("Đường vân tách thành hai nhánh", font_size=15, color=TEXT_DIM)

        bifur_content = VGroup(bifur_ridges, bifur_point, bifur_glow)
        bifur_group = VGroup(bifur_title, bifur_content, bifur_desc).arrange(DOWN, buff=0.3)

        both = VGroup(term_group, bifur_group).arrange(RIGHT, buff=1.5).shift(DOWN * 0.3)
        divider = DashedLine(
            UP * 2.2 + ORIGIN,
            DOWN * 2.5 + ORIGIN,
            color=TEXT_DIM, stroke_width=1,
        ).move_to([both.get_center()[0], 0, 0])

        # ── Animations ──
        self.play(FadeIn(term_title), run_time=0.5)                                    # 2.25s
        self.play(
            LaggedStart(*[Create(r) for r in term_ridges], lag_ratio=0.1),
            run_time=1.0,
        )                                                                               # 3.25s
        self.play(FadeIn(term_point, scale=2), Create(term_glow), FadeIn(term_desc), run_time=0.7)  # 3.95s

        self.play(Create(divider), run_time=0.4)                                        # 4.35s
        self.play(FadeIn(bifur_title), run_time=0.5)                                    # 4.85s
        self.play(
            LaggedStart(*[Create(r) for r in bifur_ridges], lag_ratio=0.1),
            run_time=1.0,
        )                                                                               # 5.85s
        self.play(FadeIn(bifur_point, scale=2), Create(bifur_glow), FadeIn(bifur_desc), run_time=0.7)  # 6.55s

        # Tổng elapsed ≈ 6.55s + overhead 1.2s header = ~7.75s → cần 11.95s
        self.wait(4.4)   # → ~12.95s  (+1.0s to close gap)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.8)   # khoảng lặng 0.8s trước seg_04

    # ─── seg_04  (11.11s) ───────────────────────────────────────────────────

    def minutiae_representation(self):
        """Biểu diễn toán học m = {x, y, θ} — seg_04 = 11.11s."""
        section = self.get_section_hdr("Biểu diễn Minutiae")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)  # 0.6s

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
        self.play(Create(axes), FadeIn(axes_labels), run_time=1.0)  # 1.6s

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
        )  # 3.1s

        # Công thức và mô tả — bên phải
        formula = MathTex(r"m = \{x,\; y,\; \theta\}", font_size=42, color=TEXT_BRIGHT)
        formula.shift(RIGHT * 3.5 + UP * 1.2)
        self.play(Write(formula), run_time=0.8)  # 3.9s

        desc_xy = VGroup(
            MathTex(r"(x,\, y)", font_size=24, color=RIDGE_COLOR),
            self.ct("= tọa độ vị trí", font_size=18, color=TEXT_DIM),
        ).arrange(RIGHT, buff=0.12)
        desc_th = VGroup(
            MathTex(r"\theta", font_size=24, color=MINUTIA_BIFUR),
            self.ct("= góc đường vân", font_size=18, color=TEXT_DIM),
        ).arrange(RIGHT, buff=0.12)
        descs = VGroup(desc_xy, desc_th).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        descs.next_to(formula, DOWN, buff=0.5)
        self.play(FadeIn(descs, shift=UP * 0.2), run_time=0.7)  # 4.6s

        # Chú thích màu (legend)
        legend = VGroup(
            VGroup(
                Dot(color=MINUTIA_TERM, radius=0.07),
                self.ct("Kết thúc", font_size=14, color=MINUTIA_TERM),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Dot(color=MINUTIA_BIFUR, radius=0.07),
                self.ct("Phân nhánh", font_size=14, color=MINUTIA_BIFUR),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.next_to(descs, DOWN, buff=0.5)
        self.play(FadeIn(legend), run_time=0.6)  # 5.2s

        # Tổng elapsed ≈ 5.2s + overhead 0.6s header = ~5.8s → cần 11.11s
        self.wait(5.31)   # → ~11.91s  (+0.8s to close gap)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
