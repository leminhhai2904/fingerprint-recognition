"""
Scene 4: Quy trình Trích xuất Đặc trưng (Feature Extraction)
- Ước lượng trường hướng (Orientation Field) với đường quét laser và góc xoay
- Trường tần số (Ridge Frequency) với đồ thị sóng sin biểu diễn khoảng cách d
- Phân vùng ảnh và Chỉ số Poincaré (Poincaré Index) tích phân đường khép kín có bộ đếm góc tăng dần
- Quy trình xử lý ảnh: Grayscale -> Gabor Enhanced -> Binarized -> Skeleton với đường quét laser trượt ngang
- Thuật toán Crossing Number (CN) chi tiết với lưới pixel 3x3 và hoạt ảnh quét vòng tròn tìm Termination/Bifurcation
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
        self.segmentation_and_singularities()
        self.enhancement_pipeline()
        self.crossing_number_extraction()

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

    def section_title(self):
        """Tiêu đề mục — Segment 1 = 5.76s."""
        num = self.ct("03", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Trích Xuất Đặc Trưng", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Các thuật toán xử lý ảnh và nhị phân hóa", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)

        # Total play = 2.5s. Target = 5.76s.
        self.wait(2.26)
        self.play(FadeOut(group), run_time=1.0)
        self.wait(0.8)

    def orientation_and_frequency(self):
        """Trường hướng & Trường tần số — Segment 2 = 13.25s."""
        section = self.get_section_hdr("Trường Hướng & Trường Tần Số")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        # 1. Trường hướng (Trái)
        orient_label = self.ct("Trường hướng đường vân", font_size=16, color=CHART_BLUE, weight=BOLD)
        field = create_orientation_field(rows=7, cols=9, width=4.5, height=3.2)
        field_box = create_rounded_box(width=5.0, height=3.6, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=CHART_BLUE, stroke_width=1.5)
        field.move_to(field_box.get_center())
        orient_label.next_to(field_box, UP, buff=0.2)
        orient_group = VGroup(field_box, field, orient_label).shift(LEFT * 3.3 + DOWN * 0.2)

        formula_part = MathTex(r"\theta(x, y)", font_size=26, color=PRIMARY)
        text_part = self.ct("= hướng đường vân cục bộ", font_size=13, color=TEXT_DIM)
        orient_formula = VGroup(formula_part, text_part).arrange(RIGHT, buff=0.1).next_to(field_box, DOWN, buff=0.3)

        # Quét laser đo góc cục bộ
        scan_bar = Line(field_box.get_left() + UP * 1.6, field_box.get_right() + UP * 1.6, color=PRIMARY, stroke_width=3.5)

        # 2. Trường tần số (Phải)
        freq_label = self.ct("Trường tần số đường vân", font_size=16, color=CHART_ORANGE, weight=BOLD)
        freq_box = create_rounded_box(width=5.0, height=3.6, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=CHART_ORANGE, stroke_width=1.5)
        freq_label.next_to(freq_box, UP, buff=0.2)

        # Vẽ đường vân song song
        freq_ridges = VGroup()
        for idx in range(10):
            x = (idx - 4.5) * 0.35
            line = Line(UP * 1.1 + RIGHT * x, DOWN * 1.1 + RIGHT * x, color=RIDGE_COLOR, stroke_width=3.5)
            freq_ridges.add(line)
        freq_ridges.move_to(freq_box.get_center())

        # Đồ thị sóng hình sin bên dưới mô phỏng cường độ pixel sáng/tối
        axes = Axes(x_range=[0, 4, 1], y_range=[-1.2, 1.2, 1], x_length=4.2, y_length=1.4, tips=False, axis_config={"include_ticks": False, "stroke_width": 1.0}).move_to(freq_box.get_center() + DOWN * 0.2)
        sin_curve = axes.plot(lambda x: np.sin(2 * np.pi * x * 1.1), x_range=[0, 3.8], color=CHART_ORANGE, stroke_width=2.5)
        
        # Create a standard-sized brace and scale it down to prevent distortion
        dummy_line = Line(LEFT * 0.5, RIGHT * 0.5)
        brace = Brace(dummy_line, DOWN, color=CHART_ORANGE).set_width(0.35)
        brace.next_to(freq_ridges[3:5], DOWN, buff=0.15)
        spacing_label = self.ct("Khoảng cách d", font_size=11, color=CHART_ORANGE).next_to(brace, DOWN, buff=0.05)

        freq_group = VGroup(freq_box, freq_ridges, freq_label, axes, sin_curve, brace, spacing_label)
        freq_group.shift(RIGHT * 3.3 + DOWN * 0.2)

        formula_part_f = MathTex(r"f(x, y) = 1 / d", font_size=26, color=PRIMARY)
        text_part_f = self.ct("= tần số đường vân cục bộ", font_size=13, color=TEXT_DIM)
        freq_formula = VGroup(formula_part_f, text_part_f).arrange(RIGHT, buff=0.1).next_to(freq_box, DOWN, buff=0.3)

        # Hoạt ảnh xuất hiện
        self.play(FadeIn(field_box), FadeIn(orient_label), run_time=0.8) # Total 1.4s
        self.play(FadeIn(scan_bar), run_time=0.4) # Total 1.8s
        
        # Di chuyển laser quét qua trường hướng và xoay dần các kim hướng
        self.play(
            scan_bar.animate.move_to(field_box.get_bottom() + UP * 0.2),
            LaggedStart(*[FadeIn(seg, scale=0.5) for seg in field], lag_ratio=0.015),
            run_time=2.0
        ) # Total 3.8s
        self.play(FadeOut(scan_bar), FadeIn(orient_formula), run_time=0.6) # Total 4.4s

        # Xuất hiện trường tần số
        self.play(FadeIn(freq_box), FadeIn(freq_label), run_time=0.8) # Total 5.2s
        self.play(Create(freq_ridges), run_time=1.0) # Total 6.2s
        
        # Vẽ sóng sin tần số bên dưới cùng dấu ngoặc đo khoảng cách d
        self.play(Create(sin_curve), FadeIn(axes), run_time=1.2) # Total 7.4s
        self.play(GrowFromCenter(brace), FadeIn(spacing_label), run_time=0.6) # Total 8.0s
        self.play(FadeIn(freq_formula), run_time=0.6) # Total 8.6s

        # Target = 13.25s. Play = 8.6s. Wait = 13.25 - 8.6 - 1.0 = 3.65s
        self.wait(3.65)
        self.play(FadeOut(VGroup(section, field_box, orient_label, field, orient_formula, freq_box, freq_label, freq_ridges, axes, sin_curve, brace, spacing_label, freq_formula)), run_time=1.0)
        self.wait(0.8)

    def segmentation_and_singularities(self):
        """Phân vùng & Phát hiện vùng kỳ dị — Segment 3 = 17.59s."""
        section = self.get_section_hdr("Phân Vùng & Điểm Kỳ Dị")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        # Trái: Segmentation Card
        seg_box = create_rounded_box(width=5.0, height=3.5, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=CHART_ORANGE, stroke_width=1.5)
        seg_title = self.ct("Phân đoạn", font_size=16, color=CHART_ORANGE, weight=BOLD)
        seg_title.next_to(seg_box, UP, buff=-0.45)
        
        seg_desc = self.ct("Loại bỏ nhiễu nền & tránh đặc trưng giả", font_size=9.5, color=TEXT_COLOR)
        seg_desc.next_to(seg_box, DOWN, buff=-0.4)
        
        # Raw image frame representation
        raw_img_box = Square(side_length=1.7, color=TEXT_DIM, stroke_width=1.5)
        
        # Central fingerprint region (Foreground boundary)
        fg_boundary = Ellipse(width=1.1, height=1.4, color=CHART_ORANGE, stroke_width=2.5)
        fg_boundary.set_fill(CHART_ORANGE, opacity=0.12)
        
        # Ridges inside the foreground (loaded from SVG)
        finger_lines = SVGMobject("utils/fingerprint.svg")
        finger_lines.set_color(CHART_ORANGE)
        finger_lines.scale_to_fit_height(0.9)
            
        # Noise dots representing background noise (distributed in the corners/margins)
        noise_dots = VGroup()
        np.random.seed(42)
        for _ in range(16):
            while True:
                rx = np.random.uniform(-0.8, 0.8)
                ry = np.random.uniform(-0.8, 0.8)
                if (rx/0.55)**2 + (ry/0.7)**2 > 1.05:
                    dot = Dot([rx, ry, 0], color=TEXT_DIM, radius=0.035).set_opacity(0.6)
                    noise_dots.add(dot)
                    break
                    
        # Red 'X' crosses to mark discarded noise dots
        crosses = VGroup()
        for dot in noise_dots:
            pos = dot.get_center()
            cross = VGroup(
                Line(pos + np.array([-0.04, -0.04, 0]), pos + np.array([0.04, 0.04, 0]), color=RED, stroke_width=1.5),
                Line(pos + np.array([-0.04, 0.04, 0]), pos + np.array([0.04, -0.04, 0]), color=RED, stroke_width=1.5)
            )
            crosses.add(cross)

        # Position elements relative to raw_img_box center
        finger_lines.move_to(raw_img_box.get_center())
        fg_boundary.move_to(raw_img_box.get_center())
        noise_dots.shift(raw_img_box.get_center())
        crosses.shift(raw_img_box.get_center())
        
        fg_lbl = self.ct("Vùng vân tay (Foreground)", font_size=9, color=CHART_ORANGE).next_to(raw_img_box, DOWN, buff=0.1)
        bg_lbl = self.ct("Vùng nền (Background)", font_size=9, color=TEXT_DIM).next_to(raw_img_box, UP, buff=0.1)
        
        seg_vis = VGroup(raw_img_box, finger_lines, noise_dots, fg_boundary, fg_lbl, bg_lbl)
        seg_vis.scale(0.88).move_to(seg_box.get_center() + DOWN * 0.1)
        crosses.scale(0.88).move_to(seg_vis[2].get_center())

        seg_group = VGroup(seg_box, seg_title, seg_vis, seg_desc, crosses).shift(LEFT * 3.3 + DOWN * 0.25)

        # Phải: Poincaré Index Card
        poincare_box = create_rounded_box(width=5.0, height=3.5, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=CHART_BLUE, stroke_width=1.5)
        poincare_title = self.ct("Phương Pháp Chỉ Số Poincaré", font_size=16, color=CHART_BLUE, weight=BOLD)
        
        formula = MathTex(
            r"P(C) = \frac{1}{2\pi} \oint_C d\theta",
            font_size=28, color=TEXT_BRIGHT
        ).shift(UP * 0.2)
        
        results = VGroup(
            self.ct("Loop (Core): P(C) = +180° (+π)", font_size=12, color=CHART_BLUE, weight=BOLD),
            self.ct("Delta: P(C) = -180° (-π)", font_size=12, color=DELTA_COLOR, weight=BOLD),
            self.ct("Whorl: P(C) = +360° (+2π)", font_size=12, color=CHART_PURPLE, weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        
        poincare_content = VGroup(poincare_title, formula, results).arrange(DOWN, buff=0.3)
        poincare_content.move_to(poincare_box.get_center())
        poincare_group = VGroup(poincare_box, poincare_content).shift(RIGHT * 3.3 + DOWN * 0.25)

        # Trực quan hóa Segmentation trước
        self.play(FadeIn(seg_box), FadeIn(seg_title), run_time=0.8) # Total 1.4s
        
        # Show raw image with noise
        self.play(
            FadeIn(raw_img_box),
            FadeIn(finger_lines),
            FadeIn(noise_dots),
            FadeIn(bg_lbl),
            run_time=0.8
        ) # Total 2.2s
        
        # Segmentation separation animation:
        # 1. Draw boundary and show foreground label
        self.play(
            Create(fg_boundary),
            FadeIn(fg_lbl, shift=UP * 0.12),
            run_time=1.0
        ) # Total 3.2s
        
        # 2. Show red crosses over the noise dots to indicate rejection
        self.play(
            FadeIn(crosses, scale=0.5),
            run_time=0.6
        ) # Total 3.8s
        
        # 3. Discard noise (fade out dots and crosses, dark mask/dim raw box, show description)
        self.play(
            FadeOut(noise_dots),
            FadeOut(crosses),
            raw_img_box.animate.set_color(TEXT_DIM).set_opacity(0.4),
            FadeIn(seg_desc, shift=UP * 0.12),
            run_time=1.0
        ) # Total 4.8s
        self.wait(1.5) # Total 6.3s

        # Xuất hiện Poincaré Card
        self.play(FadeIn(poincare_box), FadeIn(poincare_title), run_time=0.8) # Total 7.1s
        self.play(Write(formula), run_time=1.0) # Total 8.1s
        self.play(FadeIn(results, shift=UP * 0.15), run_time=1.2) # Total 9.3s

        # --- CHẠY HOẠT ẢNH TÍCH PHÂN ĐƯỜNG POINCARÉ ---
        # Tạm thời dọn dẹp các công thức ở thẻ phải để biểu diễn tích phân
        self.play(FadeOut(formula), FadeOut(results), run_time=0.8) # Total 10.1s

        pc_center = poincare_box.get_center() + DOWN * 0.3
        cand_dot = Dot(pc_center, color=CORE_POINT, radius=0.09)
        cand_lbl = self.ct("Điểm kiểm tra P", font_size=11, color=CORE_POINT).next_to(cand_dot, UP, buff=0.08)
        
        # Đường cong tích phân C
        circle_c = Circle(radius=0.75, color=CHART_BLUE, stroke_width=2.0).move_to(pc_center)
        circle_lbl = MathTex(r"C", font_size=18, color=CHART_BLUE).next_to(circle_c, UR, buff=0.02)
        
        # Các vạch hướng cục bộ xung quanh đường cong khép kín C
        orient_segs = VGroup()
        for idx in range(8):
            ang_pos = idx * (2 * PI / 8)
            pos = pc_center + np.array([0.75 * np.cos(ang_pos), 0.75 * np.sin(ang_pos), 0])
            ang_orient = ang_pos / 2.0  # Hướng quay một nửa góc vị trí (mô phỏng Loop)
            seg = Line(
                pos + 0.16 * np.array([np.cos(ang_orient), np.sin(ang_orient), 0]),
                pos - 0.16 * np.array([np.cos(ang_orient), np.sin(ang_orient), 0]),
                color=TEXT_DIM,
                stroke_width=2.5
            )
            orient_segs.add(seg)
            
        pointer = Dot(pc_center + np.array([0.75, 0, 0]), color=PRIMARY, radius=0.08)
        accum_vec = Arrow(pc_center, pc_center + RIGHT * 0.5, color=PRIMARY, buff=0, stroke_width=3)

        self.play(
            FadeIn(cand_dot), FadeIn(cand_lbl),
            FadeIn(circle_c), FadeIn(circle_lbl),
            FadeIn(orient_segs), FadeIn(accum_vec),
            run_time=1.0
        ) # Total 9.7s

        # Chạy tích phân: Con trỏ di chuyển trên đường cong, vector hướng tích lũy góc xoay
        counter_val = ValueTracker(0)
        counter_lbl = self.ct("Tích lũy: 0°", font_size=11, color=PRIMARY, weight=BOLD).next_to(circle_c, DOWN, buff=0.1)

        def update_cnt(mobject):
            mobject.become(
                self.ct(f"Tích lũy: {int(counter_val.get_value())}°", font_size=11, color=PRIMARY, weight=BOLD).next_to(circle_c, DOWN, buff=0.1)
            )
        counter_lbl.add_updater(update_cnt)
        self.add(counter_lbl)

        self.play(
            MoveAlongPath(pointer, circle_c),
            Rotate(accum_vec, angle=PI, about_point=pc_center),
            counter_val.animate.set_value(180),
            run_time=3.0,
            rate_func=linear
        ) # Total 12.7s
        
        counter_lbl.remove_updater(update_cnt)
        res_lbl = self.ct("P(C) = +180° (Phát hiện Điểm lõi)", font_size=12, color=MATCH_COLOR, weight=BOLD).next_to(circle_c, DOWN, buff=0.15)
        
        self.play(
            FadeOut(counter_lbl),
            FadeIn(res_lbl, shift=UP * 0.1),
            Indicate(cand_dot, color=MATCH_COLOR, scale_factor=2.0),
            run_time=1.0
        ) # Total 13.7s
        # Target = 17.59s. Play = 13.7s. Need 17.59s - 13.7s - 1.0s (FadeOut) = 2.89s
        self.wait(2.89)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    def enhancement_pipeline(self):
        """Pipeline xử lý: xám -> tăng cường -> nhị phân -> làm mỏng — Segment 4 = 17.21s."""
        section = self.get_section_hdr("Quy Trình Tiền Xử Lý Ảnh Vân Tay")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        stages = [
            ("1. Ảnh Xám", TEXT_DIM, self._create_grayscale_sim()),
            ("2. Tăng cường", RIDGE_COLOR, self._create_enhanced_sim()),
            ("3. Nhị phân hóa", CHART_BLUE, self._create_binary_sim()),
            ("4. Làm mảnh", CORE_POINT, self._create_thinned_sim()),
        ]

        stage_groups = VGroup()
        for title_text, color, content in stages:
            box = create_rounded_box(width=2.5, height=2.5, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=color, stroke_width=1.5)
            label = self.ct(title_text, font_size=13, color=color, weight=BOLD).next_to(box, DOWN, buff=0.25)
            content.move_to(box.get_center()).scale(0.8)
            stage_groups.add(VGroup(box, content, label))

        stage_groups.arrange(RIGHT, buff=0.6).shift(DOWN * 0.3)

        # Mũi tên liên kết các bước
        arrows = VGroup()
        for idx in range(len(stage_groups) - 1):
            arrow = Arrow(
                stage_groups[idx][0].get_right(), stage_groups[idx+1][0].get_left(),
                color=PRIMARY, buff=0.08, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.22
            )
            arrows.add(arrow)

        filter_desc = self.ct(
            "Bộ lọc ngữ cảnh Gabor hoạt động như một bộ lọc thông dải cục bộ giúp làm rõ đường vân",
            font_size=15, color=PRIMARY, weight=BOLD
        ).to_edge(DOWN, buff=0.85)

        # Đường laser quét reveal
        scan_group = Line(UP * 2.2, DOWN * 2.2, color=PRIMARY, stroke_width=4.0).move_to(LEFT * 6.8)

        self.play(FadeIn(scan_group), run_time=0.5) # Total 1.1s

        # Quét laser lần lượt để kích hoạt/hiển thị từng Card xử lý ảnh
        for idx, sg in enumerate(stage_groups):
            card_x = sg.get_center()[0]
            self.play(
                scan_group.animate.move_to([card_x, 0, 0]),
                FadeIn(sg, shift=UP * 0.25),
                run_time=0.8
            )
            if idx < len(arrows):
                self.play(GrowArrow(arrows[idx]), run_time=0.3)

        self.play(scan_group.animate.move_to(RIGHT * 6.8), run_time=0.6) # Total 5.8s
        self.play(FadeOut(scan_group), run_time=0.4) # Total 6.2s
        self.play(FadeIn(filter_desc, shift=UP * 0.15), run_time=0.8) # Total 7.0s

        # Target = 17.21s. Anim play = 7.0s. Need 17.21s - 7.0s - 1.0s (FadeOut) = 9.21s
        self.wait(9.21)
        self.play(FadeOut(VGroup(section, stage_groups, arrows, filter_desc)), run_time=1.0)
        self.wait(0.8)

    def crossing_number_extraction(self):
        """Thuật toán Crossing Number (CN) — Segment 5 = 13.66s."""
        section = self.get_section_hdr("Trích Xuất Minutiae: Crossing Number")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        # Công thức Crossing Number
        formula = MathTex(
            r"\text{CN}(P) = \frac{1}{2} \sum_{i=1}^{8} |P_i - P_{i+1}|",
            font_size=30, color=TEXT_BRIGHT
        ).shift(LEFT * 3.3 + UP * 0.8)

        # Lưới pixel 3x3
        grid = create_crossing_number_grid(scale=1.4)
        grid.shift(RIGHT * 3.3 + UP * 0.15)
        grid_lbl = self.ct("Cửa sổ quét 3x3 pixel", font_size=13, color=TEXT_DIM).next_to(grid, DOWN, buff=0.2)

        p_center = Dot(grid[4].get_center(), color=PRIMARY, radius=0.1)
        p_label = MathTex(r"P", font_size=18, color=PRIMARY).next_to(p_center, UR, buff=0.02)

        # Định vị các điểm lân cận P1 đến P8 (theo chiều kim đồng hồ)
        # Các chỉ số ô vuông trong grid 3x3:
        # [0, 1, 2]
        # [3, 4, 5]
        # [6, 7, 8]
        # Thứ tự quét vòng quanh P: P1 (ô 1), P2 (ô 2), P3 (ô 5), P4 (ô 8), P5 (ô 7), P6 (ô 6), P7 (ô 3), P8 (ô 0)
        neighbor_indices = [1, 2, 5, 8, 7, 6, 3, 0]
        neighbors = VGroup()
        for n_idx in neighbor_indices:
            dot = Dot(grid[n_idx].get_center(), color=CHART_BLUE, radius=0.08)
            neighbors.add(dot)

        cases = VGroup(
            self.ct("CN(P) = 1  →  Điểm kết thúc", font_size=14, color=MINUTIA_TERM, weight=BOLD),
            self.ct("CN(P) = 3  →  Điểm phân nhánh", font_size=14, color=MINUTIA_BIFUR, weight=BOLD),
            self.ct("CN(P) = 2  →  Đường vân liên tục bình thường", font_size=13, color=TEXT_DIM)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).shift(LEFT * 3.3 + DOWN * 1.1)

        self.play(Write(formula), run_time=0.8) # Total 1.4s
        self.play(Create(grid), FadeIn(grid_lbl), run_time=1.0) # Total 2.4s
        self.play(FadeIn(p_center), FadeIn(p_label), run_time=0.5) # Total 2.9s

        # Quét vòng quanh P để minh họa thuật toán CN
        sweep_circle = Circle(radius=0.55, color=PRIMARY, stroke_width=2).move_to(p_center)
        self.play(FadeIn(sweep_circle), run_time=0.4) # Total 3.3s
        
        self.play(
            Rotate(sweep_circle, angle=2*PI, about_point=p_center.get_center()),
            LaggedStart(*[FadeIn(n, scale=1.4) for n in neighbors], lag_ratio=0.12),
            run_time=2.2
        ) # Total 5.5s
        
        self.play(FadeOut(sweep_circle), FadeIn(cases), run_time=0.8) # Total 6.3s

        # Target = 13.66s. Play = 6.3s. Need 13.66s - 6.3s - 1.0s (FadeOut) = 6.36s.
        self.wait(6.36)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.8)

    # ─── MÔ PHỎNG XỬ LÝ ẢNH (ẢNH MINH HỌA ĐƯỜNG VÂN CHO CÁC CARD) ───────────

    def _create_grayscale_sim(self):
        """Mô phỏng đường vân xám nhiễu nhẹ."""
        g = VGroup()
        for idx in range(5):
            y = (idx - 2) * 0.22
            g.add(Line(LEFT * 0.85 + UP * y, RIGHT * 0.85 + UP * y, color=TEXT_DIM, stroke_width=6).set_opacity(0.35))
        # Dấu chấm nhiễu xung quanh
        for _ in range(8):
            g.add(Dot([np.random.uniform(-0.8, 0.8), np.random.uniform(-0.5, 0.5), 0], color=TEXT_DIM, radius=0.03).set_opacity(0.3))
        return g

    def _create_enhanced_sim(self):
        """Mô phỏng đường vân đã tăng cường rõ nét."""
        g = VGroup()
        for idx in range(5):
            y = (idx - 2) * 0.22
            g.add(Line(LEFT * 0.85 + UP * y, RIGHT * 0.85 + UP * y, color=TEXT_COLOR, stroke_width=6.5))
        return g

    def _create_binary_sim(self):
        """Mô phỏng đường vân nhị phân thuần tuý 2 màu."""
        g = VGroup()
        for idx in range(5):
            y = (idx - 2) * 0.22
            g.add(Line(LEFT * 0.85 + UP * y, RIGHT * 0.85 + UP * y, color=CHART_BLUE, stroke_width=5.0))
        return g

    def _create_thinned_sim(self):
        """Mô phỏng đường xương vân mảnh 1-pixel."""
        g = VGroup()
        for idx in range(5):
            y = (idx - 2) * 0.22
            g.add(Line(LEFT * 0.85 + UP * y, RIGHT * 0.85 + UP * y, color=CORE_POINT, stroke_width=1.6))
        return g
