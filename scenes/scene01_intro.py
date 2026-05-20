"""
Scene 1: Giới thiệu về Nhận dạng Vân tay (Không có giọng nói)
- Tiêu đề mở đầu
- Vân tay là gì? (đường vân và rãnh)
- Tại sao vân tay là đặc trưng sinh trắc tốt
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

    def intro_title(self):
        """Chuỗi hoạt hình tiêu đề mở đầu."""
        # Nhãn nhỏ phía trên
        top_label = Text(
            "N H Ậ N   D Ạ N G   M Ẫ U",
            font_size=16,
            color=TEXT_DIM,
        ).to_edge(UP, buff=1.5)

        # Tiêu đề chính
        title = Text(
            "Nhận Dạng Vân Tay",
            font_size=56,
            color=TEXT_BRIGHT,
            weight=BOLD,
        )

        # Đường trang trí
        line_left = Line(LEFT * 3.5, LEFT * 0.5, color=PRIMARY, stroke_width=2)
        line_right = Line(RIGHT * 0.5, RIGHT * 3.5, color=PRIMARY, stroke_width=2)
        lines = VGroup(line_left, line_right).next_to(title, DOWN, buff=0.3)

        # Phụ đề
        subtitle = Text(
            "Máy tính nhận diện danh tính bạn như thế nào?",
            font_size=24,
            color=RIDGE_COLOR,
        ).next_to(lines, DOWN, buff=0.4)

        # Icon vân tay
        fp_icon = create_fingerprint_simple(scale=0.6, color=RIDGE_COLOR)
        fp_icon.set_opacity(0.15).scale(2).move_to(ORIGIN)

        self.play(FadeIn(fp_icon, run_time=2))
        self.play(
            Write(title, run_time=1.5),
            FadeIn(top_label, shift=DOWN * 0.3),
        )
        self.play(
            Create(line_left),
            Create(line_right),
        )
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        self.wait(3.35)
        self.play(
            FadeOut(VGroup(title, top_label, lines, subtitle, fp_icon)),
            run_time=1,
        )

    def what_is_fingerprint(self):
        """Giải thích vân tay là gì - đường vân và rãnh."""
        section = get_section_title("Vân tay là gì?")
        section.to_edge(UP, buff=0.8)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Tạo visualization đường vân
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

        ridges_group.shift(DOWN * 0.3)

        # Nhãn cho đường vân và rãnh
        ridge_label = Text("Đường vân (Ridge)", font_size=36, color=RIDGE_COLOR).scale(20 / 36)
        valley_label = Text("Rãnh (Valley)", font_size=36, color=TEXT_DIM).scale(20 / 36)

        ridge_arrow = Arrow(
            RIGHT * 4.2 + DOWN * 0.3,
            RIGHT * 2.7 + DOWN * 0.3,
            color=RIDGE_COLOR,
            stroke_width=2,
        )
        ridge_label.next_to(ridge_arrow, RIGHT, buff=0.1)

        valley_arrow = Arrow(
            RIGHT * 4.2 + UP * 0.17,
            RIGHT * 2.7 + UP * 0.17,
            color=TEXT_DIM,
            stroke_width=2,
        )
        valley_label.next_to(valley_arrow, RIGHT, buff=0.1)

        desc = Text(
            "Vân tay = hệ thống các đường vân và rãnh xen kẽ nhau",
            font_size=36,
            color=TEXT_COLOR,
        ).scale(20 / 36).to_edge(DOWN, buff=0.8)

        self.play(
            LaggedStart(
                *[Create(r, run_time=0.8) for r in ridges_group],
                lag_ratio=0.15,
            ),
        )
        self.wait(0.5)
        self.play(
            Create(ridge_arrow),
            FadeIn(ridge_label),
        )
        self.play(
            Create(valley_arrow),
            FadeIn(valley_label),
        )
        self.play(FadeIn(desc, shift=UP * 0.2))

        self.wait(1.53)
        self.play(FadeOut(VGroup(
            section, ridges_group, ridge_arrow, ridge_label,
            valley_arrow, valley_label, desc,
        )))

    def why_fingerprints(self):
        """Tại sao vân tay là đặc trưng sinh trắc tốt."""
        section = get_section_title("Tại sao dùng vân tay?")
        section.to_edge(UP, buff=0.8)
        self.play(FadeIn(section, shift=DOWN * 0.3))

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
            title = Text(title_text, font_size=36, color=TEXT_BRIGHT, weight=BOLD).scale(24 / 36)
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

        # Hiện từng thẻ khớp với tiếng nói
        self.play(FadeIn(cards[0], shift=UP * 0.5, scale=0.9))
        self.wait(3.50)
        self.play(FadeIn(cards[1], shift=UP * 0.5, scale=0.9))
        self.wait(2.70)
        self.play(FadeIn(cards[2], shift=UP * 0.5, scale=0.9))
        self.wait(2.46)

        self.play(FadeOut(VGroup(section, cards)))

    def fingerprint_patterns(self):
        """Phân loại vân tay cơ bản."""
        section = get_section_title("Các mẫu vân tay cơ bản")
        section.to_edge(UP, buff=0.8)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        patterns = [
            ("Vân Móc", "Khoảng 65% dân số.\nĐường vân cong\nvà quay trở lại."),
            ("Vân Xoáy", "Khoảng 30% dân số.\nĐường vân xoay tròn\nquanh tâm."),
            ("Vân Cung", "Khoảng 5% dân số.\nĐường vân đi từ\nbên này sang bên kia."),
        ]

        # Tải hình ảnh 3 loại vân tay từ file SVG
        icons = VGroup()
        
        loop_icon = SVGMobject("assets/loop.svg").set_color(RIDGE_COLOR)
        whorl_icon = SVGMobject("assets/whorl.svg").set_color(RIDGE_COLOR)
        arch_icon = SVGMobject("assets/arch.svg").set_color(RIDGE_COLOR)

        icons.add(loop_icon, whorl_icon, arch_icon)

        cards = VGroup()
        for icon, (title_text, desc_text) in zip(icons, patterns):
            bg = create_rounded_box(width=2.5, height=2.5, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=PRIMARY, stroke_width=1.5)
            icon.scale_to_fit_height(1.8)
            icon.move_to(bg.get_center())
            icon_group = VGroup(bg, icon)

            title = Text(title_text, font_size=32, color=TEXT_BRIGHT, weight=BOLD).scale(20 / 32)
            desc = Paragraph(
                *desc_text.split("\n"),
                font_size=28, color=TEXT_DIM, alignment="center", line_spacing=1.2
            ).scale(15 / 28)
            card = VGroup(icon_group, title, desc).arrange(DOWN, buff=0.3)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.8).shift(DOWN * 0.2)

        # Hiện từng loại vân tay khớp với tiếng nói
        self.play(FadeIn(cards[0], shift=UP * 0.5))
        self.wait(2.50)
        self.play(FadeIn(cards[1], shift=UP * 0.5))
        self.wait(1.20)
        self.play(FadeIn(cards[2], shift=UP * 0.5))
        self.wait(2.56)

        self.play(FadeOut(VGroup(section, cards)))

    def history_timeline(self):
        """Lịch sử phát triển nhận dạng vân tay."""
        section = get_section_title("Lịch sử phát triển")
        section.to_edge(UP, buff=0.8)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        timeline_line = Line(LEFT * 5.5, RIGHT * 5.5, color=TEXT_DIM, stroke_width=2)
        timeline_line.shift(DOWN * 0.2)

        self.play(Create(timeline_line))

        events = [
            (-4.5, "1686", "Malpighi\nghi nhận\nđường vân", CHART_BLUE),
            (-1.8, "1880", "Fauld đề xuất\ntính duy nhất\ncủa vân tay", CHART_ORANGE),
            (-0.2, "1888", "Galton giới thiệu\nđặc trưng\nminutiae", CHART_PURPLE),
            (1.8, "1899", "Hệ thống phân\nloại Henry\nra đời", PRIMARY),
            (4.2, "1960s", "Hệ thống AFIS\ntự động đầu\ntiên", CORE_POINT),
        ]

        dots = VGroup()
        labels = VGroup()

        # Thời gian chờ ngắn giữa mỗi mốc (audio đọc liên tục)
        event_wait_times = [0.4, 0.4, 0.4, 0.4, 0.4]

        for i, (x, year, desc, color) in enumerate(events):
            dot = Dot(point=np.array([x, -0.2, 0]), color=color, radius=0.1)
            year_label = Text(year, font_size=36, color=color, weight=BOLD).scale(18 / 36)
            year_label.next_to(dot, UP, buff=0.25)
            desc_label = Paragraph(
                *desc.split("\n"),
                font_size=28,
                color=TEXT_DIM,
                line_spacing=1.1,
                alignment="center"
            ).scale(13 / 28)
            desc_label.next_to(year_label, UP, buff=0.15)
            tick = Line(
                np.array([x, -0.35, 0]),
                np.array([x, -0.05, 0]),
                color=color, stroke_width=2,
            )
            self.play(
                FadeIn(dot, scale=2), Create(tick),
                FadeIn(year_label, shift=DOWN * 0.2),
                FadeIn(desc_label, shift=DOWN * 0.2),
                run_time=0.7,
            )
            dots.add(dot, tick)
            labels.add(year_label, desc_label)
            self.wait(event_wait_times[i])

        modern_note = Text(
            "Ngày nay: Hơn 200 triệu bản ghi vân tay tại FBI",
            font_size=36, color=RIDGE_COLOR,
        ).scale(18 / 36).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(modern_note, shift=UP * 0.2))
        self.wait(4.02)

        self.play(FadeOut(VGroup(section, timeline_line, dots, labels, modern_note)))
        self.wait(0.3)
