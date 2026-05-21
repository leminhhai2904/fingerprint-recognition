"""
Scene 5: Đối sánh dựa trên tương quan (Correlation-based Matching)
- Thách thức đối sánh vân tay
- Ba họ phương pháp đối sánh
- Đối sánh tương quan chéo + Khớp hộp sáng nháy xanh lá
- Vấn đề của tương quan trực tiếp
"""
from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene05Correlation(Scene):
    def construct(self):
        scene_setup(self)
        self.section_title()
        self.three_methods()
        self.correlation_concept()
        self.correlation_problems()

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
        """Tiêu đề mục + Thách thức — Segment 1 = 16.99s."""
        num = self.ct("04", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Đối Sánh Vân Tay", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("So sánh vân tay để xác thực danh tính", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)

        # Show challenges text
        challenges = self.ct(
            "Thách thức: Lệch vị trí lớn, biến dạng cơ học, thay đổi da, lỗi trích xuất đặc trưng",
            font_size=16, color=DELTA_COLOR, weight=BOLD
        ).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(challenges, shift=UP * 0.2), run_time=0.8)

        # Target = 16.99s. Anim play = 3.3s. FadeOut = 1.0s. Need 12.69s wait.
        self.wait(12.69)
        self.play(FadeOut(VGroup(group, challenges)), run_time=1.0)
        self.wait(0.8) # Silence gap

    def three_methods(self):
        """Ba họ phương pháp đối sánh — Segment 2 = 11.38s."""
        section = self.get_section_hdr("Ba phương pháp đối sánh")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        approaches = [
            ("1", "Dựa trên tương quan", CHART_BLUE, "So sánh trực tiếp\ncường độ pixel"),
            ("2", "Dựa trên Minutiae", CHART_ORANGE, "Đối sánh tập điểm\nđặc trưng cục bộ"),
            ("3", "Dựa trên đặc trưng vân", CHART_PURPLE, "Duyệt kết cấu đường vân\nvà trường hướng"),
        ]

        cards = VGroup()
        for num_text, name, color, desc in approaches:
            box = create_rounded_box(
                width=3.6, height=3.0,
                fill_color=color, fill_opacity=0.08,
                stroke_color=color, stroke_width=1.5,
            )
            num_label = self.ct(num_text, font_size=36, color=color, weight=BOLD)
            name_label = self.ct(name, font_size=18, color=TEXT_BRIGHT, weight=BOLD)
            desc_label = Paragraph(
                *desc.split("\n"),
                font_size=28, color=TEXT_DIM, alignment="center", line_spacing=1.2
            ).scale(14 / 28)
            content = VGroup(num_label, name_label, desc_label).arrange(DOWN, buff=0.25)
            content.move_to(box)
            cards.add(VGroup(box, content))

        cards.arrange(RIGHT, buff=0.4).shift(DOWN * 0.4)

        # Show cards sequentially matching audio: Target = 11.38s before FadeOut
        self.play(FadeIn(cards[0], shift=UP * 0.4), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(cards[1], shift=UP * 0.4), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(cards[2], shift=UP * 0.4), run_time=0.8)
        self.wait(3.38)

        self.play(FadeOut(VGroup(section, cards)), run_time=1.0)
        self.wait(0.8)

    def correlation_concept(self):
        """Minh họa đối sánh tương quan chéo — Segment 3 = 17.40s."""
        section = self.get_section_hdr("Đối sánh dựa trên tương quan")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Ảnh mẫu T (trái)
        t_box = Square(side_length=2.5, color=CHART_BLUE, stroke_width=2)
        t_label = self.ct("Mẫu T", font_size=18, color=CHART_BLUE, weight=BOLD)
        t_label.next_to(t_box, UP, buff=0.2)

        t_ridges = VGroup()
        for i in range(6):
            y = (i - 2.5) * 0.25
            ridge = Line(LEFT * 0.9 + UP * y, RIGHT * 0.9 + UP * y, color=RIDGE_COLOR, stroke_width=3)
            t_ridges.add(ridge)
        t_ridges.move_to(t_box)
        t_group = VGroup(t_box, t_ridges, t_label).shift(LEFT * 4)

        # Ảnh đầu vào I (phải)
        i_box = Square(side_length=2.5, color=CHART_ORANGE, stroke_width=2)
        i_label = self.ct("Đầu vào I", font_size=18, color=CHART_ORANGE, weight=BOLD)
        i_label.next_to(i_box, UP, buff=0.2)

        i_ridges = VGroup()
        for i in range(6):
            y = (i - 2.5) * 0.25
            ridge = Line(LEFT * 0.9 + UP * y, RIGHT * 0.9 + UP * y, color=RIDGE_COLOR, stroke_width=3)
            i_ridges.add(ridge)
        i_ridges.move_to(i_box)
        i_ridges.shift(RIGHT * 0.15 + UP * 0.1)
        i_ridges.rotate(0.15, about_point=i_box.get_center())
        i_group = VGroup(i_box, i_ridges, i_label).shift(RIGHT * 1)

        formula = MathTex(
            r"S(T, I) = \max_{\Delta x, \Delta y, \theta} \text{CC}(T, I_{(\Delta x, \Delta y, \theta)})",
            font_size=28, color=TEXT_BRIGHT,
        ).to_edge(DOWN, buff=1.5)

        search_text = self.ct("Tìm căn chỉnh tốt nhất (Δx, Δy, θ)", font_size=16, color=PRIMARY)
        search_text.next_to(formula, UP, buff=0.3)

        score = self.ct("Điểm CC: 0.94", font_size=20, color=MATCH_COLOR, weight=BOLD)
        score.next_to(i_group, DOWN, buff=0.5)

        self.play(FadeIn(t_group), FadeIn(i_group), run_time=0.8)
        self.play(Write(formula), run_time=0.8)
        self.play(FadeIn(search_text), run_time=0.6)
        
        self.play(
            i_ridges.animate.shift(LEFT * 0.15 + DOWN * 0.1).rotate(-0.15, about_point=i_box.get_center()),
            run_time=2.0, rate_func=smooth,
        )
        
        # Match Green Flash (Premium visual)
        flash_box = i_box.copy().set_color(MATCH_COLOR).set_stroke(width=4)
        self.play(
            FadeIn(score, scale=1.5),
            Create(flash_box),
            run_time=0.6
        )
        self.play(FadeOut(flash_box), run_time=0.4)

        # Target = 17.40s. Anim play = 0.6 + 0.8 + 0.8 + 0.6 + 2.0 + 0.6 + 0.4 = 5.8s. FadeOut = 1.0s. Need 10.60s wait.
        self.wait(10.60)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    def correlation_problems(self):
        """Hiển thị các vấn đề khi dùng tương quan trực tiếp — Segment 4 = 14.42s."""
        section = self.get_section_hdr("Thách thức của phương pháp tương quan")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        problems = [
            ("Biến dạng phi tuyến", "Áp lực ngón tay gây biến dạng không đồng đều", MINUTIA_TERM),
            ("Điều kiện thay đổi", "Độ sáng, tương phản, độ dày đường vân biến đổi", CHART_ORANGE),
            ("Chi phí tính toán", "Tìm kiếm trên toàn bộ không gian (Δx, Δy, θ) rất tốn kém", CHART_PURPLE),
        ]

        problem_groups = VGroup()
        for title, desc, color in problems:
            icon = VGroup(
                Circle(radius=0.25, color=color, stroke_width=2),
                self.ct("!", font_size=20, color=color, weight=BOLD),
            )
            title_text = self.ct(title, font_size=20, color=color, weight=BOLD)
            desc_text = self.ct(desc, font_size=15, color=TEXT_DIM)
            row = VGroup(icon, VGroup(title_text, desc_text).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
            row.arrange(RIGHT, buff=0.4)
            problem_groups.add(row)

        problem_groups.arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(DOWN * 0.3)

        solution = self.ct("→ Giải pháp: Sử dụng đối sánh dựa trên minutiae!", font_size=20, color=MATCH_COLOR, weight=BOLD)
        solution.to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in problem_groups], lag_ratio=0.4),
            run_time=2.0,
        )
        self.play(FadeIn(solution, shift=UP * 0.2), run_time=0.8)

        # Target = 14.42s. Anim play = 0.6 + 2.0 + 0.8 = 3.4s. FadeOut = 1.0s. Need 10.02s wait.
        self.wait(10.02)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
