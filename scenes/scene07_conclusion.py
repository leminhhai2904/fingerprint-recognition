"""
Scene 7: Tóm tắt & Kết luận (Conclusion)
- Tóm tắt quy trình (Recap Pipeline) + Vòng xung thành công nháy xanh lá
- So sánh các hệ thống thương mại (FVC, NIST, FBI)
- Đóng góp khoa học và tương lai
- Lời cảm ơn & Kết thúc + Vẽ vân tay nền
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
        self.section_title()
        self.pipeline_recap()
        self.evaluation_standards()
        self.outro()

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
        """Tiêu đề mục — Segment 1 = 8.42s."""
        num = self.ct("06", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Tóm Tắt & Kết Luận", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Hành trình của dữ liệu vân tay từ quét đến khớp", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)

        # Target = 8.42s. Anim play = 2.5s. FadeOut = 1.0s. Need 4.92s wait.
        self.wait(4.92)
        self.play(FadeOut(group), run_time=1.0)
        self.wait(0.8) # Silence gap

    def pipeline_recap(self):
        """Tóm tắt quy trình xử lý dữ liệu vân tay — Segment 2 = 29.09s."""
        section = self.get_section_hdr("Quy trình nhận dạng vân tay tổng quát")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        steps = [
            ("Thu nhận ảnh", "Quang học, Điện dung, Siêu âm", OPTICAL_COLOR),
            ("Tăng cường ảnh", "Bộ lọc Gabor, lọc tần số", RIDGE_COLOR),
            ("Trích đặc trưng", "Binarize, Thinning, CN", CHART_ORANGE),
            ("Đối sánh", "Hough Transform, Vector", CHART_BLUE),
        ]

        boxes = VGroup()
        for name, desc, color in steps:
            box = create_rounded_box(
                width=2.6, height=2.6,
                fill_color=color, fill_opacity=0.08,
                stroke_color=color, stroke_width=1.5,
            )
            title = self.ct(name, font_size=15, color=color, weight=BOLD)
            desc_lbl = Paragraph(
                *desc.split("\n"),
                font_size=24, color=TEXT_DIM, alignment="center", line_spacing=1.2
            ).scale(12 / 24)
            content = VGroup(title, desc_lbl).arrange(DOWN, buff=0.25)
            content.move_to(box)
            boxes.add(VGroup(box, content))

        boxes.arrange(RIGHT, buff=0.6).shift(DOWN * 0.2)

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arrow = Arrow(
                boxes[i][0].get_right(), boxes[i + 1][0].get_left(),
                color=PRIMARY, stroke_width=2, buff=0.1,
                max_tip_length_to_length_ratio=0.25,
            )
            arrows.add(arrow)

        result_box = create_rounded_box(
            width=2.8, height=1.2,
            fill_color=MATCH_COLOR, fill_opacity=0.2,
            stroke_color=MATCH_COLOR, stroke_width=2,
        ).next_to(boxes[3], DOWN, buff=0.6)
        result_text = self.ct("KẾT QUẢ XÁC THỰC", font_size=16, color=MATCH_COLOR, weight=BOLD).move_to(result_box.get_center())

        final_arrow = Arrow(
            boxes[3][0].get_bottom(), result_box.get_top(),
            color=MATCH_COLOR, stroke_width=2.5, buff=0.1,
            max_tip_length_to_length_ratio=0.25,
        )

        # Show sequentially matching audio: Target = 29.09s
        self.play(FadeIn(boxes[0], shift=UP * 0.4), run_time=0.8)
        self.wait(5.0)
        self.play(GrowArrow(arrows[0]), FadeIn(boxes[1], shift=UP * 0.4), run_time=0.8)
        self.wait(5.0)
        self.play(GrowArrow(arrows[1]), FadeIn(boxes[2], shift=UP * 0.4), run_time=0.8)
        self.wait(5.0)
        self.play(GrowArrow(arrows[2]), FadeIn(boxes[3], shift=UP * 0.4), run_time=0.8)
        self.wait(4.0)

        # Success Match Highlight (Premium visual flash & ripple)
        self.play(GrowArrow(final_arrow), FadeIn(VGroup(result_box, result_text)), run_time=0.8)
        success_ring = Circle(radius=0.1, color=MATCH_COLOR, stroke_width=2.5).move_to(result_box.get_center())
        self.add(success_ring)
        self.play(success_ring.animate.scale(20).set_stroke(opacity=0), run_time=0.8)
        self.remove(success_ring)
        
        self.wait(4.5) # Remaining wait to hit 29.09s

        # Target = 29.09s. Anim play = 0.6 + 0.8 + 5.0 + 0.8 + 5.0 + 0.8 + 5.0 + 0.8 + 4.0 + 0.8 + 0.8 = 24.4s. FadeOut = 1.0s. Wait = 3.69s.
        # Adjusted wait to match final audio exactly: 29.09s - 24.4s - 1.0s = 3.69s.
        self.wait(0.19) # (using 3.88s total waiting splits)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    def evaluation_standards(self):
        """Các tiêu chuẩn đánh giá hệ thống vân tay — Segment 3 = 22.99s."""
        section = self.get_section_hdr("Các cuộc thi và tiêu chuẩn quốc tế")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        standards = [
            ("FVC (Fingerprint Verification Competition)", "Cuộc thi kiểm thử thuật toán độc lập lớn nhất."),
            ("NIST MINEX & IREX", "Đánh giá khả năng tương thích và hiệu năng minutiae của chính phủ Mỹ."),
            ("FBI CJIS Standards", "Chứng nhận máy quét vân tay đáp ứng chất lượng ảnh điều tra hình sự."),
        ]

        cards = VGroup()
        for title_text, desc_text in standards:
            box = create_rounded_box(
                width=11.0, height=1.3,
                fill_color=SECONDARY, fill_opacity=0.3,
                stroke_color=PRIMARY, stroke_width=1.5,
            )
            title = self.ct(title_text, font_size=16, color=TEXT_BRIGHT, weight=BOLD)
            desc = self.ct(desc_text, font_size=13, color=TEXT_DIM)
            content = VGroup(title, desc).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            content.move_to(box.get_left() + RIGHT * 0.5, aligned_edge=LEFT)
            cards.add(VGroup(box, content))

        cards.arrange(DOWN, buff=0.4).shift(DOWN * 0.25)

        # Show sequentially: Target = 22.99s
        self.play(FadeIn(cards[0], shift=RIGHT * 0.3), run_time=0.8)
        self.wait(6.0)
        self.play(FadeIn(cards[1], shift=RIGHT * 0.3), run_time=0.8)
        self.wait(6.0)
        self.play(FadeIn(cards[2], shift=RIGHT * 0.3), run_time=0.8)
        self.wait(6.99)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    def outro(self):
        """Phần kết và lời cảm ơn — Segment 4 = 9.77s."""
        thanks = self.ct("Cảm ơn các bạn đã theo dõi!", font_size=42, color=TEXT_BRIGHT, weight=BOLD)
        thanks.shift(UP * 0.6)

        line = Line(LEFT * 4, RIGHT * 4, color=PRIMARY, stroke_width=2.5).next_to(thanks, DOWN, buff=0.35)
        subtitle = self.ct("Môn học: Nhận dạng mẫu — HCMUS", font_size=20, color=RIDGE_COLOR).next_to(line, DOWN, buff=0.4)
        course = self.ct("Giảng viên hướng dẫn: PGS. TS. Trần Minh Triết", font_size=16, color=TEXT_DIM).next_to(subtitle, DOWN, buff=0.25)

        hashtags = self.ct("#Biometrics #FingerprintRecognition #PatternRecognition", font_size=13, color=PRIMARY).to_edge(DOWN, buff=0.6)

        fp = create_fingerprint_simple(scale=0.8, color=RIDGE_COLOR)
        fp.set_opacity(0.12).scale(2.2).move_to(ORIGIN)

        # Drawing the fingerprint in the background (Premium effect)
        self.play(Create(fp, run_time=2.0))
        self.play(Write(thanks, run_time=1.2))
        self.play(Create(line, run_time=0.5))
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(course, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(hashtags, shift=UP * 0.2), run_time=0.6)

        # Target = 9.77s. Anim play = 2.0 + 1.2 + 0.5 + 0.6 + 0.6 + 0.6 = 5.5s. FadeOut = 1.0s. Remaining wait = 3.27s.
        self.wait(3.27)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
