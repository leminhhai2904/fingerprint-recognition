"""
Scene 2: Thu nhận vân tay (Fingerprint Sensing)
- So sánh thu nhận ngoại tuyến (Off-line) vs quét trực tiếp (Live-scan)
- Nguyên lý cảm biến quang học: Phản xạ toàn phần bị chặn (FTIR) + Trích hạt sáng
- So sánh 3 công nghệ cảm biến: Quang học (Optical), Bán dẫn (Solid-state), Siêu âm (Ultrasound)
  + Demo phóng to cảm biến điện dung (Capacitive sensor zoom-in)
  + Hiệu ứng sóng siêu âm truyền và phản hồi
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

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kwargs):
        """create_text with CMU Serif kerning workaround (render big → scale down)."""
        return Text(text_str, font_size=36, color=color, weight=weight, **kwargs).scale(font_size / 36)

    def get_section_title(self, text):
        title = self.ct(text, font_size=30, color=TEXT_BRIGHT, weight=BOLD)
        underline = Line(
            start=title.get_left() + DOWN * 0.3,
            end=title.get_right() + DOWN * 0.3,
            color=PRIMARY,
            stroke_width=3,
        )
        return VGroup(title, underline)

    def section_title(self):
        """Tiêu đề mục — Segment 1 = 4.87s."""
        num = self.ct("01", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Thu Nhận Vân Tay", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Làm thế nào để số hóa cấu trúc đường vân?", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)

        # Total anim play = 2.5s. Target 4.87s before FadeOut completes.
        self.wait(1.37)
        self.play(FadeOut(group), run_time=1.0)
        self.wait(0.8) # Silence gap

    def offline_vs_livescan(self):
        """So sánh phương pháp offline (mực) và live-scan — Segment 2 = 11.83s."""
        section = self.get_section_title("Phương pháp thu nhận vân tay")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Phương pháp offline (trái)
        offline_box = create_rounded_box(
            width=5.3, height=3.8,
            fill_color=SECONDARY, fill_opacity=0.2,
            stroke_color=TEXT_DIM, stroke_width=1.5,
        )
        offline_title = self.ct("Thu nhận Ngoại tuyến", font_size=20, color=TEXT_DIM, weight=BOLD)
        offline_subtitle = self.ct("Kỹ thuật lăn mực truyền thống", font_size=14, color=TEXT_DIM)
        offline_steps = VGroup(
            self.ct("1. Phủ mực đen lên đầu ngón tay", font_size=14, color=TEXT_DIM),
            self.ct("2. Ấn ngón tay lên thẻ giấy chuyên dụng", font_size=14, color=TEXT_DIM),
            self.ct("3. Quét thẻ giấy bằng máy quét phẳng", font_size=14, color=TEXT_DIM),
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
        livescan_title = self.ct("Thu nhận Trực tiếp", font_size=20, color=PRIMARY, weight=BOLD)
        livescan_subtitle = self.ct("Công nghệ quét điện tử hiện đại", font_size=14, color=PRIMARY)
        livescan_steps = VGroup(
            self.ct("1. Đặt ngón tay trực tiếp lên cảm biến", font_size=14, color=TEXT_COLOR),
            self.ct("2. Cảm biến quét và số hóa trực tiếp", font_size=14, color=TEXT_COLOR),
            self.ct("3. Không cần mực, cho ảnh số tức thì", font_size=14, color=CORE_POINT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        livescan_content = VGroup(livescan_title, livescan_subtitle, livescan_steps).arrange(DOWN, buff=0.3)
        livescan_group = VGroup(livescan_box, livescan_content)
        livescan_content.move_to(livescan_box)

        both = VGroup(offline_group, livescan_group).arrange(RIGHT, buff=1.2).shift(DOWN * 0.3)

        arrow = Arrow(
            offline_box.get_right(), livescan_box.get_left(),
            color=PRIMARY, stroke_width=3, buff=0.3,
        )
        arrow_label = self.ct("Phát triển", font_size=14, color=PRIMARY).next_to(arrow, UP, buff=0.2)

        self.play(FadeIn(offline_group, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(3.5)  # Đọc đoạn offline
        self.play(GrowArrow(arrow), FadeIn(arrow_label), run_time=0.8)
        self.play(FadeIn(livescan_group, shift=LEFT * 0.3), run_time=0.8)

        # Target 11.83s. Total play so far = 0.6 + 0.8 + 3.5 + 0.8 + 0.8 = 6.5s.
        self.wait(4.33)
        self.play(FadeOut(VGroup(section, both, arrow, arrow_label)), run_time=1.0)
        self.wait(0.8) # Silence gap

    def ftir_principle(self):
        """Minh họa nguyên lý FTIR — Segment 3 = 17.64s."""
        section = self.get_section_title("Cảm biến quang học: Nguyên lý FTIR")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

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
        prism_label = self.ct("Lăng kính thủy tinh", font_size=16, color=TEXT_DIM).next_to(prism, DOWN, buff=0.2)

        # Ngón tay
        skin_points = []
        for x in np.linspace(-1.8, 1.8, 100):
            y = 0.5 + 0.25 * (np.sin(np.pi * x / 0.8))**4
            skin_points.append(np.array([x, y, 0]))
        
        skin = VMobject()
        skin.set_points_smoothly(skin_points)
        skin.set_stroke(color="#d4a574", width=4)

        finger_body = Polygon(
            *skin_points,
            np.array([1.8, 1.5, 0]),
            np.array([-1.8, 1.5, 0]),
            fill_color="#d4a574", fill_opacity=0.3,
            stroke_width=0
        )
        finger_group = VGroup(finger_body, skin)
        finger_label = self.ct("Đầu ngón tay", font_size=16, color="#d4a574").move_to([0, 1.7, 0])

        valley_label = self.ct("Rãnh - Không tiếp xúc", font_size=13, color=TEXT_DIM).move_to([-1.5, 1.1, 0])
        valley_arrow = Arrow(
            start=[-1.6, 0.95, 0], end=[-1.275, 0.775, 0],
            color=TEXT_DIM, stroke_width=1.5, max_tip_length_to_length_ratio=0.15
        )
        
        ridge_label = self.ct("Đường vân - Tiếp xúc", font_size=13, color=RIDGE_COLOR).move_to([1.5, 1.1, 0])
        ridge_arrow = Arrow(
            start=[1.0, 0.95, 0], end=[0.8, 0.55, 0],
            color=RIDGE_COLOR, stroke_width=1.5, max_tip_length_to_length_ratio=0.15
        )

        # Thiết bị
        light_source = VGroup(
            Dot([-3.5, -0.75, 0], color=OPTICAL_COLOR, radius=0.15),
            self.ct("Nguồn sáng", font_size=14, color=OPTICAL_COLOR)
        ).arrange(DOWN, buff=0.15).move_to([-3.8, -0.75, 0])

        ccd_sensor = VGroup(
            create_rounded_box(width=0.4, height=1.5, fill_color=CORE_POINT, fill_opacity=0.2, stroke_color=CORE_POINT, stroke_width=1.5),
            self.ct("Cảm biến CCD/CMOS", font_size=14, color=CORE_POINT)
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
            self.ct("Tại rãnh: Phản xạ toàn phần → Cảm biến nhận sáng → Tạo vùng SÁNG", font_size=15, color=OPTICAL_COLOR),
            self.ct("Tại đường vân: Phản xạ bị chặn → Ánh sáng bị hấp thụ/tán xạ → Tạo vùng TỐI", font_size=15, color=MINUTIA_TERM)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)

        self.play(Create(prism), FadeIn(prism_label), FadeIn(finger_group), FadeIn(finger_label), run_time=1.2)
        self.wait(0.5)

        self.play(
            GrowArrow(valley_arrow), FadeIn(valley_label),
            FadeIn(light_source), FadeIn(ccd_sensor),
            run_time=1.2
        )
        self.play(GrowArrow(ridge_arrow), FadeIn(ridge_label), run_time=0.8)

        # Trace photons along the rays
        photon_valley = Dot(color=OPTICAL_COLOR, radius=0.08)
        photon_ridge = Dot(color=OPTICAL_COLOR, radius=0.08)

        self.play(Create(ray_valley), run_time=1.0)
        self.play(MoveAlongPath(photon_valley, ray_valley), run_time=1.2, rate_func=smooth)
        self.play(FadeOut(photon_valley), run_time=0.2)

        self.play(Create(ray_ridge), run_time=1.0)
        self.play(MoveAlongPath(photon_ridge, ray_ridge), run_time=0.8, rate_func=smooth)
        self.play(
            Create(scatter_rays), Create(cross),
            FadeOut(photon_ridge),
            run_time=0.8
        )
        self.wait(0.5)

        self.play(FadeIn(explanation, shift=UP * 0.2), run_time=0.8)

        # Target 17.64s. Total play so far = 10.0s. Need 6.64s wait.
        self.wait(6.64)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8) # Silence gap

    def sensor_comparison(self):
        """So sánh ba loại cảm biến — Segment 4 = 23.23s."""
        section = self.get_section_title("Ba dòng công nghệ cảm biến chính")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        sensors = [
            ("Cảm biến Quang học", OPTICAL_COLOR, [
                "Nguyên lý: Phản xạ toàn phần bị chặn",
                "Ưu điểm: Độ bền vật lý cao, diện tích lớn",
                "Nhược điểm: Cồng kềnh, dễ bị đánh lừa"
            ]),
            ("Cảm biến Bán dẫn", SOLID_STATE_COLOR, [
                "Nguyên lý: Điện dung, Nhiệt, Điện trường",
                "Ưu điểm: Nhỏ gọn, dễ tích hợp điện thoại",
                "Nhược điểm: Dễ bị hỏng do tĩnh điện"
            ]),
            ("Cảm biến Siêu âm", ULTRASOUND_COLOR, [
                "Nguyên lý: Phản hồi sóng siêu âm",
                "Ưu điểm: Xuyên thấu chất bẩn, da khô/ướt",
                "Nhược điểm: Giá thành cao, công nghệ phức tạp"
            ]),
        ]

        cards = VGroup()
        for name, color, desc_lines in sensors:
            card_box = create_rounded_box(
                width=4.1, height=3.2,
                fill_color=color, fill_opacity=0.08,
                stroke_color=color, stroke_width=1.5,
            )
            title = self.ct(name, font_size=20, color=color, weight=BOLD)
            desc_group = VGroup(*[
                self.ct(line, font_size=13, color=TEXT_COLOR)
                for line in desc_lines
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            content = VGroup(title, desc_group).arrange(DOWN, buff=0.3)
            content.move_to(card_box)
            cards.add(VGroup(card_box, content))

        cards.arrange(RIGHT, buff=0.35).shift(DOWN * 0.3)

        # 1. Fade in Optical card (0.0s - 0.8s)
        self.play(FadeIn(cards[0], shift=UP * 0.5), run_time=0.8)
        self.wait(3.5) # Total 4.3s

        # 2. Fade in Solid-state card (4.3s - 5.1s)
        self.play(FadeIn(cards[1], shift=UP * 0.5), run_time=0.8)
        self.wait(1.0) # Total 6.1s

        # --- CAPACITIVE SENSOR ZOOM-IN POP-UP TRANSITION ---
        # Shift the two cards out of the center
        self.play(
            cards[0].animate.scale(0.6).to_edge(LEFT, buff=0.4).shift(UP * 0.8).set_opacity(0.4),
            cards[1].animate.scale(0.6).to_edge(RIGHT, buff=0.4).shift(UP * 0.8).set_opacity(0.4),
            run_time=1.0
        ) # Total 7.1s

        # Build detailed capacitive schematic
        popup_box = create_rounded_box(width=8.0, height=4.2, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=2).shift(DOWN * 0.4)
        popup_title = self.ct("Cơ chế Cảm biến Điện dung (Capacitive)", font_size=16, color=CHART_BLUE, weight=BOLD).next_to(popup_box.get_top(), DOWN, buff=0.2)
        
        silicon = Line(LEFT * 3.0, RIGHT * 3.0, color="#555555", stroke_width=4).shift(popup_box.get_center() + DOWN * 0.8)
        silicon_lbl = self.ct("Bề mặt Silicon", font_size=11, color=TEXT_DIM).next_to(silicon, DOWN, buff=0.1)
        
        e1 = Square(side_length=0.4, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.3, stroke_width=1).move_to(silicon.get_center() + LEFT * 1.5 + UP * 0.2)
        e2 = Square(side_length=0.4, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.3, stroke_width=1).move_to(silicon.get_center() + RIGHT * 1.5 + UP * 0.2)
        e1_lbl = self.ct("Điện cực 1 (Ridge)", font_size=9, color=PRIMARY).next_to(e1, DOWN, buff=0.05)
        e2_lbl = self.ct("Điện cực 2 (Valley)", font_size=9, color=PRIMARY).next_to(e2, DOWN, buff=0.05)
        
        skin_path = VMobject()
        skin_path.set_points_smoothly([
            silicon.get_center() + LEFT * 2.8 + UP * 0.3,
            silicon.get_center() + LEFT * 1.5 + UP * 0.21,  # Ridge touches
            silicon.get_center() + ORIGIN + UP * 1.3,
            silicon.get_center() + RIGHT * 1.5 + UP * 1.0, # Valley floats above
            silicon.get_center() + RIGHT * 2.8 + UP * 1.1,
        ])
        skin_path.set_stroke(color="#d4a574", width=3)
        skin_lbl = self.ct("Lớp da ngón tay", font_size=11, color="#d4a574").next_to(skin_path.get_top(), UP, buff=0.05)
        
        c1_lbl = MathTex(r"C_{\text{High}}", font_size=20, color=MATCH_COLOR).next_to(e1, UP, buff=0.1)
        c2_lbl = MathTex(r"C_{\text{Low}}", font_size=20, color=MISMATCH_COLOR).next_to(e2, UP, buff=0.1)
        
        # Charges
        charge_plus1 = self.ct("+", font_size=12, color=MATCH_COLOR).move_to(e1.get_center())
        charge_plus2 = self.ct("+", font_size=8, color=MISMATCH_COLOR).move_to(e2.get_center())
        charge_minus1 = self.ct("-", font_size=12, color=MATCH_COLOR).move_to(silicon.get_center() + LEFT * 1.5 + UP * 0.25)
        charge_minus2 = self.ct("-", font_size=8, color=MISMATCH_COLOR).move_to(silicon.get_center() + RIGHT * 1.5 + UP * 0.9)
        
        charges = VGroup(charge_plus1, charge_plus2, charge_minus1, charge_minus2)
        capacitive_popup = VGroup(popup_box, popup_title, silicon, silicon_lbl, e1, e2, e1_lbl, e2_lbl, skin_path, skin_lbl, c1_lbl, c2_lbl, charges)

        self.play(FadeIn(popup_box), FadeIn(popup_title), run_time=0.6) # Total 7.7s
        self.play(Create(silicon), FadeIn(silicon_lbl), Create(e1), Create(e2), FadeIn(e1_lbl), FadeIn(e2_lbl), run_time=0.9) # Total 8.6s
        self.play(Create(skin_path), FadeIn(skin_lbl), run_time=0.8) # Total 9.4s
        self.play(FadeIn(c1_lbl), FadeIn(c2_lbl), FadeIn(charges), run_time=0.7) # Total 10.1s
        self.play(Indicate(c1_lbl, color=MATCH_COLOR, scale_factor=1.3), run_time=0.8) # Total 10.9s
        self.wait(1.2) # Total 12.1s

        # Fade out pop-up and restore layout
        self.play(
            FadeOut(capacitive_popup),
            cards[0].animate.scale(1/0.6).move_to(cards[0].get_center()).set_opacity(1.0),
            cards[1].animate.scale(1/0.6).move_to(cards[1].get_center()).set_opacity(1.0),
            run_time=1.0
        ) # Total 13.1s

        # 3. Fade in Ultrasound card (13.1s - 13.9s)
        self.play(FadeIn(cards[2], shift=UP * 0.5), run_time=0.8) # Total 13.9s

        # Animate ultrasound waves inside card 3
        wave_center = cards[2].get_center() + DOWN * 0.8
        waves_up = VGroup()
        for i in range(3):
            arc = Arc(radius=0.25 + i * 0.25, start_angle=PI/6, angle=2*PI/3, color=CHART_BLUE, stroke_width=2.0).move_to(wave_center, aligned_edge=DOWN)
            waves_up.add(arc)
            
        waves_down = VGroup()
        for i in range(3):
            arc = Arc(radius=0.75 - i * 0.25, start_angle=PI/6, angle=2*PI/3, color=CHART_ORANGE, stroke_width=1.5).move_to(wave_center, aligned_edge=DOWN)
            d_arc = DashedVMobject(arc, num_dashes=6)
            waves_down.add(d_arc)

        self.play(LaggedStart(*[Create(w) for w in waves_up], lag_ratio=0.25), run_time=1.2) # Total 15.1s
        self.play(LaggedStart(*[Create(w) for w in waves_down], lag_ratio=0.25), run_time=1.2) # Total 16.3s

        # Target = 23.23s. FadeOut = 1.0s. Wait remaining: 23.23s - 16.3s - 1.0s = 5.93s.
        self.wait(5.93)
        self.play(FadeOut(VGroup(section, cards, waves_up, waves_down)), run_time=1.0)
        self.wait(0.8) # Silence gap

    def new_tech_and_challenges(self):
        """Thách thức và công nghệ mới — Segment 5 = 15.31s."""
        section = self.get_section_title("Thách thức & Hướng phát triển mới")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Khối bên trái: Thách thức (Challenges)
        left_box = create_rounded_box(
            width=5.0, height=3.2,
            fill_color=SECONDARY, fill_opacity=0.2,
            stroke_color=DELTA_COLOR, stroke_width=1.5,
        )
        left_title = self.ct("Hạn chế của máy quét hiện tại", font_size=18, color=DELTA_COLOR, weight=BOLD)
        left_points = VGroup(
            self.ct("Khó hoạt động khi ngón tay quá khô hoặc ướt", font_size=13, color=TEXT_COLOR),
            self.ct("Biến dạng da do lực ép ngón tay", font_size=13, color=TEXT_COLOR),
            self.ct("Nguy cơ bị đánh lừa bởi vân tay giả", font_size=13, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.2)
        left_content = VGroup(left_title, left_points).arrange(DOWN, buff=0.35)
        left_content.move_to(left_box)
        left_group = VGroup(left_box, left_content)

        # Khối bên phải: Công nghệ mới (New Technologies)
        right_box = create_rounded_box(
            width=5.0, height=3.2,
            fill_color=SECONDARY, fill_opacity=0.3,
            stroke_color=MATCH_COLOR, stroke_width=1.5,
        )
        right_title = self.ct("Giải pháp công nghệ tương lai", font_size=18, color=MATCH_COLOR, weight=BOLD)
        right_points = VGroup(
            self.ct("Quét đa phổ: Đọc vân dưới biểu bì", font_size=13, color=TEXT_COLOR),
            self.ct("Quét 3D không tiếp xúc: Loại bỏ biến dạng cơ học", font_size=13, color=TEXT_COLOR),
            self.ct("Tiêu chuẩn FBI CJIS: Chuẩn hóa chất lượng ảnh AFIS", font_size=13, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.2)
        right_content = VGroup(right_title, right_points).arrange(DOWN, buff=0.35)
        right_content.move_to(right_box)
        right_group = VGroup(right_box, right_content)

        both = VGroup(left_group, right_group).arrange(RIGHT, buff=0.6).shift(DOWN * 0.3)

        self.play(FadeIn(left_group, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(5.0)
        self.play(FadeIn(right_group, shift=LEFT * 0.3), run_time=0.8)

        # Target = 15.31s. Total play so far = 0.6 + 0.8 + 5.0 + 0.8 = 7.2s. Remaining wait: 15.31s - 7.2s - 1.0s = 7.11s.
        self.wait(7.11)
        self.play(FadeOut(VGroup(section, both)), run_time=1.0)