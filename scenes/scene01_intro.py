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
        self.wait(0.85)
        self.what_is_fingerprint()
        self.wait(0.85)
        self.why_fingerprints()
        self.wait(0.85)
        self.fingerprint_patterns()
        self.wait(0.88)
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

        # Drawing the fingerprint in the background (Premium effect)
        self.play(Create(fp_icon, run_time=2.0))
        self.play(
            Write(title, run_time=1.2),
            FadeIn(top_label, shift=DOWN * 0.3, run_time=0.8),
        )
        self.play(
            Create(line_left, run_time=0.6),
            Create(line_right, run_time=0.6),
        )
        self.play(FadeIn(subtitle, shift=UP * 0.2, run_time=0.8))

        # Total anim time = 2.0 + 1.2 + 0.6 + 0.8 = 4.6s. Need 7.22s before FadeOut completes.
        self.wait(1.62)
        self.play(
            FadeOut(VGroup(title, top_label, lines, subtitle, fp_icon)),
            run_time=1.0,
        )

    def what_is_fingerprint(self):
        """Giải thích vân tay là gì — Segment 2 = 20.83s."""
        section = get_section_title("Vân tay là gì?")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

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

        ridge_label = self.ct("Đường vân", font_size=16, color=RIDGE_COLOR)  # Bỏ định nghĩa tiếng Anh
        valley_label = self.ct("Rãnh", font_size=16, color=TEXT_DIM)  # Bỏ định nghĩa tiếng Anh

        ridge_arrow = Arrow(LEFT * 0.5 + DOWN * 0.5, LEFT * 1.5 + DOWN * 0.5, color=RIDGE_COLOR, stroke_width=2)
        ridge_label.next_to(ridge_arrow, RIGHT, buff=0.1)

        valley_arrow = Arrow(LEFT * 0.5 + DOWN * 0.1, LEFT * 1.5 + DOWN * 0.1, color=TEXT_DIM, stroke_width=2)
        valley_label.next_to(valley_arrow, RIGHT, buff=0.1)

        desc = self.ct("Hệ thống các đường vân và rãnh xen kẽ nhau", font_size=18, color=TEXT_BRIGHT)
        desc.next_to(ridges_group, DOWN, buff=0.4)

        # Laser Scan effect
        scan_line = Line(LEFT * 6.0, LEFT * 1.0, color=PRIMARY, stroke_width=3).set_opacity(0.8)
        scan_line.move_to(LEFT * 4.0 + UP * 1.0)

        self.play(FadeIn(scan_line, run_time=0.4))
        self.play(
            scan_line.animate.move_to(LEFT * 4.0 + DOWN * 2.4),  # Kéo dài thêm một chút
            LaggedStart(*[Create(r) for r in ridges_group], lag_ratio=0.1),
            run_time=1.5
        )
        self.play(FadeOut(scan_line, run_time=0.3))

        self.play(
            Create(ridge_arrow, run_time=1),
            FadeIn(ridge_label, run_time=1),
        )
        self.wait(0.2)
        self.play(
            Create(valley_arrow, run_time=1),
            FadeIn(valley_label, run_time=1),
        )
        self.play(FadeIn(desc, shift=UP * 0.2, run_time=0.6))
        self.wait(0.40)

        # --- PHẦN PHÁT TRIỂN THÊM (DNA & Bào Thai & Sinh đôi) ---
        # Hộp minh họa ADN & Môi trường bào thai xuất hiện bên phải
        dna_box = create_rounded_box(width=4.5, height=3.0, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=PRIMARY, stroke_width=1.5)
        dna_box.shift(RIGHT * 3.8 + DOWN * 0.3)
        dna_title = self.ct("Yếu tố hình thành", font_size=18, color=PRIMARY, weight=BOLD).next_to(dna_box.get_top(), DOWN, buff=0.25)
        
        # DNA helix representation
        dna_helix = VGroup()
        for x_val in np.linspace(-1.5, 1.5, 12):
            y_offset = 0.5 * np.sin(2 * np.pi * x_val)
            dot1 = Dot([x_val, y_offset, 0], color=CHART_BLUE, radius=0.06)
            dot2 = Dot([x_val, -y_offset, 0], color=CHART_ORANGE, radius=0.06)
            link = Line([x_val, y_offset, 0], [x_val, -y_offset, 0], stroke_width=1, color=TEXT_DIM).set_opacity(0.4)
            dna_helix.add(dot1, dot2, link)
        dna_helix.scale(0.8).move_to(dna_box.get_center() + UP * 0.3)
        dna_label = self.ct("1. Di truyền", font_size=13, color=CHART_BLUE).next_to(dna_helix, DOWN, buff=0.25)

        # Ripples representing fluid environment
        fluid_waves = VGroup()
        for idx in range(3):
            wave = Arc(radius=0.2 + idx * 0.15, start_angle=-PI/4, angle=PI/2, stroke_width=1.5, color=PRIMARY).set_opacity(0.6 - idx*0.15)
            fluid_waves.add(wave)
        fluid_waves.move_to(dna_box.get_center() + DOWN * 0.7 + LEFT * 0.8)
        fluid_label = self.ct("2. Mật độ nước ối & Vị trí thai nhi", font_size=13, color=CHART_ORANGE).next_to(dna_label, DOWN, buff=0.2)
        fluid_group = VGroup(fluid_waves, fluid_label)

        self.play(FadeIn(dna_box), FadeIn(dna_title), run_time=0.6)
        self.play(Create(dna_helix), FadeIn(dna_label), run_time=1.0)
        
        self.play(FadeIn(fluid_label), run_time=1.0)
        self.wait(11.48)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)

    def why_fingerprints(self):
        """Tại sao vân tay là đặc trưng sinh trắc tốt — Segment 3 = 11.33s."""
        section = get_section_title("Tại sao dùng vân tay?")
        section.to_edge(UP, buff=0.8)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        properties = [
            ("Duy nhất", "Ngay cả cặp sinh đôi\ncùng trứng cũng có\nvân tay khác nhau"),
            ("Bền vững", "Ổn định từ tháng thứ 7\nthai kỳ và không\nthay đổi suốt đời"),
            ("Đo lường được", "Có thể thu nhận\nbằng các cảm biến\nđiện tử hiện đại"),
        ]

        cards = VGroup()
        for title_text, desc_text in properties:
            card = create_rounded_box(
                width=3.5, height=2.8,
                fill_color=SECONDARY, fill_opacity=0.3,
                stroke_color=PRIMARY, stroke_width=1.5,
            )
            title = self.ct(title_text, font_size=24, color=TEXT_BRIGHT, weight=BOLD)
            desc = Paragraph(
                *desc_text.split("\n"),
                font_size=30,
                color=TEXT_DIM,
                line_spacing=1.2,
                alignment="center"
            ).scale(15 / 30)
            content = VGroup(title, desc).arrange(DOWN, buff=0.25)
            content.move_to(card.get_center())
            cards.add(VGroup(card, content))

        cards.arrange(RIGHT, buff=0.5).shift(DOWN * 0.3)

        # Show sequentially: Total target = 11.97s before next section
        self.play(FadeIn(cards[0], shift=UP * 0.5, scale=0.9), run_time=0.6)
        self.wait(2.7)
        self.play(FadeIn(cards[1], shift=UP * 0.5, scale=0.9), run_time=0.6)
        self.wait(2.7)
        self.play(FadeIn(cards[2], shift=UP * 0.5, scale=0.9), run_time=0.6)
        self.wait(2.97)
        self.play(FadeOut(VGroup(section, cards)), run_time=0.8)
        self.wait(0.4)

    def fingerprint_patterns(self):
        """Phân loại vân tay cơ bản — Segment 4 = 8.21s."""
        section = get_section_title("Các mẫu vân tay cơ bản")
        section.to_edge(UP, buff=0.8)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        patterns = [
            ("Vân Móc", "Khoảng 65% dân số.\nĐường vân cong\nvà quay trở lại."),
            ("Vân Xoáy", "Khoảng 30% dân số.\nĐường vân xoay tròn\nquanh tâm."),
            ("Vân Cung", "Khoảng 5% dân số.\nĐường vân đi từ\nbên này sang bên kia."),
        ]

        from pathlib import Path
        assets_dir = Path(__file__).resolve().parent.parent / "assets"

        # Load SVG assets
        loop_icon = SVGMobject(str(assets_dir / "loop.svg")).scale_to_fit_height(1.4).set_color(RIDGE_COLOR)
        whorl_icon = SVGMobject(str(assets_dir / "whorl.svg")).scale_to_fit_height(1.4).set_color(RIDGE_COLOR)
        arch_icon = SVGMobject(str(assets_dir / "arch.svg")).scale_to_fit_height(1.4).set_color(RIDGE_COLOR)

        icons = VGroup(loop_icon, whorl_icon, arch_icon)

        cards = VGroup()
        for icon, (title_text, desc_text) in zip(icons, patterns):
            bg = create_rounded_box(width=2.8, height=2.8, fill_color=SECONDARY, fill_opacity=0.1, stroke_color=PRIMARY, stroke_width=1.5)
            icon.move_to(bg.get_center() + UP * 0.1)
            icon_group = VGroup(bg, icon)

            title = self.ct(title_text, font_size=20, color=TEXT_BRIGHT, weight=BOLD)
            desc = Paragraph(
                *desc_text.split("\n"),
                font_size=28, color=TEXT_DIM, alignment="center", line_spacing=1.2
            ).scale(15 / 28)
            card = VGroup(icon_group, title, desc).arrange(DOWN, buff=0.25)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.6).shift(DOWN * 0.2)

        # Show cards: Target = 7.62s before next section
        self.play(FadeIn(cards[0], shift=UP * 0.5), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(cards[1], shift=UP * 0.5), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(cards[2], shift=UP * 0.5), run_time=0.6)
        self.wait(2.42)
        self.play(FadeOut(VGroup(section, cards)), run_time=0.8)

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
            (-0.2, "1888", "Galton giới thiệu\nđặc trưng\nminutiae", CHART_PURPLE),
            (1.8, "1899", "Hệ thống phân\nloại Henry\nra đời", PRIMARY),
            (4.2, "1960s", "Hệ thống AFIS\ntự động đầu\ntiên", CORE_POINT),
        ]

        dots = VGroup()
        labels = VGroup()

        # Custom wait times for each event to match the narration speed of each sentence
        # Event 1: Malpighi (1686) -> wait 1.7s
        # Event 2: Fauld (1880) -> wait 2.2s
        # Event 3: Galton (1888) -> wait 2.2s
        # Event 4: Henry (1899) -> wait 2.2s
        # Event 5: AFIS (1960s) -> wait 2.2s
        wait_times = [1.7, 2.2, 2.2, 2.2, 2.2]

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

        # Elapsed: 0.6 + 0.8 + 5 * 0.5 + 1.7 + 2.2 * 4 = 14.4s.
        modern_note = self.ct("Ngày nay: Hơn 200 triệu bản ghi vân tay tại FBI", font_size=18, color=RIDGE_COLOR)
        modern_note.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(modern_note, shift=UP * 0.2), run_time=0.6)
        
        # 14.4 + 0.6 = 15.0s. Need 26.78s.
        self.wait(10.78)
        self.play(FadeOut(VGroup(section, timeline_line, dots, labels, modern_note)), run_time=1.0)
