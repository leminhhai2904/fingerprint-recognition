"""
Scene 7: Tóm tắt & Kết luận (Conclusion)
- Tóm tắt quy trình (Recap Pipeline) gồm 3 giai đoạn chính với hiệu ứng laser pulse & ripple
- Đánh giá hiệu suất: FVC, EER Graph (FMR vs FNMR), NIST FpVTE 2003 database card
- Thách thức mở & Tạo vân tay ảo SFinGe với ValueTracker count-up
- Lời cảm ơn & Kết thúc + Vẽ vân tay nền quay chậm
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
        self.performance_evaluation()
        self.open_challenges()
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

    def make_glowing(self, mobject, color=PRIMARY, stroke_width_base=3, opacities=[0.1, 0.25, 0.65]):
        """Tạo hiệu ứng phát sáng Neon cao cấp bằng cách xếp lớp chồng lên nhau."""
        glow = VGroup()
        for op, w_mul in zip(opacities, [4, 2, 1]):
            glow.add(
                mobject.copy().set_stroke(color=color, width=stroke_width_base * w_mul, opacity=op)
            )
        return glow

    def pipeline_recap(self):
        """Tóm tắt quy trình 3 giai đoạn — Segment 1 = 8.42s."""
        title_main = self.ct("Tóm Tắt Quy Trình Nhận Dạng", font_size=28, color=TEXT_BRIGHT, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(FadeIn(title_main, shift=DOWN * 0.2), run_time=0.5)

        # Hộp bo góc cho 3 giai đoạn
        box_w, box_h = 3.2, 1.8
        pos1 = LEFT * 4 + DOWN * 0.4
        pos2 = DOWN * 0.4
        pos3 = RIGHT * 4 + DOWN * 0.4

        # Giai đoạn 1: Thu nhận
        card1 = create_rounded_box(width=box_w, height=box_h, fill_color=OPTICAL_COLOR, fill_opacity=0.08, stroke_color=OPTICAL_COLOR, stroke_width=1.5).move_to(pos1)
        lbl1 = self.ct("1. Thu nhận ảnh", font_size=15, color=OPTICAL_COLOR, weight=BOLD).next_to(card1.get_top(), DOWN, buff=0.25)
        sensor_bg = Square(side_length=0.6, color=TEXT_DIM, fill_opacity=0.1).move_to(card1.get_center() + DOWN * 0.2)
        sensor_line = Line(sensor_bg.get_left(), sensor_bg.get_right(), color=OPTICAL_COLOR, stroke_width=2).move_to(sensor_bg.get_center())
        card1_content = VGroup(lbl1, sensor_bg, sensor_line)

        # Giai đoạn 2: Trích đặc trưng
        card2 = create_rounded_box(width=box_w, height=box_h, fill_color=CHART_ORANGE, fill_opacity=0.08, stroke_color=CHART_ORANGE, stroke_width=1.5).move_to(pos2)
        lbl2 = self.ct("2. Trích đặc trưng", font_size=15, color=CHART_ORANGE, weight=BOLD).next_to(card2.get_top(), DOWN, buff=0.25)
        m_pt = Dot(card2.get_center() + DOWN * 0.2, color=CHART_ORANGE, radius=0.08)
        m_line1 = Line(m_pt.get_center(), m_pt.get_center() + UP * 0.25 + RIGHT * 0.15, color=CHART_ORANGE, stroke_width=2)
        m_line2 = Line(m_pt.get_center(), m_pt.get_center() + DOWN * 0.25 + LEFT * 0.15, color=CHART_ORANGE, stroke_width=2)
        card2_content = VGroup(lbl2, m_pt, m_line1, m_line2)

        # Giai đoạn 3: Đối sánh
        card3 = create_rounded_box(width=box_w, height=box_h, fill_color=CHART_BLUE, fill_opacity=0.08, stroke_color=CHART_BLUE, stroke_width=1.5).move_to(pos3)
        lbl3 = self.ct("3. Đối sánh", font_size=15, color=CHART_BLUE, weight=BOLD).next_to(card3.get_top(), DOWN, buff=0.25)
        c_circle1 = Circle(radius=0.25, color=CHART_BLUE, stroke_width=1.5).move_to(card3.get_center() + DOWN * 0.2 + LEFT * 0.1)
        c_circle2 = Circle(radius=0.25, color=PRIMARY, stroke_width=1.5).move_to(card3.get_center() + DOWN * 0.2 + RIGHT * 0.1)
        card3_content = VGroup(lbl3, c_circle1, c_circle2)

        # Đường liên kết laser
        laser1 = DashedLine(card1.get_right(), card2.get_left(), color=PRIMARY, stroke_width=2, dash_length=0.1)
        laser2 = DashedLine(card2.get_right(), card3.get_left(), color=PRIMARY, stroke_width=2, dash_length=0.1)

        # Hộp hiển thị kết quả
        res_box = create_rounded_box(width=4.0, height=0.9, fill_color=SECONDARY, fill_opacity=0.4, stroke_color=TEXT_DIM, stroke_width=1.5).shift(DOWN * 2.2)
        res_text = self.ct("ĐANG ĐỐI SÁNH...", font_size=14, color=TEXT_DIM, weight=BOLD).move_to(res_box.get_center())

        # Animate các khối xuất hiện
        self.play(
            FadeIn(card1), FadeIn(card1_content),
            FadeIn(card2), FadeIn(card2_content),
            FadeIn(card3), FadeIn(card3_content),
            run_time=0.8
        )
        self.play(Create(laser1), Create(laser2), run_time=0.6)

        laser1_glow = self.make_glowing(laser1, color=PRIMARY)
        laser2_glow = self.make_glowing(laser2, color=PRIMARY)
        self.play(FadeIn(laser1_glow), FadeIn(laser2_glow), run_time=0.4)

        # Kết quả đối sánh
        self.play(FadeIn(res_box), FadeIn(res_text), run_time=0.5)

        success_text = self.ct("KHỚP THÀNH CÔNG!", font_size=14, color=MATCH_COLOR, weight=BOLD).move_to(res_box.get_center())
        self.play(
            FadeOut(res_text),
            FadeIn(success_text),
            res_box.animate.set_color(MATCH_COLOR).set_stroke(width=2.5),
            run_time=0.5
        )

        # Hiệu ứng sóng lan tỏa từ kết quả
        ripple = Circle(radius=0.1, color=MATCH_COLOR, stroke_width=2.5).move_to(res_box.get_center())
        self.add(ripple)
        self.play(ripple.animate.scale(25).set_stroke(opacity=0), run_time=0.8, rate_func=smooth)
        self.remove(ripple)

        # Target = 8.42s. Anim play = 0.5 + 0.8 + 0.6 + 0.4 + 0.5 + 0.5 + 0.8 = 4.1s
        # Remaining: 8.42 - 4.1 - 0.8 (FadeOut) = 3.52s
        self.wait(3.52)
        self.play(
            FadeOut(VGroup(
                title_main, card1, card1_content, card2, card2_content, card3, card3_content,
                laser1, laser2, laser1_glow, laser2_glow, res_box, success_text
            )),
            run_time=0.8
        )
        self.wait(0.8)

    def performance_evaluation(self):
        """Đánh giá hiệu suất: FVC, NIST FpVTE và EER Graph — Segment 2 = 29.09s."""
        section = self.get_section_hdr("Chuẩn Đánh Giá & Hiệu Suất")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # --- Giai đoạn 1: FVC & Biểu đồ tăng trưởng (0.6s - 19.0s) ---
        fvc_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=PRIMARY, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        fvc_title = self.ct("Đánh giá thuật toán: Cuộc thi FVC", font_size=15, color=PRIMARY, weight=BOLD).next_to(fvc_box.get_top(), DOWN, buff=0.2)

        # Biểu đồ cột mini cho sự tham gia FVC (2000 vs 2006)
        bar_bg_left = fvc_box.get_center() + DOWN * 0.6
        bar_2000 = Rectangle(width=0.8, height=0.5, color=CHART_BLUE, fill_opacity=0.6, stroke_width=1, stroke_color=CHART_BLUE).move_to(bar_bg_left + LEFT * 1.0, aligned_edge=DOWN)
        bar_2006 = Rectangle(width=0.8, height=3.0, color=PRIMARY, fill_opacity=0.6, stroke_width=1, stroke_color=PRIMARY).move_to(bar_bg_left + RIGHT * 1.0, aligned_edge=DOWN)

        lbl_2000 = self.ct("25 Đội\n(FVC2000)", font_size=9, color=TEXT_DIM).next_to(bar_2000, DOWN, buff=0.1)
        lbl_2006 = self.ct("150 Đội\n(FVC2006)", font_size=9, color=PRIMARY).next_to(bar_2006, DOWN, buff=0.1)
        fvc_growth = VGroup(bar_2000, bar_2006, lbl_2000, lbl_2006)

        fvc_best = create_rounded_box(width=4.8, height=0.7, fill_color=MATCH_COLOR, fill_opacity=0.15, stroke_color=MATCH_COLOR, stroke_width=1.5).move_to(fvc_box.get_center() + UP * 0.8)
        fvc_best_lbl = self.ct("Kỷ lục EER tốt nhất: 2.07% (FVC2004)", font_size=11, color=MATCH_COLOR, weight=BOLD).move_to(fvc_best.get_center())

        # --- Giai đoạn 2: Đồ thị EER ở bên phải ---
        graph_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        graph_title = self.ct("Chỉ số lỗi tương đương (EER)", font_size=15, color=CHART_BLUE, weight=BOLD).next_to(graph_box.get_top(), DOWN, buff=0.2)

        graph_center = graph_box.get_center() + DOWN * 0.4
        origin = graph_center + LEFT * 2.0 + DOWN * 0.7
        x_axis = Line(origin, origin + RIGHT * 3.8, color=TEXT_DIM, stroke_width=1.5)
        y_axis = Line(origin, origin + UP * 2.2, color=TEXT_DIM, stroke_width=1.5)
        x_lbl = self.ct("Ngưỡng quyết định (t)", font_size=9, color=TEXT_DIM).next_to(x_axis, DOWN, buff=0.08)
        y_lbl = self.ct("Tỷ lệ lỗi (%)", font_size=9, color=TEXT_DIM).next_to(y_axis, UP, buff=0.08)

        # FMR curve (False Match Rate): giảm dần
        fmr_points = []
        for x_val in np.linspace(0, 3.4, 25):
            y_val = 1.9 * np.exp(-1.4 * x_val)
            fmr_points.append(origin + np.array([x_val, y_val, 0]))
        fmr_curve = VMobject()
        fmr_curve.set_points_smoothly(fmr_points)
        fmr_curve.set_stroke(color=DELTA_COLOR, width=2.5)
        fmr_lbl = self.ct("FMR", font_size=10, color=DELTA_COLOR).next_to(fmr_points[5], UR, buff=0.05)

        # FNMR curve (False Non-Match Rate): tăng dần
        fnmr_points = []
        for x_val in np.linspace(0, 3.4, 25):
            y_val = 1.9 * (1 - np.exp(-1.0 * x_val))
            fnmr_points.append(origin + np.array([x_val, y_val, 0]))
        fnmr_curve = VMobject()
        fnmr_curve.set_points_smoothly(fnmr_points)
        fnmr_curve.set_stroke(color=CHART_BLUE, width=2.5)
        fnmr_lbl = self.ct("FNMR", font_size=10, color=CHART_BLUE).next_to(fnmr_points[20], UL, buff=0.05)

        # Điểm giao EER
        eer_pos = origin + np.array([0.54, 0.89, 0])
        eer_dot = Dot(eer_pos, color=MATCH_COLOR, radius=0.08)
        eer_txt = self.ct("EER (FMR=FNMR)", font_size=11, color=MATCH_COLOR, weight=BOLD).next_to(eer_dot, UR, buff=0.05)
        proj_x = DashedLine(eer_pos, [eer_pos[0], origin[1], 0], color=TEXT_DIM, stroke_width=1.0)
        proj_y = DashedLine(eer_pos, [origin[0], eer_pos[1], 0], color=TEXT_DIM, stroke_width=1.0)

        # Animate FVC Card
        self.play(FadeIn(fvc_box), FadeIn(fvc_title), run_time=0.8) # Total 1.4s
        self.play(
            GrowFromEdge(bar_2000, DOWN), GrowFromEdge(bar_2006, DOWN),
            FadeIn(lbl_2000), FadeIn(lbl_2006),
            run_time=1.2
        ) # Total 2.6s
        self.wait(2.0) # Total 4.6s

        # Animate Graph & curves
        self.play(FadeIn(graph_box), FadeIn(graph_title), Create(x_axis), Create(y_axis), FadeIn(x_lbl), FadeIn(y_lbl), run_time=1.2) # Total 5.8s
        self.play(Create(fmr_curve), FadeIn(fmr_lbl), run_time=1.0) # Total 6.8s
        self.play(Create(fnmr_curve), FadeIn(fnmr_lbl), run_time=1.0) # Total 7.8s
        
        self.play(
            Create(eer_dot), FadeIn(eer_txt, shift=UP * 0.15),
            Create(proj_x), Create(proj_y),
            Indicate(eer_dot, color=MATCH_COLOR, scale_factor=2.0),
            run_time=1.2
        ) # Total 9.0s

        # Show best FVC statistics card
        self.play(FadeIn(fvc_best), FadeIn(fvc_best_lbl), run_time=0.8) # Total 9.8s
        self.wait(5.0) # Total 14.8s

        # --- Giai đoạn 3: NIST FpVTE 2003 (14.8s - 28.29s) ---
        # Dọn dẹp FVC và Graph
        self.play(
            FadeOut(VGroup(fvc_box, fvc_title, fvc_growth, fvc_best, fvc_best_lbl)),
            FadeOut(VGroup(graph_box, graph_title, x_axis, y_axis, x_lbl, y_lbl, fmr_curve, fmr_lbl, fnmr_curve, fnmr_lbl, eer_dot, eer_txt, proj_x, proj_y)),
            run_time=1.0
        ) # Total 15.8s

        # Khởi tạo Card NIST
        nist_box = create_rounded_box(width=10.0, height=4.2, fill_color=CHART_PURPLE, fill_opacity=0.15, stroke_color=CHART_PURPLE, stroke_width=2.0).shift(DOWN * 0.4)
        nist_title = self.ct("Đánh giá NIST FpVTE 2003 (Mỹ)", font_size=18, color=CHART_PURPLE, weight=BOLD).next_to(nist_box.get_top(), DOWN, buff=0.3)

        # Database stack icon
        db_icon = VGroup()
        for i in range(3):
            ellipse = Ellipse(width=1.0, height=0.3, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.3, stroke_width=1.5).move_to(nist_box.get_center() + LEFT * 2.8 + DOWN * (0.25 * i) + UP * 0.2)
            db_icon.add(ellipse)
            
        db_lbl = self.ct("48,000+ Bộ vân tay thực tế", font_size=15, color=TEXT_BRIGHT, weight=BOLD).next_to(db_icon, RIGHT, buff=0.4)
        db_sub = self.ct("Cơ sở dữ liệu thực nghiệm kiểm thử quy mô lớn", font_size=11, color=TEXT_DIM).next_to(db_lbl, DOWN, buff=0.1, aligned_edge=LEFT)
        db_group = VGroup(db_icon, db_lbl, db_sub)

        # Systems card
        sys_icon = VGroup(
            Square(side_length=0.4, color=CHART_ORANGE, fill_opacity=0.2),
            Square(side_length=0.4, color=CHART_ORANGE, fill_opacity=0.2).shift(RIGHT * 0.25 + UP * 0.15)
        ).move_to(nist_box.get_center() + LEFT * 2.8 + DOWN * 1.0)
        
        sys_lbl = self.ct("34 Hệ thống thương mại", font_size=15, color=TEXT_BRIGHT, weight=BOLD).next_to(sys_icon, RIGHT, buff=0.4)
        sys_sub = self.ct("Thuật toán được đánh giá độc lập bởi NIST", font_size=11, color=TEXT_DIM).next_to(sys_lbl, DOWN, buff=0.1, aligned_edge=LEFT)
        sys_group = VGroup(sys_icon, sys_lbl, sys_sub)

        self.play(FadeIn(nist_box), FadeIn(nist_title), run_time=1.0) # Total 16.8s
        self.play(FadeIn(db_group, shift=RIGHT * 0.3), run_time=0.8) # Total 17.6s
        self.play(FadeIn(sys_group, shift=RIGHT * 0.3), run_time=0.8) # Total 18.4s

        # Target = 29.09s. Remaining wait = 29.09s - 18.4s - 1.0s (FadeOut) = 9.69s.
        self.wait(9.69)
        self.play(FadeOut(VGroup(section, nist_box, nist_title, db_group, sys_group)), run_time=1.0)
        self.wait(0.8)

    def open_challenges(self):
        """Bốn thách thức mở & Tạo vân tay ảo SFinGe — Segment 3 = 22.99s."""
        section = self.get_section_hdr("Thách thức mở & Công nghệ SFinGe")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)

        # Left panel: 4 challenges
        ch_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=DELTA_COLOR, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        ch_title = self.ct("Bốn thách thức lớn còn mở", font_size=16, color=DELTA_COLOR, weight=BOLD).next_to(ch_box.get_top(), DOWN, buff=0.2)

        items_text = [
            "1. Ảnh chất lượng kém & Cảm biến giá rẻ",
            "2. Chống tấn công giả mạo (Fake fingerprint)",
            "3. Bảo mật mẫu sinh trắc khỏi giải mã ngược",
            "4. Đối sánh siêu tốc trên CSDL hàng trăm triệu"
        ]
        
        ch_items = VGroup()
        for txt in items_text:
            warn_icon = Polygon(
                [-0.15, -0.1, 0], [0.15, -0.1, 0], [0, 0.18, 0],
                color=DELTA_COLOR, fill_color=DELTA_COLOR, fill_opacity=0.2, stroke_width=1.5
            )
            item_lbl = self.ct(txt, font_size=12, color=TEXT_COLOR)
            row = VGroup(warn_icon, item_lbl).arrange(RIGHT, buff=0.15)
            ch_items.add(row)
            
        ch_items.arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ch_title, DOWN, buff=0.3)
        ch_card = VGroup(ch_box, ch_title, ch_items)

        # Right panel: SFinGe Generator
        sf_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_PURPLE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        sf_title = self.ct("Sinh vân tay ảo SFinGe", font_size=16, color=CHART_PURPLE, weight=BOLD).next_to(sf_box.get_top(), DOWN, buff=0.2)

        sf_center = sf_box.get_center() + DOWN * 0.2
        sf_ridges = VGroup()
        for r_idx in range(6):
            radius = 0.25 + r_idx * 0.25
            arc = Arc(
                radius=radius, start_angle=-PI/4, angle=3*PI/2,
                color=CHART_PURPLE, stroke_width=2.0
            ).move_to(sf_center)
            sf_ridges.add(arc)

        # Laser scan line inside SFinGe
        scan_line = Line(sf_box.get_left() + UP * 1.5, sf_box.get_right() + UP * 1.5, color=PRIMARY, stroke_width=2).move_to(sf_box.get_top() + DOWN * 0.7)
        scan_line_glow = self.make_glowing(scan_line, color=PRIMARY, stroke_width_base=2)
        scan_group = VGroup(scan_line, scan_line_glow)

        counter_val = ValueTracker(0)
        counter_lbl = self.ct("Ảnh vân tay ảo: 0", font_size=12, color=PRIMARY, weight=BOLD).next_to(sf_box, DOWN, buff=0.1)

        def update_counter(mobject):
            mobject.become(
                self.ct(f"Ảnh vân tay ảo: {int(counter_val.get_value()):,}", font_size=12, color=PRIMARY, weight=BOLD).next_to(sf_box, DOWN, buff=0.1)
            )

        counter_lbl.add_updater(update_counter)

        # Animating layout
        self.play(FadeIn(ch_card, shift=RIGHT * 0.3), run_time=1.0) # Total 1.6s
        self.wait(3.0) # Total 4.6s

        self.play(FadeIn(sf_box), FadeIn(sf_title), FadeIn(counter_lbl), run_time=0.8) # Total 5.4s
        self.play(FadeIn(scan_group), run_time=0.4) # Total 5.8s

        # Procedural drawing scan animation
        self.play(
            scan_group.animate.move_to(sf_box.get_bottom() + UP * 0.4),
            LaggedStart(*[Create(r) for r in sf_ridges], lag_ratio=0.12),
            counter_val.animate.set_value(50000),
            run_time=3.0,
            rate_func=linear
        ) # Total 8.8s
        
        self.play(FadeOut(scan_group), run_time=0.4) # Total 9.2s
        counter_lbl.remove_updater(update_counter)

        # Target = 22.99s. Remaining wait = 22.99s - 9.2s - 1.0s (FadeOut) = 12.79s.
        self.wait(12.79)
        self.play(FadeOut(VGroup(section, ch_card, sf_box, sf_title, sf_ridges, counter_lbl)), run_time=1.0)
        self.wait(0.8)

    def outro(self):
        """Phần kết và lời cảm ơn — Segment 4 = 9.77s."""
        # Vân tay mờ xoay chậm ở nền làm watermark
        fp = create_fingerprint_simple(scale=0.8, color=RIDGE_COLOR)
        fp.set_opacity(0.08).scale(2.5).move_to(ORIGIN)

        # Frosted glassmorphic card trong suốt ở giữa
        outro_box = create_rounded_box(width=10.0, height=4.5, fill_color=SECONDARY, fill_opacity=0.25, stroke_color=PRIMARY, stroke_width=2.0)
        
        thanks = self.ct("Cảm ơn các bạn đã theo dõi!", font_size=38, color=TEXT_BRIGHT, weight=BOLD).next_to(outro_box.get_top(), DOWN, buff=0.4)
        thanks_glow = self.make_glowing(thanks, color=PRIMARY)

        line = Line(LEFT * 4, RIGHT * 4, color=PRIMARY, stroke_width=2.5).next_to(thanks, DOWN, buff=0.35)
        line_glow = self.make_glowing(line, color=PRIMARY)

        subtitle = self.ct("Môn học: Nhận dạng mẫu — HCMUS", font_size=20, color=RIDGE_COLOR, weight=BOLD).next_to(line, DOWN, buff=0.4)
        course = self.ct("Sinh viên thực hiện: Lê Minh Hải", font_size=16, color=TEXT_DIM).next_to(subtitle, DOWN, buff=0.25)

        hashtags = self.ct("#Biometrics #FingerprintRecognition #PatternRecognition", font_size=13, color=PRIMARY).to_edge(DOWN, buff=0.6)

        # Animate outro
        self.play(Create(fp), run_time=1.5) # Total 1.5s
        
        self.play(
            FadeIn(outro_box), Write(thanks), FadeIn(thanks_glow),
            run_time=1.2
        ) # Total 2.7s
        
        self.play(Create(line), FadeIn(line_glow), run_time=0.6) # Total 3.3s
        
        self.play(
            FadeIn(subtitle, shift=UP * 0.2),
            FadeIn(course, shift=UP * 0.2),
            FadeIn(hashtags, shift=UP * 0.2),
            run_time=0.8
        ) # Total 4.1s

        # Target = 9.77s. Anim play = 4.1s. Remaining wait = 9.77s - 4.1s - 1.0s (FadeOut) = 4.67s.
        # Đồng thời xoay nhẹ watermark vân tay trong lúc chờ
        self.play(
            Rotate(fp, angle=0.15, about_point=ORIGIN),
            run_time=4.67,
            rate_func=linear
        )
        
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
