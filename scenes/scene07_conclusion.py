"""
Scene 7: Kết luận (Không có giọng nói)
- Tóm tắt pipeline
- Đánh giá hiệu suất (FVC)
- Các thách thức còn mở
- Outro
"""
from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene07Conclusion(Scene):
    def construct(self):
        scene_setup(self)
        self.pipeline_recap()
        self.performance()
        self.open_issues()
        self.outro()

    def pipeline_recap(self):
        """Tóm tắt toàn bộ pipeline nhận dạng vân tay."""
        section = get_section_title("Bức tranh toàn cảnh")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        stages = [
            ("Thu nhận", "📷", CHART_BLUE, "Chụp ảnh vân tay\nbằng cảm biến\nquang học/bán dẫn"),
            ("Trích xuất\nĐặc trưng", "🔍", CHART_ORANGE, "Trích xuất minutiae\nm = {x, y, θ}\ntừ mẫu đường vân"),
            ("Đối sánh", "🔗", CHART_PURPLE, "So sánh mẫu\nvới đầu vào\nbằng đối sánh điểm"),
        ]

        stage_groups = VGroup()
        for title, icon_text, color, desc in stages:
            box = create_rounded_box(
                width=3.2, height=3.5,
                fill_color=color, fill_opacity=0.08,
                stroke_color=color, stroke_width=2,
            )
            icon = Text(icon_text, font_size=36)
            title_label = Text(title, font_size=20, color=color, weight=BOLD)
            desc_label = Text(desc, font_size=14, color=TEXT_DIM, line_spacing=1.2)
            content = VGroup(icon, title_label, desc_label).arrange(DOWN, buff=0.3)
            content.move_to(box)
            stage_groups.add(VGroup(box, content))

        stage_groups.arrange(RIGHT, buff=0.5).shift(DOWN * 0.3)

        arrows = VGroup()
        for i in range(len(stage_groups) - 1):
            arrow = Arrow(
                stage_groups[i][0].get_right(), stage_groups[i + 1][0].get_left(),
                color=PRIMARY, stroke_width=3, buff=0.1,
            )
            arrows.add(arrow)

        result_box = create_rounded_box(
            width=3, height=0.8,
            fill_color=MATCH_COLOR, fill_opacity=0.15,
            stroke_color=MATCH_COLOR, stroke_width=2,
        ).to_edge(DOWN, buff=0.8)
        result_text = Text("Khớp / Không khớp", font_size=18, color=MATCH_COLOR, weight=BOLD)
        result_text.move_to(result_box)

        final_arrow = Arrow(
            stage_groups[-1][0].get_bottom(), result_box.get_top(),
            color=MATCH_COLOR, stroke_width=2, buff=0.1,
        )

        for i, sg in enumerate(stage_groups):
            self.play(FadeIn(sg, shift=UP * 0.4, scale=0.9), run_time=0.6)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.3)
        self.play(GrowArrow(final_arrow), FadeIn(VGroup(result_box, result_text)))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def performance(self):
        """Hiển thị thông tin đánh giá hiệu suất."""
        section = get_section_title("Hiệu suất: Cuộc thi FVC")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        fvc_data = [
            ("FVC2000", "11", "—"),
            ("FVC2002", "31", "—"),
            ("FVC2004", "67", "2.07%"),
            ("FVC2006", "70", "—"),
        ]

        header = VGroup(
            Text("Cuộc thi", font_size=16, color=PRIMARY, weight=BOLD),
            Text("Số thuật toán", font_size=16, color=PRIMARY, weight=BOLD),
            Text("EER tốt nhất", font_size=16, color=PRIMARY, weight=BOLD),
        ).arrange(RIGHT, buff=1.5)

        rows = VGroup()
        for year, algos, eer in fvc_data:
            row = VGroup(
                Text(year, font_size=16, color=TEXT_COLOR),
                Text(algos, font_size=16, color=CHART_BLUE),
                Text(eer, font_size=16, color=MATCH_COLOR if eer != "—" else TEXT_DIM),
            ).arrange(RIGHT, buff=1.5)
            rows.add(row)

        table = VGroup(header, *rows).arrange(DOWN, buff=0.35).shift(DOWN * 0.3)

        for row in [header, *rows]:
            for i, elem in enumerate(row):
                target_x = header[i].get_center()[0]
                elem.move_to([target_x, elem.get_center()[1], 0])

        h_line = Line(
            header.get_left() + DOWN * 0.2 + LEFT * 0.3,
            header.get_right() + DOWN * 0.2 + RIGHT * 0.3,
            color=TEXT_DIM, stroke_width=1,
        )

        growth_text = Text(
            "25 → 150 tổ chức đăng ký (tăng 6 lần!)",
            font_size=18, color=RIDGE_COLOR,
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(header), Create(h_line))
        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3),
            run_time=2,
        )
        self.play(FadeIn(growth_text, shift=UP * 0.2))

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def open_issues(self):
        """Trình bày các thách thức còn mở."""
        section = get_section_title("Các thách thức còn mở")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        challenges = [
            ("Ảnh chất lượng kém", "Cảm biến giá rẻ, ngón tay\nướt/khô, người cao tuổi", CHART_ORANGE),
            ("Tấn công giả mạo", "Vân tay giả có thể đánh lừa\ncảm biến", MINUTIA_TERM),
            ("Bảo mật mẫu", "Mẫu bị đánh cắp có thể\nbị giải mã ngược", CHART_PURPLE),
            ("Đối sánh quy mô lớn", "Cơ sở dữ liệu FBI: hơn\n200 triệu bản ghi", CHART_BLUE),
        ]

        challenge_groups = VGroup()
        for title, desc, color in challenges:
            icon = VGroup(
                RoundedRectangle(
                    width=0.4, height=0.4, corner_radius=0.05,
                    fill_color=color, fill_opacity=0.2,
                    stroke_color=color, stroke_width=1.5,
                ),
                Text("⚠", font_size=16, color=color),
            )
            title_text = Text(title, font_size=18, color=color, weight=BOLD)
            desc_text = Text(desc, font_size=14, color=TEXT_DIM, line_spacing=1.2)
            content = VGroup(title_text, desc_text).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            row = VGroup(icon, content).arrange(RIGHT, buff=0.4)
            challenge_groups.add(row)

        challenge_groups.arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(DOWN * 0.3)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=RIGHT * 0.3) for c in challenge_groups],
                lag_ratio=0.3,
            ),
            run_time=3,
        )

        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

    def outro(self):
        """Màn hình kết thúc."""
        fp = create_fingerprint_simple(scale=0.8, color=RIDGE_COLOR)
        fp.set_opacity(0.1).scale(2)

        thanks = Text("Cảm ơn các bạn đã theo dõi!", font_size=48, color=TEXT_BRIGHT, weight=BOLD)
        line = Line(LEFT * 3, RIGHT * 3, color=PRIMARY, stroke_width=2)
        subtitle = Text("Nhận Dạng Vân Tay", font_size=28, color=PRIMARY)
        course = Text(
            "CSC14006 - Nhận dạng mẫu\nĐại học Khoa học Tự nhiên, ĐHQG TP.HCM",
            font_size=18, color=TEXT_DIM, line_spacing=1.3,
        )
        hashtags = Text(
            "#fithcmus  #patternrecognition  #ai  #ml",
            font_size=16, color=RIDGE_COLOR,
        )

        content = VGroup(thanks, line, subtitle, course, hashtags)
        content.arrange(DOWN, buff=0.4)

        self.play(FadeIn(fp, run_time=2))
        self.play(Write(thanks, run_time=1.5))
        self.play(Create(line))
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.play(FadeIn(course, shift=UP * 0.2))
        self.play(FadeIn(hashtags, shift=UP * 0.2))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
        self.wait(1)
