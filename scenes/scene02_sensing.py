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
        """Tiêu đề mục — Segment 1 = 5.06s."""
        num = self.ct("01", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Thu Nhận Vân Tay", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Làm thế nào để số hóa cấu trúc đường vân?", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)

        # Total anim play = 2.5s. Target 5.06s before FadeOut completes (5.86s total including start offset).
        self.wait(1.56)
        self.play(FadeOut(group), run_time=1.0)
        self.wait(0.8) # Silence gap

    def offline_vs_livescan(self):
        """So sánh phương pháp offline (mực) và live-scan — Segment 2 & 3 = 12.18s."""
        section = self.get_section_title("Phương pháp thu nhận vân tay")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Phương pháp offline (trái)
        offline_box = create_rounded_box(
            width=5.3, height=3.8,
            fill_color=CHART_ORANGE, fill_opacity=0.08,
            stroke_color=CHART_ORANGE, stroke_width=1.5,
        )
        offline_title = self.ct("Thu nhận Ngoại tuyến", font_size=20, color=CHART_ORANGE, weight=BOLD)
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
            fill_color=RIDGE_COLOR, fill_opacity=0.08,
            stroke_color=RIDGE_COLOR, stroke_width=2,
        )
        livescan_title = self.ct("Thu nhận Trực tiếp", font_size=20, color=RIDGE_COLOR, weight=BOLD)
        livescan_subtitle = self.ct("Công nghệ quét điện tử hiện đại", font_size=14, color=RIDGE_COLOR)
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
            color=RIDGE_COLOR, stroke_width=3, buff=0.3,
        )
        arrow_label = self.ct("Phát triển", font_size=14, color=RIDGE_COLOR).next_to(arrow, UP, buff=0.2)

        self.play(FadeIn(offline_group, shift=RIGHT * 0.3), run_time=0.8)
        # Segment 2 starts at 5.86s, Segment 3 starts at 12.44s.
        # Section (0.6s) + offline_group (0.8s) + wait (4.38s) + Arrow (0.8s) = 6.58s.
        self.wait(4.38)  # Đọc đoạn offline
        self.play(GrowArrow(arrow), FadeIn(arrow_label), run_time=0.8)
        self.play(FadeIn(livescan_group, shift=LEFT * 0.3), run_time=0.8)

        # Segment 3 starts at 12.44s, Segment 4 starts at 18.84s (Gap = 6.40s).
        # livescan_group in (0.8s) + wait (3.8s) + FadeOut (1.0s) = 5.60s.
        # Silence gap (0.8s) = 6.40s.
        self.wait(3.8)
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

        # Segment 4 starts at 18.84s, Segment 5 starts at 23.84s (Gap = 5.00s)
        # Section (0.6s) + prism_in (1.2s) + wait(0.5s) + valley_arrow/source (1.2s) + ridge_arrow (0.8s) + wait (0.7s) = 5.00s.
        self.wait(0.7)

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
        # Segment 5 starts at 23.84s, Segment 6 starts at 31.68s (Gap = 7.84s)
        # ray_valley (1.0s) + photon_valley (1.2s) + fade (0.2s) + ray_ridge (1.0s) + photon_ridge (0.8s) + scatter (0.8s) + wait (2.84s) = 7.84s.
        self.wait(2.84)

        self.play(FadeIn(explanation, shift=UP * 0.2), run_time=0.8)

        # Segment 6 starts at 31.68s, Segment 7 starts at 36.42s (Gap = 4.74s)
        # explanation_in (0.8s) + wait (2.14s) + FadeOut (1.0s) = 3.94s.
        # Silence gap (0.8s) = 4.74s.
        self.wait(2.44)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.7) # Silence gap

    def sensor_comparison(self):
        """So sánh ba loại cảm biến — Segment 7 - 10 = 23.64s."""
        section = self.get_section_title("Ba dòng công nghệ cảm biến chính")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        sensors = [
            ("Cảm biến Quang học", OPTICAL_COLOR, [
                "Nguyên lý: Phản xạ toàn phần bị suy giảm",
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

        # 1. Fade in Optical card
        self.play(FadeIn(cards[0], shift=UP * 0.5), run_time=0.8)
        # Segment 7 starts at 36.42s, Segment 8 starts at 40.74s (Gap = 4.32s).
        # section_in (0.6s) + card0_in (0.8s) + wait (2.92s) = 4.32s.
        self.wait(2.62)

        # 2. Fade in Solid-state card
        self.play(FadeIn(cards[1], shift=UP * 0.5), run_time=0.8)
        # Segment 8 starts at 40.74s, Segment 9 starts at 45.68s (Gap = 4.94s).
        # card1_in (0.8s) + wait (4.14s) = 4.94s.
        self.wait(4.14)

        # --- CAPACITIVE SENSOR ZOOM-IN POP-UP TRANSITION ---
        cards[0].save_state()
        cards[1].save_state()
        self.play(
            cards[0].animate.scale(0.6).to_edge(LEFT, buff=0.4).shift(UP * 0.8).set_opacity(0.4),
            cards[1].animate.scale(0.6).to_edge(RIGHT, buff=0.4).shift(UP * 0.8).set_opacity(0.4),
            run_time=1.0
        )

        # Build detailed capacitive schematic
        popup_box = create_rounded_box(width=8.0, height=4.2, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=2).shift(DOWN * 0.4)
        popup_title = self.ct("Cơ chế Cảm biến Điện dung", font_size=16, color=CHART_BLUE, weight=BOLD).next_to(popup_box.get_top(), DOWN, buff=0.2)
        
        center = popup_box.get_center()

        # Silicon substrate
        substrate = RoundedRectangle(
            width=6.6, height=0.6,
            fill_color="#2c3e50", fill_opacity=0.8,
            stroke_color=GRAY, stroke_width=1.5
        ).move_to(center + DOWN * 0.9)
        substrate_lbl = self.ct("Đế Silicon", font_size=11, color=TEXT_DIM).next_to(substrate, DOWN, buff=0.15)
        
        # Embedded sensing electrodes
        e1 = Rectangle(width=1.2, height=0.2, fill_color=PRIMARY, fill_opacity=0.6, stroke_color=PRIMARY, stroke_width=1.5).move_to(center + LEFT * 1.8 + DOWN * 0.7)
        e2 = Rectangle(width=1.2, height=0.2, fill_color=PRIMARY, fill_opacity=0.6, stroke_color=PRIMARY, stroke_width=1.5).move_to(center + RIGHT * 1.8 + DOWN * 0.7)
        e1_lbl = self.ct("Điện cực", font_size=11, color=TEXT_DIM).move_to(center + LEFT * 1.8 + DOWN * 1.0)
        e2_lbl = self.ct("Điện cực", font_size=11, color=TEXT_DIM).move_to(center + RIGHT * 1.8 + DOWN * 1.0)
        
        # Skin profile
        skin_path = VMobject()
        skin_path.set_points_smoothly([
            center + LEFT * 3.0 + DOWN * 0.2,
            center + LEFT * 1.8 + DOWN * 0.55,  # Ridge
            center + ORIGIN + UP * 0.5,
            center + RIGHT * 1.8 + UP * 0.6,    # Valley
            center + RIGHT * 3.0 + UP * 0.7,
        ])
        skin_path.set_stroke(color="#d4a574", width=4)
        
        ridge_lbl = self.ct("Đường vân", font_size=12, color=RIDGE_COLOR, weight=BOLD).move_to(center + LEFT * 1.8 + UP * 0.25)
        valley_lbl = self.ct("Rãnh", font_size=12, color=TEXT_DIM, weight=BOLD).move_to(center + RIGHT * 1.8 + UP * 1.05)
        
        c1_lbl = MathTex(r"C_{\text{High}}", font_size=24, color=MATCH_COLOR).move_to(center + LEFT * 1.8 + DOWN * 0.3)
        c2_lbl = MathTex(r"C_{\text{Low}}", font_size=24, color=MISMATCH_COLOR).move_to(center + RIGHT * 1.8 + UP * 0.15)
        
        # Electric field lines
        field_lines = VGroup()
        for dx in [-0.4, -0.2, 0.0, 0.2, 0.4]:
            line = DashedLine(
                start=center + LEFT * 1.8 + dx * RIGHT + DOWN * 0.6,
                end=center + LEFT * 1.8 + dx * RIGHT + DOWN * 0.55,
                color=MATCH_COLOR, stroke_width=2, dashed_ratio=0.5
            )
            field_lines.add(line)
            
        for dx in [-0.3, 0.0, 0.3]:
            line = DashedLine(
                start=center + RIGHT * 1.8 + dx * RIGHT + DOWN * 0.6,
                end=center + RIGHT * 1.8 + dx * RIGHT + UP * 0.6,
                color=MISMATCH_COLOR, stroke_width=1.5, dashed_ratio=0.5
            )
            field_lines.add(line)
            
        # Charges
        charges = VGroup()
        for dx in [-0.3, 0.0, 0.3]:
            charges.add(self.ct("+", font_size=14, color=TEXT_BRIGHT, weight=BOLD).move_to(center + LEFT * 1.8 + dx * RIGHT + DOWN * 0.7))
        for dx in [-0.2, 0.2]:
            charges.add(self.ct("+", font_size=10, color=TEXT_DIM).move_to(center + RIGHT * 1.8 + dx * RIGHT + DOWN * 0.7))
            
        for dx in [-0.4, -0.2, 0.0, 0.2, 0.4]:
            charges.add(self.ct("-", font_size=14, color=MATCH_COLOR, weight=BOLD).move_to(center + LEFT * 1.8 + dx * RIGHT + DOWN * 0.45))
        for dx in [-0.3, 0.3]:
            charges.add(self.ct("-", font_size=10, color=MISMATCH_COLOR).move_to(center + RIGHT * 1.8 + dx * RIGHT + UP * 0.85))

        capacitive_popup = VGroup(
            popup_box, popup_title, substrate, substrate_lbl, 
            e1, e2, e1_lbl, e2_lbl, skin_path, ridge_lbl, valley_lbl, 
            c1_lbl, c2_lbl, field_lines, charges
        )

        self.play(FadeIn(popup_box), FadeIn(popup_title), run_time=0.6)
        self.play(Create(substrate), FadeIn(substrate_lbl), Create(e1), Create(e2), FadeIn(e1_lbl), FadeIn(e2_lbl), run_time=0.9)
        self.play(Create(skin_path), FadeIn(ridge_lbl), FadeIn(valley_lbl), run_time=0.8)
        self.play(FadeIn(c1_lbl), FadeIn(c2_lbl), Create(field_lines), FadeIn(charges), run_time=0.8)
        self.play(Indicate(c1_lbl, color=MATCH_COLOR, scale_factor=1.3), run_time=0.8)
        
        # Segment 9 starts at 45.68s, Segment 10 starts at 51.08s (Gap = 5.40s).
        # scale_out (1.0s) + box_in (0.6s) + sub_in (0.9s) + skin_in (0.8s) + field_in (0.8s) + indicate (0.8s) + wait (0.5s) = 5.40s.
        self.wait(0.5)

        # Fade out pop-up and restore layout
        self.play(
            FadeOut(capacitive_popup),
            Restore(cards[0]),
            Restore(cards[1]),
            run_time=1.0
        )

        # 3. Fade in Ultrasound card (Dim cards 0 and 1)
        self.play(
            FadeIn(cards[2], shift=UP * 0.5),
            cards[0].animate.set_opacity(0.3),
            cards[1].animate.set_opacity(0.3),
            run_time=0.8
        )

        # Animate ultrasound waves inside card 3
        wave_center = cards[2].get_center() + DOWN * 1.0
        waves_up = VGroup()
        for i in range(3):
            arc = Arc(radius=0.15 + i * 0.15, start_angle=PI/6, angle=2*PI/3, color=CHART_BLUE, stroke_width=1.5).move_to(wave_center, aligned_edge=DOWN)
            waves_up.add(arc)
            
        waves_down = VGroup()
        for i in range(3):
            arc = Arc(radius=0.45 - i * 0.15, start_angle=-5*PI/6, angle=2*PI/3, color=CHART_ORANGE, stroke_width=1.0).move_to(wave_center, aligned_edge=UP)
            d_arc = DashedVMobject(arc, num_dashes=6)
            waves_down.add(d_arc)

        # Pulse animation
        self.play(LaggedStart(*[Create(w) for w in waves_up], lag_ratio=0.2), run_time=1.0)
        self.play(
            LaggedStart(*[Create(w) for w in waves_down], lag_ratio=0.2), 
            FadeOut(waves_up), 
            run_time=1.0
        )
        self.play(
            FadeOut(waves_down), 
            Restore(cards[0]),
            Restore(cards[1]),
            run_time=0.8
        )

        # Segment 10 starts at 51.08s, Segment 11 starts at 60.06s (Gap = 8.98s).
        # restore_pop (1.0s) + card2_in (0.8s) + waves_up (1.0s) + waves_down (1.0s) + waves_out (0.8s) + wait (2.58s) + FadeOut (1.0s) + silence_gap (0.8s) = 8.98s.
        self.wait(3.18)
        self.play(FadeOut(VGroup(section, cards)), run_time=0.6)
        self.wait(0.6) # Silence gap

    def new_tech_and_challenges(self):
        """Thách thức và công nghệ mới — Segment 11 - 13 = 14.10s."""
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
        # Segment 11 starts at 60.06s, Segment 12 starts at 66.90s (Gap = 6.84s).
        # Section (0.6s) + left_group_in (0.8s) + wait (5.44s) = 6.84s.
        self.wait(5.44)

        self.play(FadeIn(right_group, shift=LEFT * 0.3), run_time=0.8)
        # Segment 12 starts at 66.90s, Segment 13 starts at 70.48s (Gap = 3.58s).
        # right_group_in (0.8s) + wait (2.78s) = 3.58s.
        self.wait(2.78)

        # Segment 13 starts at 70.48s, End of Scene 2 at 74.16s (Gap = 3.68s).
        # Highlight FBI CJIS standard bullet point
        self.play(Indicate(right_points[2], color=PRIMARY, scale_factor=1.15), run_time=1.0)
        self.wait(4.08)
        self.play(FadeOut(VGroup(section, both)), run_time=1.0)