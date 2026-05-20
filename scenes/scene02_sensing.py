"""
Scene 2: Thu nhận vân tay (Fingerprint Sensing) (Không có giọng nói trực tiếp trong manim, nhưng có kịch bản ghi âm riêng)
- So sánh thu nhận ngoại tuyến (Off-line) vs quét trực tiếp (Live-scan)
- Nguyên lý cảm biến quang học: Phản xạ toàn phần bị chặn (FTIR)
- So sánh 3 công nghệ cảm biến: Quang học (Optical), Bán dẫn (Solid-state), Siêu âm (Ultrasound)
- Thách thức & Công nghệ tương lai (Quét đa phổ, Quét 3D không tiếp xúc, Quy chuẩn FBI CJIS)
"""
from manim import *
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *

class Scene02Sensing(Scene):
    def construct(self):
        scene_setup(self)
        self.section_title()
        self.offline_vs_livescan()
        self.ftir_principle()
        self.sensor_comparison()
        self.new_tech_and_challenges()

    def create_text(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kwargs):
        # We render it at font_size=36 and then scale it down to the desired size.
        # This resolves kerning issues in CMU Serif font on Windows.
        return Text(text_str, font_size=36, color=color, weight=weight, **kwargs).scale(font_size / 36)

    def create_paragraph(self, *lines, font_size=18, color=TEXT_COLOR, **kwargs):
        # Paragraph version of the workaround
        return Paragraph(*lines, font_size=36, color=color, **kwargs).scale(font_size / 36)

    def get_section_title(self, text):
        title = Text(text, font_size=40, color=TEXT_BRIGHT, weight=BOLD).scale(30 / 40)
        underline = Line(
            start=title.get_left() + DOWN * 0.3,
            end=title.get_right() + DOWN * 0.3,
            color=PRIMARY,
            stroke_width=3,
        )
        return VGroup(title, underline)

    def section_title(self):
        """Tiêu đề mục."""
        num = self.create_text("01", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.create_text("Thu Nhận Vân Tay", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.create_text(
            "Làm thế nào để số hóa cấu trúc đường vân?",
            font_size=22, color=TEXT_DIM,
        )
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3))
        self.play(FadeIn(subtitle, shift=UP * 0.2))

        self.wait(1.5)
        self.play(FadeOut(group))

    def offline_vs_livescan(self):
        """So sánh phương pháp offline (mực) và live-scan."""
        section = self.get_section_title("Phương pháp thu nhận vân tay")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Phương pháp offline (trái)
        offline_box = create_rounded_box(
            width=5.3, height=3.8,
            fill_color=SECONDARY, fill_opacity=0.2,
            stroke_color=TEXT_DIM, stroke_width=1.5,
        )
        offline_title = self.create_text("Thu nhận Ngoại tuyến (Off-line)", font_size=20, color=TEXT_DIM, weight=BOLD)
        offline_subtitle = self.create_text("Kỹ thuật lăn mực truyền thống", font_size=14, color=TEXT_DIM)
        offline_steps = VGroup(
            self.create_text("1. Phủ mực đen lên đầu ngón tay", font_size=14, color=TEXT_DIM),
            self.create_text("2. Ấn ngón tay lên thẻ giấy chuyên dụng", font_size=14, color=TEXT_DIM),
            self.create_text("3. Quét thẻ giấy bằng máy quét phẳng", font_size=14, color=TEXT_DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        offline_content = VGroup(offline_title, offline_subtitle, offline_steps).arrange(DOWN, buff=0.3)
        offline_group = VGroup(offline_box, offline_content)
        offline_content.move_to(offline_box)

        # Phương pháp live-scan (phải)
        livescan_box = create_rounded_box(
            width=5.3, height=3.8,
            fill_color=SECONDARY, fill_opacity=0.3,
            stroke_color=PRIMARY, stroke_width=2,
        )
        livescan_title = self.create_text("Thu nhận Trực tiếp (Live-scan)", font_size=20, color=PRIMARY, weight=BOLD)
        livescan_subtitle = self.create_text("Công nghệ quét điện tử hiện đại", font_size=14, color=PRIMARY)
        livescan_steps = VGroup(
            self.create_text("1. Đặt ngón tay trực tiếp lên cảm biến", font_size=14, color=TEXT_COLOR),
            self.create_text("2. Cảm biến quét và số hóa trực tiếp", font_size=14, color=TEXT_COLOR),
            self.create_text("3. Không cần mực, cho ảnh số tức thì", font_size=14, color=CORE_POINT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        livescan_content = VGroup(livescan_title, livescan_subtitle, livescan_steps).arrange(DOWN, buff=0.3)
        livescan_group = VGroup(livescan_box, livescan_content)
        livescan_content.move_to(livescan_box)

        both = VGroup(offline_group, livescan_group).arrange(RIGHT, buff=0.8).shift(DOWN * 0.3)

        arrow = Arrow(
            offline_box.get_right(), livescan_box.get_left(),
            color=PRIMARY, stroke_width=3, buff=0.15,
        )
        arrow_label = self.create_text("Phát triển", font_size=14, color=PRIMARY).next_to(arrow, UP, buff=0.1)

        self.play(FadeIn(offline_group, shift=RIGHT * 0.3))
        self.wait(1.5)
        self.play(GrowArrow(arrow), FadeIn(arrow_label))
        self.play(FadeIn(livescan_group, shift=LEFT * 0.3))

        self.wait(2.5)
        self.play(FadeOut(VGroup(section, both, arrow, arrow_label)))

    def ftir_principle(self):
        """Minh họa nguyên lý FTIR."""
        section = self.get_section_title("Cảm biến quang học: Nguyên lý FTIR")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Vẽ lăng kính
        prism_points = [
            np.array([-2.5, -0.7, 0]),
            np.array([2.5, -0.7, 0]),
            np.array([2.0, 0.5, 0]),
            np.array([-2.0, 0.5, 0]),
        ]
        prism = Polygon(
            *prism_points,
            fill_color="#3a506b", fill_opacity=0.3,
            stroke_color=RIDGE_COLOR, stroke_width=2,
        )
        prism_label = self.create_text("Lăng kính thủy tinh (Prism)", font_size=16, color=TEXT_DIM).next_to(prism, DOWN, buff=0.2)

        # Ngón tay
        skin_points = []
        for x in np.linspace(-1.8, 1.8, 100):
            y = 0.5 + 0.25 * (np.sin(np.pi * x / 0.8))**4
            skin_points.append(np.array([x, y, 0]))
        
        skin = VMobject()
        skin.set_points_smoothly(skin_points)
        skin.set_stroke(color="#d4a574", width=4) # Màu da ngón tay

        finger_body = Polygon(
            *skin_points,
            np.array([1.8, 1.5, 0]),
            np.array([-1.8, 1.5, 0]),
            fill_color="#d4a574", fill_opacity=0.3,
            stroke_width=0
        )
        finger_group = VGroup(finger_body, skin)
        finger_label = self.create_text("Đầu ngón tay (Finger)", font_size=16, color="#d4a574").move_to([0, 1.7, 0])

        # Nhãn mô tả trạng thái tiếp xúc
        valley_label = self.create_text("Rãnh (Valleys) - Không tiếp xúc", font_size=13, color=TEXT_DIM).move_to([-1.5, 1.1, 0])
        valley_arrow = Arrow(start=[-1.5, 1.0, 0], end=[-1.2, 0.7, 0], color=TEXT_DIM, stroke_width=1.5, max_tip_length_to_length_ratio=0.15)
        
        ridge_label = self.create_text("Đường vân (Ridges) - Tiếp xúc", font_size=13, color=RIDGE_COLOR).move_to([1.5, 1.1, 0])
        ridge_arrow = Arrow(start=[1.5, 1.0, 0], end=[0.8, 0.55, 0], color=RIDGE_COLOR, stroke_width=1.5, max_tip_length_to_length_ratio=0.15)

        # Thiết bị
        light_source = VGroup(
            Dot([-3.5, -0.5, 0], color=OPTICAL_COLOR, radius=0.15),
            self.create_text("Nguồn sáng", font_size=14, color=OPTICAL_COLOR)
        ).arrange(DOWN, buff=0.15).move_to([-3.8, -0.5, 0])

        ccd_sensor = VGroup(
            create_rounded_box(width=0.4, height=1.5, fill_color=CORE_POINT, fill_opacity=0.2, stroke_color=CORE_POINT, stroke_width=1.5),
            self.create_text("Cảm biến CCD/CMOS", font_size=14, color=CORE_POINT)
        ).arrange(DOWN, buff=0.15).move_to([3.8, -0.5, 0])

        # Tia sáng
        ray_valley = VMobject()
        ray_valley.set_points_as_corners([[-3.5, -0.5, 0], [-2.15, -0.2, 0], [-0.4, 0.5, 0], [1.35, -0.2, 0], [3.5, -0.5, 0]])
        ray_valley.set_stroke(color=OPTICAL_COLOR, width=3)

        ray_ridge = VMobject()
        ray_ridge.set_points_as_corners([[-3.5, -0.5, 0], [-2.35, -0.1, 0], [0, 0.5, 0]])
        ray_ridge.set_stroke(color=OPTICAL_COLOR, width=3)

        scatter_rays = VGroup(*[
            Line([0, 0.5, 0], [dx, 0.8, 0], stroke_width=1.5, color=MINUTIA_TERM).set_opacity(0.6)
            for dx in [-0.2, 0, 0.2]
        ])
        cross = Cross(scale_factor=0.08, stroke_color=MINUTIA_TERM).move_to([0, 0.5, 0])

        explanation = VGroup(
            self.create_text("✓ Tại rãnh: Phản xạ toàn phần → Cảm biến nhận sáng → Tạo vùng SÁNG", font_size=15, color=OPTICAL_COLOR),
            self.create_text("✗ Tại đường vân: Phản xạ bị chặn → Ánh sáng bị hấp thụ/tán xạ → Tạo vùng TỐI", font_size=15, color=MINUTIA_TERM)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)

        # Chạy animation
        self.play(Create(prism), FadeIn(prism_label))
        self.play(FadeIn(finger_group), FadeIn(finger_label))
        self.play(
            GrowArrow(valley_arrow), FadeIn(valley_label),
            GrowArrow(ridge_arrow), FadeIn(ridge_label)
        )
        self.wait(1.5)
        self.play(FadeIn(light_source), FadeIn(ccd_sensor))
        
        # Animate tia sáng
        self.play(Create(ray_valley), run_time=1.5)
        self.wait(0.5)
        self.play(Create(ray_ridge), run_time=1.2)
        self.play(Create(scatter_rays), Create(cross))
        self.wait(1.0)
        self.play(FadeIn(explanation, shift=UP * 0.2))
        self.wait(3.5)

        # Xóa
        self.play(FadeOut(Group(*self.mobjects)))

    def sensor_comparison(self):
        """So sánh ba loại cảm biến."""
        section = self.get_section_title("Ba dòng công nghệ cảm biến chính")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        sensors = [
            ("Cảm biến Quang học\n(Optical Sensors)", OPTICAL_COLOR, [
                "• Nguyên lý: Phản xạ toàn phần bị chặn (FTIR)",
                "• Ưu điểm: Độ bền vật lý cao, diện tích lớn",
                "• Nhược điểm: Cồng kềnh, dễ bị đánh lừa"
            ]),
            ("Cảm biến Bán dẫn\n(Solid-state Sensors)", SOLID_STATE_COLOR, [
                "• Nguyên lý: Điện dung, Nhiệt, Điện trường",
                "• Ưu điểm: Nhỏ gọn, dễ tích hợp điện thoại",
                "• Nhược điểm: Dễ bị hỏng do tĩnh điện"
            ]),
            ("Cảm biến Siêu âm\n(Ultrasound Sensors)", ULTRASOUND_COLOR, [
                "• Nguyên lý: Phản hồi sóng siêu âm (Echo)",
                "• Ưu điểm: Xuyên thấu chất bẩn, da khô/ướt",
                "• Nhược điểm: Giá thành cao, công nghệ phức tạp"
            ]),
        ]

        cards = VGroup()
        for name, color, desc_lines in sensors:
            card_box = create_rounded_box(
                width=3.7, height=3.6,
                fill_color=color, fill_opacity=0.08,
                stroke_color=color, stroke_width=1.5,
            )
            # Split the name into two lines to center them perfectly
            lines = name.split("\n")
            title = VGroup(*[
                self.create_text(line, font_size=18, color=color, weight=BOLD)
                for line in lines
            ]).arrange(DOWN, buff=0.1)
            
            desc_group = VGroup(*[
                self.create_text(line, font_size=12, color=TEXT_COLOR)
                for line in desc_lines
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            
            content = VGroup(title, desc_group).arrange(DOWN, buff=0.35)
            content.move_to(card_box)
            cards.add(VGroup(card_box, content))

        cards.arrange(RIGHT, buff=0.4).shift(DOWN * 0.2)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.5) for c in cards],
                lag_ratio=0.3,
            ),
            run_time=2,
        )

        self.wait(4.0)
        self.play(FadeOut(VGroup(section, cards)))

    def new_tech_and_challenges(self):
        """Thách thức và công nghệ mới."""
        section = self.get_section_title("Thách thức & Hướng phát triển mới")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3))

        # Khối bên trái: Thách thức (Challenges)
        left_box = create_rounded_box(
            width=5.4, height=3.8,
            fill_color=SECONDARY, fill_opacity=0.2,
            stroke_color=DELTA_COLOR, stroke_width=1.5,
        )
        left_title = self.create_text("Hạn chế của máy quét hiện tại", font_size=18, color=DELTA_COLOR, weight=BOLD)
        left_points = VGroup(
            self.create_text("• Khó hoạt động khi ngón tay quá khô hoặc ướt", font_size=13, color=TEXT_COLOR),
            self.create_text("• Biến dạng da (skin distortion) do lực ép ngón tay", font_size=13, color=TEXT_COLOR),
            self.create_text("• Nguy cơ bị đánh lừa bởi vân tay giả (spoofing)", font_size=13, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        left_content = VGroup(left_title, left_points).arrange(DOWN, buff=0.35)
        left_content.move_to(left_box)
        left_group = VGroup(left_box, left_content)

        # Khối bên phải: Công nghệ mới (New Technologies)
        right_box = create_rounded_box(
            width=5.4, height=3.8,
            fill_color=SECONDARY, fill_opacity=0.3,
            stroke_color=MATCH_COLOR, stroke_width=1.5,
        )
        right_title = self.create_text("Giải pháp công nghệ tương lai", font_size=18, color=MATCH_COLOR, weight=BOLD)
        right_points = VGroup(
            self.create_text("• Quét đa phổ (Multispectral): Đọc vân dưới biểu bì", font_size=13, color=TEXT_COLOR),
            self.create_text("• Quét 3D không tiếp xúc: Loại bỏ biến dạng cơ học", font_size=13, color=TEXT_COLOR),
            self.create_text("• Tiêu chuẩn FBI CJIS: Chuẩn hóa chất lượng ảnh AFIS", font_size=13, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        right_content = VGroup(right_title, right_points).arrange(DOWN, buff=0.35)
        right_content.move_to(right_box)
        right_group = VGroup(right_box, right_content)

        both = VGroup(left_group, right_group).arrange(RIGHT, buff=0.6).shift(DOWN * 0.3)

        self.play(FadeIn(left_group, shift=RIGHT * 0.3))
        self.wait(1.5)
        self.play(FadeIn(right_group, shift=LEFT * 0.3))

        self.wait(4.0)
        self.play(FadeOut(VGroup(section, both)))
