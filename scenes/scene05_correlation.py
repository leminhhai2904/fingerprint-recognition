"""
Scene 5: Đối sánh dựa trên tương quan (Correlation-based Matching) - Cải tiến v2
- Thách thức đối sánh vân tay
- Ba họ phương pháp đối sánh
- Đối sánh tương quan chéo + Khớp hộp sáng nháy xanh lá
  + Minh họa tăng tốc bằng biến đổi Fourier (Fourier Domain Acceleration)
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
        self.intro_and_challenges()
        self.three_families()
        self.correlation_matching()
        self.limitations()

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kwargs):
        """create_text với CMU Serif kerning workaround (render to lớn rồi scale xuống)."""
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

    def intro_and_challenges(self):
        # Segment 1 (0.44s - 3.08s, dur 2.64s)
        # Khởi đầu với tiêu đề lớn ở chính giữa
        num = self.ct("04", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Đối Sánh Vân Tay", font_size=40, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("So sánh vân tay để xác thực danh tính", font_size=18, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.7)
        self.wait(0.64)
        
        # Tịnh tiến tiêu đề lên góc trên
        section_hdr = self.get_section_hdr("Đối Sánh Vân Tay - Tương Quan")
        section_hdr.to_edge(UP, buff=0.6)
        
        self.play(
            FadeOut(group),
            FadeIn(section_hdr, shift=DOWN * 0.3),
            run_time=0.8
        )
        
        # Segment 2 (3.48s - 11.80s, dur 8.32s)
        # Hiện hai Card đại diện cho Template T và Input I
        t_box = create_rounded_box(width=2.8, height=2.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=1.5)
        t_finger = create_fingerprint_simple(color=CHART_BLUE).scale_to_fit_height(1.8).move_to(t_box.get_center())
        t_label = self.ct("Template T", font_size=12, color=CHART_BLUE, weight=BOLD).next_to(t_box, UP, buff=0.15)
        t_group = VGroup(t_box, t_finger, t_label).shift(LEFT * 3.2 + DOWN * 0.4)
        
        i_box = create_rounded_box(width=2.8, height=2.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_ORANGE, stroke_width=1.5)
        i_finger = create_fingerprint_simple(color=CHART_ORANGE).scale_to_fit_height(1.8).move_to(i_box.get_center())
        i_label = self.ct("Input I", font_size=12, color=CHART_ORANGE, weight=BOLD).next_to(i_box, UP, buff=0.15)
        i_group = VGroup(i_box, i_finger, i_label).shift(RIGHT * 3.2 + DOWN * 0.4)
        
        self.play(FadeIn(t_group, shift=RIGHT * 0.3), FadeIn(i_group, shift=LEFT * 0.3), run_time=1.0)
        self.wait(0.5)
        
        # 1. Lệch vị trí (Global Displacement): Di chuyển Input I chéo xuống và xoay nghiêng
        self.play(
            i_group.animate.shift(DOWN * 0.4 + RIGHT * 0.4).rotate(25 * DEGREES, about_point=i_group.get_center()),
            run_time=1.5
        )
        self.wait(0.5)
        
        # 2. Biến dạng phi tuyến (Non-linear Distortion): Co giãn cục bộ hình học đường vân
        def distort_fn(p):
            c = i_box.get_center()
            d = p - c
            r = np.linalg.norm(d)
            if r < 1.2:
                factor = 1.0 + 0.3 * np.cos(PI * r / 2.4)
                return c + d * factor
            return p
            
        self.play(
            i_finger.animate.apply_function(distort_fn),
            i_box.animate.set_stroke(color=RED, width=2.5),
            run_time=1.5
        )
        self.wait(0.5)
        
        # 3. Thay đổi điều kiện da (Skin conditions): Độ dày cộm và đứt nét
        self.play(
            i_finger.animate.set_stroke(width=5.0).set_fill(opacity=0.9),
            run_time=1.2
        )
        self.play(
            i_finger.animate.set_stroke(width=0.6).set_fill(opacity=0.35),
            run_time=1.2
        )
        
        # Sắc đỏ cảnh báo xung quanh vùng lỗi
        warn_ring = Circle(radius=0.45, color=RED, stroke_width=2.0).move_to(i_box.get_center())
        self.play(
            Broadcast(warn_ring, focal_point=i_box.get_center()),
            i_box.animate.set_stroke(color=CHART_ORANGE, width=1.5),
            run_time=1.0
        )
        self.wait(0.42)
        
        # Segment 3 (12.18s - 17.42s, dur 5.24s)
        # So sánh tương phản: hiện nhãn đỏ lỗi cấu trúc
        mismatch_highlight = i_finger.copy().set_color(RED).set_opacity(0.4)
        mismatch_label = self.ct("Khác biệt cấu trúc", font_size=10, color=RED, weight=BOLD).next_to(i_box, DOWN, buff=0.15)
        self.play(
            FadeIn(mismatch_highlight),
            FadeIn(mismatch_label),
            run_time=1.5
        )
        self.wait(3.74)
        
        # Dọn dẹp chuyển cảnh
        self.play(
            FadeOut(t_group),
            FadeOut(i_group),
            FadeOut(mismatch_highlight),
            FadeOut(mismatch_label),
            run_time=0.88
        )

    def three_families(self):
        # Segment 4 (18.30s - 24.50s, dur 6.20s)
        # Card 1: Tương Quan Pixel
        card1_box = create_rounded_box(width=3.7, height=2.6, fill_color=CHART_BLUE, fill_opacity=0.06, stroke_color=CHART_BLUE, stroke_width=1.5)
        card1_top_bar = Line(
            start=card1_box.get_top() + LEFT * 1.0 + DOWN * 0.05,
            end=card1_box.get_top() + RIGHT * 1.0 + DOWN * 0.05,
            color=CHART_BLUE,
            stroke_width=2.5
        )
        card1_title = self.ct("Tương Quan Pixel", font_size=13.5, color=CHART_BLUE, weight=BOLD)
        card1_bullets = VGroup(
            VGroup(Dot(radius=0.035, color=CHART_BLUE), self.ct("So khớp cường độ pixel trực tiếp", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.035, color=CHART_BLUE), self.ct("Đo lường độ tương quan chéo", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.035, color=CHART_BLUE), self.ct("Nhạy cảm với biến dạng phi tuyến", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card1_content = VGroup(card1_title, card1_bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(card1_box.get_center())
        c1 = VGroup(card1_box, card1_top_bar, card1_content)

        # Card 2: Dựa Trên Minutiae
        card2_box = create_rounded_box(width=3.7, height=2.6, fill_color=CHART_ORANGE, fill_opacity=0.06, stroke_color=CHART_ORANGE, stroke_width=1.5)
        card2_top_bar = Line(
            start=card2_box.get_top() + LEFT * 1.0 + DOWN * 0.05,
            end=card2_box.get_top() + RIGHT * 1.0 + DOWN * 0.05,
            color=CHART_ORANGE,
            stroke_width=2.5
        )
        card2_title = self.ct("Dựa Trên Minutiae", font_size=13.5, color=CHART_ORANGE, weight=BOLD)
        card2_bullets = VGroup(
            VGroup(Dot(radius=0.035, color=CHART_ORANGE), self.ct("Trích xuất điểm rẽ nhánh, kết thúc", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.035, color=CHART_ORANGE), self.ct("Biểu diễn tọa độ hình học (x, y, θ)", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.035, color=CHART_ORANGE), self.ct("Bất biến với phép tịnh tiến và xoay", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card2_content = VGroup(card2_title, card2_bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(card2_box.get_center())
        c2 = VGroup(card2_box, card2_top_bar, card2_content)

        # Card 3: Đặc Trưng Kết Cấu
        card3_box = create_rounded_box(width=3.7, height=2.6, fill_color=CHART_PURPLE, fill_opacity=0.06, stroke_color=CHART_PURPLE, stroke_width=1.5)
        card3_top_bar = Line(
            start=card3_box.get_top() + LEFT * 1.0 + DOWN * 0.05,
            end=card3_box.get_top() + RIGHT * 1.0 + DOWN * 0.05,
            color=CHART_PURPLE,
            stroke_width=2.5
        )
        card3_title = self.ct("Đặc Trưng Kết Cấu", font_size=13.5, color=CHART_PURPLE, weight=BOLD)
        card3_bullets = VGroup(
            VGroup(Dot(radius=0.035, color=CHART_PURPLE), self.ct("Khai thác trường hướng & tần số vân", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.035, color=CHART_PURPLE), self.ct("Sử dụng bộ lọc thông dải Gabor", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.035, color=CHART_PURPLE), self.ct("Biểu diễn dạng vector FingerCode", font_size=8.2, color=TEXT_COLOR)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card3_content = VGroup(card3_title, card3_bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(card3_box.get_center())
        c3 = VGroup(card3_box, card3_top_bar, card3_content)

        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.35).shift(DOWN * 0.5)

        self.play(
            LaggedStart(
                AnimationGroup(Create(card1_box), Create(card1_top_bar), FadeIn(card1_content, shift=UP * 0.25)),
                AnimationGroup(Create(card2_box), Create(card2_top_bar), FadeIn(card2_content, shift=UP * 0.25)),
                AnimationGroup(Create(card3_box), Create(card3_top_bar), FadeIn(card3_content, shift=UP * 0.25)),
                lag_ratio=0.25
            ),
            run_time=2.2
        )
        self.wait(3.70)

        # Gap (24.50s - 25.46s, dur 0.96s)
        # Ẩn 3 method cards đi để có không gian thoáng đạt cho Template T và Input I
        self.play(FadeOut(cards), run_time=0.96)
        
        # Segment 5 (25.46s - 28.38s, dur 2.92s)
        # Template T và Input I lớn xuất hiện
        self.t_box = create_rounded_box(width=2.5, height=2.5, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=1.5).shift(LEFT * 3.2 + DOWN * 0.6)
        self.t_finger = create_fingerprint_simple(color=CHART_BLUE).scale_to_fit_height(1.6).move_to(self.t_box.get_center())
        self.t_lbl = self.ct("Template T", font_size=12, color=CHART_BLUE, weight=BOLD).next_to(self.t_box, UP, buff=0.1)
        self.t_group = VGroup(self.t_box, self.t_finger, self.t_lbl)
        
        self.i_box = create_rounded_box(width=2.5, height=2.5, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_ORANGE, stroke_width=1.5).shift(RIGHT * 1.0 + DOWN * 0.6)
        self.i_finger = create_fingerprint_simple(color=CHART_ORANGE).scale_to_fit_height(1.6).move_to(self.i_box.get_center())
        self.i_lbl = self.ct("Input I", font_size=12, color=CHART_ORANGE, weight=BOLD).next_to(self.i_box, UP, buff=0.1)
        self.i_group = VGroup(self.i_box, self.i_finger, self.i_lbl)
        
        self.play(
            FadeIn(self.t_group, shift=RIGHT * 0.2),
            FadeIn(self.i_group, shift=LEFT * 0.2),
            run_time=1.0
        )
        
        # Nháy viền khi nhắc đến Template T
        self.play(
            self.t_box.animate.set_stroke(color=PRIMARY, width=2.5),
            run_time=0.8
        )
        # Nháy viền khi nhắc đến Input I và hoàn trả viền T
        self.play(
            self.i_box.animate.set_stroke(color=PRIMARY, width=2.5),
            self.t_box.animate.set_stroke(color=CHART_BLUE, width=1.5),
            run_time=0.8
        )
        self.play(
            self.i_box.animate.set_stroke(color=CHART_ORANGE, width=1.5),
            run_time=0.32
        )
        
        # Chuyển cảnh sang Segment 6 (gap: 28.38s - 29.62s, dur 1.24s)
        self.wait(1.24)

    def correlation_matching(self):
        # Segment 6 (29.62s - 32.80s, dur 3.18s)
        # Hiển thị công thức tương quan chéo LaTeX
        formula = MathTex(
            r"S(T, I) = \max_{\Delta x, \Delta y, \theta} CC(T, I(\Delta x, \Delta y, \theta))",
            font_size=28, color=TEXT_BRIGHT
        ).to_edge(UP, buff=1.8)
        
        # Đồ thị hai chiều CC
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.2, 1],
            x_length=3.5, y_length=1.6,
            tips=False,
            axis_config={"stroke_color": TEXT_DIM, "stroke_width": 1.0}
        ).shift(RIGHT * 4.4 + DOWN * 1.0)
        axes_lbl = self.ct("Hàm tương quan CC", font_size=9, color=PRIMARY, weight=BOLD).next_to(axes, UP, buff=0.1)
        axes_group = VGroup(axes, axes_lbl)
        
        self.play(
            Write(formula),
            FadeIn(axes_group),
            run_time=2.0
        )
        self.wait(1.18)
        
        # Gap (32.80s - 33.64s, dur 0.84s)
        self.wait(0.84)
        
        # Segment 7 (33.64s - 39.86s, dur 6.22s)
        # Di chuyển I đè chồng lên T
        i_overlay = self.i_finger.copy().set_opacity(0.45).move_to(self.i_box.get_center())
        self.add(i_overlay)
        self.play(
            i_overlay.animate.move_to(self.t_box.get_center() + UP * 0.3 + RIGHT * 0.3).rotate(15 * DEGREES),
            FadeOut(self.i_group),
            run_time=1.2
        )
        
        self.wait(0.6)
        
        # Vẽ hàm CC bằng ValueTracker
        tracker = ValueTracker(0.0)
        def get_cc_val(x):
            return 0.15 + 0.81 * np.exp(-((x - 7.0) / 2.0)**2)
            
        cc_curve = always_redraw(lambda: axes.plot(
            lambda x: get_cc_val(x),
            x_range=[0, max(0.1, tracker.get_value())],
            color=PRIMARY, stroke_width=2.0
        ))
        
        graph_dot = always_redraw(lambda: Dot(
            axes.coords_to_point(tracker.get_value(), get_cc_val(tracker.get_value())),
            color=PRIMARY, radius=0.06
        ))
        
        self.add(cc_curve, graph_dot)
        
        # Chạy trượt và xoay để tìm điểm tương quan lớn nhất
        self.play(
            tracker.animate.set_value(7.0),
            i_overlay.animate.move_to(self.t_box.get_center()).rotate(-15 * DEGREES),
            run_time=2.2,
            rate_func=linear
        )
        
        # Khi trùng khít: đổi màu Match Green + Sóng lan tỏa
        flash_ring = Circle(radius=0.2, color=MATCH_COLOR, stroke_width=3.0).move_to(self.t_box.get_center())
        self.play(
            i_overlay.animate.set_color(MATCH_COLOR).set_opacity(0.8),
            self.t_finger.animate.set_color(MATCH_COLOR),
            flash_ring.animate.scale(6.0).set_opacity(0),
            run_time=0.8,
            rate_func=smooth
        )
        self.remove(flash_ring)
        self.wait(1.42)
        
        # Gap (39.86s - 40.12s, dur 0.26s)
        self.wait(0.26)
        
        # Segment 8 (40.12s - 47.14s, dur 7.02s)
        # Miền tần số Fourier Domain Acceleration
        self.play(
            FadeOut(self.t_group),
            FadeOut(i_overlay),
            FadeOut(formula),
            FadeOut(cc_curve),
            FadeOut(graph_dot),
            FadeOut(axes_group),
            run_time=1.2
        )
        
        fourier_formula = MathTex(
            r"\mathcal{F}(T \circledast I) = \mathcal{F}(T) \cdot \mathcal{F}(I)^*",
            font_size=28, color=TEXT_BRIGHT
        ).to_edge(UP, buff=1.8)
        
        # Hiện hai Phổ tần số
        spec_t_box = create_rounded_box(width=2.5, height=2.5, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=1.5).shift(LEFT * 3.2 + DOWN * 0.4)
        spec_t_lbl = self.ct("Phổ tần Template", font_size=11, color=CHART_BLUE, weight=BOLD).next_to(spec_t_box, UP, buff=0.1)
        spec_t_pts = VGroup()
        # DC peak at the center
        spec_t_pts.add(Dot(spec_t_box.get_center(), color=CHART_BLUE, radius=0.06))
        # Concentric ring of frequency
        np.random.seed(2026)
        for theta in np.linspace(0, 2 * np.pi, 24, endpoint=False):
            r = 0.6 + np.random.uniform(-0.06, 0.06)
            pt = spec_t_box.get_center() + r * np.array([np.cos(theta), np.sin(theta), 0])
            # Higher opacity near main orientation (e.g., 45 degrees and 225 degrees)
            opacity = 0.9 if abs(np.sin(theta - np.pi/4)) > 0.7 else 0.35
            spec_t_pts.add(Dot(pt, color=CHART_BLUE, radius=0.03).set_opacity(opacity))
            
        spec_t_group = VGroup(spec_t_box, spec_t_pts, spec_t_lbl)
        
        spec_i_box = create_rounded_box(width=2.5, height=2.5, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_ORANGE, stroke_width=1.5).shift(RIGHT * 3.2 + DOWN * 0.4)
        spec_i_lbl = self.ct("Phổ tần Input", font_size=11, color=CHART_ORANGE, weight=BOLD).next_to(spec_i_box, UP, buff=0.1)
        spec_i_pts = VGroup()
        # DC peak at the center
        spec_i_pts.add(Dot(spec_i_box.get_center(), color=CHART_ORANGE, radius=0.06))
        # Concentric ring of frequency (rotated by 15 degrees to match the rotation of Input I)
        for theta in np.linspace(0, 2 * np.pi, 24, endpoint=False):
            r = 0.6 + np.random.uniform(-0.06, 0.06)
            theta_rot = theta + 15 * DEGREES
            pt = spec_i_box.get_center() + r * np.array([np.cos(theta_rot), np.sin(theta_rot), 0])
            # Higher opacity near rotated orientation
            opacity = 0.9 if abs(np.sin(theta - np.pi/4)) > 0.7 else 0.35
            spec_i_pts.add(Dot(pt, color=CHART_ORANGE, radius=0.03).set_opacity(opacity))
            
        spec_i_group = VGroup(spec_i_box, spec_i_pts, spec_i_lbl)
        
        multiply_sign = MathTex(r"\times", font_size=48, color=TEXT_BRIGHT).move_to(DOWN * 0.4)
        
        # So sánh độ phức tạp tính toán
        spatial_col = VGroup(
            self.ct("Không gian", font_size=11, color=TEXT_DIM, weight=BOLD),
            self.ct("Phép chập chéo", font_size=10, color=TEXT_COLOR),
            MathTex(r"\mathcal{O}(N^4)", font_size=18, color=RED)
        ).arrange(DOWN, buff=0.1).shift(LEFT * 5.2 + DOWN * 0.4)
        
        freq_col = VGroup(
            self.ct("Tần số", font_size=11, color=PRIMARY, weight=BOLD),
            self.ct("Phép nhân trực tiếp", font_size=10, color=TEXT_COLOR),
            MathTex(r"\mathcal{O}(N^2 \log N)", font_size=18, color=MATCH_COLOR)
        ).arrange(DOWN, buff=0.1).shift(RIGHT * 5.2 + DOWN * 0.4)
        
        self.play(
            Write(fourier_formula),
            FadeIn(spec_t_group),
            FadeIn(spec_i_group),
            FadeIn(multiply_sign),
            FadeIn(spatial_col),
            FadeIn(freq_col),
            run_time=2.0
        )
        
        spark = Flash(freq_col[2].get_center(), color=MATCH_COLOR, line_length=0.2, flash_radius=0.25)
        self.play(spark, run_time=0.6)
        self.wait(3.22)
        
        self.play(
            FadeOut(fourier_formula),
            FadeOut(spec_t_group),
            FadeOut(spec_i_group),
            FadeOut(multiply_sign),
            FadeOut(spatial_col),
            FadeOut(freq_col),
            run_time=1.02
        )

    def limitations(self):
        # Segment 9 (48.16s - 59.94s, dur 11.78s)
        # Minh họa đồng hồ cát ảo tự vẽ và ma trận số
        hg_top = Line(LEFT * 0.3, RIGHT * 0.3, color=CHART_ORANGE, stroke_width=2.5)
        hg_bottom = Line(LEFT * 0.3, RIGHT * 0.3, color=CHART_ORANGE, stroke_width=2.5).shift(DOWN * 0.8)
        hg_diag1 = Line(hg_top.get_left(), hg_bottom.get_right(), color=CHART_ORANGE, stroke_width=2.0)
        hg_diag2 = Line(hg_top.get_right(), hg_bottom.get_left(), color=CHART_ORANGE, stroke_width=2.0)
        hourglass = VGroup(hg_top, hg_bottom, hg_diag1, hg_diag2).shift(LEFT * 3.6 + UP * 0.6)
        
        # Grid số tính toán cố định
        grid_nums = VGroup()
        np.random.seed(42)
        for r in range(4):
            row_vals = VGroup()
            for c in range(4):
                row_vals.add(self.ct(str(np.random.randint(10, 99)), font_size=8, color=TEXT_DIM))
            row_vals.arrange(RIGHT, buff=0.22)
            grid_nums.add(row_vals)
        grid_nums.arrange(DOWN, buff=0.22).next_to(hourglass, DOWN, buff=0.3)
        
        h_label = self.ct("Chi phí tính toán lớn", font_size=11, color=CHART_ORANGE, weight=BOLD).next_to(grid_nums, DOWN, buff=0.2)
        left_side = VGroup(hourglass, grid_nums, h_label)
        
        # Bên phải: Lưới và méo đường vân (Biến dạng phi tuyến)
        m_box = create_rounded_box(width=4.0, height=3.2, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=DELTA_COLOR, stroke_width=1.5).shift(RIGHT * 2.8 + DOWN * 0.2)
        m_lbl = self.ct("Biến dạng & Thay đổi độ dày vân", font_size=11, color=DELTA_COLOR, weight=BOLD).next_to(m_box, UP, buff=0.15)
        
        t_ridges_m = VGroup()
        for idx in range(5):
            y = (idx - 2.0) * 0.25
            t_ridges_m.add(Line(LEFT * 1.2 + UP * y, RIGHT * 1.2 + UP * y, color=CHART_BLUE, stroke_width=2.0))
            
        # Biến dạng vân và độ dày thay đổi mượt mà bằng amplitude_tracker
        amplitude_tracker = ValueTracker(0.0)
        
        def get_distorted_ridges():
            amp = amplitude_tracker.get_value()
            ridges = VGroup()
            for idx in range(5):
                y = (idx - 2.0) * 0.25
                points = []
                for j in range(20):
                    x_val = (j / 19 - 0.5) * 2.4
                    # Sóng sin tạo biến dạng phi tuyến
                    y_val = y + amp * np.sin(3 * PI * j / 19)
                    points.append([x_val, y_val, 0])
                curve = VMobject()
                curve.set_points_smoothly([np.array(p) for p in points])
                stroke_w = 2.0 + 1.2 * amp * np.sin(3 * PI * idx / 5)
                curve.set_stroke(
                    color=interpolate_color(ManimColor(CHART_ORANGE), ManimColor(RED), amp / 0.12),
                    width=stroke_w
                )
                ridges.add(curve)
            ridges.move_to(m_box.get_center())
            return ridges

        i_ridges_m = always_redraw(get_distorted_ridges)
        t_ridges_m.move_to(m_box.get_center())
        
        # Bắt đầu hiển thị trạng thái ban đầu (vân chưa biến dạng)
        self.add(i_ridges_m)
        self.play(
            FadeIn(m_box),
            FadeIn(t_ridges_m),
            FadeIn(m_lbl, shift=UP * 0.25),
            Create(hourglass),
            FadeIn(grid_nums),
            FadeIn(h_label, shift=UP * 0.25),
            run_time=2.0
        )
        self.wait(0.5)
        
        # Chạy hoạt ảnh chính: Xoay hourglass (quay đúng 3 vòng để kết thúc nằm ngang), biến dạng vân
        self.play(
            Rotate(hourglass, angle=-6 * PI, run_time=7.0, rate_func=linear),
            amplitude_tracker.animate.set_value(0.12),
            run_time=7.0,
            rate_func=linear
        )
        
        self.wait(2.28)
        
        # Gap (59.94s - 60.48s, dur 0.54s)
        self.wait(0.54)
        
        # Segment 10 (60.48s - 62.84s, dur 2.36s)
        target_center = DOWN * 0.2
        minutiae_group = VGroup(
            Dot(target_center + np.array([-0.8, 0.4, 0]), color=MINUTIA_TERM, radius=0.08),
            Dot(target_center + np.array([0.6, -0.5, 0]), color=MINUTIA_BIFUR, radius=0.08),
            Dot(target_center + np.array([0.2, 0.6, 0]), color=MINUTIA_TERM, radius=0.08),
            Dot(target_center + np.array([-0.4, -0.4, 0]), color=MINUTIA_BIFUR, radius=0.08),
        )
        
        minutiae_lbl = self.ct("Trích xuất các đặc trưng điểm", font_size=12, color=PRIMARY, weight=BOLD).next_to(m_box, DOWN, buff=0.25).shift(LEFT * 2.8)
        
        legend = VGroup(
            VGroup(Dot(ORIGIN, color=MINUTIA_TERM, radius=0.06), self.ct("Điểm kết thúc", font_size=9.5, color=TEXT_DIM)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(ORIGIN, color=MINUTIA_BIFUR, radius=0.06), self.ct("Điểm rẽ nhánh", font_size=9.5, color=TEXT_DIM)).arrange(RIGHT, buff=0.15)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(m_box, RIGHT, buff=0.4).shift(LEFT * 2.8)
        
        # Dịch chuyển hộp vân tay vào giữa, mờ vân nền, ẩn các yếu tố lỗi
        self.play(
            FadeOut(left_side),
            FadeOut(i_ridges_m),
            FadeOut(m_lbl),
            t_ridges_m.animate.set_opacity(0.15).shift(LEFT * 2.8),
            m_box.animate.move_to(target_center).set_stroke(color=PRIMARY, width=2.0),
            run_time=1.0
        )
        
        # Xuất hiện các hạt minutiae từ tâm của chúng (GrowFromCenter)
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in minutiae_group], lag_ratio=0.15),
            FadeIn(minutiae_lbl, shift=UP * 0.2),
            FadeIn(legend, shift=LEFT * 0.2),
            run_time=1.0
        )
        
        self.wait(0.36)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
