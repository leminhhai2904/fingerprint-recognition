"""
Scene 1: Giới thiệu về Nhận dạng Vân tay (Section 2.1)
- Tiêu đề mở đầu (Đặc biệt: Vẽ vân tay)
- Vân tay là gì? (đường vân và rãnh + Quét laser + DNA & bào thai & sinh đôi)
- Tại sao vân tay là đặc trưng sinh trắc tốt
- Các mẫu vân tay cơ bản: Loop, Whorl, Arch
- Lịch sử phát triển
"""
from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene01Intro(Scene):
    def construct(self):
        scene_setup(self)
        self.intro_title()
        self.what_is_fingerprint()
        self.why_fingerprints()
        self.fingerprint_patterns()
        self.history_timeline()

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kw):
        """create_text with CMU Serif kerning workaround (render big → scale down)."""
        return Text(text_str, font_size=36, color=color, weight=weight, **kw).scale(font_size / 36)

    def intro_title(self):
        """Chuỗi hoạt hình tiêu đề mở đầu — Segment 1 & 2."""
        top_label = self.ct("N H Ậ N   D Ạ N G   M Ẫ U", font_size=16, color=TEXT_DIM).to_edge(UP, buff=1.5)
        title = self.ct("Nhận Dạng Vân Tay", font_size=56, color=TEXT_BRIGHT, weight=BOLD)

        line_left = Line(LEFT * 3.5, LEFT * 0.5, color=PRIMARY, stroke_width=2)
        line_right = Line(RIGHT * 0.5, RIGHT * 3.5, color=PRIMARY, stroke_width=2)
        lines = VGroup(line_left, line_right).next_to(title, DOWN, buff=0.3)

        subtitle = self.ct("Máy tính nhận diện danh tính bạn như thế nào?", font_size=24, color=RIDGE_COLOR)
        subtitle.next_to(lines, DOWN, buff=0.4)

        fp_icon = create_fingerprint_simple(scale=0.6, color=RIDGE_COLOR)
        fp_icon.set_opacity(0.15).scale(2).move_to(ORIGIN)

        # Drawing the fingerprint in the background with a laser sweep (Premium effect)
        scan_line = Line(LEFT * 4.5, RIGHT * 4.5, color=RIDGE_COLOR, stroke_width=3.5).set_opacity(0.9)
        scan_glow = Line(LEFT * 4.5, RIGHT * 4.5, color=RIDGE_COLOR, stroke_width=8.0).set_opacity(0.2)
        scan_group = VGroup(scan_glow, scan_line)
        scan_group.move_to(UP * 2.5)
        
        # Segment 1 (0.22s - 0.90s, dur 0.68s)
        self.wait(0.22)
        self.play(FadeIn(top_label, shift=DOWN * 0.3), run_time=0.4)
        self.wait(0.28)
        
        # Gap between Segment 1 & Segment 2 (0.90s - 1.06s, dur 0.16s)
        self.wait(0.16)
        
        # Segment 2 (1.06s - 7.52s, dur 6.46s)
        self.add(scan_group)
        self.play(
            FadeIn(fp_icon, run_time=2.0),
            scan_group.animate.move_to(DOWN * 2.5),
            Write(title, run_time=1.5),
            run_time=2.0,
            rate_func=linear
        )
        self.play(FadeOut(scan_group, run_time=0.2))
        self.play(
            Create(line_left, run_time=0.5),
            Create(line_right, run_time=0.5),
        )
        self.play(FadeIn(subtitle, shift=UP * 0.2, run_time=0.7))

        # Total Segment 2 elapsed: 2.0 (sweep) + 0.2 (fade out scan) + 0.5 (create lines) + 0.7 (subtitle) = 3.40s.
        # Remaining Segment 2 duration: 6.46s - 3.40s = 3.06s.
        self.wait(3.06)
        
        # Gap between Segment 2 & Segment 3 (7.52s - 8.28s, dur 0.76s)
        # Use this gap to fade out the title group
        self.play(
            FadeOut(VGroup(title, top_label, lines, subtitle, fp_icon)),
            run_time=0.76,
        )

    def what_is_fingerprint(self):
        """Giải thích vân tay là gì — Segments 3 to 7."""
        section = get_section_title("Vân tay là gì?")
        section.to_edge(UP, buff=0.6)
        
        # Segment 3 (8.28s - 11.68s, dur 3.40s)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.4)

        # Tạo visualization đường vân (trái)
        ridges_group = VGroup()
        num_ridges = 9
        for i in range(num_ridges):
            y = (i - num_ridges // 2) * 0.35
            if i % 2 == 0:
                ridge = Line(
                    LEFT * 2.5 + UP * y,
                    RIGHT * 2.5 + UP * y,
                    color=RIDGE_COLOR,
                    stroke_width=6,
                )
                ridge.set_points_smoothly([
                    np.array([-2.5, y, 0]),
                    np.array([-0.8, y + 0.08, 0]),
                    np.array([0.8, y + 0.08, 0]),
                    np.array([2.5, y, 0]),
                ])
                ridges_group.add(ridge)

        ridges_group.shift(LEFT * 4.0 + DOWN * 0.5)  # Dịch khung qua trái thêm một chút

        ridge_label = self.ct("Đường vân", font_size=16, color=RIDGE_COLOR)
        valley_label = self.ct("Rãnh", font_size=16, color=TEXT_DIM)

        ridge_arrow = Arrow(LEFT * 0.5 + DOWN * 0.5, LEFT * 1.5 + DOWN * 0.5, color=RIDGE_COLOR, stroke_width=2)
        ridge_label.next_to(ridge_arrow, RIGHT, buff=0.1)

        valley_arrow = Arrow(LEFT * 0.5 + DOWN * 0.1, LEFT * 1.5 + DOWN * 0.1, color=TEXT_DIM, stroke_width=2)
        valley_label.next_to(valley_arrow, RIGHT, buff=0.1)

        desc = self.ct("Hệ thống các đường vân và rãnh xen kẽ nhau", font_size=18, color=TEXT_BRIGHT)
        desc.next_to(ridges_group, DOWN, buff=0.4)

        # Laser Scan effect
        scan_line = Line(LEFT * 6.0, LEFT * 1.0, color=PRIMARY, stroke_width=3).set_opacity(0.8)
        scan_line.move_to(LEFT * 4.0 + UP * 1.0)

        self.play(FadeIn(scan_line, run_time=0.2))
        self.play(
            scan_line.animate.move_to(LEFT * 4.0 + DOWN * 2.4),
            LaggedStart(*[Create(r) for r in ridges_group], lag_ratio=0.08),
            run_time=1.0
        )
        self.play(FadeOut(scan_line, run_time=0.2))

        self.play(
            Create(ridge_arrow, run_time=0.3),
            FadeIn(ridge_label, run_time=0.3),
            Create(valley_arrow, run_time=0.3),
            FadeIn(valley_label, run_time=0.3),
        )
        self.play(FadeIn(desc, shift=UP * 0.2, run_time=0.4))
        
        # Segment 3 duration: 3.40s.
        # Elapsed: 0.4 (section) + 0.2 + 1.0 + 0.2 (scan) + 0.3 (arrows) + 0.4 (desc) = 2.50s.
        # Segment 3 resting wait: 3.40 - 2.50 = 0.90s.
        self.wait(0.90)
        
        # Gap between Segment 3 & 4 (11.68s - 12.26s, dur 0.58s)
        self.wait(0.58)

        # --- Segment 4 (12.26s - 15.24s, dur 2.98s) ---
        dna_box = create_rounded_box(width=5.2, height=3.6, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=PRIMARY, stroke_width=1.5)
        dna_box.shift(RIGHT * 3.6 + DOWN * 0.3)
        dna_title = self.ct("Yếu tố hình thành", font_size=18, color=PRIMARY, weight=BOLD).next_to(dna_box.get_top(), DOWN, buff=0.25)
        
        # DNA helix (Trái)
        dna_helix = VGroup()
        for x_val in np.linspace(-0.8, 0.8, 8):
            y_offset = 0.35 * np.sin(2 * np.pi * x_val / 1.6)
            dot1 = Dot([x_val, y_offset, 0], color=CHART_BLUE, radius=0.05)
            dot2 = Dot([x_val, -y_offset, 0], color=CHART_ORANGE, radius=0.05)
            link = Line([x_val, y_offset, 0], [x_val, -y_offset, 0], stroke_width=1, color=TEXT_DIM).set_opacity(0.4)
            dna_helix.add(dot1, dot2, link)
        dna_helix.scale(0.85).move_to(dna_box.get_center() + UP * 0.3 + LEFT * 1.5)
        dna_label = self.ct("1. Di truyền", font_size=12, color=CHART_BLUE).next_to(dna_helix, DOWN, buff=0.15)

        # Ripples representing fluid environment (Giữa)
        fluid_waves = VGroup()
        for idx in range(3):
            wave = Arc(radius=0.15 + idx * 0.12, start_angle=-PI/4, angle=PI/2, stroke_width=1.5, color=PRIMARY).set_opacity(0.6 - idx*0.15)
            fluid_waves.add(wave)
        fluid_waves.move_to(dna_box.get_center() + UP * 0.3)
        fluid_label = self.ct("2. Nước ối", font_size=12, color=PRIMARY).next_to(fluid_waves, DOWN, buff=0.15)

        # Capillary (Mao mạch) representation (Phải)
        capillary = VGroup()
        c_main = Line(DOWN * 0.4, UP * 0.1, color="#e63946", stroke_width=2)
        c_br1 = Line(UP * 0.0, UP * 0.25 + RIGHT * 0.25, color="#e63946", stroke_width=1.5)
        c_br2 = Line(UP * 0.0, UP * 0.2 + LEFT * 0.25, color="#e63946", stroke_width=1.5)
        c_br1_sub = Line(UP * 0.25 + RIGHT * 0.25, UP * 0.45 + RIGHT * 0.35, color="#e63946", stroke_width=1)
        c_br2_sub = Line(UP * 0.2 + LEFT * 0.25, UP * 0.4 + LEFT * 0.35, color="#e63946", stroke_width=1)
        capillary.add(c_main, c_br1, c_br2, c_br1_sub, c_br2_sub)
        capillary.move_to(dna_box.get_center() + UP * 0.3 + RIGHT * 1.5)
        capillary_label = self.ct("3. Mao mạch", font_size=12, color="#e63946").next_to(capillary, DOWN, buff=0.15)

        initial_factors_seg4 = VGroup(dna_helix, dna_label, fluid_waves, fluid_label)

        self.play(FadeIn(dna_box), FadeIn(dna_title), run_time=0.4)
        self.play(
            LaggedStart(
                FadeIn(dna_helix), FadeIn(dna_label),
                FadeIn(fluid_waves), FadeIn(fluid_label),
                lag_ratio=0.15
            ),
            run_time=1.0
        )
        # Segment 4 duration: 2.98s.
        # Elapsed: 0.4 + 1.0 = 1.40s.
        # Segment 4 resting wait: 2.98 - 1.40 = 1.58s.
        self.wait(1.58)  
        
        # Gap between Segment 4 & 5 (15.24s - 16.18s, dur 0.94s)
        self.wait(0.94)

        # --- Segment 5 (16.18s - 19.30s, dur 3.12s) ---
        self.play(
            Create(capillary), FadeIn(capillary_label),
            run_time=0.8
        )
        # Segment 5 duration: 3.12s.
        # Elapsed: 0.80s.
        # Segment 5 resting wait: 3.12 - 0.80 = 2.32s.
        self.wait(2.32)  
        
        # Gap between Segment 5 & 6 (19.30s - 20.58s, dur 1.28s)
        self.wait(1.28)

        # --- Segment 6 (20.58s - 25.18s, dur 4.60s) ---
        self.play(
            Indicate(fluid_waves, color=PRIMARY, scale_factor=1.25),
            Indicate(capillary, color="#e63946", scale_factor=1.25),
            run_time=1.2
        )
        # Segment 6 duration: 4.60s.
        # Elapsed: 1.20s.
        # Segment 6 resting wait: 4.60 - 1.20 = 3.40s.
        self.wait(3.40)  

        # --- Segment 7 (25.18s - 30.24s, dur 5.06s) ---
        # TWIN COMPARISON POP-UP INSIDE BOX
        twin_title = self.ct("Sinh đôi cùng trứng", font_size=16, color=PRIMARY, weight=BOLD).next_to(dna_box.get_top(), DOWN, buff=0.25)
        
        twin_a = self.ct("Sinh đôi A", font_size=12, color=CHART_BLUE).move_to(dna_box.get_center() + LEFT * 1.3 + UP * 0.6)
        twin_b = self.ct("Sinh đôi B", font_size=12, color=CHART_BLUE).move_to(dna_box.get_center() + RIGHT * 1.3 + UP * 0.6)
        
        fp_a = create_fingerprint_simple(color=RIDGE_COLOR).scale(0.35).move_to(dna_box.get_center() + LEFT * 1.3 + DOWN * 0.15)
        fp_b = create_fingerprint_simple(color=RIDGE_COLOR).scale(0.35).move_to(dna_box.get_center() + RIGHT * 1.3 + DOWN * 0.15)
        
        # Mismatch markers (Highlighting the different minutia types at same location)
        diff_a = Dot(fp_a.get_center() + UP * 0.12, color=MINUTIA_TERM, radius=0.05)
        diff_b = Dot(fp_b.get_center() + UP * 0.12, color=MINUTIA_BIFUR, radius=0.05)
        arrow_a = Arrow(fp_a.get_center() + LEFT * 0.5 + DOWN * 0.2, diff_a.get_center(), color=MINUTIA_TERM, stroke_width=1.5, buff=0.05, max_tip_length_to_length_ratio=0.15)
        arrow_b = Arrow(fp_b.get_center() + RIGHT * 0.5 + DOWN * 0.2, diff_b.get_center(), color=MINUTIA_BIFUR, stroke_width=1.5, buff=0.05, max_tip_length_to_length_ratio=0.15)
        
        neq_sign = self.ct("≠", font_size=32, color=MISMATCH_COLOR, weight=BOLD).move_to(dna_box.get_center() + DOWN * 0.15)
        twin_desc = self.ct("Vân tay vẫn khác biệt hoàn toàn!", font_size=13, color=MISMATCH_COLOR, weight=BOLD).move_to(dna_box.get_bottom() + UP * 0.35)
        
        twin_group = VGroup(twin_title, twin_a, twin_b, fp_a, fp_b, diff_a, diff_b, arrow_a, arrow_b, neq_sign, twin_desc)

        # Transition DNA box interior
        self.play(
            FadeOut(initial_factors_seg4),
            FadeOut(capillary),
            FadeOut(capillary_label),
            FadeOut(dna_title),
            run_time=0.4
        )
        self.play(
            FadeIn(twin_group),
            run_time=0.8
        )
        self.play(
            Indicate(neq_sign, color=MISMATCH_COLOR, scale_factor=1.4),
            Indicate(diff_a, color=MINUTIA_TERM, scale_factor=1.6),
            Indicate(diff_b, color=MINUTIA_BIFUR, scale_factor=1.6),
            run_time=1.0
        )

        # Segment 7 duration: 5.06s.
        # Elapsed: 0.4 + 0.8 + 1.0 = 2.20s.
        # Segment 7 resting wait: 5.06 - 2.20 = 2.86s.
        # We wait 2.26s, then fade out the whole scene during the remaining 0.6s.
        self.wait(2.26)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

    def why_fingerprints(self):
        """Tại sao vân tay là đặc trưng sinh trắc tốt — Segment 8."""
        section = get_section_title("Tại sao dùng vân tay?")
        section.to_edge(UP, buff=0.8)
        
        # Segment 8 (30.24s - 42.16s, dur 11.92s)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.4)

        # Tạo icon 1: Vân tay nhỏ cho "Duy nhất"
        icon1 = create_fingerprint_simple(color=CHART_BLUE).scale_to_fit_height(0.45)
        
        # Tạo icon 2: Ký hiệu vô cực đại diện cho sự "Bền vững" suốt đời
        icon2 = VMobject(color=CHART_ORANGE, stroke_width=2.5)
        t_vals = np.linspace(0, 2 * PI, 60)
        points = []
        for t in t_vals:
            denom = 1 + np.sin(t)**2
            x = 0.55 * np.cos(t) / denom
            y = 0.55 * np.sin(t) * np.cos(t) / denom
            points.append([x, y, 0])
        icon2.set_points_smoothly([np.array(p) for p in points])
        icon2.scale_to_fit_height(0.42)
        
        # Tạo icon 3: Đồ thị/Cảm biến cho "Đo lường được"
        icon3 = VGroup(
            Line(LEFT * 0.2 + DOWN * 0.2, LEFT * 0.2 + UP * 0.1, color="#bd93f9", stroke_width=3.0),
            Line(ORIGIN + DOWN * 0.2, ORIGIN + UP * 0.25, color="#bd93f9", stroke_width=3.0),
            Line(RIGHT * 0.2 + DOWN * 0.2, RIGHT * 0.2 + UP * 0.0, color="#bd93f9", stroke_width=3.0),
            Line(LEFT * 0.35 + DOWN * 0.2, RIGHT * 0.35 + DOWN * 0.2, color="#bd93f9", stroke_width=1.5),
        )
        icon3.scale_to_fit_height(0.42)

        cards = VGroup()
        for idx, (title_text, desc_text, color, icon) in enumerate([
            ("Duy nhất", "Ngay cả cặp sinh đôi\ncùng trứng cũng có\nvân tay khác nhau", CHART_BLUE, icon1),
            ("Bền vững", "Ổn định từ tháng thứ 7\nthai kỳ và không\nthay đổi suốt đời", CHART_ORANGE, icon2),
            ("Đo lường được", "Có thể thu nhận\nbằng các cảm biến\nđiện tử hiện đại", "#bd93f9", icon3),
        ]):
            card = create_rounded_box(
                width=3.5, height=2.8,
                fill_color=color, fill_opacity=0.08,
                stroke_color=color, stroke_width=1.5,
            )
            title = self.ct(title_text, font_size=22, color=color, weight=BOLD)
            desc = Paragraph(
                *desc_text.split("\n"),
                font_size=28,
                color=TEXT_DIM,
                line_spacing=1.2,
                alignment="center"
            ).scale(13.5 / 28)
            content = VGroup(icon, title, desc).arrange(DOWN, buff=0.18)
            content.move_to(card.get_center())
            cards.add(VGroup(card, content))

        cards.arrange(RIGHT, buff=0.5).shift(DOWN * 0.3)

        self.wait(2.0)
        self.play(FadeIn(cards[0], shift=UP * 0.5, scale=0.9), run_time=0.6)
        self.wait(1.56)
        self.play(FadeIn(cards[1], shift=UP * 0.5, scale=0.9), run_time=0.6)
        self.wait(3.07)
        self.play(FadeIn(cards[2], shift=UP * 0.5, scale=0.9), run_time=0.6)
        
        # Segment 8 duration: 11.92s.
        # Elapsed: 0.4 (section) + 2.0 + 0.6 (card 0) + 1.56 + 0.6 (card 1) + 3.07 + 0.6 (card 2) = 8.83s.
        # Segment 8 resting wait: 11.92s - 8.83s = 3.09s.
        self.wait(3.09)
        
        # Gap between Segment 8 & 9 (42.16s - 43.48s, dur 1.32s)
        # Use this gap to fade out the cards without trailing wait
        self.play(FadeOut(VGroup(section, cards)), run_time=1.32)

    def fingerprint_patterns(self):
        """Phân loại vân tay cơ bản — Segment 9."""
        section = get_section_title("Các mẫu vân tay cơ bản")
        section.to_edge(UP, buff=0.8)
        
        # Segment 9 (43.48s - 50.12s, dur 6.64s)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.4)

        assets_dir = Path(__file__).resolve().parent.parent / "assets"

        patterns = [
            ("Vân Móc", "Khoảng 65% dân số.\nĐường vân cong\nvà quay trở lại.", CHART_BLUE, SVGMobject(str(assets_dir / "loop.svg")).scale_to_fit_height(1.4)),
            ("Vân Xoáy", "Khoảng 30% dân số.\nĐường vân xoay tròn\nquanh tâm.", CHART_ORANGE, SVGMobject(str(assets_dir / "whorl.svg")).scale_to_fit_height(1.4)),
            ("Vân Cung", "Khoảng 5% dân số.\nĐường vân đi từ\nbên này sang bên kia.", "#bd93f9", SVGMobject(str(assets_dir / "arch.svg")).scale_to_fit_height(1.4)),
        ]

        cards = VGroup()
        for title_text, desc_text, color, icon in patterns:
            bg = create_rounded_box(width=2.8, height=2.8, fill_color=color, fill_opacity=0.08, stroke_color=color, stroke_width=1.5)
            icon.set_color(color).move_to(bg.get_center() + UP * 0.1)
            icon_group = VGroup(bg, icon)

            title = self.ct(title_text, font_size=20, color=color, weight=BOLD)
            desc = Paragraph(
                *desc_text.split("\n"),
                font_size=28, color=TEXT_DIM, alignment="center", line_spacing=1.2
            ).scale(13.5 / 28)
            card = VGroup(icon_group, title, desc).arrange(DOWN, buff=0.25)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.6).shift(DOWN * 0.4)

        self.wait(0.82)
        # Show cards
        self.play(FadeIn(cards[0], shift=UP * 0.5), run_time=0.6)
        self.wait(1.2)
        self.play(FadeIn(cards[1], shift=UP * 0.5), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(cards[2], shift=UP * 0.5), run_time=0.6)

        # Segment 9 duration: 6.64s.
        # Elapsed: 0.4 (section) + 0.82 (wait) + 0.6 (card 0) + 1.2 (wait) + 0.6 (card 1) + 1.0 (wait) + 0.6 (card 2) = 5.22s.
        # Segment 9 resting wait (1.42s) and Gap (3.34s) combined:
        # We wait 3.76s before the FadeOut, and FadeOut during the final 1.0s.
        self.wait(1.76)
        self.play(FadeOut(VGroup(section, cards)), run_time=0.6)

    def history_timeline(self):
        """Lịch sử phát triển nhận dạng vân tay — Segments 10 to 13."""
        section = get_section_title("Lịch sử phát triển")
        section.to_edge(UP, buff=0.8)
        
        # Segment 10 start (53.46s - 54.98s, dur 1.52s)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.8)

        timeline_line = Line(LEFT * 5.5, RIGHT * 5.5, color=TEXT_DIM, stroke_width=2)
        timeline_line.shift(DOWN * 0.2)
        self.play(Create(timeline_line), run_time=0.4)

        events = [
            (-4.5, "1686", "Malpighi\nghi nhận\nđường vân", CHART_BLUE),
            (-1.8, "1880", "Fauld đề xuất\ntính duy nhất\ncủa vân tay", CHART_ORANGE),
            (-0.2, "1888", "Galton giới thiệu\nđặc trưng\nminutiae", "#bd93f9"),
            (1.8, "1899", "Hệ thống phân\nloại Henry\nra đời", PRIMARY),
            (4.2, "1960s", "Hệ thống AFIS\ntự động đầu\ntiên", CORE_POINT),
        ]

        dots = VGroup()
        labels = VGroup()

        # Event 1: Malpighi 1686
        x1, year1, desc1, color1 = events[0]
        dot1 = Dot(point=np.array([x1, -0.2, 0]), color=color1, radius=0.1)
        year_label1 = self.ct(year1, font_size=18, color=color1, weight=BOLD)
        year_label1.next_to(dot1, UP, buff=0.25)
        desc_label1 = Paragraph(
            *desc1.split("\n"),
            font_size=28,
            color=TEXT_DIM,
            line_spacing=1.1,
            alignment="center"
        ).scale(13 / 28)
        desc_label1.next_to(year_label1, UP, buff=0.15)
        tick1 = Line(np.array([x1, -0.35, 0]), np.array([x1, -0.05, 0]), color=color1, stroke_width=2)

        self.play(
            FadeIn(dot1, scale=2), Create(tick1),
            FadeIn(year_label1, shift=DOWN * 0.2),
            FadeIn(desc_label1, shift=DOWN * 0.2),
            run_time=0.4,
        )
        dots.add(dot1, tick1)
        labels.add(year_label1, desc_label1)
        
        # Segment 10 target: 1.52s.
        # Elapsed: 0.4 (section) + 0.4 (line) + 0.4 (event 1) = 1.20s.
        # Segment 10 resting wait: 1.52 - 1.20 = 0.32s.
        self.wait(3.04)

        # Event 2: Fauld 1880, Event 3: Galton 1888, Event 4: Henry 1899
        # Segment 11 (56.20s - 62.76s, dur 6.56s)
        x2, year2, desc2, color2 = events[1]
        dot2 = Dot(point=np.array([x2, -0.2, 0]), color=color2, radius=0.1)
        year_label2 = self.ct(year2, font_size=18, color=color2, weight=BOLD)
        year_label2.next_to(dot2, UP, buff=0.25)
        desc_label2 = Paragraph(
            *desc2.split("\n"),
            font_size=28,
            color=TEXT_DIM,
            line_spacing=1.1,
            alignment="center"
        ).scale(13 / 28)
        desc_label2.next_to(year_label2, UP, buff=0.15)
        tick2 = Line(np.array([x2, -0.35, 0]), np.array([x2, -0.05, 0]), color=color2, stroke_width=2)

        self.play(
            FadeIn(dot2, scale=2), Create(tick2),
            FadeIn(year_label2, shift=DOWN * 0.2),
            FadeIn(desc_label2, shift=DOWN * 0.2),
            run_time=0.4,
        )
        dots.add(dot2, tick2)
        labels.add(year_label2, desc_label2)
        self.wait(2.70)

        x3, year3, desc3, color3 = events[2]
        dot3 = Dot(point=np.array([x3, -0.2, 0]), color=color3, radius=0.1)
        year_label3 = self.ct(year3, font_size=18, color=color3, weight=BOLD)
        year_label3.next_to(dot3, UP, buff=0.25)
        desc_label3 = Paragraph(
            *desc3.split("\n"),
            font_size=28,
            color=TEXT_DIM,
            line_spacing=1.1,
            alignment="center"
        ).scale(13 / 28)
        desc_label3.next_to(year_label3, UP, buff=0.15)
        tick3 = Line(np.array([x3, -0.35, 0]), np.array([x3, -0.05, 0]), color=color3, stroke_width=2)

        self.play(
            FadeIn(dot3, scale=2), Create(tick3),
            FadeIn(year_label3, shift=DOWN * 0.2),
            FadeIn(desc_label3, shift=DOWN * 0.2),
            run_time=0.4,
        )
        dots.add(dot3, tick3)
        labels.add(year_label3, desc_label3)
        self.wait(2.40)

        x4, year4, desc4, color4 = events[3]
        dot4 = Dot(point=np.array([x4, -0.2, 0]), color=color4, radius=0.1)
        year_label4 = self.ct(year4, font_size=18, color=color4, weight=BOLD)
        year_label4.next_to(dot4, UP, buff=0.25)
        desc_label4 = Paragraph(
            *desc4.split("\n"),
            font_size=28,
            color=TEXT_DIM,
            line_spacing=1.1,
            alignment="center"
        ).scale(13 / 28)
        desc_label4.next_to(year_label4, UP, buff=0.15)
        tick4 = Line(np.array([x4, -0.35, 0]), np.array([x4, -0.05, 0]), color=color4, stroke_width=2)

        self.play(
            FadeIn(dot4, scale=2), Create(tick4),
            FadeIn(year_label4, shift=DOWN * 0.2),
            FadeIn(desc_label4, shift=DOWN * 0.2),
            run_time=0.4,
        )
        dots.add(dot4, tick4)
        labels.add(year_label4, desc_label4)

        # Gap between Segment 11 & 12 (62.76s - 64.56s, dur 1.80s)
        self.wait(2.8)

        # Event 5: AFIS 1960s
        # Segment 12 (64.56s - 68.42s, dur 3.86s)
        x5, year5, desc5, color5 = events[4]
        dot5 = Dot(point=np.array([x5, -0.2, 0]), color=color5, radius=0.1)
        year_label5 = self.ct(year5, font_size=18, color=color5, weight=BOLD)
        year_label5.next_to(dot5, UP, buff=0.25)
        desc_label5 = Paragraph(
            *desc5.split("\n"),
            font_size=28,
            color=TEXT_DIM,
            line_spacing=1.1,
            alignment="center"
        ).scale(13 / 28)
        desc_label5.next_to(year_label5, UP, buff=0.15)
        tick5 = Line(np.array([x5, -0.35, 0]), np.array([x5, -0.05, 0]), color=color5, stroke_width=2)

        self.play(
            FadeIn(dot5, scale=2), Create(tick5),
            FadeIn(year_label5, shift=DOWN * 0.2),
            FadeIn(desc_label5, shift=DOWN * 0.2),
            run_time=0.4,
        )
        dots.add(dot5, tick5)
        labels.add(year_label5, desc_label5)

        # Segment 12 duration: 3.86s.
        # Elapsed: 0.40s.
        # Segment 12 resting wait: 3.86 - 0.40 = 3.46s.
        self.wait(3.46)
        
        # Gap between Segment 12 & 13 (68.42s - 69.28s, dur 0.86s)
        # Use this gap to fade out the timeline
        self.play(FadeOut(VGroup(timeline_line, dots, labels)), run_time=0.5)
        self.wait(0.36)

        # Segment 13 (69.28s - 77.52s, dur 8.24s)
        # 1. Forensic / Criminal Application (FBI) Panel
        forensic_title = self.ct("Ứng Dụng Pháp Y & Hình Sự", font_size=22, color=CHART_ORANGE, weight=BOLD)
        forensic_title.next_to(section, DOWN, buff=0.5)
        
        fbi_card = create_rounded_box(width=5.8, height=3.0, fill_color=CHART_ORANGE, fill_opacity=0.08, stroke_color=CHART_ORANGE, stroke_width=1.5)
        fbi_card.shift(DOWN * 0.3)
        
        fbi_fp = create_fingerprint_simple(color=CHART_ORANGE).scale(0.35)
        fbi_fp.move_to(fbi_card.get_center() + LEFT * 1.5)
        
        fbi_label = self.ct("Cơ sở dữ liệu FBI", font_size=16, color=TEXT_BRIGHT, weight=BOLD)
        fbi_desc = Paragraph(
            "Quản lý hơn 200 triệu bản ghi",
            "vân tay phục vụ điều tra hình sự",
            font_size=28, color=TEXT_DIM, alignment="left", line_spacing=1.2
        ).scale(12 / 28)
        fbi_text = VGroup(fbi_label, fbi_desc).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fbi_text.next_to(fbi_fp, RIGHT, buff=0.4)
        
        fbi_panel = VGroup(fbi_card, fbi_fp, fbi_text)

        self.play(
            FadeIn(forensic_title, shift=DOWN * 0.2),
            FadeIn(fbi_panel, shift=UP * 0.3),
            run_time=0.8
        )
        self.wait(2.0)

        self.play(
            FadeOut(forensic_title, shift=UP * 0.2),
            FadeOut(fbi_panel, shift=DOWN * 0.2),
            run_time=0.6
        )

        # 2. Civilian Applications Panel
        civil_title = self.ct("Ứng Dụng Đời Sống Dân Sự", font_size=22, color=PRIMARY, weight=BOLD)
        civil_title.next_to(section, DOWN, buff=0.5)
        
        # App 1: Thiết bị cá nhân
        app1 = create_rounded_box(width=3.6, height=2.8, fill_color=CHART_BLUE, fill_opacity=0.08, stroke_color=CHART_BLUE, stroke_width=1.5)
        app1_title = self.ct("Đăng Nhập Thiết Bị", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        app1_desc = Paragraph(
            "Mở khóa điện thoại, máy tính",
            "Touch ID, Windows Hello",
            font_size=28, color=TEXT_DIM, alignment="center", line_spacing=1.2
        ).scale(11 / 28)
        app1_content = VGroup(app1_title, app1_desc).arrange(DOWN, buff=0.2).move_to(app1.get_center())
        app1_group = VGroup(app1, app1_content)
        
        # App 2: Thương mại & Thanh toán
        app2 = create_rounded_box(width=3.6, height=2.8, fill_color=CHART_ORANGE, fill_opacity=0.08, stroke_color=CHART_ORANGE, stroke_width=1.5)
        app2_title = self.ct("Thương Mại & Thanh Toán", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        app2_desc = Paragraph(
            "Xác thực Apple Pay, ví điện tử",
            "Giao dịch trực tuyến bảo mật",
            font_size=28, color=TEXT_DIM, alignment="center", line_spacing=1.2
        ).scale(11 / 28)
        app2_content = VGroup(app2_title, app2_desc).arrange(DOWN, buff=0.2).move_to(app2.get_center())
        app2_group = VGroup(app2, app2_content)
        
        # App 3: Kiểm soát an ninh
        app3 = create_rounded_box(width=3.6, height=2.8, fill_color="#bd93f9", fill_opacity=0.08, stroke_color="#bd93f9", stroke_width=1.5)
        app3_title = self.ct("Kiểm Soát An Ninh", font_size=15, color=TEXT_BRIGHT, weight=BOLD)
        app3_desc = Paragraph(
            "Khóa cửa thông minh nhà ở",
            "Chấm công tự động doanh nghiệp",
            font_size=28, color=TEXT_DIM, alignment="center", line_spacing=1.2
        ).scale(11 / 28)
        app3_content = VGroup(app3_title, app3_desc).arrange(DOWN, buff=0.2).move_to(app3.get_center())
        app3_group = VGroup(app3, app3_content)
        
        civil_apps = VGroup(app1_group, app2_group, app3_group).arrange(RIGHT, buff=0.4).shift(DOWN * 0.3)
        
        self.play(
            FadeIn(civil_title, shift=DOWN * 0.2),
            run_time=0.5
        )
        self.play(
            LaggedStart(
                FadeIn(app1_group, shift=UP * 0.3),
                FadeIn(app2_group, shift=UP * 0.3),
                FadeIn(app3_group, shift=UP * 0.3),
                lag_ratio=0.15
            ),
            run_time=1.2
        )

        # Segment 13 duration: 8.24s.
        # Elapsed: 0.8 (fbi in) + 2.0 (wait) + 0.6 (fbi out) + 0.5 (civil title) + 1.2 (apps in) = 5.10s.
        # Segment 13 resting wait: 8.24 - 5.10 = 3.14s.
        self.wait(3.14)
        
        # Extended resting wait at the end of the scene before final fadeout
        self.wait(0.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
