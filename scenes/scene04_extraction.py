"""
Scene 4: Quy trình Trích xuất Đặc trưng chi tiết (Không có giọng nói)
- Hướng và tần số đường vân cục bộ
- Tăng cường ảnh bằng bộ lọc ngữ cảnh
- Nhị phân hóa → Thinning → Phát hiện minutiae
- Khái niệm Crossing Number
- Sơ đồ pipeline hoàn chỉnh
"""
from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene04Extraction(Scene):
    def construct(self):
        scene_setup(self)
        self.section_title()
        self.orientation_and_frequency()
        self.enhancement_pipeline()
        self.crossing_number()
        self.full_pipeline()

    def section_title(self):
        """Tiêu đề mục."""
        num = Text("03", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = Text("Quy Trình Trích Xuất", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = Text(
            "Từ ảnh thô đến các đặc trưng minutiae",
            font_size=22, color=TEXT_DIM,
        )
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3))
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        self.wait(0.5)
        self.play(FadeOut(group))

    def orientation_and_frequency(self):
        """Minh họa hướng và tần số đường vân cục bộ."""
        section = get_section_title("Hướng và Tần số Đường vân")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Trường hướng
        orient_label = Text("Trường hướng", font_size=20, color=RIDGE_COLOR, weight=BOLD)
        field = create_orientation_field(
            rows=8, cols=10, width=4.5, height=3.2,
            center=np.array([-3, -0.5, 0])
        )
        orient_label.next_to(field, UP, buff=0.3)

        orient_formula = MathTex(r"\theta_{xy}", font_size=28, color=RIDGE_COLOR).next_to(field, DOWN, buff=0.3)
        orient_desc = Text(
            "Góc của đường vân tại\nđiểm (x,y) so với\ntrục ngang",
            font_size=14, color=TEXT_DIM, line_spacing=1.2,
        ).next_to(orient_formula, DOWN, buff=0.15)

        # Tần số
        freq_label = Text("Tần số đường vân", font_size=20, color=MINUTIA_BIFUR, weight=BOLD)
        freq_label.move_to(RIGHT * 3.2 + UP * 1.2)

        freq_ridges = VGroup()
        for rp in [0, 0.35, 0.7, 1.05, 1.4]:
            ridge = Line(
                RIGHT * 1.5 + UP * (rp - 0.5),
                RIGHT * 5 + UP * (rp - 0.5),
                color=RIDGE_COLOR, stroke_width=4,
            )
            freq_ridges.add(ridge)
        freq_ridges.shift(DOWN * 0.8)

        brace = BraceBetweenPoints(
            freq_ridges[0].get_left() + LEFT * 0.1,
            freq_ridges[1].get_left() + LEFT * 0.1,
            direction=LEFT, color=MINUTIA_BIFUR,
        )
        spacing_label = MathTex(r"\frac{1}{f_{xy}}", font_size=22, color=MINUTIA_BIFUR)
        spacing_label.next_to(brace, LEFT, buff=0.15)

        formula_part = MathTex(r"f_{xy} =", font_size=20, color=TEXT_DIM)
        text_part = Text(" số đường vân trên đơn vị độ dài", font_size=15, color=TEXT_DIM)
        freq_formula = VGroup(formula_part, text_part).arrange(RIGHT, buff=0.1).next_to(freq_ridges, DOWN, buff=0.4)

        self.play(FadeIn(orient_label))
        self.play(
            LaggedStart(*[FadeIn(seg, scale=0) for seg in field], lag_ratio=0.01),
            run_time=1.5,
        )
        self.play(FadeIn(orient_formula), FadeIn(orient_desc))
        self.wait(0.5)
        self.play(FadeIn(freq_label))
        self.play(
            LaggedStart(*[Create(r) for r in freq_ridges], lag_ratio=0.15),
            run_time=1,
        )
        self.play(GrowFromCenter(brace), FadeIn(spacing_label))
        self.play(FadeIn(freq_formula))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def enhancement_pipeline(self):
        """Hiển thị pipeline: tăng cường → nhị phân → thinning."""
        section = get_section_title("Quy trình xử lý ảnh")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        stages = [
            ("Ảnh\nxám", TEXT_DIM, self._create_grayscale_sim()),
            ("Ảnh\ntăng cường", RIDGE_COLOR, self._create_enhanced_sim()),
            ("Ảnh\nnhị phân", CHART_BLUE, self._create_binary_sim()),
            ("Ảnh\nxương", CORE_POINT, self._create_thinned_sim()),
        ]

        stage_groups = VGroup()
        for title_text, color, content in stages:
            box = create_rounded_box(
                width=2.6, height=2.6,
                fill_color=color, fill_opacity=0.05,
                stroke_color=color, stroke_width=1.5,
            )
            label = Text(title_text, font_size=14, color=color, weight=BOLD)
            label.next_to(box, DOWN, buff=0.2)
            content.move_to(box).scale(0.8)
            stage_groups.add(VGroup(box, content, label))

        stage_groups.arrange(RIGHT, buff=0.7).shift(DOWN * 0.3)

        arrows = VGroup()
        for i in range(len(stage_groups) - 1):
            arrow = Arrow(
                stage_groups[i][0].get_right(), stage_groups[i + 1][0].get_left(),
                color=PRIMARY, buff=0.1, stroke_width=2,
                max_tip_length_to_length_ratio=0.25,
            )
            arrows.add(arrow)

        filter_desc = Text(
            "Tăng cường: Bộ lọc Gabor theo ngữ cảnh (hướng θ và tần số f)",
            font_size=16, color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.5)

        for i, sg in enumerate(stage_groups):
            self.play(FadeIn(sg, shift=UP * 0.3), run_time=0.6)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.3)
            self.wait(0.3)
        self.play(FadeIn(filter_desc, shift=UP * 0.2))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def _create_grayscale_sim(self):
        ridges = VGroup()
        for i in range(8):
            y = (i - 3.5) * 0.22
            opacity = 0.3 + 0.4 * np.random.random()
            ridge = Line(LEFT * 1 + UP * y, RIGHT * 1 + UP * y,
                         color=RIDGE_COLOR, stroke_width=5, stroke_opacity=opacity)
            ridges.add(ridge)
        return ridges

    def _create_enhanced_sim(self):
        ridges = VGroup()
        for i in range(8):
            y = (i - 3.5) * 0.22
            ridge = Line(LEFT * 1 + UP * y, RIGHT * 1 + UP * y,
                         color=RIDGE_COLOR, stroke_width=5, stroke_opacity=0.8)
            ridges.add(ridge)
        return ridges

    def _create_binary_sim(self):
        ridges = VGroup()
        for i in range(8):
            y = (i - 3.5) * 0.22
            ridge = Line(LEFT * 1 + UP * y, RIGHT * 1 + UP * y,
                         color=WHITE, stroke_width=5, stroke_opacity=1)
            ridges.add(ridge)
        return ridges

    def _create_thinned_sim(self):
        ridges = VGroup()
        for i in range(8):
            y = (i - 3.5) * 0.22
            ridge = Line(LEFT * 1 + UP * y, RIGHT * 1 + UP * y,
                         color=CORE_POINT, stroke_width=1.5, stroke_opacity=0.9)
            ridges.add(ridge)
        return ridges

    def crossing_number(self):
        """Giải thích khái niệm Crossing Number."""
        section = get_section_title("Crossing Number")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        desc = Text(
            "Phát hiện minutiae bằng cách đếm chuyển đổi pixel trong vùng lân cận 8",
            font_size=17, color=TEXT_COLOR,
        ).next_to(section, DOWN, buff=0.5)
        self.play(FadeIn(desc, shift=UP * 0.2))

        formula = MathTex(
            r"CN(p) = \frac{1}{2} \sum_{i=1}^{8} |p_i - p_{i+1}|",
            font_size=32, color=TEXT_BRIGHT,
        ).shift(UP * 0.5)

        cases = [
            ("CN = 1", "Kết thúc", MINUTIA_TERM,
             [[0, 0, 0], [0, 1, 0], [0, 1, 0]]),
            ("CN = 2", "Đường vân\nliên tục", RIDGE_COLOR,
             [[0, 1, 0], [0, 1, 0], [0, 1, 0]]),
            ("CN = 3", "Phân nhánh", MINUTIA_BIFUR,
             [[0, 1, 0], [0, 1, 0], [1, 1, 0]]),
        ]

        case_groups = VGroup()
        for cn_text, label_text, color, grid_data in cases:
            grid = VGroup()
            cell_size = 0.35
            for r in range(3):
                for c in range(3):
                    fill = WHITE if grid_data[r][c] == 1 else "#222244"
                    fill_op = 0.9 if grid_data[r][c] == 1 else 0.3
                    cell = Square(
                        side_length=cell_size,
                        fill_color=fill, fill_opacity=fill_op,
                        stroke_color=TEXT_DIM, stroke_width=1,
                    ).move_to(np.array([(c - 1) * cell_size, (1 - r) * cell_size, 0]))
                    grid.add(cell)
            center_highlight = Square(
                side_length=cell_size, stroke_color=color, stroke_width=2.5, fill_opacity=0,
            ).move_to(ORIGIN)
            grid.add(center_highlight)
            cn_label = Text(cn_text, font_size=18, color=color, weight=BOLD)
            type_label = Text(label_text, font_size=14, color=TEXT_DIM)
            case_content = VGroup(cn_label, grid, type_label).arrange(DOWN, buff=0.25)
            case_groups.add(case_content)

        case_groups.arrange(RIGHT, buff=1.5).shift(DOWN * 1.5)

        self.play(Write(formula))
        self.wait(0.5)
        self.play(
            LaggedStart(
                *[FadeIn(cg, shift=UP * 0.3) for cg in case_groups],
                lag_ratio=0.3,
            ),
            run_time=2,
        )

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def full_pipeline(self):
        """Sơ đồ pipeline trích xuất đặc trưng hoàn chỉnh."""
        section = get_section_title("Pipeline hoàn chỉnh")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        steps = [
            ("Ảnh\nđầu vào", TEXT_DIM),
            ("Ước lượng\nhướng", CHART_BLUE),
            ("Phân\nvùng", CHART_ORANGE),
            ("Tăng\ncường", RIDGE_COLOR),
            ("Nhị phân\nhóa", CHART_PURPLE),
            ("Làm\nmỏng", CORE_POINT),
            ("Phát hiện\nMinutiae", PRIMARY),
        ]

        row1_steps = steps[:4]
        row2_steps = steps[4:]

        row1 = VGroup()
        for text, color in row1_steps:
            box = create_pipeline_box(text, width=2.5, height=1, color=color)
            row1.add(box)
        row1.arrange(RIGHT, buff=0.5)

        row2 = VGroup()
        for text, color in row2_steps:
            box = create_pipeline_box(text, width=2.5, height=1, color=color)
            row2.add(box)
        row2.arrange(RIGHT, buff=0.5)

        pipeline = VGroup(row1, row2).arrange(DOWN, buff=1.0).shift(DOWN * 0.3)

        arrows1 = VGroup()
        for i in range(len(row1) - 1):
            arrow = create_arrow_between(row1[i], row1[i + 1])
            arrows1.add(arrow)

        connector = Arrow(
            row1[-1][0].get_bottom(), row2[0][0].get_top(),
            color=PRIMARY, stroke_width=2, buff=0.1,
        )

        arrows2 = VGroup()
        for i in range(len(row2) - 1):
            arrow = create_arrow_between(row2[i], row2[i + 1])
            arrows2.add(arrow)

        output_highlight = SurroundingRectangle(row2[-1], color=PRIMARY, stroke_width=3, buff=0.15)
        output_label = Text(
            "Đầu ra: Tập hợp minutiae m = {x, y, θ}",
            font_size=18, color=PRIMARY,
        ).to_edge(DOWN, buff=0.5)

        for i, box in enumerate(row1):
            self.play(FadeIn(box, shift=RIGHT * 0.3), run_time=0.35)
            if i < len(arrows1):
                self.play(GrowArrow(arrows1[i]), run_time=0.2)
        self.play(GrowArrow(connector), run_time=0.3)
        for i, box in enumerate(row2):
            self.play(FadeIn(box, shift=RIGHT * 0.3), run_time=0.35)
            if i < len(arrows2):
                self.play(GrowArrow(arrows2[i]), run_time=0.2)
        self.play(Create(output_highlight))
        self.play(FadeIn(output_label))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))
