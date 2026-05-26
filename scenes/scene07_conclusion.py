"""
Scene 7: Tóm tắt & Kết luận (Conclusion) - Phiên bản cải tiến v2
- Tóm tắt quy trình (Recap Pipeline) gồm 3 giai đoạn chính với hiệu ứng laser pulse & ripple
- Đánh giá hiệu suất: FVC, EER Graph (FMR vs FNMR), NIST FpVTE 2003 database card
- Thách thức mở & Tạo vân tay ảo SFinGe với ValueTracker count-up
- Lời cảm ơn & Kết thúc + Vẽ vân tay nền quay chậm
- Căn chỉnh thời gian chính xác theo script detect_scene_07.txt
"""
from manim import *
import numpy as np
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene07Conclusion(Scene):
    def construct(self):
        scene_setup(self)
        # 1. Pipeline Recap (0.18s - 8.58s, Duration: 8.40s)
        self.pipeline_recap()
        # 2. Performance Evaluation (FVC) (9.12s - 23.34s, Duration: 14.22s)
        self.fvc_evaluation()
        # 3. EER Graph (25.08s - 31.24s, Duration: 6.16s)
        self.eer_explanation()
        # 4. NIST Evaluation (31.64s - 37.84s, Duration: 6.20s)
        self.nist_evaluation()
        # 5. Open Challenges (39.22s - 55.76s, Duration: 16.54s)
        self.open_challenges()
        # 6. SFinGe Generation (56.60s - 64.62s, Duration: 8.02s)
        self.sfinge_generation()
        # 7. Future & Applications (65.42s - 73.64s, Duration: 8.22s)
        self.future_applications()
        # 8. Outro (73.64s - 75.24s, Duration: 1.60s + Extra Wait)
        self.outro()

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kwargs):
        """create_text với CMU Serif kerning workaround (render to lớn rồi scale xuống)."""
        return Text(text_str, font_size=36, color=color, weight=weight, **kwargs).scale(font_size / 36)

    def get_section_hdr(self, text):
        title = self.ct(text, font_size=26, color=TEXT_BRIGHT, weight=BOLD)
        underline = Line(
            start=title.get_left() + DOWN * 0.25,
            end=title.get_right() + DOWN * 0.25,
            color=PRIMARY,
            stroke_width=2.5,
        )
        return VGroup(title, underline)

    def make_glowing(self, mobject, color=PRIMARY, stroke_width_base=3, opacities=[0.1, 0.25, 0.65]):
        """Create a neon glow effect by layering."""
        glow = VGroup()
        for op, w_mul in zip(opacities, [4, 2, 1]):
            glow.add(
                mobject.copy().set_stroke(color=color, width=stroke_width_base * w_mul, opacity=op)
            )
        return glow

    def pipeline_recap(self):
        """
        Segment 1: 0.18s - 8.58s (Duration: 8.40s)
        Nhìn lại toàn bộ, hệ thống nhận dạng vân tay gồm ba giai đoạn: 
        thu nhận ảnh qua cảm biến, trích xuất đặc trưng minutiae, và đối sánh để đưa ra kết quả khớp hoặc không khớp.
        """
        # Initial wait before starting (0.18s)
        self.wait(0.18)

        # Title
        title_main = self.ct("TỔNG QUAN QUY TRÌNH NHẬN DẠNG VÂN TAY", font_size=24, color=TEXT_BRIGHT, weight=BOLD).to_edge(UP, buff=0.5)
        
        # Layout positions
        box_w, box_h = 3.4, 2.0
        pos1 = LEFT * 4 + DOWN * 0.3
        pos2 = DOWN * 0.3
        pos3 = RIGHT * 4 + DOWN * 0.3

        # Card 1: Thu nhận
        card1 = create_rounded_box(width=box_w, height=box_h, fill_color=OPTICAL_COLOR, fill_opacity=0.08, stroke_color=OPTICAL_COLOR, stroke_width=1.5).move_to(pos1)
        lbl1 = self.ct("1. Thu nhận ảnh", font_size=15, color=OPTICAL_COLOR, weight=BOLD).next_to(card1.get_top(), DOWN, buff=0.2)
        # Scanner visualization inside Card 1
        scanner_plate = RoundedRectangle(width=1.4, height=1.0, corner_radius=0.1, color=TEXT_DIM, fill_opacity=0.15).move_to(card1.get_center() + DOWN * 0.2)
        laser_line = Line(scanner_plate.get_left(), scanner_plate.get_right(), color=OPTICAL_COLOR, stroke_width=2.5).move_to(scanner_plate.get_top())
        card1_content = VGroup(lbl1, scanner_plate, laser_line)

        # Card 2: Trích đặc trưng
        card2 = create_rounded_box(width=box_w, height=box_h, fill_color=CHART_ORANGE, fill_opacity=0.08, stroke_color=CHART_ORANGE, stroke_width=1.5).move_to(pos2)
        lbl2 = self.ct("2. Trích đặc trưng", font_size=15, color=CHART_ORANGE, weight=BOLD).next_to(card2.get_top(), DOWN, buff=0.2)
        # Minutiae details inside Card 2
        fp_contour = create_fingerprint_simple(scale=0.36, color=TEXT_DIM).move_to(card2.get_center() + DOWN * 0.2)
        m_dot1 = Dot(card2.get_center() + UP * 0.1 + LEFT * 0.15, color=MINUTIA_TERM, radius=0.07)
        m_dot2 = Dot(card2.get_center() + DOWN * 0.35 + RIGHT * 0.2, color=MINUTIA_BIFUR, radius=0.07)
        card2_content = VGroup(lbl2, fp_contour, m_dot1, m_dot2)

        # Card 3: Đối sánh
        card3 = create_rounded_box(width=box_w, height=box_h, fill_color=CHART_BLUE, fill_opacity=0.08, stroke_color=CHART_BLUE, stroke_width=1.5).move_to(pos3)
        lbl3 = self.ct("3. Đối sánh", font_size=15, color=CHART_BLUE, weight=BOLD).next_to(card3.get_top(), DOWN, buff=0.2)
        # Twin fingerprint match visualization inside Card 3
        fp_left = create_fingerprint_simple(scale=0.25, color=CHART_BLUE).move_to(card3.get_center() + DOWN * 0.2 + LEFT * 0.55)
        fp_right = create_fingerprint_simple(scale=0.25, color=CHART_BLUE).move_to(card3.get_center() + DOWN * 0.2 + RIGHT * 0.55)
        match_line = Line(fp_left.get_center() + UP * 0.1, fp_right.get_center() + UP * 0.1, color=MATCH_COLOR, stroke_width=1.5)
        card3_content = VGroup(lbl3, fp_left, fp_right, match_line)

        # Fiber-optic laser connectors
        laser1 = DashedLine(card1.get_right(), card2.get_left(), color=PRIMARY, stroke_width=2, dash_length=0.1)
        laser2 = DashedLine(card2.get_right(), card3.get_left(), color=PRIMARY, stroke_width=2, dash_length=0.1)

        # Result box at the bottom
        res_box = create_rounded_box(width=4.5, height=0.8, fill_color=SECONDARY, fill_opacity=0.4, stroke_color=TEXT_DIM, stroke_width=1.5).shift(DOWN * 2.2)
        res_text = self.ct("ĐANG PHÂN TÍCH...", font_size=13, color=TEXT_DIM, weight=BOLD).move_to(res_box.get_center())

        # Anim 1: Title and cards fade in (0.8s) - ends at 0.98s
        self.play(
            FadeIn(title_main, shift=DOWN * 0.2),
            FadeIn(card1), FadeIn(lbl1), FadeIn(scanner_plate),
            FadeIn(card2), FadeIn(lbl2),
            FadeIn(card3), FadeIn(lbl3),
            run_time=0.8
        )

        # Anim 2: Scanner laser sweeps down in Card 1 (1.2s) - ends at 2.18s
        self.play(
            laser_line.animate.move_to(scanner_plate.get_bottom()),
            run_time=1.2,
            rate_func=linear
        )

        # Anim 3: Create Connector 1 (0.6s) - ends at 2.78s
        self.play(FadeOut(laser_line), run_time=0.3)
        self.play(Create(laser1), run_time=0.6)

        # Anim 4: Minutiae extraction inside Card 2 (1.2s) - ends at 3.98s
        self.play(
            Create(fp_contour),
            FadeIn(m_dot1, scale=1.5),
            FadeIn(m_dot2, scale=1.5),
            run_time=1.2
        )

        # Anim 5: Create Connector 2 (0.6s) - ends at 4.58s
        self.play(Create(laser2), run_time=0.6)

        # Anim 6: Dual fingerprints & Match line inside Card 3 (1.2s) - ends at 5.78s
        self.play(
            Create(fp_left),
            Create(fp_right),
            Create(match_line),
            run_time=1.2
        )

        # Anim 7: Display results box & update to MATCHED (0.8s) - ends at 6.58s
        self.play(FadeIn(res_box), FadeIn(res_text), run_time=0.4)
        success_text = self.ct("KẾT QUẢ: KHỚP VÂN TAY", font_size=13, color=MATCH_COLOR, weight=BOLD).move_to(res_box.get_center())
        self.play(
            FadeOut(res_text),
            FadeIn(success_text),
            res_box.animate.set_color(MATCH_COLOR).set_stroke(width=2.5),
            run_time=0.4
        )

        # Wait remaining time (8.40s - 0.18s(start wait) - 6.40s(anim duration) = 1.82s)
        # Let's add a ripple effect to make it visually outstanding during the wait
        ripple = Circle(radius=0.1, color=MATCH_COLOR, stroke_width=2.0).move_to(res_box.get_center())
        self.add(ripple)
        self.play(
            ripple.animate.scale(22).set_stroke(opacity=0),
            run_time=1.0,
            rate_func=smooth
        )
        self.remove(ripple)
        
        self.wait(0.82)  # Remaining wait

        # Transition out (0.54s) - ends at 9.12s
        self.play(
            FadeOut(VGroup(
                title_main, card1, card1_content, card2, card2_content, card3, card3_content,
                laser1, laser2, res_box, success_text
            )),
            run_time=0.54
        )

    def fvc_evaluation(self):
        """
        Segment 2: 9.12s - 14.16s (Duration: 5.04s)
        Text: Chuỗi cuộc thi FVC từ năm 2000 đến 2006 là chuẩn mực quốc tế để đánh giá thuật toán nhận dạng vân tay.
        
        Segment 3: 15.34s - 20.12s (Duration: 4.78s)
        Text: Số tổ chức tham gia tăng từ 25 lên 150, cho thấy sự quan tâm ngày càng lớn.
        
        Segment 4: 20.44s - 23.34s (Duration: 2.90s)
        Text: Tỷ lệ lỗi EER tốt nhất đạt 2.07% tại FVC2004.
        """
        # Section Header
        self.section_hdr = self.get_section_hdr("CHUẨN ĐÁNH GIÁ THUẬT TOÁN: CUỘC THI FVC").to_edge(UP, buff=0.5)
        self.play(FadeIn(self.section_hdr, shift=DOWN * 0.2), run_time=0.6) # ends at 9.72s

        # Set up Bar Chart containers and labels
        chart_w, chart_h = 7.0, 3.8
        chart_bg = create_rounded_box(width=8.5, height=4.4, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=PRIMARY, stroke_width=1.5).shift(DOWN * 0.4)
        
        # Draw axes
        origin = chart_bg.get_center() + LEFT * 3.2 + DOWN * 1.5
        x_axis = Line(origin, origin + RIGHT * 6.5, color=TEXT_DIM, stroke_width=1.5)
        y_axis = Line(origin, origin + UP * 2.8, color=TEXT_DIM, stroke_width=1.5)
        x_label = self.ct("Năm cuộc thi", font_size=10, color=TEXT_DIM).next_to(x_axis, DOWN, buff=0.5)
        y_label = self.ct("Số đội tham gia", font_size=10, color=TEXT_DIM).next_to(y_axis, UP, buff=0.1)

        # X ticks and labels
        years = ["FVC2000", "FVC2002", "FVC2004", "FVC2006"]
        x_positions = [1.5, 3.0, 4.5, 6.0]
        year_mobs = VGroup()
        for yr, x_pos in zip(years, x_positions):
            tick = Line(origin + RIGHT * x_pos + UP * 0.05, origin + RIGHT * x_pos + DOWN * 0.05, color=TEXT_DIM)
            yr_lbl = self.ct(yr, font_size=11, color=TEXT_COLOR).next_to(tick, DOWN, buff=0.1)
            year_mobs.add(tick, yr_lbl)

        # Initialize Bars
        # FVC2000 = 25 teams
        # FVC2002 = 45 teams (reference)
        # FVC2004 = 90 teams (reference)
        # FVC2006 = 150 teams
        # Max height = 2.5 (150 teams)
        h_factor = 2.5 / 150.0
        
        bar_2000 = Rectangle(width=0.6, height=25 * h_factor, color=CHART_BLUE, fill_opacity=0.6, stroke_width=1.5).move_to(origin + RIGHT * 1.5 + UP * (25 * h_factor / 2.0))
        lbl_2000 = self.ct("25", font_size=11, color=TEXT_BRIGHT, weight=BOLD).next_to(bar_2000, UP, buff=0.1)

        # Bar 2006 (Starts at height of 25 teams, will grow in Segment 3)
        bar_2006 = Rectangle(width=0.6, height=25 * h_factor, color=PRIMARY, fill_opacity=0.6, stroke_width=1.5).move_to(origin + RIGHT * 6.0 + UP * (25 * h_factor / 2.0))
        lbl_2006 = self.ct("25", font_size=11, color=PRIMARY, weight=BOLD).next_to(bar_2006, UP, buff=0.1)

        # Other intermediate bars
        bar_2002 = Rectangle(width=0.6, height=45 * h_factor, color=CHART_BLUE, fill_opacity=0.4, stroke_width=1.0).move_to(origin + RIGHT * 3.0 + UP * (45 * h_factor / 2.0))
        lbl_2002 = self.ct("48", font_size=11, color=TEXT_DIM).next_to(bar_2002, UP, buff=0.1)
        bar_2004 = Rectangle(width=0.6, height=90 * h_factor, color=CHART_BLUE, fill_opacity=0.4, stroke_width=1.0).move_to(origin + RIGHT * 4.5 + UP * (90 * h_factor / 2.0))
        lbl_2004 = self.ct("110", font_size=11, color=TEXT_DIM).next_to(bar_2004, UP, buff=0.1)

        # Anim 1: Chart containers and axes appear (0.8s) - ends at 10.52s
        self.play(
            FadeIn(chart_bg),
            Create(x_axis), Create(y_axis),
            FadeIn(x_label), FadeIn(y_label),
            FadeIn(year_mobs),
            run_time=0.8
        )

        # Anim 2: Bar 2000 appears (1.0s) - ends at 11.52s
        self.play(
            GrowFromEdge(bar_2000, DOWN),
            FadeIn(lbl_2000),
            run_time=1.0
        )

        # Anim 3: Intermediate placeholder bars (2002, 2004) appear dimly (1.0s) - ends at 12.52s
        self.play(
            GrowFromEdge(bar_2002, DOWN),
            GrowFromEdge(bar_2004, DOWN),
            FadeIn(lbl_2002),
            FadeIn(lbl_2004),
            FadeIn(bar_2006), FadeIn(lbl_2006), # Initial state of 2006
            run_time=1.0
        )

        # Wait remaining time of Segment 2 (14.16s - 12.52s = 1.64s)
        self.wait(1.64)

        # Gap between Segment 2 and Segment 3 (15.34s - 14.16s = 1.18s)
        self.wait(1.18)

        # --- Segment 3: 15.34s - 20.12s (Duration: 4.78s) ---
        # ValueTracker to animate growing of FVC2006 bar
        participants_tracker = ValueTracker(25)
        
        def update_bar_2006(mob):
            val = participants_tracker.get_value()
            new_h = val * h_factor
            mob.become(
                Rectangle(
                    width=0.6,
                    height=new_h,
                    color=PRIMARY,
                    fill_color=PRIMARY,
                    fill_opacity=0.7,
                    stroke_width=2.0
                ).move_to(origin + RIGHT * 6.0 + UP * (new_h / 2.0))
            )

        def update_lbl_2006(mob):
            val = int(participants_tracker.get_value())
            mob.become(
                self.ct(f"{val}", font_size=11, color=PRIMARY, weight=BOLD).next_to(bar_2006, UP, buff=0.1)
            )

        bar_2006.add_updater(update_bar_2006)
        lbl_2006.add_updater(update_lbl_2006)

        # Anim 1: Growing of bar 2006 (2.5s) - ends at 17.84s
        self.play(
            participants_tracker.animate.set_value(150),
            run_time=2.5,
            rate_func=smooth
        )
        bar_2006.remove_updater(update_bar_2006)
        lbl_2006.remove_updater(update_lbl_2006)

        # Wait remaining time of Segment 3 (20.12s - 17.84s = 2.28s)
        self.wait(2.28)

        # Gap between Segment 3 and Segment 4 (20.44s - 20.12s = 0.32s)
        self.wait(0.32)

        # --- Segment 4: 20.44s - 23.34s (Duration: 2.90s) ---
        # Highlight FVC2004 and display EER Callout
        badge_bg = create_rounded_box(width=2.8, height=0.8, fill_color=MATCH_COLOR, fill_opacity=0.15, stroke_color=MATCH_COLOR, stroke_width=1.5).move_to(origin + RIGHT * 3.1 + UP * 2.5)
        badge_lbl1 = self.ct("Kỷ lục EER FVC2004", font_size=10, color=MATCH_COLOR, weight=BOLD).move_to(badge_bg.get_center() + UP * 0.16)
        badge_lbl2 = self.ct("EER = 2.07%", font_size=14, color=MATCH_COLOR, weight=BOLD).move_to(badge_bg.get_center() + DOWN * 0.16)
        badge = VGroup(badge_bg, badge_lbl1, badge_lbl2)

        # Draw a diagonal arrow pointing from the bottom-right of the badge to the top of FVC2004 bar
        arrow_start = badge_bg.get_bottom() + RIGHT * 0.6 + UP * 0.045
        arrow_end = bar_2004.get_top() + UP * 0.0 + LEFT * 0.3
        pointer = Arrow(
            start=arrow_start,
            end=arrow_end,
            color=MATCH_COLOR,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.15,
            buff=0.05
        )

        # Anim 1: Show badge and arrow (1.0s) - ends at 21.44s
        self.play(
            bar_2004.animate.set_color(MATCH_COLOR).set_fill(color=MATCH_COLOR, opacity=0.7),
            FadeIn(badge, shift=DOWN * 0.15),
            Create(pointer),
            run_time=1.0
        )

        # Wait remaining time of Segment 4 (23.34s - 21.44s = 1.90s)
        self.wait(1.90)

        # Gap transition to EER Graph (Total Gap: 1.74s from 23.34s to 25.08s)
        # Fade out FVC Elements (0.8s) - ends at 24.14s
        self.play(
            FadeOut(VGroup(
                chart_bg, x_axis, y_axis, x_label, y_label, year_mobs,
                bar_2000, lbl_2000, bar_2002, lbl_2002, bar_2004, lbl_2004, bar_2006, lbl_2006,
                badge, pointer
            )),
            run_time=0.8
        )
        self.wait(0.94) # Wait remainder of gap

    def eer_explanation(self):
        """
        Segment 5: 25.08s - 31.24s (Duration: 6.16s)
        Chỉ số EER là điểm mà tỷ lệ từ chối sai bằng tỷ lệ chấp nhận sai; chỉ số này càng thấp chứng tỏ thuật toán càng chính xác.
        """
        # Update Section Header
        new_header = self.get_section_hdr("CHỈ SỐ ĐÁNH GIÁ LỖI EER").to_edge(UP, buff=0.5)
        self.play(
            Transform(self.section_hdr, new_header),
            run_time=0.8
        ) # ends at 25.88s

        # Graph Container
        graph_bg = create_rounded_box(width=8.5, height=4.4, fill_color=SECONDARY, fill_opacity=0.1, stroke_color=CHART_BLUE, stroke_width=1.5).shift(DOWN * 0.4)
        
        # Origin and axes
        graph_origin = graph_bg.get_center() + LEFT * 2.8 + DOWN * 1.5
        x_axis = Line(graph_origin, graph_origin + RIGHT * 6.0, color=TEXT_DIM, stroke_width=1.5)
        y_axis = Line(graph_origin, graph_origin + UP * 2.8, color=TEXT_DIM, stroke_width=1.5)
        x_label = self.ct("Ngưỡng quyết định (t)", font_size=10, color=TEXT_DIM).next_to(x_axis, DOWN, buff=0.1)
        y_label = self.ct("Tỷ lệ lỗi (%)", font_size=10, color=TEXT_DIM).next_to(y_axis, UP, buff=0.08)

        # Smooth Bezier Curves for FMR and FNMR intersecting at x=2.5, y=1.25
        fmr_points = [
            graph_origin + np.array([0.0, 2.5, 0]),
            graph_origin + np.array([1.25, 1.8, 0]),
            graph_origin + np.array([2.5, 1.15, 0]),
            graph_origin + np.array([3.75, 0.4, 0]),
            graph_origin + np.array([5.2, 0.08, 0])
        ]
        fmr_curve = VMobject().set_points_smoothly(fmr_points).set_color(DELTA_COLOR).set_stroke(width=3.5)
        fmr_lbl = self.ct("FMR (Chấp nhận sai)", font_size=10, color=DELTA_COLOR).move_to(graph_origin + np.array([1.4, 2.2, 0]))

        fnmr_points = [
            graph_origin + np.array([0.0, 0.08, 0]),
            graph_origin + np.array([1.25, 0.4, 0]),
            graph_origin + np.array([2.5, 1.15, 0]),
            graph_origin + np.array([3.75, 1.8, 0]),
            graph_origin + np.array([5.2, 2.5, 0])
        ]
        fnmr_curve = VMobject().set_points_smoothly(fnmr_points).set_color(CHART_BLUE).set_stroke(width=3.5)
        fnmr_lbl = self.ct("FNMR (Từ chối sai)", font_size=10, color=CHART_BLUE).move_to(graph_origin + np.array([3.6, 2.2, 0]))

        # EER Intersection Dot and labels
        eer_pos = graph_origin + np.array([2.5, 1.15, 0])
        eer_dot = Dot(eer_pos, color=MATCH_COLOR, radius=0.1)
        eer_lbl = self.ct("Điểm EER", font_size=10, color=MATCH_COLOR, weight=BOLD).move_to(eer_pos + UP * 0.4 + RIGHT * 0.0)

        # Projection lines
        proj_x = DashedLine(eer_pos, [eer_pos[0], graph_origin[1], 0], color=TEXT_DIM, stroke_width=1.0)
        proj_y = DashedLine(eer_pos, [graph_origin[0], eer_pos[1], 0], color=TEXT_DIM, stroke_width=1.0)

        # "Lower EER = More Accurate" helper visual
        # Create a beautiful box around the description text
        desc_lbl = self.ct("Chỉ số EER càng thấp\nthuật toán càng chính xác", font_size=10, color=MATCH_COLOR, weight=BOLD)
        desc_bg = create_rounded_box(width=2.8, height=0.75, fill_color=SECONDARY, fill_opacity=0.9, stroke_color=MATCH_COLOR, stroke_width=1.5)
        desc_box = VGroup(desc_bg, desc_lbl).move_to(graph_origin + np.array([5, 1.5, 0]))
        desc_lbl.move_to(desc_bg.get_center())

        desc_arrow = Arrow(
            start=desc_bg.get_left() + DOWN * 0.1,
            end=eer_pos,
            color=MATCH_COLOR,
            stroke_width=2.0,
            tip_length=0.15,
            max_tip_length_to_length_ratio=0.12,
            buff=0.15
        )

        # Anim 1: Draw axes (0.7s) - ends at 26.58s
        self.play(
            FadeIn(graph_bg),
            Create(x_axis), Create(y_axis),
            FadeIn(x_label), FadeIn(y_label),
            run_time=0.7
        )

        # Anim 2: Draw FMR and FNMR curves (1.5s) - ends at 28.08s
        self.play(
            Create(fmr_curve), FadeIn(fmr_lbl),
            Create(fnmr_curve), FadeIn(fnmr_lbl),
            run_time=1.5
        )

        # Anim 3: Highlight EER intersection (1.2s) - ends at 29.28s
        self.play(
            Create(eer_dot), FadeIn(eer_dot),
            FadeIn(eer_lbl, shift=UP * 0.1),
            Create(proj_x), Create(proj_y),
            Indicate(eer_dot, color=MATCH_COLOR, scale_factor=2.0),
            run_time=1.2
        )

        # Anim 4: Lower EER indicator (0.8s) - ends at 30.08s
        self.play(
            Create(desc_arrow),
            FadeIn(desc_box),
            run_time=0.8
        )

        # Wait remaining time of Segment 5 (31.24s - 30.08s = 1.16s)
        self.wait(1.16)

        # Gap transition to NIST (Total Gap: 0.40s from 31.24s to 31.64s)
        # Fade out EER Graph elements (0.4s) - ends at 31.64s
        self.play(
            FadeOut(VGroup(
                graph_bg, x_axis, y_axis, x_label, y_label,
                fmr_curve, fmr_lbl, fnmr_curve, fnmr_lbl,
                eer_dot, eer_lbl, proj_x, proj_y, desc_arrow, desc_box
            )),
            run_time=0.4
        )

    def nist_evaluation(self):
        """
        Segment 6: 31.64s - 37.84s (Duration: 6.20s)
        Đánh giá FpVTE 2003 do NIST tổ chức đã kiểm tra 34 hệ thống trên cơ sở dữ liệu hơn 48 nghìn bộ vân tay.
        """
        # Update Section Header
        new_header = self.get_section_hdr("ĐÁNH GIÁ CHUẨN MỸ: NIST FpVTE 2003").to_edge(UP, buff=0.5)
        self.play(
            Transform(self.section_hdr, new_header),
            run_time=0.8
        ) # ends at 32.44s

        # NIST Dashboard Container
        nist_bg = create_rounded_box(width=9.5, height=4.4, fill_color=CHART_PURPLE, fill_opacity=0.12, stroke_color=CHART_PURPLE, stroke_width=2.0).shift(DOWN * 0.4)
        
        # Subpanels
        left_sub = create_rounded_box(width=4.2, height=2.8, fill_color=ACCENT, fill_opacity=0.3, stroke_color=CHART_ORANGE, stroke_width=1.5).move_to(nist_bg.get_center() + LEFT * 2.2 + DOWN * 0.1)
        right_sub = create_rounded_box(width=4.2, height=2.8, fill_color=ACCENT, fill_opacity=0.3, stroke_color=CHART_BLUE, stroke_width=1.5).move_to(nist_bg.get_center() + RIGHT * 2.2 + DOWN * 0.1)

        # Left subcontent: 34 Systems
        left_lbl1 = self.ct("34 Hệ Thống Thương Mại", font_size=15, color=CHART_ORANGE, weight=BOLD).next_to(left_sub.get_top(), DOWN, buff=0.2)
        # Visual grid of systems
        sys_grid = VGroup()
        for i in range(3):
            for j in range(6):
                square = Square(side_length=0.25, stroke_color=TEXT_DIM, stroke_width=1.0, fill_color=CHART_ORANGE, fill_opacity=0.25)
                square.move_to(left_sub.get_center() + LEFT * 0.8 + RIGHT * (j * 0.32) + UP * 0.35 + DOWN * (i * 0.32))
                sys_grid.add(square)
        sys_desc = self.ct("Thuật toán từ các tổ chức quốc tế\nđược đánh giá độc lập bởi NIST", font_size=11, color=TEXT_DIM).next_to(sys_grid, DOWN, buff=0.25)
        left_content = VGroup(left_lbl1, sys_grid, sys_desc)

        # Right subcontent: 48,000 Fingerprints
        right_lbl1 = self.ct("48,000+ Bộ Vân Tay", font_size=15, color=CHART_BLUE, weight=BOLD).next_to(right_sub.get_top(), DOWN, buff=0.2)
        # Database stack visualization
        db_group = VGroup()
        for i in range(3):
            db_disk = Ellipse(width=1.2, height=0.35, color=CHART_BLUE, fill_color=CHART_BLUE, fill_opacity=0.25, stroke_width=1.5)
            db_disk.move_to(right_sub.get_center() + LEFT * 1.0 + UP * 0.3 + DOWN * (i * 0.28))
            db_group.add(db_disk)
        fp_mini = create_fingerprint_simple(scale=0.3, color=RIDGE_COLOR).next_to(db_group, RIGHT, buff=0.3).shift(UP * 0.1)
        right_desc = self.ct("Dữ liệu thực nghiệm quy mô lớn\nđảm bảo tính khách quan tối đa", font_size=11, color=TEXT_DIM).next_to(right_sub.get_bottom(), UP, buff=0.25)
        right_content = VGroup(right_lbl1, db_group, fp_mini, right_desc)

        # Anim 1: Fade in NIST board (0.8s) - ends at 33.24s
        self.play(
            FadeIn(nist_bg),
            FadeIn(left_sub),
            FadeIn(right_sub),
            run_time=0.8
        )

        # Anim 2: Fade in Left Sub-content (1.0s) - ends at 34.24s
        self.play(
            FadeIn(left_content, shift=UP * 0.15),
            run_time=1.0
        )

        # Anim 3: Fade in Right Sub-content (1.0s) - ends at 35.24s
        self.play(
            FadeIn(right_content, shift=UP * 0.15),
            run_time=1.0
        )

        # Wait remaining time of Segment 6 (37.84s - 35.24s = 2.60s)
        self.wait(2.60)

        # Gap transition to Open Challenges (Total Gap: 1.38s from 37.84s to 39.22s)
        # Fade out NIST board (0.8s) - ends at 38.64s
        self.play(
            FadeOut(VGroup(nist_bg, left_sub, right_sub, left_content, right_content)),
            run_time=0.8
        )
        self.wait(0.58) # Wait remainder of gap

    def open_challenges(self):
        """
        Segment 7: 39.22s - 43.20s (Duration: 3.98s)
        Text: Dù đã phát triển hơn 50 năm, nhận dạng vân tay vẫn chưa phải bài toán đã giải quyết xong.
        
        Segment 8: 44.00s - 55.76s (Duration: 11.76s)
        Text: Bốn thách thức lớn còn mở gồm: cải thiện thuật toán cho ảnh chất lượng kém và cảm biến giá rẻ, 
        chống tấn công giả mạo bằng vân tay nhân tạo, bảo vệ mẫu sinh trắc khỏi bị giải mã ngược, 
        và đối sánh nhanh trên cơ sở dữ liệu hàng trăm triệu bản ghi.
        """
        # Update Section Header
        new_header = self.get_section_hdr("THÁCH THỨC CÒN MỞ TRONG CÔNG NGHỆ").to_edge(UP, buff=0.5)
        self.play(
            Transform(self.section_hdr, new_header),
            run_time=0.8
        ) # ends at 40.02s

        # Timeline elements for Segment 7
        timeline_line = Line(start=LEFT * 3.5 + DOWN * 0.5, end=RIGHT * 3.5 + DOWN * 0.5, color=TEXT_DIM, stroke_width=2.5)
        t_start_tick = Line(start=LEFT * 3.5 + DOWN * 0.3, end=LEFT * 3.5 + DOWN * 0.7, color=TEXT_DIM)
        t_start_lbl = self.ct("1970s\nKhởi đầu", font_size=11, color=TEXT_DIM).next_to(t_start_tick, DOWN, buff=0.1)
        
        t_now_tick = Line(start=RIGHT * 3.5 + DOWN * 0.3, end=RIGHT * 3.5 + DOWN * 0.7, color=PRIMARY)
        t_now_lbl = self.ct("Hiện tại\n50+ năm phát triển", font_size=11, color=PRIMARY, weight=BOLD).next_to(t_now_tick, DOWN, buff=0.1)

        unsolved_marker = VGroup(
            Circle(radius=0.4, color=DELTA_COLOR, fill_color=DELTA_COLOR, fill_opacity=0.15, stroke_width=2),
            self.ct("?", font_size=20, color=DELTA_COLOR, weight=BOLD)
        ).move_to(RIGHT * 3.5 + UP * 0.4)
        unsolved_lbl = self.ct("Bài toán chưa hoàn toàn giải quyết!", font_size=14, color=DELTA_COLOR, weight=BOLD).next_to(unsolved_marker, UP, buff=0.2)

        # Anim 1: Draw Timeline (1.2s) - ends at 41.22s
        self.play(
            Create(timeline_line),
            Create(t_start_tick), FadeIn(t_start_lbl),
            Create(t_now_tick), FadeIn(t_now_lbl),
            run_time=1.2
        )

        # Anim 2: Highlight "unsolved" marker (1.0s) - ends at 42.22s
        self.play(
            FadeIn(unsolved_marker, scale=1.3),
            FadeIn(unsolved_lbl, shift=UP * 0.1),
            Indicate(unsolved_marker, color=DELTA_COLOR, scale_factor=1.5),
            run_time=1.0
        )

        # Wait remaining time of Segment 7 (43.20s - 42.22s = 0.98s)
        self.wait(0.98)

        # Gap between Segment 7 and Segment 8 (44.00s - 43.20s = 0.80s)
        # Fade out timeline elements (0.6s) - ends at 43.80s
        self.play(
            FadeOut(VGroup(timeline_line, t_start_tick, t_start_lbl, t_now_tick, t_now_lbl, unsolved_marker, unsolved_lbl)),
            run_time=0.6
        )
        self.wait(0.20) # Wait remainder of gap

        # --- Segment 8: 44.00s - 55.76s (Duration: 11.76s) ---
        # 4 Grid cards for challenges
        card_w, card_h = 5.8, 1.7
        card_pos = [
            [-3.2, 0.9, 0],   # Top-Left
            [3.2, 0.9, 0],    # Top-Right
            [-3.2, -1.1, 0],  # Bottom-Left
            [3.2, -1.1, 0]    # Bottom-Right
        ]

        # Challenge 1
        ch_card1 = create_rounded_box(width=card_w, height=card_h, fill_color=ACCENT, fill_opacity=0.4, stroke_color=DELTA_COLOR, stroke_width=1.5).move_to(card_pos[0])
        ch_icon1 = Triangle(color=DELTA_COLOR, stroke_width=2).scale(0.25).move_to(ch_card1.get_left() + RIGHT * 0.5)
        ch_title1 = self.ct("1. Ảnh kém & Cảm biến giá rẻ", font_size=12, color=DELTA_COLOR, weight=BOLD).next_to(ch_icon1, RIGHT, buff=0.25).shift(UP * 0.2)
        ch_desc1 = self.ct("Xử lý nhiễu và biến dạng cơ học cực lớn.", font_size=10, color=TEXT_DIM).next_to(ch_title1, DOWN, buff=0.1, aligned_edge=LEFT)
        c1 = VGroup(ch_card1, ch_icon1, ch_title1, ch_desc1)

        # Challenge 2
        ch_card2 = create_rounded_box(width=card_w, height=card_h, fill_color=ACCENT, fill_opacity=0.4, stroke_color=DELTA_COLOR, stroke_width=1.5).move_to(card_pos[1])
        ch_icon2 = Circle(radius=0.22, color=DELTA_COLOR, stroke_width=2).move_to(ch_card2.get_left() + RIGHT * 0.5)
        # Visual mask inside Circle icon
        ch_mask = Line(ch_icon2.get_left(), ch_icon2.get_right(), color=DELTA_COLOR, stroke_width=1.5)
        ch_icon2.add(ch_mask)
        ch_title2 = self.ct("2. Tấn công vân tay giả mạo", font_size=12, color=DELTA_COLOR, weight=BOLD).next_to(ch_icon2, RIGHT, buff=0.25).shift(UP * 0.2)
        ch_desc2 = self.ct("Phát hiện vật liệu nhân tạo.", font_size=10, color=TEXT_DIM).next_to(ch_title2, DOWN, buff=0.1, aligned_edge=LEFT)
        c2 = VGroup(ch_card2, ch_icon2, ch_title2, ch_desc2)

        # Challenge 3
        ch_card3 = create_rounded_box(width=card_w, height=card_h, fill_color=ACCENT, fill_opacity=0.4, stroke_color=DELTA_COLOR, stroke_width=1.5).move_to(card_pos[2])
        ch_icon3 = Square(side_length=0.4, color=DELTA_COLOR, stroke_width=2).move_to(ch_card3.get_left() + RIGHT * 0.5)
        ch_key = Line(ch_icon3.get_center(), ch_icon3.get_bottom(), color=DELTA_COLOR, stroke_width=1.5)
        ch_icon3.add(ch_key)
        ch_title3 = self.ct("3. Bảo vệ mẫu sinh trắc", font_size=12, color=DELTA_COLOR, weight=BOLD).next_to(ch_icon3, RIGHT, buff=0.25).shift(UP * 0.2)
        ch_desc3 = self.ct("Mã hóa chống khôi phục ngược lại vân tay gốc.", font_size=10, color=TEXT_DIM).next_to(ch_title3, DOWN, buff=0.1, aligned_edge=LEFT)
        c3 = VGroup(ch_card3, ch_icon3, ch_title3, ch_desc3)

        # Challenge 4
        ch_card4 = create_rounded_box(width=card_w, height=card_h, fill_color=ACCENT, fill_opacity=0.4, stroke_color=DELTA_COLOR, stroke_width=1.5).move_to(card_pos[3])
        ch_icon4 = Polygon([0, 0.25, 0], [0.22, -0.15, 0], [-0.22, -0.15, 0], color=DELTA_COLOR, stroke_width=2).move_to(ch_card4.get_left() + RIGHT * 0.5)
        ch_title4 = self.ct("4. Đối sánh CSDL khổng lồ", font_size=12, color=DELTA_COLOR, weight=BOLD).next_to(ch_icon4, RIGHT, buff=0.25).shift(UP * 0.2)
        ch_desc4 = self.ct("Tìm kiếm siêu tốc trên quy mô hàng trăm triệu.", font_size=10, color=TEXT_DIM).next_to(ch_title4, DOWN, buff=0.1, aligned_edge=LEFT)
        c4 = VGroup(ch_card4, ch_icon4, ch_title4, ch_desc4)

        # Sequential display of the 4 cards
        # 1. Card 1 (0.8s show + 1.2s wait) -> Ends at 46.00s
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.8)
        self.wait(1.2)

        # 2. Card 2 (0.8s show + 1.2s wait) -> Ends at 48.00s
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.8)
        self.wait(1.2)

        # 3. Card 3 (0.8s show + 1.2s wait) -> Ends at 50.00s
        self.play(FadeIn(c3, shift=RIGHT * 0.2), run_time=0.8)
        self.wait(1.2)

        # 4. Card 4 (0.8s show + 1.2s wait) -> Ends at 52.00s
        self.play(FadeIn(c4, shift=LEFT * 0.2), run_time=0.8)
        self.wait(1.2)

        # Wait remaining time of Segment 8 (55.76s - 52.00s = 3.76s)
        self.wait(3.76)

        # Gap transition to SFinGe (Total Gap: 0.84s from 55.76s to 56.60s)
        # Fade out challenges (0.8s) - ends at 56.56s
        self.play(
            FadeOut(VGroup(c1, c2, c3, c4)),
            run_time=0.8
        )
        self.wait(0.04)

    def sfinge_generation(self):
        """
        Segment 9: 56.60s - 64.62s (Duration: 8.02s)
        Để vượt qua rào cản quyền riêng tư dữ liệu, phần mềm SFinGe được sử dụng để 
        tự động tạo ra hàng chục nghìn ảnh vân tay nhân tạo siêu thực tế phục vụ huấn luyện và kiểm thử.
        """
        # Update Section Header
        new_header = self.get_section_hdr("SFINGE: TẠO VÂN TAY NHÂN TẠO TỰ ĐỘNG").to_edge(UP, buff=0.5)
        self.play(
            Transform(self.section_hdr, new_header),
            run_time=0.8
        ) # ends at 57.40s

        # SFinGe Generator HUD
        sf_bg = create_rounded_box(width=8.5, height=4.2, fill_color=CHART_PURPLE, fill_opacity=0.1, stroke_color=CHART_PURPLE, stroke_width=1.5).shift(DOWN * 0.3)
        
        # Left side: fingerprint contour & scanner line
        fp_placeholder = create_rounded_box(width=3.2, height=3.2, fill_opacity=0.15, stroke_color=TEXT_DIM, stroke_width=1).move_to(sf_bg.get_center() + LEFT * 2.1)
        fp_lbl = self.ct("Ảnh Vân Tay Kết Quả", font_size=11, color=TEXT_DIM).next_to(fp_placeholder, UP, buff=0.1)

        # Fingerprint pattern inside placeholder
        sf_fp = create_fingerprint_simple(scale=0.72, color=CHART_PURPLE).move_to(fp_placeholder.get_center())
        sf_fp.set_opacity(0) # start hidden

        scan_line = Line(fp_placeholder.get_left() + UP * 1.5, fp_placeholder.get_right() + UP * 1.5, color=PRIMARY, stroke_width=2.5)
        scan_line_glow = self.make_glowing(scan_line, color=PRIMARY, stroke_width_base=2)
        scan_group = VGroup(scan_line, scan_line_glow)
        scan_group.set_opacity(0) # start hidden

        # Right side: info and counter
        info_lbl1 = self.ct("HỆ THỐNG PHẦN MỀM SFINGE", font_size=14, color=CHART_PURPLE, weight=BOLD).move_to(sf_bg.get_center() + RIGHT * 2.0 + UP * 0.8)
        info_lbl2 = self.ct("Tự sinh dữ liệu vân tay siêu thực tế\nTránh vi phạm quyền riêng tư", font_size=11, color=TEXT_DIM).next_to(info_lbl1, DOWN, buff=0.15, aligned_edge=LEFT)
        
        counter_box = create_rounded_box(width=3.6, height=1.0, fill_color=ACCENT, fill_opacity=0.5, stroke_color=PRIMARY, stroke_width=1.5).next_to(info_lbl2, DOWN, buff=0.4, aligned_edge=LEFT)
        
        # ValueTracker to animate generating fingerprints counter
        count_tracker = ValueTracker(0)
        
        def update_counter_lbl(mob):
            val = int(count_tracker.get_value())
            mob.become(
                self.ct(f"Ảnh sinh ra: {val:,}", font_size=14, color=PRIMARY, weight=BOLD).move_to(counter_box.get_center())
            )

        counter_lbl = self.ct("Ảnh sinh ra: 0", font_size=14, color=PRIMARY, weight=BOLD).move_to(counter_box.get_center())
        counter_lbl.add_updater(update_counter_lbl)

        # Show panels (0.8s) - ends at 58.20s
        self.play(
            FadeIn(sf_bg), FadeIn(fp_placeholder), FadeIn(fp_lbl),
            FadeIn(info_lbl1), FadeIn(info_lbl2),
            FadeIn(counter_box), FadeIn(counter_lbl),
            run_time=0.8
        )

        # Start scan visual (0.3s)
        self.play(scan_group.animate.set_opacity(1), run_time=0.3)

        # Sweeping scan line, drawing ridges, and counting up (3.5s) - ends at 62.00s
        self.play(
            scan_group.animate.move_to(fp_placeholder.get_bottom() + UP * 0.1),
            sf_fp.animate.set_opacity(0.8),
            count_tracker.animate.set_value(50000),
            run_time=3.5,
            rate_func=linear
        )
        counter_lbl.remove_updater(update_counter_lbl)

        # Scan line fades out (0.3s) - ends at 62.30s
        self.play(FadeOut(scan_group), run_time=0.3)

        # Wait remaining time of Segment 9 (64.62s - 62.30s = 2.32s)
        self.wait(2.32)

        # Gap transition to Future & Apps (Total Gap: 0.80s from 64.62s to 65.42s)
        # Fade out SFinGe visual (0.8s) - ends at 65.42s
        self.play(
            FadeOut(VGroup(sf_bg, fp_placeholder, fp_lbl, sf_fp, info_lbl1, info_lbl2, counter_box, counter_lbl)),
            run_time=0.8
        )

    def future_applications(self):
        """
        Segment 10: 65.42s - 73.64s (Duration: 8.22s)
        Từ pháp y đến đời sống hàng ngày, từ mở khóa điện thoại đến giao dịch ngân hàng, 
        công nghệ nhận dạng vân tay tiếp tục phát triển cùng trí tuệ nhân tạo và cảm biến thế hệ mới.
        """
        # Update Section Header
        new_header = self.get_section_hdr("ỨNG DỤNG RỘNG RÃI & TƯƠNG LAI").to_edge(UP, buff=0.5)
        self.play(
            Transform(self.section_hdr, new_header),
            run_time=0.8
        ) # ends at 66.22s

        # Central Fingerprint
        center_node = VGroup(
            Circle(radius=0.9, color=PRIMARY, fill_color=ACCENT, fill_opacity=0.8, stroke_width=2.5),
            create_fingerprint_simple(scale=0.5, color=RIDGE_COLOR)
        ).move_to(DOWN * 0.5)

        # 4 surrounding Application Cards
        app_positions = [
            [-3.8, 0.9, 0],   # 1. Pháp y & Hình sự (Top-Left)
            [3.8, 0.9, 0],    # 2. Thiết bị di động (Top-Right)
            [-3.8, -1.9, 0],  # 3. Giao dịch ngân hàng (Bottom-Left)
            [3.8, -1.9, 0]    # 4. AI & Cảm biến mới (Bottom-Right)
        ]
        card_w, card_h = 4.2, 1.4

        # App 1: Pháp y
        card1 = create_rounded_box(width=card_w, height=card_h, fill_color=ACCENT, fill_opacity=0.6, stroke_color=CHART_BLUE, stroke_width=1.5).move_to(app_positions[0])
        lbl1_title = self.ct("Khoa học pháp y", font_size=15, color=CHART_BLUE, weight=BOLD)
        lbl1_desc = self.ct("Điều tra tội phạm & Tư pháp.", font_size=11.5, color=TEXT_DIM)
        txt1 = VGroup(lbl1_title, lbl1_desc).arrange(DOWN, buff=0.12).move_to(card1.get_center())
        a1 = VGroup(card1, txt1)
        conn1 = Line(center_node.get_left() + UP * 0.3, card1.get_right() + DOWN * 0.1, color=CHART_BLUE, stroke_width=1.5)

        # App 2: Thiết bị di động
        card2 = create_rounded_box(width=card_w, height=card_h, fill_color=ACCENT, fill_opacity=0.6, stroke_color=OPTICAL_COLOR, stroke_width=1.5).move_to(app_positions[1])
        lbl2_title = self.ct("Thiết bị di động", font_size=15, color=OPTICAL_COLOR, weight=BOLD)
        lbl2_desc = self.ct("Mở khóa điện thoại & Cá nhân hóa.", font_size=11.5, color=TEXT_DIM)
        txt2 = VGroup(lbl2_title, lbl2_desc).arrange(DOWN, buff=0.12).move_to(card2.get_center())
        a2 = VGroup(card2, txt2)
        conn2 = Line(center_node.get_right() + UP * 0.3, card2.get_left() + DOWN * 0.1, color=OPTICAL_COLOR, stroke_width=1.5)

        # App 3: Giao dịch ngân hàng
        card3 = create_rounded_box(width=card_w, height=card_h, fill_color=ACCENT, fill_opacity=0.6, stroke_color=SOLID_STATE_COLOR, stroke_width=1.5).move_to(app_positions[2])
        lbl3_title = self.ct("Giao dịch ngân hàng", font_size=15, color=SOLID_STATE_COLOR, weight=BOLD)
        lbl3_desc = self.ct("Thanh toán bảo mật & Tiện lợi.", font_size=11.5, color=TEXT_DIM)
        txt3 = VGroup(lbl3_title, lbl3_desc).arrange(DOWN, buff=0.12).move_to(card3.get_center())
        a3 = VGroup(card3, txt3)
        conn3 = Line(center_node.get_left() + DOWN * 0.3, card3.get_right() + UP * 0.1, color=SOLID_STATE_COLOR, stroke_width=1.5)

        # App 4: AI & Cảm biến thế hệ mới
        card4 = create_rounded_box(width=card_w, height=card_h, fill_color=ACCENT, fill_opacity=0.6, stroke_color=PRIMARY, stroke_width=1.5).move_to(app_positions[3])
        lbl4_title = self.ct("AI & Cảm biến mới", font_size=15, color=PRIMARY, weight=BOLD)
        lbl4_desc = self.ct("Nâng cấp bảo mật & Thuật toán.", font_size=11.5, color=TEXT_DIM)
        txt4 = VGroup(lbl4_title, lbl4_desc).arrange(DOWN, buff=0.12).move_to(card4.get_center())
        a4 = VGroup(card4, txt4)
        conn4 = Line(center_node.get_right() + DOWN * 0.3, card4.get_left() + UP * 0.1, color=PRIMARY, stroke_width=1.5)

        # Anim 1: Central fingerprint node fades in (0.8s) - ends at 67.02s
        self.play(FadeIn(center_node, scale=0.8), run_time=0.8)

        # Anim 2: App 1 & connection (0.8s) - ends at 67.82s
        self.play(
            FadeIn(a1, shift=DOWN * 0.15),
            Create(conn1),
            run_time=0.8
        )

        # Anim 3: App 2 & connection (0.8s) - ends at 68.62s
        self.play(
            FadeIn(a2, shift=DOWN * 0.15),
            Create(conn2),
            run_time=0.8
        )

        # Anim 4: App 3 & connection (0.8s) - ends at 69.42s
        self.play(
            FadeIn(a3, shift=UP * 0.15),
            Create(conn3),
            run_time=0.8
        )

        # Anim 5: App 4 & connection (0.8s) - ends at 70.22s
        self.play(
            FadeIn(a4, shift=UP * 0.15),
            Create(conn4),
            run_time=0.8
        )

        # Wait remaining time of Segment 10 (73.64s - 70.22s = 3.42s)
        self.wait(3.42)

        # Keep everything on screen for transition to Outro (Gap: 0s, Segment 11 starts immediately at 73.64s)
        self.app_elements = VGroup(center_node, a1, conn1, a2, conn2, a3, conn3, a4, conn4)

    def outro(self):
        """
        Segment 11: 73.64s - 75.24s (Duration: 1.60s)
        Cảm ơn các bạn đã theo dõi.
        
        Plus extra wait at the end before fading out completely (requested by user).
        """
        # Slow-spinning fingerprint watermark in background
        bg_fingerprint = create_fingerprint_simple(scale=0.8, color=RIDGE_COLOR)
        bg_fingerprint.set_opacity(0.08).scale(2.2).move_to(ORIGIN)

        # Glassmorphic Card container in the center
        outro_card = create_rounded_box(width=9.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.25, stroke_color=PRIMARY, stroke_width=2.0)
        
        thanks_lbl = self.ct("CẢM ƠN CÁC BẠN ĐÃ THEO DÕI!", font_size=32, color=TEXT_BRIGHT, weight=BOLD).next_to(outro_card.get_top(), DOWN, buff=0.4)
        thanks_glow = self.make_glowing(thanks_lbl, color=PRIMARY)

        divider = Line(LEFT * 3.5, RIGHT * 3.5, color=PRIMARY, stroke_width=2.0).next_to(thanks_lbl, DOWN, buff=0.3)
        divider_glow = self.make_glowing(divider, color=PRIMARY)

        subtitle = self.ct("Môn học: Nhận dạng mẫu - HCMUS", font_size=18, color=RIDGE_COLOR, weight=BOLD).next_to(divider, DOWN, buff=0.35)
        credits_lbl = self.ct("Sinh viên thực hiện: Lê Minh Hải", font_size=15, color=TEXT_COLOR).next_to(subtitle, DOWN, buff=0.2)
        
        hashtags = self.ct("#Biometrics #FingerprintRecognition #PatternRecognition", font_size=12, color=PRIMARY).to_edge(DOWN, buff=0.5)

        # Anim 1: Fade out apps & Fade in Outro main (1.2s) - ends at 74.84s (since it starts at 73.64s)
        self.play(
            FadeOut(VGroup(self.section_hdr, self.app_elements)),
            FadeIn(bg_fingerprint),
            FadeIn(outro_card),
            Write(thanks_lbl),
            FadeIn(thanks_glow),
            run_time=1.2
        )

        # Anim 2: Draw credits text & lines (0.8s) - ends at 75.64s
        self.play(
            Create(divider), FadeIn(divider_glow),
            FadeIn(subtitle, shift=UP * 0.15),
            FadeIn(credits_lbl, shift=UP * 0.15),
            FadeIn(hashtags, shift=UP * 0.15),
            run_time=0.8
        )

        # Target Segment 11 ends at 75.24s, but our animations ended at 75.64s.
        # Now, we do the extra wait before fading out.
        # The user requested "phân cảnh cuối nên có wait trước khi fade out. do đó khi tính toán animation cũng phải cân nhắc"
        # Let's wait for 7.0s, during which the background watermark rotates slowly.
        self.play(
            Rotate(bg_fingerprint, angle=0.16, about_point=ORIGIN),
            run_time=7.0,
            rate_func=linear
        )

        # Final Fade Out (1.0s)
        self.play(
            FadeOut(Group(*self.mobjects)),
            run_time=1.0
        )
        self.wait(0.2)
