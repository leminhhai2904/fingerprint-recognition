"""
Scene 5: Đối sánh dựa trên tương quan (Correlation-based Matching) (Không có giọng nói)
- Khái niệm tương quan chéo
- Trượt cửa sổ căn chỉnh
- Các vấn đề khi dùng tương quan trực tiếp
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
        self.correlation_concept()
        self.correlation_problems()

    def section_title(self):
        """Tiêu đề mục."""
        num = Text("04", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = Text("Đối Sánh Vân Tay", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = Text(
            "Làm thế nào để so sánh hai vân tay?",
            font_size=22, color=TEXT_DIM,
        )
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3))
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        self.wait(0.5)
        self.play(FadeOut(group))

        # Tổng quan 3 phương pháp
        families_title = get_section_title("Ba phương pháp đối sánh")
        families_title.to_edge(UP, buff=0.6)
        self.play(FadeIn(families_title, shift=DOWN * 0.3))

        approaches = [
            ("1", "Dựa trên\ntương quan", CHART_BLUE, "So sánh mẫu\ncường độ pixel"),
            ("2", "Dựa trên\nminutiae", CHART_ORANGE, "Đối sánh tập\nđiểm minutiae"),
            ("3", "Dựa trên\nđặc trưng vân", CHART_PURPLE, "Sử dụng kết cấu\nvà đặc trưng cục bộ"),
        ]

        cards = VGroup()
        for num_text, name, color, desc in approaches:
            box = create_rounded_box(
                width=3.2, height=2.8,
                fill_color=color, fill_opacity=0.08,
                stroke_color=color, stroke_width=1.5,
            )
            num_label = Text(num_text, font_size=36, color=color, weight=BOLD)
            name_label = Text(name, font_size=18, color=TEXT_BRIGHT, weight=BOLD)
            desc_label = Text(desc, font_size=14, color=TEXT_DIM, line_spacing=1.2)
            content = VGroup(num_label, name_label, desc_label).arrange(DOWN, buff=0.25)
            content.move_to(box)
            cards.add(VGroup(box, content))

        cards.arrange(RIGHT, buff=0.6).shift(DOWN * 0.4)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.4) for c in cards],
                lag_ratio=0.3,
            ),
            run_time=2,
        )

        self.wait(1)
        self.play(FadeOut(VGroup(families_title, cards)))

    def correlation_concept(self):
        """Minh họa đối sánh tương quan chéo."""
        section = get_section_title("Đối sánh dựa trên tương quan")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Ảnh mẫu T (trái)
        t_box = Square(side_length=2.5, color=CHART_BLUE, stroke_width=2)
        t_label = Text("Mẫu T", font_size=18, color=CHART_BLUE, weight=BOLD)
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
        i_label = Text("Đầu vào I", font_size=18, color=CHART_ORANGE, weight=BOLD)
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

        search_text = Text(
            "Tìm căn chỉnh tốt nhất (Δx, Δy, θ)",
            font_size=16, color=PRIMARY,
        ).next_to(formula, UP, buff=0.3)

        score = Text("Điểm CC: 0.94", font_size=20, color=MATCH_COLOR, weight=BOLD)
        score.next_to(i_group, DOWN, buff=0.5)

        self.play(FadeIn(t_group), FadeIn(i_group))
        self.play(Write(formula))
        self.play(FadeIn(search_text))
        self.play(
            i_ridges.animate.shift(LEFT * 0.15 + DOWN * 0.1).rotate(
                -0.15, about_point=i_box.get_center()
            ),
            run_time=2, rate_func=smooth,
        )
        self.play(FadeIn(score, scale=1.5))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def correlation_problems(self):
        """Hiển thị các vấn đề khi dùng tương quan trực tiếp."""
        section = get_section_title("Thách thức của phương pháp tương quan")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        problems = [
            ("Biến dạng phi tuyến", "Áp lực ngón tay gây\nbiến dạng không đồng đều", MINUTIA_TERM),
            ("Điều kiện thay đổi", "Độ sáng, tương phản,\nđộ dày đường vân thay đổi", CHART_ORANGE),
            ("Chi phí tính toán", "Tìm kiếm trên toàn bộ\n(Δx, Δy, θ) rất tốn kém", CHART_PURPLE),
        ]

        problem_groups = VGroup()
        for title, desc, color in problems:
            icon = VGroup(
                Circle(radius=0.25, color=color, stroke_width=2),
                Text("!", font_size=24, color=color, weight=BOLD),
            )
            title_text = Text(title, font_size=20, color=color, weight=BOLD)
            desc_text = Text(desc, font_size=15, color=TEXT_DIM, line_spacing=1.2)
            row = VGroup(icon, VGroup(title_text, desc_text).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
            row.arrange(RIGHT, buff=0.4)
            problem_groups.add(row)

        problem_groups.arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(DOWN * 0.3)

        solution = Text(
            "→ Giải pháp: Sử dụng đối sánh dựa trên minutiae!",
            font_size=20, color=MATCH_COLOR, weight=BOLD,
        ).to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(p, shift=RIGHT * 0.3) for p in problem_groups],
                lag_ratio=0.4,
            ),
            run_time=2.5,
        )
        self.play(FadeIn(solution, shift=UP * 0.2))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))
