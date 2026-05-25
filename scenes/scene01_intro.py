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
        self.wait(0.76)
        self.what_is_fingerprint()
        self.wait(0.01)
        self.why_fingerprints()
        self.wait(1.32)
        self.fingerprint_patterns()
        self.wait(3.34)
        self.history_timeline()

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kw):
        """create_text with CMU Serif kerning workaround (render big → scale down)."""
        return Text(text_str, font_size=36, color=color, weight=weight, **kw).scale(font_size / 36)

    def intro_title(self):
        """Chuỗi hoạt hình tiêu đề mở đầu — Segment 1 = 7.92s."""
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
        self.add(scan_group)
        self.play(
            FadeIn(fp_icon, run_time=2.0),
            scan_group.animate.move_to(DOWN * 2.5),
            Write(title, run_time=1.5),
            FadeIn(top_label, shift=DOWN * 0.3, run_time=1.0),
            run_time=2.0,
            rate_func=linear
        )
        self.play(FadeOut(scan_group, run_time=0.2))
        self.play(
            Create(line_left, run_time=0.6),
            Create(line_right, run_time=0.6),
        )
        self.play(FadeIn(subtitle, shift=UP * 0.2, run_time=0.8))

        # Total anim time = 2.0 (sweep) + 0.2 (fade scan) + 0.6 (lines) + 0.8 (subtitle) = 3.6s.
        # Need 7.92s total (including 1.0s FadeOut). Wait = 7.92 - 3.6 - 1.0 = 3.32s.
        self.wait(3.32)
        self.play(
            FadeOut(VGroup(title, top_label, lines, subtitle, fp_icon)),
            run_time=1.0,
        )

    def what_is_fingerprint(self):
        """Giải thích vân tay là gì — Segment 2 = 20.83s."""
        section = get_section_title("Vân tay là gì?")
        section.to_edge(UP, buff=0.6)
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
            Create(ridge_arrow, run_time=0.4),
            FadeIn(ridge_label, run_time=0.4),
            Create(valley_arrow, run_time=0.4),
            FadeIn(valley_label, run_time=0.4),
        )
        self.play(FadeIn(desc, shift=UP * 0.2, run_time=0.4))
        self.wait(1.38)  # Wait for Segment 3 end and gap before Segment 4

        # --- PHẦN PHÁT TRIỂN THÊM (DNA & Bào Thai & Mao mạch & Sinh đôi) ---
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

        self.play(FadeIn(dna_box), FadeIn(dna_title), run_time=0.5)
        self.play(
            LaggedStart(
                FadeIn(dna_helix), FadeIn(dna_label),
                FadeIn(fluid_waves), FadeIn(fluid_label),
                lag_ratio=0.2
            ),
            run_time=1.2
        )
        self.wait(2.22)  # Wait for Segment 4 end and gap before Segment 5

        # Segment 5 starts at 16.18s
        self.play(
            Create(capillary), FadeIn(capillary_label),
            run_time=1.0
        )
        self.wait(2.12)  # Wait for Segment 5 end

        # Gap between Segment 5 and 6 (19.30s to 20.58s)
        self.wait(1.28)

        # Segment 6 starts at 20.58s
        self.play(
            Indicate(fluid_waves, color=PRIMARY, scale_factor=1.3),
            Indicate(capillary, color="#e63946", scale_factor=1.3),
            run_time=1.5
        )
        self.wait(3.1)  # Wait for Segment 6 end

        # --- TWIN COMPARISON POP-UP INSIDE BOX ---
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

        # Transition DNA box interior (Segment 7 starts at 25.18s)
        self.play(
            FadeOut(initial_factors_seg4),
            FadeOut(capillary),
            FadeOut(capillary_label),
            FadeOut(dna_title),
            run_time=0.5
        )
        self.play(
            FadeIn(twin_group),
            run_time=0.8
        )
        self.play(
            Indicate(neq_sign, color=MISMATCH_COLOR, scale_factor=1.6),
            Indicate(diff_a, color=MINUTIA_TERM, scale_factor=2),
            Indicate(diff_b, color=MINUTIA_BIFUR, scale_factor=2),
            run_time=1.2
        )

        self.wait(1.56)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)

    def why_fingerprints(self):
        """Tại sao vân tay là đặc trưng sinh trắc tốt — Segment 3 = 11.33s."""
        section = get_section_title("Tại sao dùng vân tay?")
        section.to_edge(UP, buff=0.8)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

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

        # Show sequentially: Total target = 11.92s before next section
        self.wait(2.2)
        self.play(FadeIn(cards[0], shift=UP * 0.5, scale=0.9), run_time=0.6)
        self.wait(1.56)
        self.play(FadeIn(cards[1], shift=UP * 0.5, scale=0.9), run_time=0.6)
        self.wait(3.07)
        self.play(FadeIn(cards[2], shift=UP * 0.5, scale=0.9), run_time=0.6)
        
        # 0.6 (section in) + 2.2 (wait) + 0.6 (card 0) + 1.56 (wait) + 0.6 (card 1) + 3.07 (wait) + 0.6 (card 2) = 9.23s.
        # Remaining wait before fadeout: 11.92s - 9.23s - 0.8s (FadeOut) = 1.89s.
        self.wait(1.89)
        self.play(FadeOut(VGroup(section, cards)), run_time=0.8)

    def fingerprint_patterns(self):
        """Phân loại vân tay cơ bản — Segment 4 = 8.21s."""
        section = get_section_title("Các mẫu vân tay cơ bản")
        section.to_edge(UP, buff=0.8)
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

        self.wait(1.12)
        # Show cards
        self.play(FadeIn(cards[0], shift=UP * 0.5), run_time=0.4)
        self.wait(2.1)
        self.play(FadeIn(cards[1], shift=UP * 0.5), run_time=0.4)
        self.wait(1.1)
        self.play(FadeIn(cards[2], shift=UP * 0.5), run_time=0.4)

        # Target = 6.64s.
        # Elapsed so far: 0.4 (section) + 1.12 (wait) + 0.4 (card0) + 2.1 (wait) + 0.4 (card1) + 1.1 (wait) + 0.4 (card2) = 5.92s.
        # Remaining wait before fadeout: 6.64 - 5.92 - 0.4 (FadeOut) = 0.32s.
        self.wait(0.32)
        self.play(FadeOut(VGroup(section, cards)), run_time=0.4)

    def history_timeline(self):
        """Lịch sử phát triển nhận dạng vân tay — Segment 5 = 26.57s."""
        section = get_section_title("Lịch sử phát triển")
        section.to_edge(UP, buff=0.8)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        timeline_line = Line(LEFT * 5.5, RIGHT * 5.5, color=TEXT_DIM, stroke_width=2)
        timeline_line.shift(DOWN * 0.2)
        self.play(Create(timeline_line), run_time=0.8)

        events = [
            (-4.5, "1686", "Malpighi\nghi nhận\nđường vân", CHART_BLUE),
            (-1.8, "1880", "Fauld đề xuất\ntính duy nhất\ncủa vân tay", CHART_ORANGE),
            (-0.2, "1888", "Galton giới thiệu\nđặc trưng\nminutiae", "#bd93f9"),
            (1.8, "1899", "Hệ thống phân\nloại Henry\nra đời", PRIMARY),
            (4.2, "1960s", "Hệ thống AFIS\ntự động đầu\ntiên", CORE_POINT),
        ]

        dots = VGroup()
        labels = VGroup()

        # Wait times for timeline elements (aligned with historical overview narration)
        # Segment 10: 0.6s (line draw) + 0.5s (event 1) + 1.44s (wait) = 2.54s + 0.2s = 2.74s (start to start)
        # Segment 11: 0.5s (event 2) + 1.8s (wait) + 0.5s (event 3) + 2.2s (wait) + 0.5s (event 4) + 2.86s (wait) = 8.36s (start to start)
        # Segment 12: 0.5s (event 5) + 3.72s (wait) + 0.5s (fadeout) = 4.72s (start to start)
        wait_times = [1.44, 1.8, 2.2, 2.86, 3.72]

        for i, (x, year, desc, color) in enumerate(events):
            dot = Dot(point=np.array([x, -0.2, 0]), color=color, radius=0.1)
            year_label = self.ct(year, font_size=18, color=color, weight=BOLD)
            year_label.next_to(dot, UP, buff=0.25)
            desc_label = Paragraph(
                *desc.split("\n"),
                font_size=28,
                color=TEXT_DIM,
                line_spacing=1.1,
                alignment="center"
            ).scale(13 / 28)
            desc_label.next_to(year_label, UP, buff=0.15)
            tick = Line(np.array([x, -0.35, 0]), np.array([x, -0.05, 0]), color=color, stroke_width=2)
            
            self.play(
                FadeIn(dot, scale=2), Create(tick),
                FadeIn(year_label, shift=DOWN * 0.2),
                FadeIn(desc_label, shift=DOWN * 0.2),
                run_time=0.5,
            )
            dots.add(dot, tick)
            labels.add(year_label, desc_label)
            self.wait(wait_times[i])

        # At this point, we fade out the timeline and show the forensic/civilian applications
        self.play(FadeOut(VGroup(timeline_line, dots, labels)), run_time=0.5)

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
            run_time=0.5
        )
        self.wait(2.0)

        self.play(
            FadeOut(forensic_title, shift=UP * 0.2),
            FadeOut(fbi_panel, shift=DOWN * 0.2),
            run_time=0.5
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
            run_time=0.4
        )
        self.play(
            LaggedStart(
                FadeIn(app1_group, shift=UP * 0.3),
                FadeIn(app2_group, shift=UP * 0.3),
                FadeIn(app3_group, shift=UP * 0.3),
                lag_ratio=0.2
            ),
            run_time=0.8
        )

        # Segment 13 duration is 8.24s.
        # Forensic Panel: 0.5s (fbi in) + 2.0s (fbi wait) + 0.5s (fbi out) = 3.0s
        # Civilian Panel: 0.4s (civil in) + 0.8s (apps in) + 3.04s (civil wait) + 1.0s (FadeOut) = 5.24s
        # Total: 3.0s + 5.24s = 8.24s (Exact)
        self.wait(3.04)
        self.play(FadeOut(VGroup(section, civil_title, civil_apps)), run_time=1.0)
