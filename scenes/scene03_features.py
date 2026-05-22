"""
Scene 3: Đặc trưng vân tay (Fingerprint Features)
- Định nghĩa Singularities (Loop, Delta, Whorl) + Hiệu ứng vòng xung + Demo chuẩn hóa
- Định nghĩa Minutiae (Termination, Bifurcation, Others) + Radar ping + So sánh thực tế
- Biểu diễn toán học m = {x, y, θ} + Quét lưới tọa độ + Mô tả chi tiết điểm cụ thể
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
        title = self.ct("Trích Xuất Đặc Trưng", font_size=42, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Phân tích đặc tính toàn cục và cục bộ", font_size=20, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(LEFT * 3.2)

        # 1. Left side title group fades in (0.0s - 2.5s)
        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)
        self.wait(1.0) # Total 3.5s

        # 2. Right side fingerprint slice appears (3.5s - 5.0s)
        # Background box to represent fingerprint paper/sensor print (light grey/white)
        box = create_rounded_box(width=5.0, height=4.0, fill_color="#f5f5fa", fill_opacity=1.0, stroke_color=PRIMARY, stroke_width=2).shift(RIGHT * 3.2 + DOWN * 0.4)
        
        # Ridges inside the box (dark lines)
        ridge1 = Line(LEFT * 1.8 + UP * 1.0, RIGHT * 1.8 + UP * 1.0, color="#1a1a2e", stroke_width=4.5)
        ridge2 = Line(LEFT * 1.8 + UP * 0.35, LEFT * 0.2 + UP * 0.35, color="#1a1a2e", stroke_width=4.5)
        
        # Bifurcation line components
        ridge3_main = Line(LEFT * 1.8 + DOWN * 0.3, LEFT * 0.3 + DOWN * 0.3, color="#1a1a2e", stroke_width=4.5)
        ridge3_up = Line(LEFT * 0.3 + DOWN * 0.3, RIGHT * 1.8 + UP * 0.1, color="#1a1a2e", stroke_width=4.5)
        ridge3_down = Line(LEFT * 0.3 + DOWN * 0.3, RIGHT * 1.8 + DOWN * 0.7, color="#1a1a2e", stroke_width=4.5)
        
        ridge4 = Line(LEFT * 1.8 + DOWN * 1.1, RIGHT * 1.8 + DOWN * 1.1, color="#1a1a2e", stroke_width=4.5)
        
        ridges_group = VGroup(ridge1, ridge2, ridge3_main, ridge3_up, ridge3_down, ridge4).shift(box.get_center())
        
        self.play(FadeIn(box), LaggedStart(*[Create(r) for r in ridges_group], lag_ratio=0.15), run_time=1.5)
        # Total 5.0s

        # 3. Labeling Ridge and Valley (5.0s - 6.0s)
        ridge_lbl = self.ct("Đường vân - Tối", font_size=13, color=TEXT_BRIGHT)
        ridge_lbl.move_to(box.get_top() + UP * 0.45 + LEFT * 0.8)
        ridge_arrow = Arrow(start=ridge_lbl.get_bottom() + RIGHT * 0.2, end=box.get_center() + UP * 1.0, color=PRIMARY, buff=0.1, stroke_width=2, tip_length=0.18)
        
        valley_lbl = self.ct("Rãnh - Sáng", font_size=13, color=TEXT_BRIGHT)
        valley_lbl.move_to(box.get_bottom() + DOWN * 0.45 + RIGHT * 0.8)
        valley_arrow = Arrow(start=valley_lbl.get_top() - RIGHT * 0.2, end=box.get_center() + LEFT * 0.6 + DOWN * 0.65, color=PRIMARY, buff=0.1, stroke_width=2, tip_length=0.18)
        
        self.play(Create(ridge_arrow), FadeIn(ridge_lbl), Create(valley_arrow), FadeIn(valley_lbl), run_time=1.0)
        # Total 6.0s
        self.wait(0.5) # Total 6.5s

        # 4. Highlight Termination & Bifurcation on the print (6.5s - 8.0s)
        term_dot = Dot(ridge2.get_end(), color=MINUTIA_TERM, radius=0.08)
        bifur_dot = Dot(ridge3_main.get_end(), color=MINUTIA_BIFUR, radius=0.08)
        
        self.play(FadeIn(term_dot, scale=1.5), FadeIn(bifur_dot, scale=1.5), run_time=0.5)
        self.play(
            Indicate(term_dot, color=MINUTIA_TERM, scale_factor=2.0),
            Indicate(bifur_dot, color=MINUTIA_BIFUR, scale_factor=2.0),
            run_time=1.0
        )
        # Total 8.0s

        # Target Segment 1 = 11.23s. FadeOut = 1.0s. Need to wait: 11.23 - 8.0 - 1.0 = 2.23s.
        self.wait(2.23)
        self.play(FadeOut(VGroup(group, box, ridges_group, ridge_lbl, ridge_arrow, valley_lbl, valley_arrow, term_dot, bifur_dot)), run_time=1.0)
        self.wait(0.8) # Silence gap

    def singularities(self):
        """Singularities (Loop, Delta, Whorl) — Segment 2 = 16.54s."""
        section = self.get_section_hdr("Điểm kỳ dị")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        intro = self.ct("Mức toàn cục: Mật độ đường vân tạo ra ba cấu trúc kỳ dị chính", font_size=16, color=TEXT_COLOR)
        intro.next_to(section, DOWN, buff=0.3)
        self.play(FadeIn(intro), run_time=0.6)
        # Total 1.2s

        # ── 1. Loop (Móc) ──
        loop_box = create_rounded_box(width=3.4, height=3.4, fill_color=CHART_BLUE, fill_opacity=0.08, stroke_color=CHART_BLUE, stroke_width=1.5)
        loop = SVGMobject("assets/features/loop.svg").set_color(RIDGE_COLOR).scale(1.20).move_to(loop_box.get_center())
        loop_lbl = self.ct("Loop", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        core_dot = Dot(loop.get_center() + UP * 0.125, color=CORE_POINT, radius=0.08 * 1.5)
        core_lbl = self.ct("Core", font_size=12, color=CORE_POINT, weight=BOLD).next_to(core_dot, UP, buff=0.12).add_background_rectangle(color=BG_COLOR, opacity=0.85, buff=0.04)
        loop_group = VGroup(loop_box, loop, core_dot, core_lbl, loop_lbl)

        # ── 2. Delta (Tam sa) ──
        delta_box = create_rounded_box(width=3.4, height=3.4, fill_color=CHART_ORANGE, fill_opacity=0.08, stroke_color=CHART_ORANGE, stroke_width=1.5)
        delta = SVGMobject("assets/features/delta.svg").set_color(RIDGE_COLOR).scale(1.20).move_to(delta_box.get_center())
        delta_lbl_name = self.ct("Delta", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        delta_dot = Dot(delta.get_center() + DOWN * 0.1 + LEFT * 0.1, color=DELTA_COLOR, radius=0.08 * 1.5)
        delta_lbl = self.ct("Delta", font_size=12, color=DELTA_COLOR, weight=BOLD).next_to(delta_dot, DOWN, buff=0.12).add_background_rectangle(color=BG_COLOR, opacity=0.85, buff=0.04)
        delta_group = VGroup(delta_box, delta, delta_dot, delta_lbl, delta_lbl_name)

        # ── 3. Whorl (Xoáy) ──
        whorl_box = create_rounded_box(width=3.4, height=3.4, fill_color=CHART_PURPLE, fill_opacity=0.08, stroke_color=CHART_PURPLE, stroke_width=1.5)
        whorl = SVGMobject("assets/features/whorl.svg").set_color(RIDGE_COLOR).scale(1.20).move_to(whorl_box.get_center())
        whorl_lbl = self.ct("Whorl", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        whorl_dot = Dot(whorl.get_center() + RIGHT * 0.1, color=CORE_POINT, radius=0.08 * 1.5)
        whorl_lbl_node = self.ct("Core", font_size=12, color=CORE_POINT, weight=BOLD).next_to(whorl_dot, UP, buff=0.12).add_background_rectangle(color=BG_COLOR, opacity=0.85, buff=0.04)
        whorl_group = VGroup(whorl_box, whorl, whorl_dot, whorl_lbl_node, whorl_lbl)

        all_singular = VGroup(loop_group, delta_group, whorl_group)
        all_singular.arrange(RIGHT, buff=0.6).shift(DOWN * 0.55)

        # Positioning labels at bottom of each card
        loop_lbl.next_to(loop_box, DOWN, buff=0.2)
        delta_lbl_name.next_to(delta_box, DOWN, buff=0.2)
        whorl_lbl.next_to(whorl_box, DOWN, buff=0.2)

        # Fade in cards sequentially (1.2s - 3.6s)
        self.play(FadeIn(loop_group, shift=UP * 0.3, scale=0.9), run_time=0.8)
        self.play(FadeIn(delta_group, shift=UP * 0.3, scale=0.9), run_time=0.8)
        self.play(FadeIn(whorl_group, shift=UP * 0.3, scale=0.9), run_time=0.8)
        # Total 3.6s

        # Pulse waves on core & delta dots (3.6s - 4.6s)
        pulse_anims = []
        pulses = []
        for dot, color in [(core_dot, CORE_POINT), (delta_dot, DELTA_COLOR), (whorl_dot, CORE_POINT)]:
            p1 = Circle(radius=0.05, color=color, stroke_width=2).move_to(dot.get_center())
            p2 = Circle(radius=0.05, color=color, stroke_width=2).move_to(dot.get_center())
            self.add(p1, p2)
            pulses.extend([p1, p2])
            pulse_anims.append(
                LaggedStart(
                    p1.animate.scale(6).set_stroke(opacity=0),
                    p2.animate.scale(6).set_stroke(opacity=0),
                    lag_ratio=0.3
                )
            )
        self.play(*pulse_anims, run_time=1.0)
        self.remove(*pulses)
        # Total 4.6s

        # Transition to normalization demo (4.6s - 5.4s)
        self.play(FadeOut(VGroup(intro, all_singular)), run_time=0.7)
        self.wait(0.1)
        # Total 5.4s

        # Create elements for normalization demo
        demo_title = self.ct("Chuẩn hóa vân tay qua điểm Core", font_size=20, color=TEXT_BRIGHT, weight=BOLD).shift(LEFT * 3.5 + UP * 1.2)
        demo_desc = self.ct(
            "Xác định mốc Core để chuẩn hóa\nvị trí và hướng của vân tay,\ngiúp tối ưu hóa việc so khớp.", 
            font_size=15, 
            line_spacing=1.25,
            color=TEXT_DIM
        ).next_to(demo_title, DOWN, buff=0.4, aligned_edge=LEFT)
        
        # Center coordinate axes (dashed crosshair)
        dashed_x = DashedLine(LEFT * 3.0, RIGHT * 3.0, color=TEXT_DIM, stroke_width=1.5)
        dashed_y = DashedLine(DOWN * 3.0, UP * 3.0, color=TEXT_DIM, stroke_width=1.5)
        axes_center = np.array([2.5, -0.6, 0.0])  # Shift crosshair to the right side
        dashed_x.move_to(axes_center)
        dashed_y.move_to(axes_center)
        
        # Fingerprint pattern (tilted & offset from crosshair center)
        fp = create_fingerprint_simple(color=RIDGE_COLOR).scale(0.85)
        core_dot = Dot(fp.get_center() + UP * 0.15, color=CORE_POINT, radius=0.1)
        core_lbl = self.ct("Core", font_size=13, color=CORE_POINT, weight=BOLD).next_to(core_dot, UP, buff=0.1)
        fp_group = VGroup(fp, core_dot, core_lbl)
        
        # Set initial tilt and offset relative to target axes_center
        fp_group.shift(axes_center + RIGHT * 1.0 + UP * 0.8)
        fp_group.rotate(35 * DEGREES, about_point=core_dot.get_center())
        
        # Normalization Animations (5.4s - 11.1s)
        self.play(FadeIn(demo_title), FadeIn(demo_desc), run_time=0.6) # Total 6.0s
        self.play(FadeIn(fp_group), run_time=0.8)                       # Total 6.8s
        self.play(Create(dashed_x), Create(dashed_y), run_time=0.8)     # Total 7.6s
        self.wait(0.5)                                                  # Total 8.1s
        
        # Animate fingerprint translating and rotating back to axes_center
        self.play(
            fp_group.animate.shift(axes_center - core_dot.get_center()).rotate(-35 * DEGREES, about_point=axes_center),
            run_time=1.8,
            rate_func=smooth
        ) # Total 9.9s
        
        success_lbl = self.ct("Chuẩn hóa hoàn tất!", font_size=15, color=MATCH_COLOR, weight=BOLD).next_to(demo_desc, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(
            FadeIn(success_lbl, shift=UP * 0.1),
            core_dot.animate.scale(2.0),
            run_time=0.8
        )
        self.play(core_dot.animate.scale(0.5), run_time=0.4) # Total 11.1s
        
        # Target Segment 2 = 16.54s. FadeOut = 0.8s. Need wait: 16.54 - 11.1 - 0.8 = 4.64s.
        self.wait(4.64)
        self.play(FadeOut(VGroup(section, demo_title, demo_desc, success_lbl, fp_group, dashed_x, dashed_y)), run_time=0.8)
        self.wait(0.8)

    def minutiae_types(self):
        """Minutiae Termination & Bifurcation — Segment 3 = 14.35s."""
        section = self.get_section_hdr("Minutiae: Điểm đặc trưng cục bộ")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        definition = self.ct("Minutiae = các điểm mà đường vân bị gián đoạn", font_size=20, color=TEXT_COLOR)
        definition.next_to(section, DOWN, buff=0.45)
        self.play(FadeIn(definition, shift=UP * 0.2), run_time=0.6)
        # Total 1.2s

        # ── 1. Card Kết thúc (Termination) ──
        term_box = create_rounded_box(width=3.6, height=3.2, fill_color=CHART_BLUE, fill_opacity=0.06, stroke_color=CHART_BLUE, stroke_width=1.5)
        term_box.shift(LEFT * 4.2 + DOWN * 0.4)
        term_title = self.ct("Điểm kết thúc", font_size=16, color=MINUTIA_TERM, weight=BOLD)
        term_title.next_to(term_box, UP, buff=0.2)
        
        term_ridges = VGroup()
        for i in range(5):
            y = (i - 2) * 0.28
            length = 2.0 if i != 2 else 1.0
            ridge = Line(
                LEFT * 1.0 + UP * y,
                LEFT * 1.0 + RIGHT * length + UP * y,
                color=RIDGE_COLOR, stroke_width=3,
            )
            term_ridges.add(ridge)
        term_ridges.move_to(term_box.get_center() + UP * 0.1)
        term_point = Dot(term_ridges[2].get_end(), color=MINUTIA_TERM, radius=0.08)
        term_desc = self.ct("Vân dừng đột ngột", font_size=12, color=TEXT_DIM)
        term_desc.next_to(term_box, DOWN, buff=0.15)

        # ── 2. Card Phân nhánh (Bifurcation) ──
        bifur_box = create_rounded_box(width=3.6, height=3.2, fill_color=CHART_ORANGE, fill_opacity=0.06, stroke_color=CHART_ORANGE, stroke_width=1.5)
        bifur_box.shift(DOWN * 0.4)
        bifur_title = self.ct("Điểm rẽ nhánh", font_size=16, color=MINUTIA_BIFUR, weight=BOLD)
        bifur_title.next_to(bifur_box, UP, buff=0.2)
        
        bifur_ridges = VGroup()
        main_line = None
        for i in range(5):
            y = (i - 2) * 0.28
            if i == 2:
                main_line = Line(LEFT * 1.0 + UP * y, LEFT * 0.1 + UP * y, color=RIDGE_COLOR, stroke_width=3)
                branch1 = Line(LEFT * 0.1 + UP * y, RIGHT * 1.0 + UP * (y + 0.2), color=RIDGE_COLOR, stroke_width=3)
                branch2 = Line(LEFT * 0.1 + UP * y, RIGHT * 1.0 + UP * (y - 0.2), color=RIDGE_COLOR, stroke_width=3)
                bifur_ridges.add(main_line, branch1, branch2)
            elif i == 1:
                continue
            else:
                bifur_ridges.add(Line(LEFT * 1.0 + UP * y, RIGHT * 1.0 + UP * y, color=RIDGE_COLOR, stroke_width=3))
        bifur_ridges.move_to(bifur_box.get_center() + UP * 0.1)
        bifur_point = Dot(main_line.get_end(), color=MINUTIA_BIFUR, radius=0.08)
        bifur_desc = self.ct("Vân tách làm đôi", font_size=12, color=TEXT_DIM)
        bifur_desc.next_to(bifur_box, DOWN, buff=0.15)

        # ── 3. Card Loại khác (Others) ──
        others_box = create_rounded_box(width=3.6, height=3.2, fill_color=CHART_PURPLE, fill_opacity=0.06, stroke_color=TEXT_DIM, stroke_width=1.5)
        others_box.shift(RIGHT * 4.2 + DOWN * 0.4)
        others_title = self.ct("Loại khác", font_size=16, color=TEXT_DIM, weight=BOLD)
        others_title.next_to(others_box, UP, buff=0.2)
        
        # Bridge & Island representation
        b_ridge1 = Line(LEFT * 0.8 + UP * 0.5, RIGHT * 0.8 + UP * 0.5, color=RIDGE_COLOR, stroke_width=3)
        b_ridge2 = Line(LEFT * 0.8 + UP * 0.0, RIGHT * 0.8 + UP * 0.0, color=RIDGE_COLOR, stroke_width=3)
        b_conn = Line(LEFT * 0.2 + UP * 0.5, RIGHT * 0.2 + UP * 0.0, color=RIDGE_COLOR, stroke_width=3)
        b_lbl = self.ct("Cầu nối", font_size=10, color=TEXT_DIM).next_to(b_ridge2, DOWN, buff=0.05)
        bridge_group = VGroup(b_ridge1, b_ridge2, b_conn, b_lbl)
        
        i_ridge1 = Line(LEFT * 0.8 + DOWN * 0.5, LEFT * 0.3 + DOWN * 0.5, color=RIDGE_COLOR, stroke_width=3)
        i_island = Circle(radius=0.12, color=RIDGE_COLOR, stroke_width=3).move_to(DOWN * 0.5)
        i_ridge2 = Line(RIGHT * 0.3 + DOWN * 0.5, RIGHT * 0.8 + DOWN * 0.5, color=RIDGE_COLOR, stroke_width=3)
        i_lbl = self.ct("Đảo nhỏ", font_size=10, color=TEXT_DIM).next_to(i_island, DOWN, buff=0.05)
        island_group = VGroup(i_ridge1, i_island, i_ridge2, i_lbl)
        
        others_ridges = VGroup(bridge_group, island_group)
        others_ridges.move_to(others_box.get_center() + UP * 0.1)
        others_desc = self.ct("Đảo, Cầu nối, Điểm...", font_size=12, color=TEXT_DIM)
        others_desc.next_to(others_box, DOWN, buff=0.15)

        # ── Animations (1.2s - 7.5s) ──
        self.play(FadeIn(term_box), FadeIn(bifur_box), FadeIn(others_box), run_time=0.8) # Total 2.0s
        self.play(
            FadeIn(term_title), FadeIn(bifur_title), FadeIn(others_title),
            FadeIn(term_desc), FadeIn(bifur_desc), FadeIn(others_desc),
            run_time=0.6
        ) # Total 2.6s
        self.play(Create(term_ridges), Create(bifur_ridges), Create(others_ridges), run_time=1.5) # Total 4.1s
        self.play(FadeIn(term_point, scale=2), FadeIn(bifur_point, scale=2), run_time=0.6) # Total 4.7s

        # Radar ping effects (4.7s - 5.5s)
        pulse_term = Circle(radius=0.05, color=MINUTIA_TERM, stroke_width=2.5).move_to(term_point.get_center())
        pulse_bifur = Circle(radius=0.05, color=MINUTIA_BIFUR, stroke_width=2.5).move_to(bifur_point.get_center())
        self.add(pulse_term, pulse_bifur)
        self.play(
            pulse_term.animate.scale(6).set_stroke(opacity=0),
            pulse_bifur.animate.scale(6).set_stroke(opacity=0),
            run_time=0.8
        )
        self.remove(pulse_term, pulse_bifur) # Total 5.5s

        # Red Cross (X) over Column 3 (5.5s - 6.5s)
        cross_line1 = Line(others_box.get_corner(UL) + RIGHT*0.3 + DOWN*0.3, others_box.get_corner(DR) + LEFT*0.3 + UP*0.3, color=MISMATCH_COLOR, stroke_width=4)
        cross_line2 = Line(others_box.get_corner(DL) + RIGHT*0.3 + UP*0.3, others_box.get_corner(UR) + LEFT*0.3 + DOWN*0.3, color=MISMATCH_COLOR, stroke_width=4)
        cross = VGroup(cross_line1, cross_line2)
        cross_lbl = self.ct("Khó nhận diện tự động", font_size=13, color=MISMATCH_COLOR, weight=BOLD).next_to(others_desc, DOWN, buff=0.15)
        
        self.play(Create(cross), FadeIn(cross_lbl), run_time=1.0) # Total 6.5s

        # Green highlights and checkmarks for Column 1 & 2 (6.5s - 7.5s)
        check1 = MathTex(r"\checkmark", color=MATCH_COLOR, font_size=28).next_to(term_title, RIGHT, buff=0.1)
        check2 = MathTex(r"\checkmark", color=MATCH_COLOR, font_size=28).next_to(bifur_title, RIGHT, buff=0.1)
        
        self.play(
            term_box.animate.set_stroke(color=MATCH_COLOR, width=2.5),
            bifur_box.animate.set_stroke(color=MATCH_COLOR, width=2.5),
            FadeIn(check1), FadeIn(check2),
            run_time=1.0
        ) # Total 7.5s

        # Target Segment 3 = 14.35s. FadeOut = 0.8s. Need wait: 14.35 - 7.5 - 0.8 = 6.05s.
        self.wait(6.05)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.8)

    def minutiae_representation(self):
        """Biểu diễn toán học m = {x, y, θ} — Segment 4 = 10.61s."""
        section = self.get_section_hdr("Biểu diễn Minutiae")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        # Grid Axes
        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 5, 1],
            x_length=5, y_length=4,
            axis_config={
                "color": TEXT_DIM, "stroke_width": 1.5,
                "include_numbers": True, "font_size": 16,
            },
        ).shift(LEFT * 2.2 + DOWN * 0.3)
        axes_labels = axes.get_axis_labels(
            x_label=Text("x", font_size=18, color=TEXT_DIM),
            y_label=Text("y", font_size=18, color=TEXT_DIM),
        )
        self.play(Create(axes), FadeIn(axes_labels), run_time=1.0) # Total 1.6s

        # Plotted points representing minutiae features
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
        ) # Total 3.1s

        # Highlight point 0: (2, 3, PI/4) (3.1s - 3.8s)
        pt0_pos = axes.c2p(2, 3)
        self.play(Indicate(points[0], color=PRIMARY, scale_factor=1.8), run_time=0.7) # Total 3.8s

        # Projection lines and angle arc for the highlighted minutia (3.8s - 5.0s)
        proj_x = DashedLine(pt0_pos, axes.c2p(2, 0), color=MINUTIA_TERM, stroke_width=2)
        proj_y = DashedLine(pt0_pos, axes.c2p(0, 3), color=MINUTIA_TERM, stroke_width=2)
        ref_line = DashedLine(pt0_pos, pt0_pos + RIGHT * 0.8, color=TEXT_DIM, stroke_width=1.5)
        
        theta_arc = Arc(
            radius=0.35,
            start_angle=0,
            angle=PI / 4,
            arc_center=pt0_pos,
            color=MINUTIA_BIFUR,
            stroke_width=2,
        )
        theta_lbl = MathTex(r"\theta", font_size=20, color=MINUTIA_BIFUR).next_to(theta_arc, UR, buff=0.05)

        self.play(
            Create(proj_x), Create(proj_y), Create(ref_line), 
            Create(theta_arc), FadeIn(theta_lbl), 
            run_time=1.2
        ) # Total 5.0s

        # Formula and example - right side (5.0s - 5.8s)
        formula = MathTex(r"m = \{x,\; y,\; \theta\}", font_size=42, color=TEXT_BRIGHT)
        formula.shift(RIGHT * 3.4 + UP * 1.4)
        
        example = MathTex(r"m_1 = \{2.0,\; 3.0,\; 45^\circ\}", font_size=32, color=PRIMARY)
        example.next_to(formula, DOWN, buff=0.25)
        
        self.play(Write(formula), Write(example), run_time=0.8) # Total 5.8s

        # Explanatory descriptions (5.8s - 6.4s)
        desc_xy = VGroup(
            MathTex(r"(x,\, y)", font_size=24, color=MINUTIA_TERM),
            self.ct("= tọa độ vị trí", font_size=18, color=TEXT_DIM),
        ).arrange(RIGHT, buff=0.12)
        
        desc_th = VGroup(
            MathTex(r"\theta", font_size=24, color=MINUTIA_BIFUR),
            self.ct("= hướng góc vân", font_size=18, color=TEXT_DIM),
        ).arrange(RIGHT, buff=0.12)
        
        descs = VGroup(desc_xy, desc_th).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        descs.next_to(example, DOWN, buff=0.45)
        self.play(FadeIn(descs, shift=UP * 0.15), run_time=0.6) # Total 6.4s

        # Legend/Color guide (6.4s - 7.0s)
        legend = VGroup(
            VGroup(
                Dot(color=MINUTIA_TERM, radius=0.07),
                self.ct("Điểm kết thúc", font_size=14, color=MINUTIA_TERM),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Dot(color=MINUTIA_BIFUR, radius=0.07),
                self.ct("Điểm rẽ nhánh", font_size=14, color=MINUTIA_BIFUR),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.next_to(descs, DOWN, buff=0.4)
        self.play(FadeIn(legend), run_time=0.6) # Total 7.0s

        # Target Segment 4 = 10.61s. FadeOut = 0.8s. Need wait: 10.61 - 7.0 - 0.8 = 2.81s.
        self.wait(2.81)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
